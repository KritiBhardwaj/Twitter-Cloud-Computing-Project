import couchdb
import os
import io
import re
import json

path = 'harvest_file_data.json'
db = None
crimekeyWords=[]
alcoholkeyWords=[]
sportskeyWords=[]

def setupDB(srv,dbname):
    couchserver = couchdb.Server(srv)
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)
    return db

def keywordsToFile(keyWordpath):
    global crimekeyWords
    global alcoholkeyWords
    global sportskeyWords
    for filename in os.listdir(keyWordpath):
        if filename.lower() == 'crime.txt':
            keywordFile = io.open(keyWordpath + filename, encoding='utf8')
            for line in keywordFile:
                line = line.split(',')
                crimekeyWords=line
        if filename.lower() == 'alcohol.txt':
            keywordFile = io.open(keyWordpath + filename, encoding='utf8')
            for line in keywordFile:
                line = line.split(',')
                alcoholkeyWords=line
        if filename.lower() == 'sports.txt':
            keywordFile = io.open(keyWordpath + filename, encoding='utf8')
            for line in keywordFile:
                line = line.split(',')
                sportskeyWords=line

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

def checkIfIDEXists(tweetid):
    if tweetid in db:
        mytemp = db[tweetid]
        return "true"
    else:
        return "false"

def checkRawTweetMessage(messageProperties,rawt):
    matchedCheck = False;
    rawTweetSplit = str(rawt).split(' ')
    for elem in crimekeyWords:
        for rawSplit in rawTweetSplit:
            rawSplit = rawSplit.lower()
            rawSplit = re.sub(r'[^A-Za-z0-9]+', r'', rawSplit)
            if str(elem).lower() == rawSplit:
                messageProperties['isCrime'] += 1
                matchedCheck = True
                break
    for elem in alcoholkeyWords:
        for rawSplit in rawTweetSplit:
            rawSplit = rawSplit.lower()
            rawSplit = re.sub(r'[^A-Za-z0-9]+', r'', rawSplit)
            if str(elem).lower()== rawSplit.lower():
                messageProperties['isAlcohol'] += 1
                matchedCheck = True
                break
    for elem in sportskeyWords:
        for rawSplit in rawTweetSplit:
            rawSplit = rawSplit.lower()
            rawSplit = re.sub(r'[^A-Za-z0-9]+', r'', rawSplit)
            if str(elem).lower()== rawSplit.lower():
                messageProperties['isSports'] += 1
                matchedCheck = True
                break
    if matchedCheck:
        return True
    else:
        return False

#Disabled
# def checkSoundexofRawTweetWords(messageProperties,rawtweet):
#     lineSplit = rawtweet.split(' ')
#     for elem in crimekeyWords:
#         elemSoundex = soundex(elem)
#         for lineElem in lineSplit:
#             if elemSoundex == soundex(lineElem):
#                 messageProperties['isCrime'] = 1
#                 break;
#     for elem in alcoholkeyWords:
#         elemSoundex = soundex(elem)
#         for lineElem in lineSplit:
#             if elemSoundex == soundex(lineElem):
#                 messageProperties['isAlcohol'] = 1
#                 break;
#     for elem in sportskeyWords:
#         elemSoundex = soundex(elem)
#         for lineElem in lineSplit:
#             if elemSoundex == soundex(lineElem):
#                 messageProperties['isSports'] = 1
#                 break;

def processTweet(line):
    messageProperties = {
        'isCrime': 0,
        'isAlcohol': 0,
        'isSports': 0
    }

    writeToFileDict = {}
    line = line[:-2]
    jsonTweet = json.loads(line)
    jsonDoc = jsonTweet['doc']
    #jsonDoc = json.dumps(jsonTweet['doc']) #dumps makes the python single quotes to double quotes

    tweet_id = jsonDoc['id_tweet']
    tweet_id = str(tweet_id)+'t'
    rawtweet = jsonDoc['rawtweet']
    writeToFileDict['id_tweet'] = tweet_id
    writeToFileDict['rawtweet'] = rawtweet

    checkRawTweetMessage(messageProperties, rawtweet.encode('ascii','ignore'))
    writeToFileDict['tweet'] = jsonDoc['tweet']
    writeToFileDict['raw'] = jsonDoc['raw']
    writeToFileDict['screen_name'] = jsonDoc['screen_name']
    writeToFileDict['lat'] = jsonDoc['lat']
    writeToFileDict['long'] = jsonDoc['long']
    writeToFileDict['sentiment'] = jsonDoc['sentiment']
    writeToFileDict['suburb'] = jsonDoc['suburb']
    writeToFileDict['crime'] = messageProperties['isCrime']
    writeToFileDict['sports'] = messageProperties['isSports']
    writeToFileDict['alcohol'] = messageProperties['isAlcohol']

    if (checkIfIDEXists(tweet_id) == "false"):
        try:
            db[tweet_id] = writeToFileDict
            print("Record Inserted!")
        except couchdb.http.ResourceConflict:
            print("Document update conflict!")
    else:
        print("Duplicate id: ", tweet_id)

def Initialize(path):
    global db
    keyWordpath = 'keywords/'
    keywordsToFile(keyWordpath)
    couchsrv = "http://115.146.95.134:5984/"
    dbname = "harvester"
    db = setupDB(couchsrv, dbname)

if __name__ == "__main__":
    try:
        Initialize(path)
        readfile(path)
    except couchdb.ServerError:
        print("Server Error - Trying again")
        Initialize(path)
        readfile(path)