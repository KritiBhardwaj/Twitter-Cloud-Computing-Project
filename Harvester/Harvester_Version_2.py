import json
from textblob import TextBlob
import os
import time
import couchdb
import preprocessor as p
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from shapely.geometry import shape, Point

#Setting DB Details
print("Hello, I am CouchDB!")
couchserver = couchdb.Server("http://115.146.95.134:5984/")
dbname = "harvest"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

#ShapelyCode
suburbFileName="allsuburbs.geojson"
with open(suburbFileName) as data_file:
    grid = json.loads(data_file.read())
def checkWhichSuburb(long,lat):
	point = Point(long,lat)
	count=0
	suburb="N/A"
	for x in grid["features"]:
		count=count+1
		#print(count)
		polygon = shape(x['geometry'])
		if polygon.contains(point):
			suburb=x['properties']['sa2_name16']
			#print('This coordinate belongs to :',x['properties']['sa2_name16'])
			break
	return suburb
thisSuburb=checkWhichSuburb(144.900,-37.760)	
print(thisSuburb)

#Tweepy Code
#consumer key, consumer secret, access token, access secret.
Haaris_consumer_key = "E50fbKWMtI5X914kL4kgfURvR"
Haaris_consumer_secret = "CLWbyVUb6b8fIMlodcpgH2jsl7Xal2qVOwGRjtYTYyVRKQTN90"
Haaris_access_token = "1301016800-qi6ql98SLPDHeNYPlw6jvhge0QVElGjoyffBeAH"
Haaris_access_token_secret = "C6tQsacmOfcTPB8uOIor24u1ChUwuPyOPohhYkUzaSRDu"

Consumer_Key_Umair= "HnXTz4v9QCtjWvn7Tpb55SmOz"
Consumer_Secret_Umair= "xCd7VIrsQPrCCg1wsPrxNEvSfmUCSuI7HfTdwtthwcBmo1d4W2"
Access_Token_Umair= "62274863-7eVe1DtSb20jVf7bNLjO5RwlJRqRK0cjAmVRlVfgE"
Access_Token_Secret_Umair = "FbOD05N6TK6wm6x4yGYXs923fX9xnzHUWoiFpkQ4bvNXc"

Consumer_key_Kriti= "zOSTodo9yO17cv0pBU9MbJmQ9"
Consumer_Secret_Kriti= "8cYLBe9EDc9oNVkXbuLiE3nx6fcZhhfqCaMbwx5yHnqXawadqK"
Access_Token_Kriti= "949101970945490944-ytBXszR6zGY2xlrOmAEvOg3xGWeFhzs"
Access_Token_Secret_Kriti= "hXeSM9T2NXta3Q37tRFbeqxJu5iR5HlbfHjCIgtWDnLQf"

Consumer_Key_Sergei = "Vb0cwOkSk6q5tfSfX04h9U23p"
Consumer_Secret_Sergei = "81aM2v0eZhJaA1ksFDicqf0piOidgShokCJudSWlKYVC5BCnI8"
Access_Token_Sergei = "987288793374900224-MlYHf4qwA7K3NfhnCEcLT3o3UeNJPLM"
Access_Token_Secret_Sergei = "CGXGboiACeSWPV4PRIXdnHskWAZJSv5d0zW6pwZQsH8zm"

tweetFile = open('screen3.json', 'a+', encoding='utf8')
tweetFile.write("[")

setOfKeywords = [
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
        "FridayNights",
]


def checkJson(jsonContents):
    codeFlag = True if "coordinates" in jsonContents else False
    return codeFlag

def staticVariableForKeys(value, keyName):
    if (keyName == "A1"):
        staticVariableForKeys.A1 += value
staticVariableForKeys.A1 = 0
	
writeToFileDict={}



