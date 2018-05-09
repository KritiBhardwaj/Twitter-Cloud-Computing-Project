import json
from textblob import TextBlob
import os
import io
import sys
import re
import time
import couchdb
import preprocessor as p
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from shapely.geometry import shape, Point, box
import logging

crimekeyWords=[]
alcoholkeyWords=[]
sportskeyWords=[]

#keywords
keyWordpath = 'keywords/'

#Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('/home/ubuntu/harvester.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

#Handling:
creds=sys.argv[6]
quadrant=0

#keywords to file
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

#Setting DB Details
harv_id=sys.argv[1]+" | "+sys.argv[2]+" | "+sys.argv[3]+" | "+sys.argv[4]+" | "+sys.argv[5]+" | "+creds
logger.info("Hello, I am harvester " + harv_id + "!")
Initiate="Hello, I am CouchDB: "+harv_id
logger.info(Initiate)
couchserver = couchdb.Server("http://115.146.95.134:5984/")

dbname = "harvester"
if dbname in couchserver:
	db = couchserver[dbname]
else:
	db = couchserver.create(dbname)

#ShapelyCode -Detect Suburb
suburbFileName="allsuburbs.geojson"
with open(suburbFileName) as data_file:
    grid = json.loads(data_file.read())
def checkWhichSuburb(long,lat):
	point = Point(long,lat)
	count=0
	suburb="N/A"
	for x in grid["features"]:
		count=count+1
		polygon = shape(x['geometry'])
		if polygon.contains(point):
			suburb=x['properties']['sa2_name16']
			break
	return suburb

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

#ShapelyCode -Detect Boundry
def checkIfCoordinateExistsWithinBoundry(boxMinLong,boxMinLat,boxMaxLong,boxMaxLat,long,lat):
	b = box(boxMinLong,boxMinLat,boxMaxLong,boxMaxLat)
	point = Point(long,lat)
	polygon = shape(b)
	if polygon.contains(point):
		return True
	else:
		return False

#DB Operations
def checkIfIDEXists(tweetid):
	if tweetid in db:
		mytemp = db[tweetid]
		return "true"
	else:
		return "false"

#Tweepy Code
#consumer key, consumer secret, access token, access secret.
if(creds=='2'):
	#Haaris
	consumer_key = "E50fbKWMtI5X914kL4kgfURvR"
	consumer_secret = "CLWbyVUb6b8fIMlodcpgH2jsl7Xal2qVOwGRjtYTYyVRKQTN90"
	access_token = "1301016800-qi6ql98SLPDHeNYPlw6jvhge0QVElGjoyffBeAH"
	access_token_secret = "C6tQsacmOfcTPB8uOIor24u1ChUwuPyOPohhYkUzaSRDu"
elif(creds=='1'):
	#Umair
	consumer_key= "HnXTz4v9QCtjWvn7Tpb55SmOz"
	consumer_secret= "xCd7VIrsQPrCCg1wsPrxNEvSfmUCSuI7HfTdwtthwcBmo1d4W2"
	access_token= "62274863-7eVe1DtSb20jVf7bNLjO5RwlJRqRK0cjAmVRlVfgE"
	access_token_secret = "FbOD05N6TK6wm6x4yGYXs923fX9xnzHUWoiFpkQ4bvNXc"
elif(creds=='3'):
	#Kriti
	consumer_key= "zOSTodo9yO17cv0pBU9MbJmQ9"
	consumer_secret= "8cYLBe9EDc9oNVkXbuLiE3nx6fcZhhfqCaMbwx5yHnqXawadqK"
	access_token= "949101970945490944-ytBXszR6zGY2xlrOmAEvOg3xGWeFhzs"
	access_token_secret= "hXeSM9T2NXta3Q37tRFbeqxJu5iR5HlbfHjCIgtWDnLQf"
elif(creds=='4'):
	#Sergey
	consumer_key = "Vb0cwOkSk6q5tfSfX04h9U23p"
	consumer_secret = "81aM2v0eZhJaA1ksFDicqf0piOidgShokCJudSWlKYVC5BCnI8"
	access_token = "987288793374900224-MlYHf4qwA7K3NfhnCEcLT3o3UeNJPLM"
	access_token_secret = "CGXGboiACeSWPV4PRIXdnHskWAZJSv5d0zW6pwZQsH8zm"

#Filing (if REquired)
textFileName="Q"+str(creds)+".json"
tweetFile = open(textFileName, 'a+', encoding='utf8')
tweetFile.write("[")
def checkJson(jsonContents):
    codeFlag = True if "coordinates" in jsonContents else False
    return codeFlag

#Static Variables
def staticVariableForKeys(value, keyName):
    if (keyName == "A1"):
        staticVariableForKeys.A1 += value
staticVariableForKeys.A1 = 0

#Analyse sentiment
def sentimentAnalyser(tweet):
	blob = TextBlob(tweet)
	sentiment="neutral"
	if blob.sentiment.polarity < 0:
		sentiment = "negative"
	elif blob.sentiment.polarity == 0:
		sentiment = "neutral"
	else:
		sentiment = "positive"
	return sentiment

