#This is a live twitter streamer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

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

class StdOutListener(StreamListener):
    # def on_status(self, status): #More elaborate tweet information
    #     for elem in setOfKeywords:
    #         if elem.lower() in status.text.lower():
    #             print(status)
    #             print(status.text)
    #             print(status.user.location)
    #             return True

    #Less elaborate tweet information
    def on_data(self, data):
        for elem in setOfKeywords:
            if elem.lower() in data.lower():
                print(data)
                return True
    def on_error(self, status):
        print(status)
        return False

#Location is acquired only from tweets using a mobile (GPS) devices. Not from a computer
if __name__ == '__main__':
    output = StdOutListener()
    auth = OAuthHandler(Consumer_Key_Umair, Consumer_Secret_Umair)
    auth.set_access_token(Access_Token_Umair, Access_Token_Secret_Umair)
    stream = Stream(auth, output)

    #stream.filter(track=['UJamil']) #for tracking using tweet content only

    '''
    Location based tracking - Note that both location and content tracking cannot work in the same line
    Therefore, if using location based tracking, content check should be done after this.
    '''

    stream.filter(locations=[144.5937, -38.4339, 145.5125, -37.5113])  # Just Melbourne Australia gridbox
    #stream.filter(locations=[144.01, -38.57, 151.61, -33.26])  # Gridbox for whole sydney to melbourne
    #stream.filter(locations=[150.520929,-34.118347,151.343021,-33.578141])  # Just Sydney Australia gridbox
