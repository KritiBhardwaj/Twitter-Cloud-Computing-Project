#Random twitter cursor code that works like streaming
import tweepy
#Key Removed
auth = tweepy.OAuthHandler(Consumer_Key_Umair, Consumer_Secret_Umair)
auth.set_access_token(Access_Token_Umair, Access_Token_Secret_Umair)

api = tweepy.API(auth)

query = 'crime'
max_tweets = 20
for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
    print(status.text)
    print(status.user.location)
    print("")

