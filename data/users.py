"""
This module interfaces to our user data.
"""
# import bcrypt
import data.db_connect as dbc
import hashlib

USERS_COLLECT = "users"

EMAIL = "email"
USERNAME = "username"
PASSWORD = "password"
FIRSTNAME = "firstname"
LASTNAME = "lastname"
PHONE = "phonenumber"
ROLE = 'role'

users = {}


def get_all_users():
    dbc.connect_db()
    print(dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT))
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)


# check if the username exists
# returns the user info if exists, else, return none
def exists(username):
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USERNAME: username})


def create_user(email, username, password, first_name, last_name, phone):
    if not username:
        raise ValueError('Username missing')
    if exists(username):
        raise ValueError('Username already exists')

    # Previous code
    # id = (hashlib.sha3_512(username.encode('UTF-8'),
    #                        usedforsecurity=True)).hexdigest()
    # # print(id)
    # if (id in users):
    #     raise ValueError(f'Username already exists')

    # users[id] = {
    #     'email': email,
    #     'username': username,
    #     'hashedPass': hashlib.sha3_512(password.encode('UTF-8'),
    #                                     usedforsecurity=True),
    #     'first_name': first_name,
    #     'last_name': last_name,
    #     'phone': phone,
    #     'role': 'user'
    # }

    # user[id] = {
    #     'email': email,
    #     'username': username,
    #     'hashedPass': password,
    #     'first_name': first_name,
    #     'last_name': last_name,
    #     'phone': phone,
    #     'role': 'user'
    # }

    user = {}
    user[EMAIL] = email
    user[USERNAME] = username
    user[PASSWORD] = hashlib.sha3_512(password.encode('UTF-8'),
                                      usedforsecurity=True).hexdigest()
    user[FIRSTNAME] = first_name
    user[LASTNAME] = last_name
    user[PHONE] = phone
    user[ROLE] = 'user'

    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, user)
    return _id is not None
    # return _id


def delete_user(username):
    dbc.connect_db()
    if exists(username):
        id = dbc.del_one(USERS_COLLECT, {'username': username})
    else:
        raise ValueError(f'Delete failure: {username} not in database.')
    return id is not None


# # Remove the user from the db
# def delete_user(username):
#     if exists(username):
#         return dbc.del_one(USERS_COLLECT, {USERNAME : username})


# # Update User information
# def update_user(username, field, update):
#     # parameter: userId
#     #     use the userId to grab the user information
#     # return: True is successful, else -1
#     user_info = exists(username)

#     if user_info:
#         user_info[field] = update
#         return True
#     return -1

def login_user(userId, passwordAttempt):
    if exists(userId):
        users = get_all_users()
        print(users[userId])
        if (hashlib.sha3_512(passwordAttempt.encode('UTF-8'),
                             usedforsecurity=True)
                .hexdigest() == users[userId][PASSWORD]):
            return True
    return False
