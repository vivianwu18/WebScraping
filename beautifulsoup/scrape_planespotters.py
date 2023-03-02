from bs4 import BeautifulSoup
import requests


### Web scraping
### 1. Access https://www.planespotters.net/user/login Links to an external site.using a standard GET request. Read and store the cookies received in the response.  In addition, parse the response and read (and store to a string variable) the value of the hidden input field that will (most likely) be required in the login process.

url1 = 'https://www.planespotters.net/user/login'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}
page1 = requests.get(url1, headers = headers)
cookies = page1.cookies.get_dict()
print(cookies)

### read and store the hidden field

soup = BeautifulSoup(page1.content, 'html.parser')
loginform = soup.find('div', class_ = 'planespotters-form')
all_info = soup.find_all('input', attrs = {'type':'hidden'})
payload = {}
for info in all_info:
    payload.update({info.get('id'):info.get('value')})
print(payload)


### 2. Make a post request using the cookies from (1) as well as all required name-value-pairs (including your username and passwords).

payload.update({'username':'mengweiwu', 'password':'12345678'})
print(payload)

session = requests.Session()
res = session.post(url1, data = payload, headers = headers, cookies = cookies, timeout = 15)

if res.status_code == 200:
    print('Login successfully!')
else:
    print('Please try again!')


### 3. Get the cookies from the response of the post request and add them to your cookies from (1).

print(session.cookies.get_dict())

### update cookies
cookies.update(session.cookies.get_dict())
print(cookies)


### 4. Verifies that you are logged in by accessing the profile page https://www.planespotters.net/member/profile Links to an external site.with the saved cookies.

url2 = 'https://www.planespotters.net/member/profile'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}
page2 = session.get(url2, cookies = cookies, headers = headers)


### 5. Then, print out the following at the end:
###     A. The entire Jsoup/BeautifulSoup document of your profile page.
###     B. All (combined) cookies from (3).
###     C. A boolean value to show your username is contained in the document in part (5)(a).

### print entire profile page
soup2 = BeautifulSoup(page2.content, 'html.parser')
print(soup2.prettify())

### print all cookies
print(cookies)

### check whether the username is contained in the document
if 'mengweiwu' in soup2.text:
    print('Username appears on the page.')
else:
    print('Username does not appear on the page.')

