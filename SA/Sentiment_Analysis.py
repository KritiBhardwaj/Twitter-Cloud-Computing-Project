#Testing the output for sentiment analysis


#import TextBLob
from textblob import TextBlob
import nltk
import io

#reading text file format
with open("test_SA.txt") as f:
    for line in f:
        line_sa = TextBlob(line)
        print(line_sa.sentiment)


