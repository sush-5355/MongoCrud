from mongo_utilities.mongo_config_class import MongoDBUtility


data = {
    'name':'sfdff',
    'age':28
}

mongoObj = MongoDBUtility(collection_name='test1')
r = mongoObj.create(data=data)
print(r)