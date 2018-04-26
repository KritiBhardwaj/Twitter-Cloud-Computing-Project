from shapely.geometry import shape, Point
import json
import tweepy
import os
import json
import preprocessor as p

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
#thisSuburb=checkWhichSuburb(144.900,-37.760)	
#print(thisSuburb)

#Tweepy code

def writeToFile(fileName, message):
    fileName.write(message)

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

onesuburbName = {
        'Melbourne':'10|-37.800|145.000'
}

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


Consumer_key_Kriti= "zOSTodo9yO17cv0pBU9MbJmQ9"
Consumer_Secret_Kriti= "8cYLBe9EDc9oNVkXbuLiE3nx6fcZhhfqCaMbwx5yHnqXawadqK"
Access_Token_Kriti= "949101970945490944-ytBXszR6zGY2xlrOmAEvOg3xGWeFhzs"
Access_Token_Secret_Kriti= "hXeSM9T2NXta3Q37tRFbeqxJu5iR5HlbfHjCIgtWDnLQf"

auth = tweepy.OAuthHandler(Consumer_key_Kriti, Consumer_Secret_Kriti)
auth.set_access_token(Access_Token_Kriti, Access_Token_Secret_Kriti)
api = tweepy.API(auth, wait_on_rate_limit=True,parser=tweepy.parsers.JSONParser())
#api = tweepy.API(auth, wait_on_rate_limit=True)
language = "en"
count = 100

p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.MENTION, p.OPT.SMILEY)
for subs in onesuburbName:
    tweetMessageFile = open('OriginalTweets.txt', 'w', encoding='utf8')
    tweetFile = open('tweetsCleansed.json', 'w', encoding='utf8')
    tweetFileDetails = open('tweetsDetails.txt', 'w', encoding='utf8')
    subDetails = onesuburbName[subs].split('|')
    subradius = str(subDetails[0])
    sublat = str(subDetails[1])
    sublon = str(subDetails[2])
    geocode = sublat + ',' + sublon + ',' + subradius + 'km' #geocode format: '-37.800,144.960,70km'

data={}
tweetFile.write("[")
for elem in setOfKeywords:
	results = api.search(q=elem, lang=language, count=5000, geocode=geocode,tweet_mode='extended') #Melbourne
	for tweet in results["statuses"]:
		parsedTweet = json.loads(json.dumps(tweet))
		if(str(parsedTweet['coordinates'])!='None'):
			#print(parsedTweet['coordinates']['coordinates'])
			count=0
			lat=0
			long=0
			for coordinates in parsedTweet['coordinates']['coordinates']:
				count+=1
				if(count==1):
					long=coordinates
					#print(coordinates)
					#print(tweet)
				else:
					lat=coordinates
			#print("Long/Lat: ",long," | ",lat)
			thisSuburb=checkWhichSuburb(long,lat)	
			print("Tweet belongs to suburb: ",thisSuburb)
			cleansedTweet = p.clean(parsedTweet['full_text'])
			#print("Orignal: ",parsedTweet['full_text'])
			#print("Cleansed: ",cleansedTweet)
			data['id']=parsedTweet['id']
			data['tweet'] = parsedTweet['full_text']
			data['suburb']=thisSuburb
			data['long']=long
			data['lat']=lat
			writeLine=json.dumps(data, ensure_ascii=False)
			writeLine+=",\n"
			tweetFile.write(writeLine)
tweetFile.close()

with open('tweetsCleansed.json', 'rb+') as f:
    f.seek(0,2)                 # end of file
    size=f.tell()               # the size...
    f.truncate(size-2) 

tweetFile = open('tweetsCleansed.json', 'a+', encoding='utf8')
tweetFile.write(']')
tweetFile.close()
