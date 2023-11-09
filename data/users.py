"""
This module interfaces to our user data.
"""
# import random

LEVEL = 'level'
MIN_USER_NAME_LEN = 2

# Dictionary of Users
"""
Each users have ...
    - hashed id (primary key)
        - for now, used number
    - email
    - username
    - first name
    - last name
    - phone
    - role
        - admin
        - user
-
"""
users = {
        'ch123': {
            'email': 'cas123@nyu.edu',
            'username': 'ch123',
            'first_name': 'Smith',
            'last_name': 'Callahan',
            'phone': 1231231234,
            'role': 'user'
        },

        'cf123': {
            'email': 'afd123@gmail.com',
            'username': 'cf123',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone': 9879879876,
            'role': 'user'
        },

        'an982': {
            'email': 'ani987@gmail.com',
            'username': 'an982',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': 2472472478,
            'role': 'user'
        }
    }


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    return users


# def id_generator():
#     return random.randint(10000, 99999)


# def create_admin(username, email, first_name, last_name, phone):

#     id = id_generator()

#     if not username:
#         raise ValueError()
#     elif (username in users):
#         return False
#     else:
#         users[id] = {
#             'email': email,
#             'username': username,
#             'first_name': first_name,
#             'last_name': last_name,
#             'phone': phone,
#             'role': 'admin'}
#         return True


def create_user(username, email, first_name, last_name, phone):

    # id = id_generator()

    if not username:
        raise ValueError()
    elif (username in users):
        return -1
    else:
        users[username] = {
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'role': 'user'}
        return username


def delete_user(username):
    if (not (username in users)):
        return -1
    else:
        del users[username]
        return True
