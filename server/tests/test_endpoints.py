
import server.endpoints as ep
from unittest.mock import patch
import werkzeug.exceptions as wz
import data.categories as categ
import data.users as usrs
import data.nutrition as nutr
import data.finances as fin
import data.ems as ems

import pytest

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)
USERNAME = "test_username"
BAD_USERNAME = ""
PASSWORD = "test_password"
BAD_PASSWORD= ""

TEST_CLIENT = ep.app.test_client()
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

def test_login():
    resp = TEST_CLIENT.get(ep.LOGIN_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    resp_json = str(resp_json)[:15]
    assert ep.LOGIN_RESP in resp_json


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json

def test_endpoints():
    resp = TEST_CLIENT.get('/endpoints')
    resp_json = resp.get_json()
    print(resp_json)
    assert resp_json["Available endpoints"] == sorted(rule.rule for rule in ep.api.app.url_map.iter_rules())

def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp_json[ep.DATA] == usrs.get_all_users()

def test_main_menu():
    resp = TEST_CLIENT.get(ep.MAIN_MENU_EP)
    resp_json = resp.get_json()
    print(resp_json)
    assert isinstance(resp_json, dict)
    assert resp_json[ep.TITLE] == ep.MAIN_MENU_NM

def test_user_menu():
    resp = TEST_CLIENT.get(ep.USER_MENU_EP)
    resp_json = resp.get_json()
    print(resp_json)
    assert isinstance(resp_json, dict)
    assert resp_json[ep.TITLE] == ep.USER_MENU_NM


@pytest.mark.skip('bad test')
def test_bad_user_delete(create_test_user):
    username = create_test_user
    usrs.delete_user(username)
    resp = TEST_CLIENT.delete(ep.DEL_USERS_EP+'/'+username)
    resp_json = resp.get_json()
    print(resp_json)
    assert resp.status_code == NOT_FOUND


@pytest.mark.skip('bad test')
def test_user_delete(create_test_user):
    username = create_test_user
    resp = TEST_CLIENT.delete(ep.DEL_USERS_EP+'/'+username)
    resp_json = resp.get_json()
    print(resp_json)
    assert resp_json[username] == 'Deleted'


@pytest.mark.skip('bad test')
@patch('data.users.create_user', side_effect=ValueError(), autospec=True)
def test_post_bad_user(mock_post):
    resp = TEST_CLIENT.post(ep.USERS_EP, json={usrs.EMAIL:"test@gmail.com", usrs.USERNAME: USERNAME,usrs.PASSWORD:PASSWORD,usrs.FIRSTNAME:"test",usrs.LASTNAME:"test",usrs.PHONE:1111111111})
    assert resp.status_code == NOT_ACCEPTABLE
    
@pytest.mark.skip('bad test')
@patch('data.users.create_user', return_value=USERNAME, autospec=True)
def test_post_user(mock_post):
    resp = TEST_CLIENT.post(ep.USERS_EP, json={usrs.EMAIL:"test@gmail.com", usrs.USERNAME: USERNAME,usrs.PASSWORD:PASSWORD,usrs.FIRSTNAME:"test",usrs.LASTNAME:"test",usrs.PHONE:1111111111})
    assert resp.status_code == OK
    

@pytest.mark.skip('bad test, just showing how skip works')
def test_to_skip_categ():
    assert(categ.add_category("test")=="test")


def test_list_categories():
    resp = TEST_CLIENT.get(ep.CATEGORIES_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp_json[ep.DATA] == categ.get_categories()

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

@patch('data.categories.update_category_name', return_value=categ.MOCK_ID, autospec=True)
def test_good_update_category_name(mock_update):
    """
    Testing successful category name update
    """
    category_id = categ.generate_category_id()
    new_category_name = "NEW CATEGORY NAME"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_NAME_EP}/{category_id}/{new_category_name}', json=categ.get_test_category())
    assert resp.status_code == OK

@patch('data.categories.update_category_name', side_effect=ValueError(), autospec=True)
def test_bad_value_error_update_category_name(mock_update):
    """
    Testing bad value error category name update
    """
    category_id = categ.generate_category_id()
    new_category_name = "NEW CATEGORY NAME"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_NAME_EP}/{category_id}/{new_category_name}', json=categ.get_test_category())
    assert resp.status_code == NOT_FOUND

@patch('data.categories.update_category_name', side_effect=Exception(), autospec=True)
def test_bad_exception_update_category_name(mock_update):
    """
    Testing bad exception category name update
    """
    category_id = categ.generate_category_id()
    new_category_name = "NEW CATEGORY NAME"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_NAME_EP}/{category_id}/{new_category_name}', json=categ.get_test_category())
    assert resp.status_code == BAD_REQUEST

@patch('data.categories.update_category_sections', return_value=categ.MOCK_ID, autospec=True)
def test_good_update_category_sections(mock_update):
    """
    Testing successful category num section update
    """
    category_id = categ.generate_category_id()
    updated_num_sections = "1"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_SECTIONS_EP}/{category_id}/{updated_num_sections}', json=categ.get_test_category())
    assert resp.status_code == OK

