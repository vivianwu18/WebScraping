### Automatically Login

### a) Following the steps we discussed in class and write code that automatically logs into the website fctables.com Links to an external site..
### b) Verify that you have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/ Links to an external site..  Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.

payload = {'login_username':'username',
           'login_password':'password',
           'user_remeber':'1',
           'login_action':'1'}

post_url = 'https://www.fctables.com/user/login/'

session = requests.session()
res = session.post(post_url, data = payload, timeout = 15)


cookies = session.cookies.get_dict()

get_url = 'https://www.fctables.com/tipster/my_bets/'
page = session.post(get_url, cookies = cookies)
soup = BeautifulSoup(page.content, 'html.parser')
        
if 'Wolfsburg' in soup.text:
    print('Wolfsburg appears on the page.')
else:
    print('Wolfsburg does not appear on the page.')
