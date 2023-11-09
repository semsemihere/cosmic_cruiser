import pytest
import data.users as usrs
from unittest.mock import patch

def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)

# Test to make sure that the user is created 
# (User exists in users)
def test_create_user_ideal():
    username = "test"
    user = usrs.create_user(username)
    users = usrs.get_users()
    assert (username in users)
    user2 = usrs.create_user("test")
    assert user2==-1

@patch('data.users.create_user', side_effect=ValueError(), autospec=True)
# Test to make sure the exception is handled 
def test_create_user_fail(mockArg):
    with pytest.raises(ValueError):
        usrs.create_user("")
        


def test_delete_user():
    username = "test"
    users = usrs.get_users()
    assert (username in users)
    user = usrs.delete_user(username)
    assert (not(username in users))
    user2 = usrs.delete_user(username)
    assert user2==-1
