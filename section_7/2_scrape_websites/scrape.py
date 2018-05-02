# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def html_to_dom(url):
    # fetch the web page using requests
    response = requests.get(url)

    # represent page as BeautifoulSoup "soup" DOM object
    return BeautifulSoup(response.content, 'html.parser')


def scrape_example_dotcom():
    # get DOM
    dom = html_to_dom('http://example.com')

    # get the paragraphs
    paragraphs = dom.find_all('p')
    print('\n\nFound: {} paragraphs'.format(len(paragraphs)))
    for index, p in enumerate(paragraphs):
        print('Paragraph n.{} text: {}'.format(index + 1, p.text))

    # we know some paragraphs contain "a" tags, that have links to other pages
    for p in paragraphs:
        # extract children tags "a" of the paragraph
        for child in p.find_all('a'):
            # if the child contains the href property, print it
            link_url = child.get('href')
            if link_url is not None:
                print('\nFound: inner link - {}'.format(link_url))


def scrape_coinmarketcap_dotcom_litecoin_price():
    # get DOM
    dom = html_to_dom('https://coinmarketcap.com')

    # examining the page, we suppose to find this tabular HTML structure:
    # <table>
    #   <tr id="id-litecoin">
    #     <td>
    #       <a href="..." class="price" data-usd="..." data-btc="..." >XXX</a>
    #     </td>
    #   </tr>
    # </table>
    #
    # So we need to find the "a" element having class "price" among the children
    # items of "tr" element having id "id-litecoin"

    # first, extract the table row
    trs = dom.find_all('tr', id='id-litecoin')
    assert len(trs) == 1  # check that only one is found
    tr = trs[0]

    # second, extract its child tag that links to Litecoin price
    price_links = tr.find_all('a', class_='price')
    assert len(price_links) == 1
    return price_links[0].text


if __name__ == '__main__':


    # --- SCRAPE PARAGRAPHS OF EXAMPLE.COM WEBPAGE ---
    print('*** SCRAPING WEB PAGE http://example.com ***')
    scrape_example_dotcom()

    # --- SCRAPE CURRENT LITECOIN PRICE FROM COINMARKETCAP.COM WEBPAGE ---
    print('*** SCRAPING WEB PAGE http://coinmarketcap.com ***')
    litecoin_price = scrape_coinmarketcap_dotcom_litecoin_price()
    print('Current Litecoin price is: {}'.format(litecoin_price))
