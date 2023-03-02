from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

### Web scraping
### a) Use the URL identified above and write code that loads the first page with 40 items per page of “B&N Top 100”.

headers = {'User-Agent':'Mozilla/5.0'}
url= "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
page = requests.get(url, headers = headers)
soup = BeautifulSoup(page.content, 'html5lib')

### b) Take your code in (a) and create a list of each book’s product page URL. This list should be of length 40.

all_url = soup.find_all('a', class_ = 'pTopXImageLink')

url_list = []
for url in all_url:
    time.sleep(1)
    url_list.append('https://www.barnesandnoble.com'+ url.get('href'))
    
# check the length of the list
print('The length of the list:', len(url_list))

# make sure the urls have the same order of the webpage
url_list[0:10]

### c) Write a loop that downloads each product page of the top 40 books in “B&N Top 100”. e., save each of these pages to your computer using a meaningful filename (e.g., "bn_top100_01.htm"). IMPORTANT: Each page request needs to be followed by at least a 5 second pause!  Remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

filename_list = []
i = 1
for i in range(1, 41):
    filename_list.append('bn_top100_' + str(i) + '.html')
filename_list[0:5]

def saveFile(url, filename):
    headers = {'user-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = headers, allow_redirects = True)
    
    with open(filename, 'w') as file:
        file.write(page.text)
        file.close

i = 0
for i in range(0, 40):
    saveFile(url_list[i], filename_list[i])
    time.sleep(1)

### d) Write a separate piece of code that loops through the pages you downloaded in (c), opens and parses them into a Python or Java xxxxsoup-object. Next, access the “Overview” section of the page and print the first 100 characters of the overview text to screen.

def readFile(filename):
    print('Book', str(i + 1), 'Overview: ')
    with open(filename, 'r', encoding = 'UTF-8') as file:
        text = file.read()
    soup = BeautifulSoup(text, 'lxml')
    overview = soup.find('div', class_ = 'content overview-expandable-section')
    all_content = overview.find_all('div')
    character = ''
    for content in all_content:
        character = character + content.text.replace("\n", "")
    print(character[:100])

i = 0
for i in range(0, 40):
    readFile(filename_list[i])

