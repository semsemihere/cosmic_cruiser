
import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

USER_DB = 'usersDB'
MONGO_DB = 'ccDB'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("MONGODB_PASSWORD")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")

            client = pm.MongoClient(f'mongodb+srv://semihong:{password}'
                                    + '@cosmiccrusier.3cyi8m1.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


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
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret
