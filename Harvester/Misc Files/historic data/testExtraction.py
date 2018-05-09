'''This is a sample test extraction utility using tweepy'''
#The twitter API searches in the last 7 days only. Extracts the tweets

import tweepy
import os
import json
import preprocessor as p

'''Helpers'''

def writeToFile(fileName, message):
    fileName.write(message)

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


oneSub = {
'Camberwell':'10|-37.820|145.060',
}

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

#Keys REMOVED
auth = tweepy.OAuthHandler(Consumer_key_Kriti, Consumer_Secret_Kriti)
auth.set_access_token(Access_Token_Kriti, Access_Token_Secret_Kriti)
api = tweepy.API(auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())
language = "en"
count = 10


p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.MENTION, p.OPT.SMILEY)
for subs in oneSub:
    path = 'suburb-tweets\\'+ subs + '\\'
    assure_path_exists(path)
    #tweetMessageFile = open(path + 'OriginalTweets.txt', 'w', encoding='utf8')
    #tweetFile = open(path + 'tweetsCleansed.txt', 'w', encoding='utf8')
    #tweetFileDetails = open(path + 'tweetsDetails.txt', 'w', encoding='utf8')
    subDetails = oneSub[subs].split('|')
    subradius = str(subDetails[0])
    sublat = str(subDetails[1])
    sublon = str(subDetails[2])
    geocode = sublat + ',' + sublon + ',' + subradius + 'km' #geocode format: '-37.800,144.960,70km'

    for elem in setOfKeywords:
      results = api.search(q=elem, lang=language, count=count, geocode=geocode,tweet_mode='extended') #Melbourne
      for tweet in results["statuses"]:
              print(json.dumps(tweet))
     