@patch('data.categories.update_category_sections', side_effect=ValueError(), autospec=True)
def test_bad_value_error_update_category_sections(mock_update):
    """
    Testing bad value error category num section update
    """
    category_id = categ.generate_category_id()
    updated_num_sections = "1"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_SECTIONS_EP}/{category_id}/{updated_num_sections}', json=categ.get_test_category())
    assert resp.status_code == NOT_FOUND

@patch('data.categories.update_category_sections', side_effect=Exception(), autospec=True)
def test_bad_exception_update_category_sections(mock_update):
    """
    Testing bad exception category name update
    """
    category_id = categ.generate_category_id()
    updated_num_sections = "1"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_SECTIONS_EP}/{category_id}/{updated_num_sections}', json=categ.get_test_category())
    assert resp.status_code == BAD_REQUEST
    
@pytest.mark.skip('temporary skip (broken test)')
def test_get_nutrition_sections():
    resp = TEST_CLIENT.get(ep.NUTRITION_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


# @patch('data.nutrition.add_section', return_value=nutr.MOCK_ID, autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_good_add_nutrition_section(mock_add):
    """
    Testing we do the right thing with a good return from add_section.
    """
    resp = TEST_CLIENT.post(ep.NUTRITION_EP, json=nutr.get_test_section())
    assert resp.status_code == OK


# @patch('data.nutrition.add_section', side_effect=ValueError(), autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_bad_add_nutrition_section(mock_add):
    """
    Testing we do the right thing with a value error from add_section.
    """
    resp = TEST_CLIENT.post(ep.NUTRITION_EP, json=nutr.get_test_section())
    assert resp.status_code == NOT_ACCEPTABLE


@pytest.mark.skip('temporary skip (broken test)')
def test_nutrition_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_section.
    """
    resp = TEST_CLIENT.post(ep.NUTRITION_EP, json=nutr.get_test_section())
    # assert resp.status_code == SERVICE_UNAVAILABLE
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.nutrition.delete_section', autospec=True)
def test_good_nutrition_delete(mock_del):
    """
    Testing we do the right thing with a call to delete_section that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_NUTRITION_SECTION_EP}/AnyName')
    assert resp.status_code == OK


@patch('data.nutrition.delete_section', side_effect=ValueError(), autospec=True)
def test_nutrition_bad_delete(mock_del):
    """
    Testing we do the right thing with a value error from delete_section.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_NUTRITION_SECTION_EP}/AnyName')
    assert resp.status_code == NOT_FOUND


# @patch('data.nutrition.update_nutrition_section_content', return_value=nutr.MOCK_ID, autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_good_update_nutrition_section_content(mock_update):
    """
    Testing we do the right thing with a good return from update_nutrition_section_content.
    """
    section_id = nutr.generate_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.NUTRITION_EP}/{section_id}/{new_content}', json=nutr.get_test_section())
    assert resp.status_code == OK


@patch('data.nutrition.update_nutrition_section_content', side_effect=ValueError(), autospec=True)
def test_bad_value_error_update_nutrition_section_content(mock_update):
    """
    Testing we do the right thing with a value error when updating nutrition contents.
    """
    section_id = nutr.generate_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.NUTRITION_EP}/{section_id}/{new_content}', json=nutr.get_test_section())
    assert resp.status_code == NOT_FOUND

# @patch('data.nutrition.update_nutrition_section_content', side_effect=Exception(), autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_bad_exception_update_nutrition_section_content(mock_update):
    """
    Testing we do the right thing with an exception when updating nutrition contents.
    """
    section_id = nutr.generate_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.NUTRITION_EP}/{section_id}/{new_content}', json=nutr.get_test_section())
    assert resp.status_code == BAD_REQUEST

def test_get_ems_sections():
    resp = TEST_CLIENT.get(ep.EMS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)

@pytest.mark.skip('temporary skip (broken test)')
# @patch('data.ems.add_ems_section', return_value=ems.MOCK_ID, autospec=True)
def test_good_add_ems_section(mock_add):
    """
    Testing we do the right thing with a good return from add_ems_section.
    """
    resp = TEST_CLIENT.post(ep.EMS_EP, json=ems.get_test_section())
    assert resp.status_code == OK

@pytest.mark.skip('temporary skip (broken test)')
# @patch('data.ems.add_ems_section', side_effect=ValueError(), autospec=True)
def test_bad_add_ems_section(mock_add):
    """
    Testing we do the right thing with a value error from add_ems_section.
    """
    resp = TEST_CLIENT.post(ep.EMS_EP, json=ems.get_test_section())
    assert resp.status_code == NOT_ACCEPTABLE


@pytest.mark.skip('temporary skip (broken test)')
def test_ems_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_ems_section.
    """
    resp = TEST_CLIENT.post(ep.EMS_EP, json=ems.get_test_section())
    # assert resp.status_code == SERVICE_UNAVAILABLE
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.ems.delete_ems_section', autospec=True)
def test_good_ems_delete(mock_del):
    """
    Testing we do the right thing with a call to delete_ems_section that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_EMS_SECTION_EP}/AnyName')
    assert resp.status_code == OK


@patch('data.ems.delete_ems_section', side_effect=ValueError(), autospec=True)
def test_ems_bad_delete(mock_del):
    """
    Testing we do the right thing with a value error from delete_ems_section.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_EMS_SECTION_EP}/AnyName')
    assert resp.status_code == NOT_FOUND


