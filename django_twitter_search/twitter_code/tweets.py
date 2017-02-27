import os
from requests_oauthlib import OAuth1Session
import json
import urllib
from datetime import datetime
from dateutil import parser

BASE_URL = 'https://api.twitter.com/1.1/search/tweets.json?q='

def search_twitter(term, count):

    # encode the search term
    encoded_string = urllib.parse.quote_plus(term)

    # build url
    url = BASE_URL + encoded_string + "&count={}".format(count)

    # get authorisation details from environment variables
    resource_owner_key = os.environ['RESOURCE_OWNER_KEY']
    resource_owner_secret = os.environ['RESOURCE_OWNER_SECRET']
    client_key = os.environ['CLIENT_KEY']
    client_secret = os.environ['CLIENT_SECRET']

    # get authorised session
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)

    # send request to Twitter
    r = oauth.get(url)
    tweets = r.json()["statuses"]
    
    # parse results and build list of dictionaries
    data = []
    for tweet in tweets:
        elem = {}
        elem["name"] = tweet["user"]["name"]
        elem["screen_name"] = tweet["user"]["screen_name"]
        elem["profile_image_url"] = tweet["user"]["profile_image_url"]
        elem["text"] = tweet["text"]
        elem["retweet_count"] = tweet["retweet_count"]
        elem["favorite_count"] = tweet["favorite_count"]
        elem["created_at"] = parser.parse(tweet['created_at'])
        data.append(elem)

    return data


"""
Test the search_twitter function
"""
if __name__ == "__main__":
    search_for = '#superbowl'
    count = 100

    results = search_twitter(search_for, count)
    print(results)