from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key = "E50fbKWMtI5X914kL4kgfURvR"
consumer_secret = "CLWbyVUb6b8fIMlodcpgH2jsl7Xal2qVOwGRjtYTYyVRKQTN90"
access_token = "1301016800-qi6ql98SLPDHeNYPlw6jvhge0QVElGjoyffBeAH"
access_token_secret = "C6tQsacmOfcTPB8uOIor24u1ChUwuPyOPohhYkUzaSRDu"

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
    def on_status(self, status): #More elaborate tweet information
        for elem in setOfKeywords:
            if elem.lower() in status.text.lower():
                print(status)
                return True

    #Less elaborate tweet information
    # def on_data(self, data):
    #     for elem in setOfKeywords:
    #         if elem.lower() in data.lower():
    #             print(data)
    #             return True
    def on_error(self, status):
        print(status)
        return False

#Location is updated only from mobile (GPS) devices. Not from a computer
if __name__ == '__main__':
    output = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, output)

    #for tracking using tweet content only

    #stream.filter(track=['UJamil'])
    #stream.filter(track=['divorce','marriage issues','money','relationships'],locations="Melbourne Australia")


    #Location based tracking - Note that both location and content tracking cannot work in the same line
    #Therefore, if using location based tracking, content check should be done after this.

    stream.filter(locations=[144.01, -38.57, 151.61, -33.26])  # Gridbox for whole sydney to melbourne
    #stream.filter(locations=[144.5937,-38.4339,145.5125,-37.5113]) #Just Melbourne Australia gridbox
    #stream.filter(locations=[150.520929,-34.118347,151.343021,-33.578141])  # Just Sydney Australia gridbox
