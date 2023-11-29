import pytest

import data.db_connect as dbc

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


# def test_fetch_one(temp_rec):
#     ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
#     assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
    assert ret is None


# check if the delete all function removes all documents from the collection
def test_delete_all(temp_rec):
    dbc.delete_all(TEST_COLLECT)
    count = dbc.count_documents(TEST_COLLECT)
    assert count == 0