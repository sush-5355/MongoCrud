from utilities.date_conversion import convert_date
from bson.objectid import ObjectId
from utilities.mongo_config import *


def create(client, database_name: str, collection_name: str, data: str):
    db = client[database_name]
    collection = db[collection_name]
    data.update({'created_at': convert_date(), 'updated_at': convert_date()})
    response = collection.insert_one(data)
    id = response.inserted_id
    query = {"_id": ObjectId(id)}
    document = collection.find_one(query)
    document.update({'_id': str(document['_id'])})
    return dict(status=True, data=document)


def get_via_id(client, database_name: str, collection_name: str, id: str):
    db = client[database_name]
    collection = db[collection_name]
    query = {"_id": ObjectId(id)}
    # retrieve the document
    try:
        document = collection.find_one(query)
        document.update({'_id': str(document['_id'])})
        return dict(status=True, data=document)
    except FileNotFoundError as e:
        return dict(status=False, msg=str(e))


def update_via_id(client, database_name: str, collection_name: str, id: str, mapping: dict):
    db = client[database_name]
    collection = db[collection_name]
    query = {'_id': ObjectId(id)}
    mapping.update({'updated_at': convert_date()})
    new_values = {'$set': mapping}
    updated_document = collection.update_one(query, new_values)
    if updated_document is not None:
        return get_via_id(client=client, database_name=database_name, collection_name=collection_name, id=id)
    else:
        return dict(status=False, msg='No record found')


def update(client, database_name: str, collection_name: str, query: dict, mapping: dict):
    db = client[database_name]
    collection = db[collection_name]
    mapping.update({'updated_at': convert_date()})
    new_values = {'$set': mapping}
    try:
        result = collection.update_many(query, new_values)
        updated_documents = collection.find(mapping)
        response_list = []
        for document in updated_documents:
            print("Updated document _id:", document['_id'])
            response = get_via_id(client=client, database_name=database_name,
                                  collection_name=collection_name, id=document['_id'])
            response_list.append(response)
        return dict(status=True, data=response_list, count=result.modified_count)
    except Exception as e:
        return dict(status=False, msg=str(e))


def get_all(client, database_name: str, collection_name: str):
    db = client[database_name]
    collection = db[collection_name]
    # retrieve all documents in the collection

    documents = collection.find({})
    all_documents = []
    # iterate over the cursor and print each document
    for document in documents:
        document['_id'] = str(document['_id'])
        print(document)
        all_documents.append(document)
    count = collection.count_documents({})
    if count > 0:
        return dict(status=True, data=all_documents, count=count)
    return dict(status=False, msg='Please check the database and collection name', count=count)


def delete_via_query(client, database_name: str, collection_name: str, query={}):
    db = client[database_name]
    collection = db[collection_name]
    try:
        result = collection.delete_many(query)
        return dict(status=True, msg='Records deleted', count=result.deleted_count)
    except Exception as e:
        return dict(status=False, msg=str(e))


def del_via_id(client, database_name: str, collection_name: str, id: str):
    db = client[database_name]
    collection = db[collection_name]

    # define the _id of the record to delete
    record_id = ObjectId(id)

    # delete the record with the specified _id
    try:
        collection.delete_one({'_id': record_id})
        return dict(status=True, msg='Records deleted')
    except Exception as e:
        return dict(status=False, msg=str(e))
