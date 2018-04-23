'''This is a sample test extraction utility using tweepy'''

import tweepy
consumer_key = "E50fbKWMtI5X914kL4kgfURvR"
consumer_secret = "CLWbyVUb6b8fIMlodcpgH2jsl7Xal2qVOwGRjtYTYyVRKQTN90"
access_token = "1301016800-qi6ql98SLPDHeNYPlw6jvhge0QVElGjoyffBeAH"
access_token_secret = "C6tQsacmOfcTPB8uOIor24u1ChUwuPyOPohhYkUzaSRDu"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



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
query = "UJamil"
results = api.search(q=query, geocode='-37.800,144.960,10km')
for tweet in results:
  print(tweet.user.screen_name,"Tweeted:",tweet.text)
  print("Location:" + tweet.user.location)
  print(" ")


# api = tweepy.API(auth)
# query = "C&CC module"
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

