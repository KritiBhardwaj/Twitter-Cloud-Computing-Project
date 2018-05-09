#This is a live twitter streamer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Key Removed

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
