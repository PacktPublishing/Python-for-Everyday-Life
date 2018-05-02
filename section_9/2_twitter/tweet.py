# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from twython import Twython, TwythonError
from section_9.accounts import TWITTER


def tweet(twitter, message):
    print('Tweeting: "{}"'.format(message))
    try:
        twitter.update_status(status=message)
        print('Done')
    except TwythonError as e:
        print('Impossible to tweet, reason: {}'.format(e))


def search_tweets(twitter, query, how_many=10, kind='recent'):
    try:
        result_set = twitter.search(q=query, count=how_many, result_type=kind)
        return result_set['statuses']
    except TwythonError as e:
        print('Something bad happened, reason: {}'.format(e))
        return []


def retweet(twitter, tweet_id):
    print('Retweeting tweet with ID={}'.format(tweet_id))
    try:
        twitter.retweet(id=tweet_id)
        print('Done')
    except TwythonError as e:
        print('Impossible to retweet, reason: {}'.format(e))


if __name__ == '__main__':

    # Retrieve tokens
    CONSUMER_KEY = TWITTER.get('consumer_key', None)
    CONSUMER_KEY_SECRET =  TWITTER.get('consumer_key_secret', None)
    ACCESS_TOKEN = TWITTER.get('access_token', None)
    ACCESS_TOKEN_SECRET = TWITTER.get('access_token_secret', None)

    # Instantiate the Twitter API local proxy using the tokens
    twitter = Twython(CONSUMER_KEY, CONSUMER_KEY_SECRET,
                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Tweet!
    tweet(twitter, '#amor vincit omnia')

    # Now search for similar tweets
    tweets = search_tweets(twitter, 'amor vincit', how_many=20, kind='recent')
    for t in tweets:
        print('\n*** Tweet {} by {} [{}]: {}'.format(t['id_str'], t['user']['name'],
                                                   t['created_at'], t['text']))
