# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import feedparser


def filter_if_title_contains(feed, query, case_insensitive=True):
    if case_insensitive:
        check = lambda entry: query.lower() in entry.title.lower()
    else:
        check = lambda entry: query in entry.title
    return filter(check, feed.entries)


if __name__ == '__main__':
    rss_url = 'https://www.reddit.com/r/Python.rss'

    # parse the target RSS feed
    print('*** Parsing: {} ...\n'.format(rss_url))
    parsed_feed = feedparser.parse(rss_url)

    # Get a few details
    print('Title: {}'.format(parsed_feed.feed.title))
    print('Subtitle: {}'.format(parsed_feed.feed.subtitle))
    print('Last updated on: {}\n'.format(parsed_feed.feed.updated))
    print('Number of entries: {}\n'.format(len(parsed_feed.entries)))

    # Show all entries
    print('*** Showing all entries ...\n')
    for index, entry in enumerate(parsed_feed.entries):
         print('{}. {} [{}]'.format(index + 1, entry.title, entry.link))

    # Only show entries containing specific text
    query = 'django'
    print('\n*** Showing only entities with title containing: "{}" ...'.format(query))
    for entry in filter_if_title_contains(parsed_feed, query):
        print('{} [{}]'.format(entry.title, entry.link))
