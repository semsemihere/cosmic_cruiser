import pytest
import hashlib
import data.users as usrs
from unittest.mock import patch
USERNAME = "test_username"
BAD_USERNAME = ""
PASSWORD = "test_password"
BAD_PASSWORD= ""
# fixture
@pytest.fixture
def create_test_user():
    if(USERNAME in usrs.get_all_users()):
        usrs.delete_user(USERNAME)
        
    print(usrs.get_all_users())
    id = usrs.create_user("test@gmail.com", USERNAME, PASSWORD, "Test", "Test", 1111111111)
    if id:
        yield USERNAME

    if(USERNAME in usrs.get_all_users()):
        usrs.delete_user(USERNAME)


def test_get_all_users():
    # users = usrs.get_all_users()
    users = usrs.get_all_users()
    assert(isinstance(users,dict))
    # assert len(users) > 0  


def test_create_user_ideal(create_test_user):
    print(usrs.get_all_users())
    assert USERNAME in usrs.get_all_users()


def test_create_dup_user(create_test_user):
    with pytest.raises(ValueError):
        usrs.create_user("test@gmail.com", USERNAME, PASSWORD, "Test", "Test", 1111111111)


# Test to make sure the exception is handled 
def test_create_user_fail():
    with pytest.raises(ValueError):
        usrs.create_user("", "","" , "", "", 0)
        
        
def test_delete_user_ideal(create_test_user):
    userId = create_test_user
    usrs.delete_user(userId)
    assert userId not in usrs.get_all_users()
    

def test_delete_non_user(create_test_user):
    with pytest.raises(ValueError):
        usrs.delete_user("")
    
    
def test_login_user_ideal(create_test_user):
    assert(usrs.login_user(create_test_user,PASSWORD))
    
def test_login_bad_user():
    assert(not(usrs.login_user(BAD_USERNAME,BAD_PASSWORD)))
    
    
def test_exists(create_test_user):
    assert USERNAME in usrs.get_all_users()


def test_bad_exists_request():
    username= ""
    assert(usrs.exists(username) == None)

@patch('data.users.create_user', return_value="null", autospec=True)
@pytest.mark.skip('bad test just to show how to skip')
def test_to_skip():
    assert (usrs.create_user("test")=="test")

def test_login_user(create_test_user):
    # password = "wrong_password"
    assert not usrs.login_user(USERNAME, BAD_PASSWORD)
