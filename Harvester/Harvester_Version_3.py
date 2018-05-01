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
from shapely.geometry import shape, Point, box

#Handling:
creds=1
quadrant=1

#Setting DB Details
print("Hello, I am CouchDB!")
couchserver = couchdb.Server("http://115.146.95.134:5984/")
dbname = "harvest_final"
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
		#print(count)
		polygon = shape(x['geometry'])
		if polygon.contains(point):
			suburb=x['properties']['sa2_name16']
			#print('This coordinate belongs to :',x['properties']['sa2_name16'])
			break
	return suburb
#thisSuburb=checkWhichSuburb(144.900,-37.760)	
#print(thisSuburb)

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
if(creds==1):
	#Haris
	consumer_key = "E50fbKWMtI5X914kL4kgfURvR"
	consumer_secret = "CLWbyVUb6b8fIMlodcpgH2jsl7Xal2qVOwGRjtYTYyVRKQTN90"
	access_token = "1301016800-qi6ql98SLPDHeNYPlw6jvhge0QVElGjoyffBeAH"
	access_token_secret = "C6tQsacmOfcTPB8uOIor24u1ChUwuPyOPohhYkUzaSRDu"
elif(creds==2):
	#Umair
	consumer_key= "HnXTz4v9QCtjWvn7Tpb55SmOz"
	consumer_secret= "xCd7VIrsQPrCCg1wsPrxNEvSfmUCSuI7HfTdwtthwcBmo1d4W2"
	access_token= "62274863-7eVe1DtSb20jVf7bNLjO5RwlJRqRK0cjAmVRlVfgE"
	access_token_secret = "FbOD05N6TK6wm6x4yGYXs923fX9xnzHUWoiFpkQ4bvNXc"
elif(creds==3):
	#Krits
	consumer_key= "zOSTodo9yO17cv0pBU9MbJmQ9"
	consumer_secret= "8cYLBe9EDc9oNVkXbuLiE3nx6fcZhhfqCaMbwx5yHnqXawadqK"
	access_token= "949101970945490944-ytBXszR6zGY2xlrOmAEvOg3xGWeFhzs"
	access_token_secret= "hXeSM9T2NXta3Q37tRFbeqxJu5iR5HlbfHjCIgtWDnLQf"
elif(creds==4):
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
	# print("B: ", blob)
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
	writeToFileDict={}
	thisSuburb = checkWhichSuburb(long, lat)
	
	if(isUser):
		rawtweet=jsonTweet['full_text']
		cleansedTweet = p.clean(jsonTweet['full_text'])
	else:
		rawtweet=jsonTweet['text']
		cleansedTweet = p.clean(jsonTweet['text'])
	
	print("Lat,Long: ",lat,",",long," | Suburb: ",thisSuburb," | Tweet: ",cleansedTweet)
	
	sentiment = sentimentAnalyser(rawtweet)
	
	tweet_id=str(jsonTweet["id"])+"t"
	#json_id=str(time.time())
	writeToFileDict['id_tweet'] = jsonTweet["id"]
	writeToFileDict['sentiment'] = sentiment
	writeToFileDict['tweet'] = cleansedTweet
	writeToFileDict['suburb'] = thisSuburb
	writeToFileDict['long'] = long
	writeToFileDict['lat'] = lat
	writeToFileDict['rawtweet']=rawtweet
	writeToFileDict['screen_name'] = jsonTweet["user"]["screen_name"]
	writeToFileDict['raw']=jsonTweet
	#print(writeToFileDict)
	if(checkIfIDEXists(tweet_id)=="false"):
		try:
			db[tweet_id] = writeToFileDict
			print("Record Inserted!")
		except couchdb.http.ResourceConflict:
			print("Document update conflict!")
	else:
		print("Duplicate id: ",tweet_id)



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
				#print("Grid Available=> bMinLa/bMinLo:",bMinLa,"/",bMinLo," | bMaxLa/bMaxLo:",bMaxLa,"/",bMaxLo)
				if(checkIfCoordinateExistsWithinBoundry(bMinLo,bMinLa,bMaxLo,bMaxLa,long,lat)):
					print("Yes, the tweet exists within specified boundry. Proceed=> ","Lat,Long: ",lat,",",long)
					processTweet(jsonTweet,long,lat,False)
					#Extract user.
					name = jsonTweet["user"]["screen_name"]
					tweetCount = 1000
					print("-------------->Starting new user tweet fetch<--------------")
					for status in tweepy.Cursor(api.user_timeline, id=name, tweet_mode='extended').items(tweetCount):
						userTweet = json.loads(json.dumps(status._json))
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
							if(checkIfCoordinateExistsWithinBoundry(bMinLo,bMinLa,bMaxLo,bMaxLa,long,lat)):
								print("User-Yes, the tweet exists within specified boundry. Proceed=> ","Lat,Long: ",lat,",",long)
								processTweet(userTweet,long,lat,True)
							else:
								print("User-No, the tweet does no exists within specified boundry. Halt=> ","Lat,Long: ",lat,",",long)	
				else:
					print("Tweet-No, the tweet does no exists within specified boundry. Halt=> ","Lat,Long: ",lat,",",long)
				print("\n\n")
		return(True)

	def on_error(self, status):
		print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
