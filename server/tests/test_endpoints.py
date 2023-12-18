
import server.endpoints as ep
from unittest.mock import patch
import data.categories as categ
import pytest

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)


TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json

# def test_endpoints():
#     TEST_CLIENT.get(ep.)

def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json

def test_main_menu():
    resp = TEST_CLIENT.get(ep.MAIN_MENU_EP)
    resp_json = resp.get_json()
    print(resp_json)
    assert isinstance(resp_json, dict)
    assert resp_json[ep.TITLE] == ep.MAIN_MENU_NM


@pytest.mark.skip('bad test, just showing how skip works')
def test_to_skip_categ():
    assert(categ.add_category("test")=="test")


@patch('data.categories.delete_category', autospec=True)
def test_category_delete(mock_del):
    """
    Testing we do the right thing with a call to del_category that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_CATEGORY_EP}/AnyName')
    assert resp.status_code == OK


@patch('data.categories.delete_category', side_effect=ValueError(), autospec=True)
def test_category_bad_delete(mock_del):
    """
    Testing we do the right thing with a value error from del_category.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_CATEGORY_EP}/AnyName')
    assert resp.status_code == NOT_FOUND


@patch('data.categories.add_category', return_value=categ.MOCK_ID, autospec=True)
def test_category_add(mock_add):
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categ.get_test_category())
    assert resp.status_code == OK


@patch('data.categories.add_category', side_effect=ValueError(), autospec=True)
def test_category_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_category.
    """
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categ.get_test_category())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.categories.add_category', return_value=None)
def test_category_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_category.
    """
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categ.get_test_category())
    assert resp.status_code == SERVICE_UNAVAILABLE
