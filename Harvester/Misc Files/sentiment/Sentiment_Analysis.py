#Testing the output for sentiment analysis

# import colorama
from textblob import TextBlob
import json
import re
import operator
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os, sys, codecs
from nltk import bigrams



#reading text file format
with open("test_SA.txt") as f:
    for line in f:
        line_sa = TextBlob(line)
        # print(line_sa.sentiment)
        print(line_sa.sentiment_assessments)


    for line in f:
        blob = TextBlob(line)
        if blob.sentiment.polarity <0:
            sentiment = "negative"
        elif blob.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

