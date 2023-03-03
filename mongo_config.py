import pymongo

username ="localhost"
port = 27017

client = pymongo.MongoClient(f"mongodb://{username}:{port}/")
