#!/usr/bin/env python

import requests
import re
from bs4 import BeautifulSoup
import csv
import calendar
import time

# user agent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

# pull html and get link names, title of page, and link locations
def getLinks(URL):
    response = requests.get(URL, headers=headers, timeout=5)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')

    #   get main content
    mainContent = soup.find('main')

    #   get the page title
    pageTitle = soup.find('title').text

    #   array to store all the links on the page
    links = []

    # loop through each <a> tag in main content
    for link in mainContent.findAll('a', attrs={'href': re.compile("^https?://")}):  # scans through main content only

        # create an array of page title, link text, and link 
        linkArray = [pageTitle, link.text, link.get('href')]

        # push to the links array
        links.append(linkArray)

    # return the list of found links
    return links


# Main function
def main():
    # open and apply list of all URLs
    with open('masterURLs.txt', 'r') as f:
        # read all of the lines
        masterURLs = f.readlines()

        # replace the end lines
        masterURLs = list(map(lambda x: x.replace("\n", ""), masterURLs))

        # open a new scraped csv
        with open('scraped-' + str(calendar.timegm(time.gmtime())) + '.csv', 'a+', newline='') as csv_file:
            # create the csv writer
            csv_writer = csv.writer(csv_file)

            # add the headings for the csv
            csv_writer.writerow(['Page Title', 'Link Name', 'Link Location'])

            # foreach url in the mastersURLs
            for url in masterURLs:
                # get links for the url
                links = getLinks(url)

                # write the found links
                csv_writer.writerows(links)


# if the script is run directly then run the main function
if __name__ == '__main__':
    main()