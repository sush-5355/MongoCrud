from bson.objectid import ObjectId
from mongo_utilities.mongo_config import db
from mongo_utilities.date_conversion import convert_date


async def create(collection_name: str, data: dict):
    collection = db[collection_name]
    data.update({'created_at': convert_date(), 'updated_at': convert_date()})
    response = collection.insert_one(data)
    id = response.inserted_id
    query = {"_id": ObjectId(id)}
    document = collection.find_one(query)
    document.update({'_id': str(document['_id'])})
    return dict(status=True, data=document)


async def get_via_id(collection_name: str, id: str):

    collection = db[collection_name]
    query = {"_id": ObjectId(id)}
    # retrieve the document
    try:
        document = collection.find_one(query)
        document.update({'_id': str(document['_id'])})
        return dict(status=True, data=document)
    except FileNotFoundError as e:
        return dict(status=False, msg=str(e))


async def update_via_id(collection_name: str, id: str, mapping: dict):

    collection = db[collection_name]
    query = {'_id': ObjectId(id)}
    mapping.update({'updated_at': convert_date()})
    new_values = {'$set': mapping}
    updated_document = collection.update_one(query, new_values)
    if updated_document is not None:
        return await get_via_id(collection_name=collection_name, id=id)
    else:
        return dict(status=False, msg='No record found')


async def update(collection_name: str, query: dict, mapping: dict):

    collection = db[collection_name]
    mapping.update({'updated_at': convert_date()})
    new_values = {'$set': mapping}
    try:
        result = collection.update_many(query, new_values)
        updated_documents = collection.find(mapping)
        response_list = []
        for document in updated_documents:
            response = await get_via_id(collection_name=collection_name, id=document['_id'])
            response_list.append(response)
        return dict(status=True, data=response_list, count=result.modified_count)
    except Exception as e:
        return dict(status=False, msg=str(e))


async def get_all(collection_name: str, query: dict = None):

    collection = db[collection_name]
    # retrieve all documents in the collection
    if query:
        documents = collection.find(query)
        count = collection.count_documents(query)
    else:
        documents = collection.find({})
        count = collection.count_documents({})
    all_documents = []
    # iterate over the cursor and print each document
    for document in documents:
        document['_id'] = str(document['_id'])
        all_documents.append(document)
    if count > 0:
        return dict(status=True, data=all_documents, count=count)
    return dict(status=False, msg='No Data found', count=count)


async def delete_via_query(collection_name: str, query={}):

    collection = db[collection_name]
    try:
        result = collection.delete_many(query)
        return dict(status=True, msg='Records deleted', count=result.deleted_count)
    except Exception as e:
        return dict(status=False, msg=str(e))


async def del_via_id(collection_name: str, id: str):

    collection = db[collection_name]
    # async define the _id of the record to delete
    record_id = ObjectId(id)
    # delete the record with the specified _id
    try:
        collection.delete_one({'_id': record_id})
        return dict(status=True, msg='Records deleted')
    except Exception as e:
        return dict(status=False, msg=str(e))
