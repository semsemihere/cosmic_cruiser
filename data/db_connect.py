
import os

import requests
from requests.auth import HTTPDigestAuth
# import ipify

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

MONGO_DB = 'ccDB'

client = None

MONGO_ID = '_id'

atlas_group_id = ""
atlas_api_key_public = "<your atlas public API key>"
atlas_api_key_private = "<your atlas private API key>"
# ip = get_ip()

# resp = requests.post(
#     "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
#     auth=HTTPDigestAuth(atlas_api_public_key, atlas_api_private_key),
#     json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]  # the comment is optional
# )
# if resp.status_code in (200, 201):
#     print("MongoDB Atlas accessList request successful", flush=True)
# else:
#     print(
#         "MongoDB Atlas accessList request problem: status code was {status_code}, content was {content}".format(
#             status_code=resp.status_code, content=resp.content
#         ),
#         flush=True
#     )

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
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


def update_one(collection, filter_query, update_query, db=MONGO_DB):
    result = client[db][collection].update_one(filter_query, update_query)
    return result.modified_count > 0 if result else False
