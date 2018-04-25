#Random twitter cursor code that works like streaming
import tweepy

Consumer_Key_Umair= "HnXTz4v9QCtjWvn7Tpb55SmOz"
Consumer_Secret_Umair= "xCd7VIrsQPrCCg1wsPrxNEvSfmUCSuI7HfTdwtthwcBmo1d4W2"
Access_Token_Umair= "62274863-7eVe1DtSb20jVf7bNLjO5RwlJRqRK0cjAmVRlVfgE"
Access_Token_Secret_Umair = "FbOD05N6TK6wm6x4yGYXs923fX9xnzHUWoiFpkQ4bvNXc"

auth = tweepy.OAuthHandler(Consumer_Key_Umair, Consumer_Secret_Umair)
auth.set_access_token(Access_Token_Umair, Access_Token_Secret_Umair)

api = tweepy.API(auth)

query = 'crime'
max_tweets = 20
for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
    print(status.text)
    print(status.user.location)
    print("")

