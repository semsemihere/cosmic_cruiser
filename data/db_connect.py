
import os


import pymongo as pm

LOCAL = "0"
CLOUD = "1"

MONGO_DB = 'ccDB'

client = None

MONGO_ID = '_id'


def get_client():
    return client


def set_client(assigment):
    global client
    client = assigment


def get_cloud_status():
    return os.environ.get("CLOUD_MONGO", LOCAL)


def get_cloud_password():
    return os.environ.get("MONGODB_PASSWORD")


def set_cloud_password(password):
    os.environ["MONGODB_PASSWORD"] = password
    return password


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    if get_client() is None:  # not connected yet!
        print("Setting client because it is None.")
        if get_cloud_status() == CLOUD:
            password = get_cloud_password()
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")

            set_client(pm.MongoClient(f'mongodb+srv://semihong:{password}'
                                      + '@cosmiccrusier.3cyi8m1.mongodb.net/'
                                      + '?retryWrites=true&w=majority'
                                      + '&connectTimeoutMS=30000'
                                      + '&socketTimeoutMS=None'
                                      + '&socketKeepAlive=True'
                                      + '&connect=False'
                                      + '&maxPoolsize=1'))
            # PA recommends these settings:

            # but they don't seem necessary
            return 1
        else:
            print("Connecting to Mongo locally.")
            set_client(pm.MongoClient())

            return 0
    else:
        return 3


# function to insert single doc into collection
def insert_one(collection, doc, db=MONGO_DB):
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


# function to return first doc found with filer
def fetch_one(collection, filt, db=MONGO_DB):
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
        return doc


# function to delete first doc found with filter
def del_one(collection, filt, db=MONGO_DB):
    client[db][collection].delete_one(filt)


# function to delete all docs in collection
def delete_all(collection, db=MONGO_DB):
    return client[db][collection].delete_many({})


# function to count number of documents in collection
def count_documents(collection, db=MONGO_DB):
    return client[db][collection].count_documents({})


# function to fetch all docs in collection
def fetch_all(collection, db=MONGO_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=MONGO_DB):
    ret = {}
    for doc in client[db][collection].find():
        if key in doc:
            del doc[MONGO_ID]
            ret[doc[key]] = doc
    return ret


def fetch_articles_by_section(nutrition_section_id,
                              section_key,
                              article_key,
                              collection, db=MONGO_DB):
    ret = {}
    article_ids = []
    for doc in client[db][collection].find():
        if section_key in doc:
            if doc[section_key] == nutrition_section_id:
                # print(doc)
                for article_id in doc['arrayOfArticleIDs']:
                    article_ids.append(article_id)

    for doc in client[db][collection].find():
        if article_key in doc:
            for _id in article_ids:
                if doc[article_key] == _id:
                    del doc[MONGO_ID]
                    ret[doc[article_key]] = doc

    return ret


def update_one(collection, filter_query, update_query, db=MONGO_DB):
    result = client[db][collection].update_one(filter_query, update_query)
    return result.modified_count > 0 if result else False
