"""
creates & reads database
"""

import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

# Create user instance
def add_user(name, email, password, role):
    """
    Inserts a user into user db, with following fields:
    - "name"
    - "email"
    - "password"
    - "role"
    """

    users_doc = { 
        'name' : name, 
        'email' : email,
        'password' : password,
        'role' : role}
    return db.users.insert_one(users_doc)


# Read users
def get_all_users():
    """
    Returns list of users' names in the database.
    """
    return list(db.users.aggregate([
        {"$unwind": "$users"}
    ]))[0]["names"]