'''This is a sample test extraction utility using tweepy'''
#The twitter API searches in the last 7 days only. Extracts the tweets

import tweepy
import os
import preprocessor as p

'''Helpers'''

def writeToFile(fileName, message):
    fileName.write(message)

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#Suburb Details
suburbNames = {
        'Abbotsford':'0.021|-37.800|145.000',
        'Aberfeldie':'0.019|-37.760|144.900',
        'Albert Park':'0.027|-37.840|144.960',
        'Alphington':'0.026|-37.780|145.030',
        'Armadale':'0.023|-37.860|145.020',
        'Ascot Vale':'0.030|-37.780|144.920',
        'Balaclava':'0.014|-37.870|145.000',
        'Balwyn':'0.036|-37.810|145.080',
        'Balwyn North':'0.046|-37.790|145.070',
        'Bellfield':'0.015|-36.940|143.210',
        'Brunswick':'0.035|-37.760|144.940',
        'Brunswick East':'0.023|-37.760|144.980',
        'Brunswick West':'0.027|-37.770|144.940',
        'Burnley':'0.020|-37.830|145.010',
        'Camberwell':'0.037|-37.820|145.060',
        'Canterbury':'0.027|-37.840|145.090',
        'Carlton':'0.021|-37.780|144.970',
        'Carlton North':'0.021|-37.780|144.970',
        'Caulfield':'0.019|-37.880|145.030',
        'Caulfield East':'0.017|-37.880|145.040',
        'Caulfield North':'0.031|-38.030|145.310',
        'Caulfield South':'0.028|-37.880|145.030',
        'Clifton Hill':'0.019|-37.790|144.990',
        'Coburg':'0.041|-37.730|144.960',
        'Collingwood':'0.017|-37.800|144.980',
        'Cremorne':'0.013|-37.830|145.010',
        'Docklands':'0.027|-37.810|144.950',
        'East Melbourne':'0.021|-37.810|144.950',
        'Elsternwick':'0.025|-37.880|145.000',
        'Elwood':'0.025|-37.880|145.000',
        'Essendon':'0.038|-37.760|144.900',
        'Essendon West':'0.015|-37.760|144.900',
        'Fairfield':'0.032|-37.780|145.030',
        'Fitzroy':'0.032|-37.800|144.980',
        'Fitzroy North':'0.024|-37.790|144.990',
        'Flemington':'0.017|-37.790|144.930',
        'Footscray':'0.034|-37.800|144.900',
        'Gardenvale':'0.008|-37.880|145.000',
        'Glen Iris':'0.041|-37.850|145.070',
        'Hawthorn':'0.037|-37.840|145.050',
        'Hawthorn East':'0.030|-37.830|145.040',
        'Ivanhoe':'0.035|-37.770|145.040',
        'Ivanhoe East':'0.023|-37.770|145.040',
        'Kensington':'0.030|-37.790|144.930',
        'Kew':'0.050|-37.810|145.040',
        'Kew East':'0.031|-37.800|145.050',
        'Kingsville':'0.013|-37.810|144.850',
        'Kooyong':'0.011|-37.840|145.030',
        'Maidstone':'0.027|-37.810|144.850',
        'Malvern':'0.026|-37.840|145.030',
        'Malvern East':'0.042|-37.880|145.040',
        'Maribyrnong':'0.036|-37.780|144.920',
        'Melbourne':'0.038|-38.370|144.770',
        'Middle Park':'0.015|-37.840|144.960',
        'Moonee Ponds':'0.032|-37.770|144.920',
        'Newport':'0.035|-37.840|144.880',
        'North Melbourne':'0.024|-37.910|145.060',
        'Northcote':'0.039|-37.770|145.000',
        'Parkville':'0.031|-37.800|144.960',
        'Pascoe Vale South':'0.027|-37.730|144.940',
        'Port Melbourne':'0.048|-37.830|144.960',
        'Prahran':'0.022|-37.850|144.990',
        'Preston':'0.052|-37.740|145.030',
        'Princes Hill':'0.010|-37.780|144.970',
        'Richmond':'0.030|-37.830|145.010',
        'Ripponlea':'0.008|-37.880|145.000',
        'Seddon':'0.015|-37.800|144.900',
        'South Kingsville':'0.012|-37.840|144.880',
        'South Melbourne':'0.024|-37.930|145.030',
        'South Wharf':'0.008|-37.820|144.970',
        'South Yarra':'0.034|-36.990|144.060',
        'Southbank':'0.020|-37.820|144.970',
        'Spotswood':'0.027|-37.840|144.880',
        'St Kilda':'0.027|-37.870|144.980',
        'St Kilda East':'0.023|-37.870|145.000',
        'St Kilda West':'0.011|-37.870|144.980',
        'Thornbury':'0.035|-37.760|145.000',
        'Toorak':'0.032|-37.840|145.000',
        'Tottenham':'0.022|-37.810|144.850',
        'Travancore':'0.010|-37.780|144.920',
        'West Footscray':'0.030|-37.810|144.850',
        'West Melbourne':'0.039|-37.810|144.940',
        'Williamstown':'0.036|-37.860|144.900',
        'Williamstown North':'0.021|-37.860|144.900',
        'Windsor':'0.015|-37.850|144.990',
        'Yarraville':'0.036|-37.820|144.890'
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

'''Access Credentials'''

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

auth = tweepy.OAuthHandler(Consumer_Key_Umair, Consumer_Secret_Umair)
auth.set_access_token(Access_Token_Umair, Access_Token_Secret_Umair)
api = tweepy.API(auth, wait_on_rate_limit=True)
language = "en"
count = 100


p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.MENTION, p.OPT.SMILEY)
for subs in suburbNames:
    path = 'suburb-tweets\\'+ subs + '\\'
    assure_path_exists(path)
    tweetMessageFile = open(path + 'OriginalTweets.txt', 'w', encoding='utf8')
    tweetFile = open(path + 'tweetsCleansed.txt', 'w', encoding='utf8')
    tweetFileDetails = open(path + 'tweetsDetails.txt', 'w', encoding='utf8')
    subDetails = suburbNames[subs].split('|')
    subradius = str(subDetails[0])
    sublat = str(subDetails[1])
    sublon = str(subDetails[2])
    geocode = sublat + ',' + sublon + ',' + subradius + 'km' #geocode format: '-37.800,144.960,70km'

    for elem in setOfKeywords:
      results = api.search(q=elem, lang=language, count=500, geocode=geocode,tweet_mode='extended') #Melbourne

      for tweet in results:
        print(tweet)
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






'''Extra Functionalities'''

#For results in melbourne
# api = tweepy.API(auth)
# query = "Melbourne"
# language = "en"
# lat = '-37.820'
# lon = '145.060'
# radius = '0.037'
# geocode = lat + ',' + lon + ',' + radius + 'km'
#
#
# results = api.search(q=query,geocode=geocode)
# for tweet in results:
#   print(tweet.user.screen_name,"Tweeted:",tweet.text)
#   print("Location:" + tweet.user.location)
#   print(" ")

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

