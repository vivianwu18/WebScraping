from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
import numpy as np

### Web scraping
### a) use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".

headers = {'User-Agent':'Mozilla/5.0'}
url = 'https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&LH_Sold=1&_pgn=1'

def saveFile(url, filename):
    headers = {'user-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers = headers, allow_redirects = True)
    
    with open(filename, 'w') as file:
        file.write(page.text)
        file.close

saveFile(url, 'amazon_gift_card_01.htm')


### b) take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

for i in range(1, 11):
    print(f'amazon_gift_card_{i:02d}.htm saved.')
    saveFile(f'https://www.ebay.com/sch/i.html?_nkw=amazon+gift+card&LH_Sold=1&_pgn={i}', f'amazon_gift_card_{i:02d}.htm')
    time.sleep(1)


### c) write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.
### d) using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.

def ReadandPrintContent(filename):
    with open(filename, 'r', encoding = 'UTF-8') as file:
        text = file.read()
    soup = BeautifulSoup(text, 'lxml')
    result = soup.find('div', class_ = 'srp-river-results')
    # title
    all_title = result.find_all('div', class_ = 's-item__title')
    title_list = []
    for title in all_title:
        title_list.append(title.span.text.replace('New Listing', ''))
    
    # item price
    all_price = result.find_all('span', class_ = 's-item__price')
    price_list = []
    for price in all_price:
        price_list.append(price.text)
    
    # shipping price
    shipping_list = []
    all_shipping = result.find_all('li', attrs = {'class':['s-item s-item__pl-on-bottom', 's-item s-item__pl-on-bottom s-item__before-answer']})
    for shipping in all_shipping:
        if shipping.find('span', class_ = 's-item__shipping s-item__logisticsCost') is None:
            shipping_list.append('Free shipping')
        else:
            shipping_list.append(shipping.find('span', class_ = 's-item__shipping s-item__logisticsCost').text)
    
    df = pd.DataFrame()
    df['Title'] = title_list
    df['Price'] = price_list
    df['Shipping price'] = shipping_list
    return df

all_df = pd.DataFrame()
for i in range(1, 11):
    all_df = pd.concat([all_df, ReadandPrintContent(f'amazon_gift_card_{i:02d}.htm')])
all_df


### e) using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.

all_df.head(10)

### extract the numeric value

all_df['Actual value'] = all_df['Title'].str.extract('\$(\d+)').astype(float)
all_df['Actual price'] = all_df['Price'].str.extract('(\d+\.\d+)').astype(float)
all_df['Actual shipping'] = np.where(all_df['Shipping price'].str == 'Free shipping', '0', all_df['Shipping price'].str.extract('(\d+\.\d+)')).astype(float)
all_df = all_df.fillna(0)
all_df['Actual price plus shipping'] = all_df['Actual price'] + all_df['Actual shipping']

### drop rows which can not grab the face value

all_df = all_df[all_df['Actual value'] != 0]

### whether a gift card sells above face value
all_df['Whether above face value'] = np.where(all_df['Actual value'] < all_df['Actual price plus shipping'], True, False)


### f) What fraction of Amazon gift cards sells above face value? Why do you think this is the case?

round(all_df.loc[all_df['Whether above face value'] == True].shape[0] / all_df.shape[0], 4)

