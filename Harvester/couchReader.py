import couchdb
import os
import io
import json

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
    print("reachedSub1")
    matchedCheck = False;
    print(rawt)
    rawTweetSplit = str(rawt).split(' ')
    print("reachedSub2")
    for elem in crimekeyWords:
        for rawSplit in rawTweetSplit:
            if str(elem).lower() == rawSplit.lower():
                messageProperties['isCrime'] += 1
                matchedCheck = True
                break
    for elem in alcoholkeyWords:
        for rawSplit in rawTweetSplit:
            if str(elem).lower()== rawSplit.lower():
                messageProperties['isAlcohol'] += 1
                matchedCheck = True
                break
    for elem in sportskeyWords:
        for rawSplit in rawTweetSplit:
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
    print("Im here")
    rawtweet = jsonDoc['rawtweet']
    print("Reached here")
    writeToFileDict['id_tweet'] = tweet_id
    writeToFileDict['rawtweet'] = rawtweet
    print("Reached here 2")

    checkRawTweetMessage(messageProperties, rawtweet)
    print("Reached here 3")
    writeToFileDict['tweet'] = jsonDoc['tweet']
    print("Reached here 3")
    writeToFileDict['raw'] = jsonDoc['raw']
    print("Reached here 4")
    writeToFileDict['screen_name'] = jsonDoc['screen_name']
    print("Reached here 5")
    writeToFileDict['lat'] = jsonDoc['lat']
    print("Reached here 6")
    writeToFileDict['long'] = jsonDoc['long']
    print("Reached here 7")
    writeToFileDict['sentiment'] = jsonDoc['sentiment']
    print("Reached here 8")
    writeToFileDict['suburb'] = jsonDoc['suburb']
    print("Reached here 9")
    writeToFileDict['crime'] = messageProperties['isCrime']
    print("Reached here 10")
    writeToFileDict['sports'] = messageProperties['isSports']
    print("Reached here 11")
    writeToFileDict['alcohol'] = messageProperties['isAlcohol']
    print("Reached here 12")

    if (checkIfIDEXists(tweet_id) == "false"):
        try:
            db[tweet_id] = writeToFileDict
            print("Record Inserted!")
        except couchdb.http.ResourceConflict:
            print("Document update conflict!")
    else:
        print("Duplicate id: ", tweet_id)

if __name__ == "__main__":
    path = 'harvest_final_data_subset.json'
    keyWordpath = 'keywords/'

    keywordsToFile(keyWordpath)
    couchsrv = "http://115.146.95.134:5984/"
    dbname = "harvest_out"
    db = setupDB(couchsrv,dbname)
    readfile(path)
