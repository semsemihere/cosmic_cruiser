import pytest
from unittest.mock import patch
import data.db_connect as dbc
import os

TEST_DB = dbc.MONGO_DB
TEST_COLLECT = 'test_collect'
# can be used for field and value:
TEST_NAME = 'test'


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})


# test for db password and connection
@patch('data.db_connect.get_client', return_value=None, autospec=True)
def test_connect_db_local_success(mock):
    assert dbc.connect_db() == 0

@patch('data.db_connect.get_client', return_value=None, autospec=True)
@patch('data.db_connect.get_cloud_status', return_value=dbc.CLOUD, autospec=True)
def test_connect_db_cloud_success(mock_client, mock_cloud_status):
    with pytest.raises(ValueError):
        dbc.connect_db()

def test_connect_db_already_connected():
    assert dbc.connect_db() == 3

def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None

def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
    assert ret is None

# check if the delete all function removes all documents from the collection
def test_del_one(temp_rec):
    dbc.del_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    count = dbc.count_documents(TEST_COLLECT)
    assert count == 0

# check if the delete all function removes all documents from the collection
def test_delete_all(temp_rec):
    dbc.delete_all(TEST_COLLECT)
    count = dbc.count_documents(TEST_COLLECT)
    assert count == 0

def test_count_documents(temp_rec):
    count = dbc.count_documents(TEST_COLLECT)
    assert count == 1

def test_fetch_all(temp_rec):
    ret = dbc.fetch_all(TEST_COLLECT)
    assert len(ret) == 1

def test_fetch_all_as_dict(temp_rec):
    fetched = dbc.fetch_all_as_dict(TEST_NAME, TEST_NAME) 
    assert isinstance(fetched, dict) 