import os
import json
import urllib

from requests_oauthlib import OAuth1Session
from dateutil import parser

CONSUMER_API_KEY = '<from_your_twitter_dev_account>'
CONSUMER_API_SECRET = '<from_your_twitter_dev_account>'

BASE_URL = 'https://api.twitter.com/1.1/search/tweets.json?q='

def search_twitter(term, count):
    """
    Search Twitter
    """

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

def authenticate():
    """
    Initial authentication. Only needs to be done once
    """

    client_key = CONSUMER_API_KEY
    client_secret = CONSUMER_API_SECRET

    # 1. Obtain a request token which will identify you (the client) in the next step.

    request_token_url = 'https://api.twitter.com/oauth/request_token'

    oauth = OAuth1Session(client_key, client_secret=client_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # 2. Obtain authorization from the user (resource owner) to access their protected resources 

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'

    authorization_url = oauth.authorization_url(base_authorization_url)
    print('Please go here and authorize,', authorization_url)
    verifier = input('Please input the verifier: ')

    # 3. Obtain an access token from the OAuth provider. 

    access_token_url = 'https://api.twitter.com/oauth/access_token'

    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)

    oauth_tokens = oauth.fetch_access_token(access_token_url)

    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    #print("oauth_token: {}".format(resource_owner_key))
    #print("oauth_token_secret: {}".format(resource_owner_secret))
    #print("client_key: {}".format(client_key))
    #print("client_secret: {}".format(client_secret))

    return (resource_owner_key, resource_owner_secret, client_key, client_secret)


"""
Test the search_twitter function
"""
if __name__ == "__main__":
    search_for = '#superbowl'
    count = 100

    results = search_twitter(search_for, count)
    print(results)