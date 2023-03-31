from bson.objectid import ObjectId
from mongo_utilities.mongo_config import db
from mongo_utilities.date_conversion import convert_date


class MongoDBUtility:
    def __init__(self, collection_name):
        self.collection = db[collection_name]

    def create(self, data):
        data.update({'created_at': convert_date(), 'updated_at': convert_date()})
        response = self.collection.insert_one(data)
        id = response.inserted_id
        query = {"_id": ObjectId(id)}
        document = self.collection.find_one(query)
        document.update({'_id': str(document['_id'])})
        return dict(status=True, data=document)

    def get_via_id(self, id):
        query = {"_id": ObjectId(id)}
        # retrieve the document
        try:
            document = self.collection.find_one(query)
            document.update({'_id': str(document['_id'])})
            return dict(status=True, data=document)
        except FileNotFoundError as e:
            return dict(status=False, msg=str(e))

    def update_via_id(self, id, mapping):
        query = {'_id': ObjectId(id)}
        mapping.update({'updated_at': convert_date()})
        new_values = {'$set': mapping}
        updated_document = self.collection.update_one(query, new_values)
        if updated_document is not None:
            return self.get_via_id(id=id)
        else:
            return dict(status=False, msg='No record found')

    def update(self, query, mapping):
        mapping.update({'updated_at': convert_date()})
        new_values = {'$set': mapping}
        try:
            result = self.collection.update_many(query, new_values)
            updated_documents = self.collection.find(mapping)
            response_list = []
            for document in updated_documents:
                response = self.get_via_id(id=document['_id'])
                response_list.append(response)
            return dict(status=True, data=response_list, count=result.modified_count)
        except Exception as e:
            return dict(status=False, msg=str(e))

    def get_all(self, query=None):
        # retrieve all documents in the collection
        if query:
            documents = self.collection.find(query)
            count = self.collection.count_documents(query)
        else:
            documents = self.collection.find({})
            count = self.collection.count_documents({})
        all_documents = []
        # iterate over the cursor and print each document
        for document in documents:
            document['_id'] = str(document['_id'])
            all_documents.append(document)
        if count > 0:
            return dict(status=True, data=all_documents, count=count)
        return dict(status=False, msg='No Data found', count=count)

    def delete_via_query(self, query={}):
        try:
            result = self.collection.delete_many(query)
            return dict(status=True, msg='Records deleted', count=result.deleted_count)
        except Exception as e:
            return dict(status=False, msg=str(e))

    def del_via_id(self, id):
        # async define the _id of the record to delete
        record_id = ObjectId(id)
        # delete the record with the specified _id
        try:
            self.collection.delete_one({'_id': record_id})
            return dict(status=True, msg='Records deleted')
        except Exception as e:
            return dict(status=False, msg=str(e))