print("AuthAcquired...")
api = tweepy.API(auth, wait_on_rate_limit=True)
twitterStream = Stream(auth, listener())

#-37.9726,144.5937,Q1S
#-37.5113,145.0531,Q1E
#-38.4339,144.5937,Q2S
#-37.9726,145.0531,Q2E
#-37.9726,145.0531,Q4S
#-37.5113,145.5125,Q4E
#-38.4339,145.0531,Q3S
#-37.9726,145.5125,Q3E


bMinLo=0
bMinLa=0
bMaxLo=0
bMaxLa=0

if(quadrant==1):
	bMinLo=144.5937
	bMinLa=-37.9726
	bMaxLo=145.0531
	bMaxLa=-37.5113
	print("Quadrant:1\nbMinLa/bMinLo:",bMinLa,"/",bMinLo," | bMaxLa/bMaxLo:",bMaxLa,"/",bMaxLo)
	twitterStream.filter(locations=[bMinLo,bMinLa,bMaxLo,bMaxLa])
elif(quadrant==2):
	bMinLo=144.5937
	bMinLa=-38.4339
	bMaxLo=145.0531
	bMaxLa=-37.9726
	print("Quadrant:2\nbMinLa/bMinLo:",bMinLa,"/",bMinLo," | bMaxLa/bMaxLo:",bMaxLa,"/",bMaxLo)
	twitterStream.filter(locations=[bMinLo,bMinLa,bMaxLo,bMaxLa])
elif(quadrant==3):
	bMinLo=145.0531
	bMinLa=-38.4339
	bMaxLo=145.5125
	bMaxLa=-37.9726
	print("Quadrant:3\nbMinLa/bMinLo:",bMinLa,"/",bMinLo," | bMaxLa/bMaxLo:",bMaxLa,"/",bMaxLo)
	twitterStream.filter(locations=[bMinLo,bMinLa,bMaxLo,bMaxLa])
elif(quadrant==4):
	bMinLo=145.0531
	bMinLa=-37.9726
	bMaxLo=145.5125
	bMaxLa=-37.5113
	print("Quadrant:4\nbMinLa/bMinLo:",bMinLa,"/",bMinLo," | bMaxLa/bMaxLo:",bMaxLa,"/",bMaxLo)
	twitterStream.filter(locations=[bMinLo,bMinLa,bMaxLo,bMaxLa])
elif(quadrant==0):
	bMinLo=144.5937
	bMinLa=-38.4339
	bMaxLo=145.5125
	bMaxLa=-37.5113
	print("Melbourne, Australia's gridbox.\nbMinLa/bMinLo:",bMinLa,"/",bMinLo," | bMaxLa/bMaxLo:",bMaxLa,"/",bMaxLo)
	twitterStream.filter(locations=[bMinLo,bMinLa,bMaxLo,bMaxLa])#Melbourne, Australia's gridbox: -38.4339,144.5937 | -37.5113,145.5125