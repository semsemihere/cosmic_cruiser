import pytest
import data.users as usrs
from unittest.mock import patch

# fixture
@pytest.fixture
def check_user():
    return usrs.get_all_users()


def test_get_all_users(check_user):
    # users = usrs.get_all_users()
    
    assert isinstance(check_user, dict)
    assert len(check_user) > 0  # at least one user!
    # for key in users:
    #     assert isinstance(key, int)
    #     assert len(key['username']) >= usrs.MIN_USER_NAME_LEN


# Test to make sure that the user is created 
# (User exists in users)
def test_create_user_ideal():
    username = usrs.create_user("test", "test@gmail.com", "Test", "Test", 1111111111)

    # username = create_test_user()
    users = usrs.get_all_users()
    assert (username in users)

# @patch('data.users.create_user', side_effect=ValueError(), autospec=True)
# def test_user_create_dup():

#     user2 = usrs.create_user("test")
#     assert user2==-1


# Test to make sure the exception is handled 
def test_create_user_fail():
    with pytest.raises(ValueError):
        usrs.create_user("", "", "", "", 0)
        


def test_delete_user():
    # username = create_test_user()
    username = usrs.create_user('semsemi', 'sh6042@nyu.edu', 'Semi', 'Hong', 1987654321)
    users = usrs.get_all_users()
    usrs.delete_user(username)
    assert (not(username in users))
    # user2 = usrs.delete_user(username)
    # assert user2==-1


def test_user_exists_delete_user():
    username = usrs.create_user('semsemi', 'sh6042@nyu.edu', 'Semi', 'Hong', 1987654321)
    usrs.delete_user(username)
    user2 = usrs.delete_user(username)
    assert user2==-1


@patch('data.users.create_user', return_value="null", autospec=True)
@pytest.mark.skip('bad test just to show how to skip')
def test_to_skip():
    assert (usrs.create_user("test")=="test")


def test_dup_user(): 
    usrs.create_user("test", "test@gmail.com", "Test", "Test", 1111111111)
    # with pytest.raises(KeyError):
    user=usrs.create_user("test", "test@gmail.com", "Test", "Test", 1111111111)
    assert(user==-1)
        