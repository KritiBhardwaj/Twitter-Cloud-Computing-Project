'''This is a sample test extraction utility using tweepy'''
#The twitter API searches in the last 7 days only

import tweepy
import json
import preprocessor as p

consumer_key = "E50fbKWMtI5X914kL4kgfURvR"
consumer_secret = "CLWbyVUb6b8fIMlodcpgH2jsl7Xal2qVOwGRjtYTYyVRKQTN90"
access_token = "1301016800-qi6ql98SLPDHeNYPlw6jvhge0QVElGjoyffBeAH"
access_token_secret = "C6tQsacmOfcTPB8uOIor24u1ChUwuPyOPohhYkUzaSRDu"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
language = "en"
count = 100


#Kriti Please Update
suburbNames = {




}

#Kriti Please Update
suburbRadius = {


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


#pulling the 20 recent most tweets
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
   #print(tweet.user.location)


'''
#for user searches
name = "umairjamil_"
tweetCount = 100
results = api.user_timeline(id=name, count=tweetCount)
for tweet in results:
   print("Location:" + tweet.user.location)
   print(" Name:" + tweet.user.name)
   print(" Tweet:" + tweet.text)
   print(" ")
'''

api = tweepy.API(auth)
#query = "Anniversary"

p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.MENTION, p.OPT.SMILEY)

tweetMessageFile = open('OriginalTweets.txt','w',encoding='utf8')
tweetFile = open('tweetsCleansed.txt','w',encoding='utf8')
tweetFileDetails = open('tweetsDetails.txt','w',encoding='utf8')
for elem in setOfKeywords:
  resultsMelbourne = api.search(q=elem, lang=language, count=500, geocode='-37.800,144.960,70km',tweet_mode='extended') #Melbourne
  resultsSydney = api.search(q=elem, lang=language, count=500, geocode='-33.90,150.99,70km',tweet_mode='extended') #Sydney
  print(elem)
  for tweet in resultsMelbourne:
    parserTweet = p.parse(tweet.full_text)
    tweetMessageFile.write(tweet.full_text + '\n')

    cleansedTweet = p.clean(tweet.full_text)
    tweetFile.write(cleansedTweet + '\n')

    hashtags = str(parserTweet.hashtags)
    emojis = str(parserTweet.emojis)
    smileys = str(parserTweet.smileys)
    mentions = str(parserTweet.mentions)
    location = str(tweet.user.location)
    tweetFileDetails.write("*********" + '\n')
    tweetFileDetails.write(cleansedTweet + '\n')
    tweetFileDetails.write("Hashtags: " + hashtags + '\n')
    tweetFileDetails.write("Emojis: " + emojis + '\n')
    tweetFileDetails.write("Smileys: " + smileys + '\n')
    tweetFileDetails.write("Mentions: " + mentions + '\n')
    tweetFileDetails.write("Location: " + location + '\n')

  for tweet in resultsSydney:
    parserTweet = p.parse(tweet.full_text)
    tweetMessageFile.write(tweet.full_text + '\n')

    cleansedTweet = p.clean(tweet.full_text)
    tweetFile.write(cleansedTweet + '\n')

    hashtags = str(parserTweet.hashtags)
    emojis = str(parserTweet.emojis)
    smileys = str(parserTweet.smileys)
    mentions = str(parserTweet.mentions)
    location = str(tweet.user.location)
    tweetFileDetails.write("*********" + '\n')
    tweetFileDetails.write(cleansedTweet + '\n')
    tweetFileDetails.write("Hashtags: " + hashtags + '\n')
    tweetFileDetails.write("Emojis: " + emojis + '\n')
    tweetFileDetails.write("Smileys: " + smileys + '\n')
    tweetFileDetails.write("Mentions: " + mentions + '\n')
    tweetFileDetails.write("Location: " + location + '\n')

tweetMessageFile.close()
tweetFile.close()
tweetFileDetails.close()

#For results in melbourne
# api = tweepy.API(auth)
# query = "Melbourne"
# language = "en"
# results = api.search(q=query,geocode='-37.800,144.960,50km')
#
# #print(len(api.search(geocode='-33.602131,-70.576876,100000km')))
# #results = api.search(q=query, lang=language, count=100, geocode='-37.760, 144.900,100km')
# for tweet in results:
#   print(tweet.user.screen_name,"Tweeted:",tweet.text)
#   print("Location:" + tweet.user.location)
#   print(" ")
#
# #location grid for melbourne:
# #