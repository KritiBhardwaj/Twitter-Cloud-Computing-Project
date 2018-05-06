import json
import re
import io
import preprocessor as p
import couchdb
from shapely.geometry import shape, Point, box
from textblob import TextBlob

db = None
grid=None
keyWords=[
            "food",
            "is",
            "am",
            "the",
            "Anniversary",
            "Anniversaries",
            "Birthday",
            "Birthdays",
            "Event",
            "events",
            "Kids",
            "Wedding",
            "weddings",
            "Marriage",
            "Husband",
            "Wife",
            "wife's",
            "Couple",
            "Couples",
            "Grocery",
            "Groceries",
            "Shopping",
            "Shoppings",
            "Dinner",
            "Dinners",
            "Issues",
            "Divorce",
            "Divorces",
            "Weekends",
            "MarriedPeopleIssues",
            "Married",
            "MarriedIssues",
            "MarriageIssues",
            "UJamil",
            "melbourne"
        ]

def sentimentAnalyser(tweet):
    blob = TextBlob(tweet)
    sentiment = "neutral"
    if blob.sentiment.polarity < 0:
        sentiment = "negative"
    elif blob.sentiment.polarity == 0:
        sentiment = "neutral"
    else:
        sentiment = "positive"
    return sentiment

def checkWhichSuburb(long, lat):
    point = Point(float(long), float(lat))
    count = 0
    suburb = "N/A"
    for x in grid["features"]:
        count = count + 1
        polygon = shape(x['geometry'])
        if polygon.contains(point):
            suburb = x['properties']['sa2_name16']
            break
    return suburb

def setupDB(srv,dbname):
    couchserver = couchdb.Server(srv)
    db = None
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)
    return db

def get_coordinates(text):
    coordinates = re.search(r'\"coordinates\"\:\[(-?\d*\.?\d*,-?\d*\.?\d*)\]',text)
    if coordinates is not None:
        coordinates = coordinates.group(1).split(',')
        return [float(coordinates[0]), float(coordinates[1])]
    return None

def processTweet(line):
    writeToFileDict = {}
    lat = ""
    long = ""
    thisSuburb = ""

    coord = get_coordinates(line)
    line = line[:-2]
    jsonTweet = json.loads(line)
    if coord is not None:
        long = str(coord[0])
        lat = str(coord[1])
        thisSuburb = checkWhichSuburb(long, lat)

    tweet_id = jsonTweet['id'] + 't'
    rawtweet = jsonTweet['value']['properties']['text']
    message = jsonTweet['value']['properties']['text'].encode('utf-8').strip()

    writeToFileDict['id_tweet'] = tweet_id
    writeToFileDict['rawtweet'] = rawtweet
    writeToFileDict['tweet'] = p.clean(message)
    writeToFileDict['raw'] = jsonTweet['doc']
    writeToFileDict['screen_name'] = jsonTweet['doc']['user']['screen_name']
    writeToFileDict['lat'] = lat
    writeToFileDict['long'] = long
    writeToFileDict['sentiment'] = sentimentAnalyser(rawtweet)
    writeToFileDict['suburb'] = thisSuburb

    if (checkIfIDEXists(tweet_id) == "false"):
        try:
            db[tweet_id] = writeToFileDict
            print("Record Inserted!")
        except couchdb.http.ResourceConflict:
            print("Document update conflict!")
    else:
        print("Duplicate id: ", tweet_id)

def checkIfIDEXists(tweetid):
    if tweetid in db:
        mytemp = db[tweetid]
        return "true"
    else:
        return "false"

def readfile(path):
    with io.open(path, encoding='utf8') as f:
        next(f)
        for line in f:
            try:
                processTweet(line)
            except ValueError as valerr:
                print("Cannot Process")
                print(valerr)
        f.close()

if __name__ == "__main__":
    path = 'filteredTweets.json'
    suburbFileName = "allsuburbs.geojson"
    couchsrv = "http://115.146.95.134:5984/"
    dbname = "harvest_file"
    with open(suburbFileName) as data_file:
        grid = json.loads(data_file.read())
    db = setupDB(couchsrv,dbname)
    readfile(path)