import requests
import re
from bs4 import BeautifulSoup
import csv

#load the page
URL = ''
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
page = requests.get(URL, headers=headers, timeout=20).text
soup = BeautifulSoup(page,'lxml')
pattern = '/href="(.*)/'

# create the csv file & write headlines
csv_file = open('scraped.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Page Title','Link Name', 'Link Location'])

# find the main content section and get page title
mainContent = soup.find('main')
pageTitle = mainContent.h1.text

#scan through site
#for link in soup.findAll('a', attrs={'href': re.compile("^https?://")}):   # scans through entire site
for link in mainContent.findAll('a',attrs={'href': re.compile("^https?://")}): # scans through main content only
    linkName = link.text
    linkLocation = link.href
    csv_writer.writerow([pageTitle,linkName, link])

#close csv file
csv_file.close()