class listener(StreamListener):

    def on_data(self, data):
        #print(data)
        jsonTweet = json.loads(data)
        if(checkJson(data)==True):
            #print("True")
            if (str(jsonTweet["coordinates"]) != "None"):
                print(jsonTweet["coordinates"])
                count=0
                lat = 0
                long = 0
                for coordinates in jsonTweet["coordinates"]["coordinates"]:
                    count += 1
                    if (count == 1):
                        long = coordinates
                    # print(coordinates)
                    # print(tweet)
                    else:
                        lat = coordinates
                # print("Long/Lat: ",long," | ",lat)
                thisSuburb = checkWhichSuburb(long, lat)
                print("Tweet belongs to suburb: ", thisSuburb)
                cleansedTweet = p.clean(jsonTweet['text'])
                blob = TextBlob(cleansedTweet)
                # print("B: ", blob)
                if blob.sentiment.polarity < 0:
                    sentiment = "negative"
                elif blob.sentiment.polarity == 0:
                    sentiment = "neutral"
                else:
                    sentiment = "positive"
                # print("Orignal: ",jsonTweet['text'])
                # print("Cleansed: ",cleansedTweet)
                writeToFileDict['id_tweet'] = jsonTweet["id"]
                writeToFileDict['sentiment'] = sentiment
                writeToFileDict['tweet'] = cleansedTweet
                writeToFileDict['suburb'] = thisSuburb
                writeToFileDict['long'] = long
                writeToFileDict['lat'] = lat
                writeToFileDict['screen_name'] = jsonTweet["user"]["screen_name"]
                json_id=str(time.time())+"t"
                #doc_id, doc_rev = db.save(writeToFileDict)
                db[json_id] = writeToFileDict
                #writeLine = json.dumps(writeToFileDict, ensure_ascii=False)
                #writeLine += ","
                #tweetFile.write(writeLine)
                #tweet harvested, now get it's user and search its tweets!
                name = jsonTweet["user"]["screen_name"]
                tweetCount = 1000
                print("-------------->Starting new user tweet fetch!")
                for status in tweepy.Cursor(api.user_timeline, id=name, tweet_mode='extended').items(tweetCount):
                    #print("-------------->2")
                    writeToFileDict_u={}
                    parsedTweet = json.loads(json.dumps(status._json))
                    #print("-------------->3")
                    if (str(parsedTweet['coordinates']) != 'None'):
                        #print(print(parsedTweet))
                        #print(parsedTweet["coordinates"])
                        for elem in setOfKeywords: #if that specific word exists in the tweet, tag it
                            #if(elem.lower() in parsedTweet["full_text"].lower()):
                            if(1):
                                count=0
                                lat = 0
                                long = 0
                                for coordinates in parsedTweet["coordinates"]["coordinates"]:
                                	count += 1
                                	if (count == 1):
                                		long = coordinates
                                	# print(coordinates)
                                	# print(tweet)
                                	else:
                                		lat = coordinates
                                # print("Long/Lat: ",long," | ",lat)
                                thisSuburb = checkWhichSuburb(long, lat)
                                cleansedTweet = p.clean(parsedTweet['full_text'])
                                #print("Tweet belongs to suburb: ", thisSuburb,"|",cleansedTweet)
                                blob = TextBlob(cleansedTweet)
                                # print("B: ", blob)
                                if blob.sentiment.polarity < 0:
                                	sentiment = "negative"
                                elif blob.sentiment.polarity == 0:
                                	sentiment = "neutral"
                                else:
                                	sentiment = "positive"
                                # print("Orignal: ",parsedTweet['text'])
                                # print("Cleansed: ",cleansedTweet)
                                writeToFileDict_u['id_tweet'] = parsedTweet["id"]
                                writeToFileDict_u['sentiment'] = sentiment
                                writeToFileDict_u['tweet'] = cleansedTweet
                                writeToFileDict_u['suburb'] = thisSuburb
                                writeToFileDict_u['long'] = long
                                writeToFileDict_u['lat'] = lat
                                writeToFileDict_u['screen_name'] = parsedTweet["user"]["screen_name"]
                                json_id_u=str(time.time())+"t"
                                #doc_id, doc_rev = db.save(writeToFileDict)
                                if (parsedTweet["id"]!=jsonTweet["id"]):
                                    if(thisSuburb!='N/A'):
                                        print("Tweet belongs to suburb: ", thisSuburb,"|",cleansedTweet)
                                        staticVariableForKeys(1,"A1")
                                        db[json_id_u] = writeToFileDict_u
                                        print("Harvested Tweets: ",staticVariableForKeys.A1)
                                    else:
                                        print("Suburb belongs to N/A region: Long: ",long," | Lat: ",lat)
                                break
                staticVariableForKeys(1,"A1")
                print("Harvested Tweets: ",staticVariableForKeys.A1)
				
        return(True)


        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(Consumer_Key_Sergei, Consumer_Secret_Sergei)
auth.set_access_token(Access_Token_Sergei, Access_Token_Secret_Sergei)
print("1-AuthAcquired")
#auth2 = OAuthHandler(Consumer_Key_Sergei, Consumer_Secret_Sergei)
#auth2.set_access_token(Access_Token_Sergei, Access_Token_Secret_Sergei)
api = tweepy.API(auth, wait_on_rate_limit=True)

twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[144.5937, -38.4339, 145.5125, -37.5113])  # Just Melbourne Australia gridbox
#twitterStream.filter(track=[
#    "Anniversary",
#        "Anniversaries",
#        "Birthday",
#        "Birthdays",
#        "Event",
#        "events",
#        "Kids",
#        "Wedding",
#        "weddings",
#        "Marriage",
#        "Husband",
#        "Wife",
#        "wife's",
#        "Couple",
#        "Couples",
#        "Grocery",
#        "Groceries",
#        "Shopping",
#        "Shoppings",
#        "Dinner",
#        "Dinners",
#        "Issues",
#        "Divorce",
#        "Divorces",
#        "Weekends",
#        "MarriedPeopleIssues",
#        "Married",
#        "MarriedIssues",
#        "MarriageIssues",
#        "UJamil",
#        "FridayNights",
#])