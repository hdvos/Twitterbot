#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys
import n_gram_sentence_generator as ngsg
from support_funcs import *


CONSUMER_KEY = 'eqeA2ZbySp6C4VwsCzMuwwJvl'
CONSUMER_SECRET = 'CyZ5BIsVCRhsk8FIWuM7iPOzftI74a1OiUp4OQMynp4gW5cBYW'
TOKEN = '1026921204-95VeSjxtkDvgjBMUjE5lcnjnBNkIzijczh4QSoa'
SECRET_TOKEN = 'm3fpO44bVKjPrBhtdppdXH8AjgQvQQtsVRTbU12Azepv4'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN, SECRET_TOKEN)
api = tweepy.API(auth)
MAXTWEETS = 30
hashtags = "#VVD #sentencegenerator"

starttweet = "Ik maakte tweet-generator die tweets genereerd op basis van woordcombinaties in verkiezingsprogrammas. Vandaag op basis van #VVD"
print (len(starttweet))


text = ngsg.read_text('input_texten/vvd.txt')
preprocessed = ngsg.pre_process(text)
ngram_dict = ngsg.build_dictionary(preprocessed, )

if not is_reboot():
    if len(starttweet) <= 140:
        print("tweeting starttweet:\n{}".format(starttweet))
        api.update_status(starttweet)
        write_checkfile()
    else:
        print("starttweet is too long. Write a starttweet that is shorter than 14 chars")
        raise SystemExit
else:
    MAXTWEETS = MAXTWEETS - get_counter()
    print("Program has already been running today.\nContinue were left...")


for i in range(MAXTWEETS):
    print ("=========================================================")
    tweet = ngsg.generate_tweet(ngram_dict, hashtags)

    if not tweet is None:
        print("tweeting: {}".format(tweet))
        api.update_status(tweet)

    else:
        print ("could not generate tweet, Terminate program")
        break

    take_a_break(15)


