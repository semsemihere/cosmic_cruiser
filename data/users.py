"""
This module interfaces to our user data.
"""

LEVEL = 'level'
MIN_USER_NAME_LEN = 2

users = {
        "Callahan": {
            LEVEL: 0,
        },
        "Reddy": {
            LEVEL: 1,
        },
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


def create_user(username):
    if not username:
        raise ValueError()
    elif (username in users):
        return -1
    else:
        users.update({username: 0})
        return {username: 0}


def delete_user(username):
    if (not (username in users)):
        return -1
    else:
        users.pop(username)
        return username
