import mysql.connector
import warnings
import requests
import json
import codecs
from bs4 import BeautifulSoup
import pprint
import time

### Web Scraping & Database building
### 1. Go to https://api.github.com Links to an external site.and familiarize yourself with the API.

### 2. Go to https://api.github.com/repos/apache/hadoop/contributors Links to an external site.. This is the Apache Hadoop Github Repo's contributors’ endpoint. Extract the JSON corresponding to the first 100 contributors from this API. (Hint: the API request is a GET request and the variable name that handles the items per page is "per_page").  Write Java or Python code that does all this.
# fetch html and convert to json

username = 'vivianwu18'
token = 'personal_github_token'
per_page = str(100)
url = "https://api.github.com/repos/apache/hadoop/contributors" + "?per_page=" + per_page
page = requests.get(url, auth = (username, token))
doc = BeautifulSoup(page.content, 'html.parser')
json_dict = json.loads(str(doc))

# check how many contributors we fetch

len(json_dict)

# get users' url to access to the user information

url_list = list()
for i in range(len(json_dict)):
    url_list.append(json_dict[i]['url'])


### 3. For each of the 100 contributors extracted in (2), write code that accesses their user information and extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", "followers", "following", "created_at" (and print those to screen)
# extract the information we need from 100 contributers
    
all_user = []
key_list = ["login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", 
       "followers", "following", "created_at"]
for i in range(len(url_list)):
    url = url_list[i]
    page = requests.get(url, auth = (username, token))
    doc = BeautifulSoup(page.content, 'html.parser')
    json_dict = json.loads(str(doc))
    user_info = {}
    for key in key_list:
        user_info[key] = json_dict[key]
    all_user.append(user_info)
    
pprint.pprint(all_user)


### 4. Wrte code that creates an SQL database + table, and stores all the information obtained in (3) in it.  Please be cautious of the data type you choose for each column and briefly justify your decisions.  What do you choose as Primary Key and why?

def create_sql_table(SQL_TABLE, SQL_TABLE_DEF):
    try:
        
        #connect to server
        conn = mysql.connector.connect(host = 'localhost',
                                       user = 'root',
                                       password = 'f5cef6a0ef9219df9f6fa3869466a1a7')
        cursor = conn.cursor()

        query = "CREATE DATABASE IF NOT EXISTS " + SQL_DB
        print(query)
        cursor.execute(query);
        
        query = "CREATE TABLE IF NOT EXISTS " + SQL_DB + "." + SQL_TABLE + " " + SQL_TABLE_DEF + ";";
        print(query)
        cursor.execute(query);
        cursor.close()
        conn.close()
        return

    except IOError as e:
        print(e)

# create SQL database
        
SQL_DB = "assignment5"
SQL_TABLE_USER = "user"
SQL_TABLE_USER_DEF = "(" +
                     "login VARCHAR(50) NOT NULL" +
                     ",id VARCHAR(50)" +
                     ",location VARCHAR(250)" +
                     ",email VARCHAR(250)" +
                     ",hireable VARCHAR(100)" +
                     ",bio VARCHAR(250)" +
                     ",twitter_username VARCHAR(50)" +
                     ",public_repos INT" +
                     ",public_gists INT" +
                     ",followers INT" +
                     ",following INT" +
                     ",created_at VARCHAR(50)" +
                     ",PRIMARY KEY (id)" +
                     ")"

create_sql_table(SQL_TABLE_USER, SQL_TABLE_USER_DEF)

# connect to server

try:
    conn = mysql.connector.connect(host = 'localhost',
                                   user = 'root',
                                   password = 'f5cef6a0ef9219df9f6fa3869466a1a7',
                                   database = 'assignment5')
    cursor = conn.cursor()
    
    stmt = "INSERT INTO " + SQL_TABLE_USER + " (login, id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for el in all_user:
        login = el['login']
        id = el['id']
        location = el['location']
        email = el['email']
        hireable = el['hireable']
        bio = el['bio']
        twitter_username = el['twitter_username']
        public_repos = el['public_repos'] 
        public_gists = el['public_gists']
        followers = el['followers']
        following = el['following']
        created_at = el['created_at']
        cursor.execute(stmt, (login, id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at))

    conn.commit()
    cursor.close()
    conn.close()

except IOError as e:
    print(e)


### 5. Optimize your code in (4) to allow for quick look-ups of "login", "location", and "hireable". 
# create new table with index

SQL_DB = "assignment5"
SQL_TABLE_USER = "user_index"
SQL_TABLE_USER_DEF = "(" +
                     "login VARCHAR(50) NOT NULL" +
                     ",id VARCHAR(50)" +
                     ",location VARCHAR(250)" +
                     ",email VARCHAR(250)" +
                     ",hireable VARCHAR(100)" +
                     ",bio VARCHAR(250)" +
                     ",twitter_username VARCHAR(50)" +
                     ",public_repos INT" +
                     ",public_gists INT" +
                     ",followers INT" +
                     ",following INT" +
                     ",created_at VARCHAR(50)" +
                     ",INDEX(login, location, hireable)" +
                     ",PRIMARY KEY (id)" +
                     ")"

create_sql_table(SQL_TABLE_USER, SQL_TABLE_USER_DEF)

# connect to server

try:
    conn = mysql.connector.connect(host = 'localhost',
                                   user = 'root',
                                   password = 'f5cef6a0ef9219df9f6fa3869466a1a7',
                                   database = 'assignment5')
    cursor = conn.cursor()
    
    stmt = "INSERT INTO " + SQL_TABLE_USER + " (login, id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for el in all_user:
        login = el['login']
        id = el['id']
        location = el['location']
        email = el['email']
        hireable = el['hireable']
        bio = el['bio']
        twitter_username = el['twitter_username']
        public_repos = el['public_repos'] 
        public_gists = el['public_gists']
        followers = el['followers']
        following = el['following']
        created_at = el['created_at']
        cursor.execute(stmt, (login, id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at))

    conn.commit()
    cursor.close()
    conn.close()

except IOError as e:
    print(e)


### 6. Compare the difference
# fetch data without index
    
conn = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = 'f5cef6a0ef9219df9f6fa3869466a1a7',
                               database = 'assignment5')

start_time1 = time.time()

cursor = conn.cursor()

cursor.execute("SELECT login, location, hireable FROM user WHERE location = 'Tokyo'")

info = cursor.fetchall()

end_time1 = time.time()

print(f'The time of fatching the specific columns without indexing: {end_time1 - start_time1}')

# fetch data with index
conn = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = 'f5cef6a0ef9219df9f6fa3869466a1a7',
                               database = 'assignment5')

start_time2 = time.time()

cursor = conn.cursor()

cursor.execute("SELECT login, location, hireable FROM user WHERE location = 'Tokyo'")

info = cursor.fetchall()

end_time2 = time.time()

print(f'The time of fatching the specific columns with indexing: {end_time2 - start_time2}')

# time difference
print(f'The difference between the time of these two methods is {(end_time1 - start_time1) - (end_time2 - start_time2)}')