#Process Tweet Here
def processTweet(jsonTweet,long,lat,isUser):
	messageProperties = {
		'isCrime': 0,
		'isAlcohol': 0,
		'isSports': 0
	}
	writeToFileDict={}
	thisSuburb = checkWhichSuburb(long, lat)
	
	if(isUser):
		rawtweet=jsonTweet['full_text']
		cleansedTweet = p.clean(jsonTweet['full_text'])
	else:
		rawtweet=jsonTweet['text']
		cleansedTweet = p.clean(jsonTweet['text'])

	logger.info("Lat,Long: "+str(lat)+","+str(long)+" | Suburb: "+thisSuburb+" | Tweet: "+cleansedTweet)
	
	sentiment = sentimentAnalyser(rawtweet)
	
	tweet_id=str(jsonTweet["id"])+"t"
	writeToFileDict['id_tweet'] = jsonTweet["id"]
	writeToFileDict['sentiment'] = sentiment
	writeToFileDict['tweet'] = cleansedTweet
	writeToFileDict['suburb'] = thisSuburb
	writeToFileDict['long'] = long
	writeToFileDict['lat'] = lat
	writeToFileDict['rawtweet']=rawtweet
	writeToFileDict['screen_name'] = jsonTweet["user"]["screen_name"]
	writeToFileDict['raw']=jsonTweet

	checkRawTweetMessage(messageProperties, rawtweet.encode('ascii', 'ignore'))

	writeToFileDict['crime'] = messageProperties['isCrime']
	writeToFileDict['sports'] = messageProperties['isSports']
	writeToFileDict['alcohol'] = messageProperties['isAlcohol']
	if(checkIfIDEXists(tweet_id)=="false"):
		try:
			db[tweet_id] = writeToFileDict
			LogHarv=harv_id+"-> Record Inserted!"
			logger.info(LogHarv)
		except couchdb.http.ResourceConflict:
			LogHarv=harv_id+"-> Document update conflict!"
			logger.info(LogHarv)
	else:
		logger.info("Duplicate id: "+tweet_id)

#Keywords to ignore.
setOfKeywords = [
        "Temperature",
        "Humidity",
		"Rain",
		"trending",
		"Babe",
		"Hot",
		"Sex",
		"Porn"
]

def rejectThisUserCrawl(tweet):
	for elem in setOfKeywords:
		if(elem.lower() in tweet["full_text"].lower()):
			return True
		else:
			return False
			

class listener(StreamListener):
	def on_data(self, data):
		#Load tweet as json.
		jsonTweet = json.loads(data) 
		#Does tweet have coordinate tag.
		if(checkJson(data)==True): 
			#Is the coordinate tag not null.
			if (str(jsonTweet["coordinates"]) != "None"): 
				count=0
				lat = 0
				long = 0
				#GetLong/Lat of the tweet.
				for coordinates in jsonTweet["coordinates"]["coordinates"]: #
					count += 1
					if (count == 1):
						long = coordinates
					else:
						lat = coordinates
				#Post-process: Check if tweet exists within strict boundy. Only then process it.
				if(checkIfCoordinateExistsWithinBoundry(bMinLo,bMinLa,bMaxLo,bMaxLa,long,lat)):
				#if(1):
					logger.info("Yes, the tweet exists within specified boundry. Proceed=> "+"Lat,Long: "+str(lat)+","+str(long))
					processTweet(jsonTweet,long,lat,False)
					#Extract user.
					name = jsonTweet["user"]["screen_name"]
					tweetCount = 10000
					logger.info("-------------->Starting new user tweet fetch<--------------")
					for status in tweepy.Cursor(api.user_timeline, id=name, tweet_mode='extended').items(tweetCount):
						userTweet = json.loads(json.dumps(status._json))
						if(rejectThisUserCrawl(userTweet)): #If this tweet's keywords are blacklisted!
							logger.info("Rejecting user's tweet...")
							break
						if (str(userTweet["coordinates"]) != "None"): 
							count=0
							lat = 0
							long = 0
							#GetLong/Lat of the tweet.
							for coordinates in userTweet["coordinates"]["coordinates"]: #
								count += 1
								if (count == 1):
									long = coordinates
								else:
									lat = coordinates
							#Check if tweet exists within melbourne's boundry, since a user can be anywhere in his timeline (scraping step)
							if(checkIfCoordinateExistsWithinBoundry(144.5937,-38.4339,145.5125,-37.5113,long,lat)):
							#if(1):
								logger.info("User-Yes, the tweet exists within specified boundry. Proceed=> "+"Lat,Long: "+str(lat)+","+str(long))
								processTweet(userTweet,long,lat,True)
							else:
								logger.info("User-No, the tweet does no exists within specified boundry. Halt=> "+"Lat,Long: "+str(lat)+","+str(long))	
				else:
					logger.info("Tweet-No, the tweet does not exists within specified boundry. Halt=> "+"Lat,Long: "+str(lat)+","+str(long))
				logger.info("\n\n")
		return(True)

	def on_error(self, status):
		logger.info(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
logger.info("AuthAcquired...")
bMinLo=float(sys.argv[2])
bMinLa=float(sys.argv[3])
bMaxLo=float(sys.argv[4])
bMaxLa=float(sys.argv[5])

def getTweets(quadrant,bMinLo,bMinLa,bMaxLo,bMaxLa):
	twitterStream = Stream(auth, listener())
	gridBoxVars="Gridbox Assgned: bMinLa/bMinLo:"+bMinLa+"/"+bMinLo+" | bMaxLa/bMaxLo:"+bMaxLa+"/"+bMaxLo
	logger.info(gridBoxVars)
	twitterStream.filter(locations=[float(bMinLo),float(bMinLa),float(bMaxLo),float(bMaxLa)])#Melbourne, Australia's gridbox: -38.4339,144.5937 | -37.5113,145.5125
	
		
while (True):		
	try:
		getTweets(quadrant,sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
	except Exception as e:
		logger.error(e)
		time.sleep(10)
		getTweets(quadrant,sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])