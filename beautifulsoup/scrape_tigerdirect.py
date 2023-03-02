from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


### Web Scraping
### Get the list price and current price of a product on tigerdirect

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url= "https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390"
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.text, 'lxml')
        all_price = soup.find('div', class_ = 'pdp-price')
        list_price = all_price.find('p', class_ = 'list-price')
        num1 = list_price.find('span', class_ = 'sr-only').text

        final_price = all_price.find('p', class_ = 'final-price')
        num2 = final_price.find('span', class_ = 'sr-only').text
        
        # remove unnecessary characters
        char_remove = ['\r', '\n', ' ', '$', ',', 'cents']
        for char in char_remove:
            num1 = num1.replace(char, '')
            num2 = num2.replace(char, '')

        # change the format to '1234.56'
        listprice = num1.replace('and', '.')
        print('list price:', listprice)
        finalprice = num2.replace('and', '.')
        print('current price:', finalprice)
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
    main()

