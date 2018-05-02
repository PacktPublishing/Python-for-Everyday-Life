# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from selenium import webdriver


def setup_driver():
    # create webdriver for Firefox
    driver = webdriver.Firefox()

    # set the default wait time for page elements to load up
    driver.implicitly_wait(5)

    # maximize browser window
    driver.maximize_window()

    return driver


def google_search(driver, query, quit_when_finished=True):
    print('*** SELENIUM WEBDRIVER ***')
    try:
        # load Google search page
        driver.get("http://www.google.com")

        # get the search text box
        search_textbox = driver.find_element_by_name("q")

        # clear it from previous input
        search_textbox.clear()

        # enter the search query
        search_textbox.send_keys(query)

        # submit query to Google
        print('\nQuerying on Google: "{}"'.format(query))
        search_textbox.submit()

        # ...then get them
        result_divs = driver.find_elements_by_class_name("g")
        print ('\nFound: {} results on first page\n'.format(len(result_divs)))

        # for each result extract the title and link
        # these are given by nested "h3" and "a" children tags
        for div in result_divs:
            # get title from "h3" tag
            h3_tags = div.find_elements_by_tag_name('h3')
            if len(h3_tags) == 1:
                h3 = h3_tags[0]
                title = h3.text

                # get link from "a" tag
                a_tags = h3.find_elements_by_tag_name('a')
                if len(a_tags) == 1:
                    link = a_tags[0].get_attribute('href')
                else:
                    link = 'Missing link'

                # print all out
                print('Found search result: "{}" ({})'.format(title, link))
    finally:
        if quit_when_finished:
            driver.quit()



if __name__ == "__main__":
    firefox = setup_driver()
    google_search(firefox, "python language", quit_when_finished=True)