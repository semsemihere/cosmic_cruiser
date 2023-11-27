import pytest
import hashlib
import data.users as usrs
from unittest.mock import patch

# fixture
@pytest.fixture
def create_test_user():
    userId = usrs.create_user("test", "test_password","test@gmail.com", "Test", "Test", 1111111111)
    yield userId
    if(userId in usrs.get_all_users()):
        usrs.delete_user(userId)

def test_get_all_users(create_test_user):
    # users = usrs.get_all_users()
    users = usrs.get_all_users()
    assert(isinstance(users,dict))
    assert len(users) > 0  # at least one user!
    # for key in users:
    #     assert isinstance(key, int)
    #     assert len(key['username']) >= usrs.MIN_USER_NAME_LEN


# Test to make sure that the user is created 
# (User exists in users)
def test_create_user_ideal(create_test_user):
    # username = create_test_user()
    users = usrs.get_all_users()
    assert (create_test_user in users)

# @patch('data.users.create_user', side_effect=ValueError(), autospec=True)
# def test_user_create_dup():

#     user2 = usrs.create_user("test")
#     assert user2==-1


# Test to make sure the exception is handled 
def test_create_user_fail():
    with pytest.raises(ValueError):
        usrs.create_user("", "","" , "", "", 0)
        
def test_get_user(create_test_user):
    userId = create_test_user
    users = usrs.get_all_users()
    assert(usrs.get_user(userId)==(users[userId]))

def test_delete_user(create_test_user):
    userId = create_test_user
    usrs.delete_user(userId)
    users = usrs.get_all_users()
    assert (not(userId in users))

def test_bad_get_user_request():
    username=""
    assert(usrs.get_user((hashlib.sha3_512(username.encode('UTF-8'),
                           usedforsecurity=True)).hexdigest())==-1)


def test_update_user(create_test_user):
    userId = create_test_user
    field = 'username'
    newValue = "test2"
    usrs.update_user(userId,field,newValue)
    assert(usrs.get_user(userId)[field]==newValue)

def test_bad_update_user(create_test_user):
    username = ""
    userId = hashlib.sha3_512(username.encode('UTF-8'),usedforsecurity=True).hexdigest()
    field = 'username'
    newValue = "test2"
    assert(usrs.update_user(userId,field,newValue)==-1)


def test_user_exists_delete_user():
    userId = create_test_user
    usrs.delete_user(userId)
    user2 = usrs.delete_user(userId)
    assert user2==False


@patch('data.users.create_user', return_value="null", autospec=True)
@pytest.mark.skip('bad test just to show how to skip')
def test_to_skip():
    assert (usrs.create_user("test")=="test")


def test_dup_user(create_test_user): 
    user=usrs.create_user("test", "test_password","test@gmail.com", "Test", "Test", 1111111111)
    assert(user==-1)
        
        
def test_login_user(create_test_user):
    userId = create_test_user
    assert(usrs.login_user(userId,"test_password")==True)