@patch('data.ems.update_ems_section_content', return_value=nutr.MOCK_ID, autospec=True)
def test_good_update_ems_section_content(mock_update):
    """
    Testing we do the right thing with a good return from update_ems_section_content.
    """
    section_id = ems.generate_section_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.EMS_EP}/{section_id}/{new_content}', json=ems.get_test_section())
    assert resp.status_code == OK


# @patch('data.ems.update_ems_section_content', side_effect=ValueError(), autospec=True)
# def test_bad_value_error_update_ems_section_content(mock_update):
#     """
#     Testing we do the right thing with a value error from update_ems_section_content.
#     """
#     section_id = ems.generate_section_id()
#     new_content = "TESTING NEW CONTENT"
#     resp = TEST_CLIENT.put(f'{ep.EMS_EP}/{section_id}/{new_content}', json=ems.get_test_section())
#     assert resp.status_code == NOT_FOUND

# @patch('data.ems.update_ems_section_content', side_effect=Exception(), autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_bad_exception_update_ems_section_content(mock_update):
    """
    Testing we do the right thing with a exception from update_ems_section_content.
    """
    section_id = ems.generate_section_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.EMS_EP}/{section_id}/{new_content}', json=ems.get_test_section())
    assert resp.status_code == BAD_REQUEST

def test_get_finances_sections():
    resp = TEST_CLIENT.get(ep.FINANCES_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)

# @patch('data.finances.add_finances_section', return_value=fin.MOCK_ID, autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_good_add_finances_section(mock_add):
    """
    Testing we do the right thing with a good return from add_finances_section.
    """
    resp = TEST_CLIENT.post(ep.FINANCES_EP, json=fin.get_test_section())
    assert resp.status_code == OK


# @patch('data.finances.add_finances_section', side_effect=ValueError(), autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_bad_add_finances_section(mock_add):
    """
    Testing we do the right thing with a value error from add_finances_section.
    """
    resp = TEST_CLIENT.post(ep.FINANCES_EP, json=fin.get_test_section())
    assert resp.status_code == NOT_ACCEPTABLE


@pytest.mark.skip('temporary skip (broken test)')
def test_finances_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_finances_section.
    """
    resp = TEST_CLIENT.post(ep.FINANCES_EP, json=fin.get_test_section())
    # assert resp.status_code == SERVICE_UNAVAILABLE
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.finances.delete_finances_section', autospec=True)
def test_good_finances_delete(mock_del):
    """
    Testing we do the right thing with a call to delete_finances_section that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_FINANCES_SECTION_EP}/AnyName')
    assert resp.status_code == OK


@patch('data.finances.delete_finances_section', side_effect=ValueError(), autospec=True)
def test_finances_bad_delete(mock_del):
    """
    Testing we do the right thing with a value error from delete_finances_section.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_FINANCES_SECTION_EP}/AnyName')
    assert resp.status_code == NOT_FOUND


# @patch('data.finances.update_finance_section_content', return_value=fin.MOCK_ID, autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_good_update_finance_section_content(mock_update):
    """
    Testing we do the right thing with a good return from update_finance_section_content.
    """
    section_id = fin.generate_section_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.FINANCES_EP}/{section_id}/{new_content}', json=fin.get_test_section())
    assert resp.status_code == OK


# @patch('data.finances.update_finance_section_content', side_effect=ValueError(), autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_bad_value_error_update_finance_section_content(mock_update):
    """
    Testing we do the right thing with a value error from update_finance_section_content.
    """
    section_id = fin.generate_section_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.FINANCES_EP}/{section_id}/{new_content}', json=fin.get_test_section())
    assert resp.status_code == NOT_FOUND

# @patch('data.finances.update_finance_section_content', side_effect=Exception(), autospec=True)
@pytest.mark.skip('temporary skip (broken test)')
def test_bad_exception_update_finance_section_content(mock_update):
    """
    Testing we do the right thing with a exception from update_finance_section_content.
    """
    section_id = fin.generate_section_id()
    new_content = "TESTING NEW CONTENT"
    resp = TEST_CLIENT.put(f'{ep.FINANCES_EP}/{section_id}/{new_content}', json=fin.get_test_section())
    assert resp.status_code == BAD_REQUEST