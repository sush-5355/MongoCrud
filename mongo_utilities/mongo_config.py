
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()


mongo_creds = {
    'username': os.environ.get('mongo_username'),
    'password': os.environ.get('mongo_password'),
    'hostname': os.environ.get('mongo_hostname'),
    "port": 27017,
    "database": "abgdatabase"
}

if mongo_creds.get('username') == 'None':
    url = f"mongodb://{mongo_creds.get('hostname')}:{mongo_creds.get('port')}/{mongo_creds.get('database')}"
else:
    url = f"mongodb://{mongo_creds.get('username')}:{mongo_creds.get('password')}@{mongo_creds.get('hostname')}:{mongo_creds.get('port')}/{mongo_creds.get('database')}"
client = pymongo.MongoClient(url)
db = client[mongo_creds['database']]