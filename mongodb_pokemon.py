import pymongo
from pymongo import MongoClient
import pprint

### MongoDB
### check the connection

username = 'username'
password = 'password'
database = 'samples_pokemon'

connection_string = f'mongodb+srv://{username}:{password}@cluster0.kfwumjq.mongodb.net/{database}?appName=mongosh+1.7.1'
client = MongoClient(connection_string)
database1 = client['samples_pokemon']
collection1 = database1['samples_pokemon']

cursor1 = collection1.find({})
for doc in cursor1:
    pprint.pprint(doc)

### (Let’s get things started …) Please write code (Python or Java) to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with candy_count >= month + day of your birthday  (e.g., my birthday is 2/12 and I query candy_count >= 14 as 2+12 = 14).  (25% of points)   (Note:  the MongoDB operator for “>=” is “$gte”)

column11 = {'name': 1, '_id': 1}
query11 = {'candy_count':{'$gte': 19}}

cursor11 = collection1.find(query11, column11)
for doc in cursor11:
    pprint.pprint(doc)


### (Let’s sprinkle in a little or …) Please write code (Python or Java) to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with num = month or num = day of your birthday  (e.g., my birthday is 2/12 and I have to query num = 2 or num = 12).  (25% of points)

column12 = {'name': 1, '_id': 1}
query12 = {'num':{'$in':['001', '018']}}

cursor12 = collection1.find(query12, column12)
for doc in cursor12:
    pprint.pprint(doc)


### RegEx & MongoDB
### check the connection
    
username = 'username'
password = 'password'
database = 'crunchbase'

connection_string = f'mongodb+srv://{username}:{password}@cluster0.kfwumjq.mongodb.net/{database}?appName=mongosh+1.7.1'
client = MongoClient(connection_string)
database = client['crunchbase']
collection = database['crunchbase_database']

cursor = collection.find({})
for doc in cursor:
    pprint.pprint(doc)

### (And some RegEx as well …) Please write code (Python or Java) to query and print to screen all Crunchbase company “name”s (and “_id” but not the entire document) that have “text” in their “tag_list”.  (25% of points)

column21 = {'name': 1, '_id': 1}
query21 = {'tag_list' : {'$regex' : '\w*\\btext\\b\w*'}}

cursor21 = collection.find(query21, column21)
for doc in cursor21:
    pprint.pprint(doc)


### (This is the final enemy. This question is equivalent of being in the final level of Super Mario facing Bowser)  Please write code (Python or Java) to query and print to screen all Crunchbase company “name”s and “twitter_username” (and “_id” but not the entire document) that 
###     (i) were founded between 2000 and 2010 (including 2000 and 2010), or 
###     (ii) email address is ending in “@gmail.com”.  (25% of points)

column22 = {'name': 1, 'twitter_username': 1, '_id': 1}
query22 = {'$or' : [{'founded_year' : {'$gte': 2000, '$lte': 2010}}, 
                    {'email_address' : {'$regex': '[a-zA-Z0-9._%+-]+@gmail.com'}}]}

cursor22 = collection.find(query22, column22)
for doc in cursor22:
    print(doc)

