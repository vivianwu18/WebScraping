from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


## Web Scraping
### Load the top two strories and the first three sentences in the top stor

def main():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url= "https://www.usnews.com/"
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.text, 'lxml')
        content_all = soup.find_all('h3', class_ = 'Heading-sc-1w5xk2o-0 ContentBox__StoryHeading-sc-1egb8dt-3 MRvpF fqJuKa story-headline')
        for content in content_all[1:3]:
            print(content.text)
            print(content.a.get('href'))
        
        new_url = content_all[2].a.get('href')
        new_page = requests.get(new_url, headers = headers)
        new_soup = BeautifulSoup(new_page.text, 'lxml')
        sentences_all = new_soup.find_all('div', class_ = 'Raw-slyvem-0 bCYKCn')
        
        all_text = ""
        for sentence in sentences_all:
            all_text = all_text + sentence.p.get_text() + ' '
        
        final_text = " ".join(re.split(r'(?<=[.:;?])\s', all_text)[:4])
        print(final_text)
     
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
    main()

