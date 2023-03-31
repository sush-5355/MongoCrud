import pymongo

mongo_creds = {
    'username': "",
    'password': "",
    'hostname': "localhost",
    "port": 27017,
    "database":"abgdatabase"
}

if mongo_creds.get('username') == "":
    url = f"mongodb://{mongo_creds.get('hostname')}:{mongo_creds.get('port')}/{mongo_creds.get('database')}"
else:
    url = f"mongodb://{mongo_creds.get('username')}:{mongo_creds.get('password')}@{mongo_creds.get('hostname')}:{mongo_creds.get('port')}/{mongo_creds.get('database')}"

client = pymongo.MongoClient(url)
db = client[mongo_creds['database']]
