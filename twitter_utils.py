"""
This module provides utility functions for interacting with the Twitter API within the World Athletics Records project.
It includes functions for authenticating with the Twitter API using Tweepy and for posting tweets, optionally with images.
These functions facilitate the automated sharing of updates and insights derived from the analysis of athletics records data on Twitter.

Functions:
- authenticate_twitter(): Authenticates a user with the Twitter API using Tweepy and returns a client for Twitter API v2 and an API object for Twitter API v1.1.
- post_tweet(client, api, message, image_path=None): Posts a tweet with an optional image using the authenticated Twitter API client and API objects.

Author: LE GOURRIEREC Titouan
"""

############################################################################################################

import logging
import os

import tweepy

logging.basicConfig(filename='log/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

############################################################################################################

def authenticate_twitter() -> tuple[tweepy.Client, tweepy.API]:
    """
    Authenticates a user with the Twitter API using Tweepy.

    This function retrieves API keys and access tokens from environment variables and uses them to authenticate with the Twitter API.
    It returns a Tweepy Client object for the Twitter API v2 and a Tweepy API object for the Twitter API v1.1.

    Returns:
        tuple: A tuple containing:
            - client (tweepy.Client): A client object for Twitter API v2.
            - api (tweepy.API): An API object for Twitter API v1.1.
    """

    API_KEY = os.getenv("API_KEY")
    API_KEY_SECRET = os.getenv("API_KEY_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=API_KEY, consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
    )
    auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    return client, api

def post_tweet(client : tweepy.Client, api : tweepy.API, message : str, image_path : str = None) -> tweepy.Response:
    """
    Posts a tweet with an image using the Twitter API.

    This function takes a Tweepy Client object for Twitter API v2, a Tweepy API object for Twitter API v1.1, a message, and an image path.
    It uploads the image using the v1.1 API and posts a tweet with the provided message and the uploaded image's media ID using the v2 API.

    Parameters:
        - client (tweepy.Client): The client object for Twitter API v2.
        - api (tweepy.API): The API object for Twitter API v1.1.
        - message (str): The text of the tweet.
        - image_path (str): The file path of the image to be uploaded.
    """
    if image_path is not None:
        media = api.media_upload(image_path)
        response = client.create_tweet(text=message, media_ids=[media.media_id])
    else:
        response = client.create_tweet(text=message)

    logging.info(f"Tweet posted: https://twitter.com/user/status/{response.data['id']}")

    return response