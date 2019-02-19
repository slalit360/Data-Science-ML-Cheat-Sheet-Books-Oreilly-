#!/usr/bin/env python

import requests
import tweepy
import re
import os

# create a file twitter_keys.py and add the tokens/keys below as variables
# in the file
from twitter_keys import consumer_key, consumer_secret

# Create the OAuthHandler
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
# Construct the API instance
api = tweepy.API(auth)

params = {
    'q': 'machinelearningflashcards.com-filter:retweets',
    'from': 'chrisalbon',
    'since': '2017-04-01',
}

ml_flashcards_json = api.search(**params)

media_urls = []
titles = []
error_counter = 0
total_tweets = len(ml_flashcards_json)
successful_tweets = total_tweets - error_counter

for i in range(total_tweets):
    txt = ml_flashcards_json[i]
    json = txt._json
    title = re.sub("#\S*", "", str(json['text']))  # removes hashtag
    title = re.sub("https\S*", "", title)  # removes url
    title = str(title.strip())
    try:  # KeyError is raised when there is no image within the tweet
        media_url = json['entities']['media'][0]['media_url']
        media_urls.append(media_url)
        titles.append(title)
    except KeyError:
        error_counter += 1

if error_counter == 0:
    print("{} tweets were processed successfully".format(successful_tweets))
elif error_counter == 1:
    print("{} tweets were processed successfully".format(successful_tweets))
    print("{} tweet was not processed due to a KeyError".format(error_counter))
else:
    print("{} tweets were processed successfully".format(successful_tweets))
    print("{} tweets were not processed due to a KeyError".format(error_counter))

# change directory to flashcards folder
current_dirctory = os.getcwd()
os.chdir(current_dirctory + "/flashcards")

# write images to the flashcards directory
for i in zip(media_urls, titles):
    img = requests.get(i[0])
    f = open(str(i[1]) + ".jpg", mode='wb')
    f.write(img.content)
    f.close()
