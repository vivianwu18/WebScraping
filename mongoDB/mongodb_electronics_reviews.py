import pymongo 
from pymongo import MongoClient
import json
import pprint
from bson.code import Code


### Creates a MongoDB DB called "amazon"

# check the connection
username = 'username'
password = 'password'

connection_string = f'mongodb+srv://{username}:{password}@cluster0.kfwumjq.mongodb.net/?appName=mongosh+1.7.1'
client = MongoClient(connection_string)
database = client['amazon']
client.server_info()


### Reads "reviews_electronics.16.json" and uploads each review as a separate document to the collection "reviews" in the DB "amazon".
reviews = []
for line in open('reviews_electronics.16.json'):
    reviews.append(json.loads(line))

# insert data into colleciton
collection = database['reviews']

size = 5000
for i in range(0, len(reviews), size):
    batch = reviews[i : i + size]
    collection.insert_many(batch)
    print(f'The reveiws from {i} to {i + size} are inserted successfully!')

# check the number of data points
len(reviews)


### Uses MongoDB's map reduce function to build a new collection "avg_scores" that averages review scores by product ("asin"). Print the first 100 entries of "avg_scores" to screen.
# change the data type of the score to integer
collection = database['reviews']
collection.update_many({}, [
    {
        '$set': {
            'overall': {'$toInt': '$overall'}
        }
    }
])

# run the aggregate operation and save the results to a new collection
collection.aggregate([
   {'$group': {'_id':'$asin', 'avg_score': {'$avg': '$overall'} } },
   {'$out': 'avg_scores' }
])

# print the first 100 entries of the "avg_scores" collection
for doc in database['avg_scores'].find().limit(100):
    print(doc)


### Uses MongoDB's map reduce function to build a new collection "weighted_avg_scores" that averages review scores by product ("asin"), weighted by the number of votes + 1 (the second number + 1). Print the first 100 entires of "weighted_avg_scores" to screen.
collection.aggregate([
    {'$project' : {'asin' : 1, 
                   'overall' : 1, 
                   'weighted_vote' : {'$add' : [{'$toInt': {'$arrayElemAt': ['$helpful', 1]}}, 1]}}},
    {'$group': {'_id': '$asin', 
                'avg_score': {'$sum': {'$multiply' : ['$overall', '$weighted_vote']}}, 
                'sum_vote' : {'$sum' : '$weighted_vote'} } },
    {'$project' : {'asin' : '$asin', 
                   'weighted_avg_score' : {'$divide' : [{'$toDouble': '$avg_score'}, {'$toDouble': '$sum_vote'}]}}},
    {'$out': 'weighted_avg_scores' }
])

# print the first 100 entries of the "weighted_avg_scores" collection
for doc in database['weighted_avg_scores'].find().limit(100):
    print(doc)

