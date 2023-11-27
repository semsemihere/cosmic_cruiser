"""
This module interfaces to our user data.
"""
# import bcrypt
import hashlib
LEVEL = 'level'
MIN_USER_NAME_LEN = 2

# Dictionary of Users
"""
Each users have ...
    - hashed id (primary key)
    - email
    - username
    - password (hashed and never stored as plain text)
    - first name
    - last name
    - phone
    - role
        - admin
        - user
-
"""

users = {
    }


def create_user(username, password, email, first_name, last_name, phone):
    if not username:
        raise ValueError()
    id = (hashlib.sha3_512(username.encode('UTF-8'),
                           usedforsecurity=True)).hexdigest()
    print(id)
    if (id in users):
        print(True)
        return -1
    else:
        users[id] = {
            'email': email,
            'username': username,
            'hashedPass': hashlib.sha3_512(password.encode('UTF-8'),
                                           usedforsecurity=True),
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'role': 'user'
        }
        return id


def get_all_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    return users


# Get specific user information
def get_user(userId):
    if not (userId in users):
        return -1
    else:
        return users[userId]


# Update User information
def update_user(userId, field, update):
    """
    parameter: userId
        use the userId to grab the user information
    return: True is successful, else -1
    """
    user_info = get_user(userId)

    if user_info == -1:
        return user_info

    user_info[field] = update

    return True


# Remove the user from the db
def delete_user(userId):
    if (not (userId in users)):
        return False
    else:
        del users[userId]
        return True


def login_user(userId, passwordAttempt):
    if (not (userId in users)):
        return False
    if (hashlib.sha3_512(passwordAttempt.encode('UTF-8'),
        usedforsecurity=True)
        .hexdigest() == users
            [userId]['hashedPass'].hexdigest()):
        return True
    return False
