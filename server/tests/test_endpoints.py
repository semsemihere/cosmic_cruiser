
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
    UNAUTHORIZED,
    OK,
    SERVICE_UNAVAILABLE,
    CREATED
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
    id = usrs.create_user("test@gmail.com",
                          USERNAME,
                          PASSWORD,
                          "Test",
                          "Test",
                          1111111111)
    if id:
        yield USERNAME

    if(USERNAME in usrs.get_all_users()):
        usrs.delete_user(USERNAME)


@pytest.fixture
def create_nutrition_section():
    TEST_CLIENT.post(ep.NUTRITION_EP,
                     json={"name": nutr.TEST_SECITON_NAME,
                           "sectionID": nutr.TEST_SECITON_ID,
                           "arrayOfArticleIDs": []})
    yield nutr.TEST_SECITON_ID
    TEST_CLIENT.delete(ep.NUTRITION_EP + "/delete/" 
                       + nutr.TEST_SECITON_ID)
    

@pytest.fixture
def create_ems_section():
    TEST_CLIENT.post(ep.EMS_EP,
                     json={"name": ems.TEST_SECITON_NAME,
                           "sectionID": ems.TEST_SECITON_ID,
                           "arrayOfArticleIDs": []})
    yield ems.TEST_SECITON_ID
    TEST_CLIENT.delete(ep.EMS_EP + "/delete/" + ems.TEST_SECITON_ID)
    

@pytest.fixture
def create_finances_section():
    TEST_CLIENT.post(ep.FINANCES_EP,
                     json={"name": fin.TEST_SECITON_NAME,
                           "sectionID": fin.TEST_SECITON_ID,
                           "arrayOfArticleIDs": []})
    yield fin.TEST_SECITON_ID
    TEST_CLIENT.delete(ep.FINANCES_EP + "/delete/" + fin.TEST_SECITON_ID)
    

def test_login():
    resp = TEST_CLIENT.get(ep.LOGIN_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    resp_json = str(resp_json)[:15]
    assert ep.LOGIN_RESP in resp_json


def test_get_article():
    resp = TEST_CLIENT.get('/categories/get_article/web scrapping')
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    resp_json = str(resp_json)
    assert ep.GET_ARTICLE_RESP in resp_json



def test_login_post(create_test_user):
    resp = TEST_CLIENT.post(ep.LOGIN_EP,
                            json={usrs.EMAIL:"test@gmail.com",
                                  usrs.USERNAME: USERNAME,
                                  usrs.PASSWORD:PASSWORD})
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert resp.status_code ==  OK


def test_bad_login_post():
    resp = TEST_CLIENT.post(ep.LOGIN_EP,
                            json={usrs.EMAIL:"test@gmail.com",
                                  usrs.USERNAME: BAD_USERNAME,
                                  usrs.PASSWORD:BAD_PASSWORD})
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    resp_json = resp.get_json()
    print(resp_json)
    assert resp.status_code ==  UNAUTHORIZED


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
    assert resp_json["Available endpoints"] == sorted(
        rule.rule for rule in ep.api.app.url_map.iter_rules())


def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert resp_json[ep.DATA] == usrs.get_all_users()


# def test_main_menu():
#     resp = TEST_CLIENT.get(ep.MAIN_MENU_EP)
#     resp_json = resp.get_json()
#     print(resp_json)
#     assert isinstance(resp_json, dict)
#     assert resp_json[ep.TITLE] == ep.MAIN_MENU_NM


# def test_user_menu():
#     resp = TEST_CLIENT.get(ep.USER_MENU_EP)
#     resp_json = resp.get_json()
#     print(resp_json)
#     assert isinstance(resp_json, dict)
#     assert resp_json[ep.TITLE] == ep.USER_MENU_NM


def test_bad_user_delete(create_test_user):
    username = create_test_user
    usrs.delete_user(username)
    resp = TEST_CLIENT.delete(ep.DEL_USERS_EP+'/'+username)
    resp_json = resp.get_json()
    print(resp_json)
    assert resp.status_code == NOT_FOUND


def test_user_delete(create_test_user):
    username = create_test_user
    resp = TEST_CLIENT.delete(ep.DEL_USERS_EP+'/'+username)
    resp_json = resp.get_json()
    print(resp_json)
    assert resp_json[username] == 'Deleted'


@patch('data.users.create_user', side_effect=ValueError(), autospec=True)
def test_post_bad_user(mock_post):
    resp = TEST_CLIENT.post(ep.USERS_EP,
                            json={usrs.EMAIL:"test@gmail.com",
                                  usrs.USERNAME: USERNAME,
                                  usrs.PASSWORD:PASSWORD,
                                  usrs.FIRSTNAME:"test",
                                  usrs.LASTNAME:"test",
                                  usrs.PHONE:1111111111})
    assert resp.status_code == NOT_ACCEPTABLE

    
@patch('data.users.create_user', return_value=USERNAME, autospec=True)
def test_post_user(mock_post):
    resp = TEST_CLIENT.post(ep.USERS_EP,
                            json={usrs.EMAIL:"test@gmail.com",
                                  usrs.USERNAME: USERNAME,
                                  usrs.PASSWORD:PASSWORD,
                                  usrs.FIRSTNAME:"test",
                                  usrs.LASTNAME:"test",
                                  usrs.PHONE:1111111111})
    assert resp.status_code == OK


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


@patch('data.categories.delete_category', side_effect=ValueError(),
       autospec=True)
def test_category_bad_delete(mock_del):
    """
    Testing we do the right thing with a value error from del_category.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_CATEGORY_EP}/AnyName')
    assert resp.status_code == NOT_FOUND


@patch('data.categories.add_category', return_value=categ.MOCK_ID,
       autospec=True)
def test_category_add(mock_add):
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categ.get_test_category())
    assert resp.status_code == OK


@patch('data.categories.add_category', side_effect=ValueError(),
       autospec=True)
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


@patch('data.categories.update_category_name',
       return_value=categ.MOCK_ID, autospec=True)
def test_good_update_category_name(mock_update):
    """
    Testing successful category name update
    """
    category_id = categ.generate_category_id()
    new_category_name = "NEW CATEGORY NAME"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_NAME_EP}/{category_id}/{new_category_name}',
                           json=categ.get_test_category())
    assert resp.status_code == OK


@patch('data.categories.update_category_name',
       side_effect=ValueError(), autospec=True)
def test_bad_value_error_update_category_name(mock_update):
    """
    Testing bad value error category name update
    """
    category_id = categ.generate_category_id()
    new_category_name = "NEW CATEGORY NAME"
    resp = TEST_CLIENT.put(f'{ep.UPDATE_CATEGORY_NAME_EP}/{category_id}/{new_category_name}',
                           json=categ.get_test_category())
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

    
def test_get_nutrition_sections(create_nutrition_section):
    resp = TEST_CLIENT.get(ep.NUTRITION_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_add_nutrition_article(create_nutrition_section):
    section_id = create_nutrition_section
    resp = TEST_CLIENT.post(f'{ep.NUTRITION_EP}/{section_id }/articles', json={"articleName": nutr.TEST_ARTICLE_NAME, "articleID": nutr.TEST_ARTICLE_ID, "articleContent": nutr.TEST_ARTICLE_CONTENT})
    TEST_CLIENT.delete(f'{ep.NUTRITION_EP}/delete/{section_id}/{nutr.TEST_ARTICLE_ID}')
    assert resp.status_code == 201

    
def test_add_bad_nutrition_article(create_nutrition_section):
    section_id = create_nutrition_section + " BAD"
    resp = TEST_CLIENT.post(f'{ep.NUTRITION_EP}/{section_id }/articles', json={"articleName": nutr.TEST_ARTICLE_NAME, "articleID": nutr.TEST_ARTICLE_ID, "articleContent": nutr.TEST_ARTICLE_CONTENT})
    assert resp.status_code == 406

    
def test_del_nutrition_article(create_nutrition_section):
    section_id = create_nutrition_section
    TEST_CLIENT.post(f'{ep.NUTRITION_EP}/{section_id}/articles', json={"articleName": nutr.TEST_ARTICLE_NAME, "articleID": nutr.TEST_ARTICLE_ID, "articleContent": nutr.TEST_ARTICLE_CONTENT})
    resp = TEST_CLIENT.delete(f'{ep.NUTRITION_EP}/delete/{section_id}/{nutr.TEST_ARTICLE_ID}')
    assert resp.status_code == 200

    
def test_get_nutrition_article(create_nutrition_section):
    section_id = create_nutrition_section
    TEST_CLIENT.post(f'{ep.NUTRITION_EP}/{section_id }/articles', json={"articleName": nutr.TEST_ARTICLE_NAME, "articleID": nutr.TEST_ARTICLE_ID, "articleContent": nutr.TEST_ARTICLE_CONTENT})
    resp = TEST_CLIENT.get(f'{ep.NUTRITION_EP}/{section_id}/articles/{nutr.TEST_ARTICLE_ID}')
    TEST_CLIENT.delete(f'{ep.NUTRITION_EP}/delete/{section_id}/{nutr.TEST_ARTICLE_ID}')
    assert resp.status_code == 200


def test_get_bad_nutrition_article(create_nutrition_section):
    section_id = create_nutrition_section
    resp = TEST_CLIENT.get(f'{ep.NUTRITION_EP}/{section_id}/articles/{nutr.TEST_ARTICLE_ID}')
    assert resp.status_code == 200
    

def test_bad_del_nutrition_article(create_nutrition_section):
    resp = TEST_CLIENT.delete(f'{ep.NUTRITION_EP}/delete/{create_nutrition_section}212312312312425235/{nutr.TEST_ARTICLE_ID}')
    print(resp)
    print(resp.get_json)
    assert resp.status_code == 404
    

def test_get_nutrition_articles(create_nutrition_section):
    resp = TEST_CLIENT.get(f'{ep.NUTRITION_EP}/{create_nutrition_section}/articles')
    print(resp)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    

def test_add_bad_nutrition_section():
    resp = TEST_CLIENT.post(ep.NUTRITION_EP, json={"name": "", "sectionID": "", "arrayOfArticleIDs": []})
    print(resp)
    assert resp.status_code == 406


def test_add_nutrition_section():
    try:
        TEST_CLIENT.delete(ep.NUTRITION_EP + "/delete/TEST_ONLY")
    except Exception as e:
        print(e)
    resp = TEST_CLIENT.post(ep.NUTRITION_EP, json={"name": "TEST_ONLY", "sectionID": "TEST_ONLY", "arrayOfArticleIDs": []})
    print(resp)
    delete_resp = TEST_CLIENT.delete(ep.NUTRITION_EP + "/delete/TEST_ONLY")
    print(delete_resp)
    assert resp.status_code == OK


def test_delete_nutrition_section():
    resp = TEST_CLIENT.post(ep.NUTRITION_EP, json={"name": "TEST_ONLY", "sectionID": "TEST_ONLY", "arrayOfArticleIDs": []})
    print(resp)
    delete_resp = TEST_CLIENT.delete(ep.NUTRITION_EP + "/delete/TEST_ONLY")
    print(delete_resp)
    assert delete_resp.status_code == OK


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
    

def test_get_ems_sections():
    resp = TEST_CLIENT.get(ep.EMS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    
    
def test_add_ems_article(create_ems_section):
    section_id = create_ems_section
    resp = TEST_CLIENT.post(f'{ep.EMS_EP}/{section_id}/articles', json={"articleName": ems.TEST_ARTICLE_NAME, "articleID": ems.TEST_ARTICLE_ID, "articleContent": ems.TEST_ARTICLE_CONTENT})
    TEST_CLIENT.delete(f'{ep.EMS_EP}/delete/{section_id}/{ems.TEST_ARTICLE_ID}')
    assert resp.status_code == CREATED


def test_add_bad_ems_article(create_ems_section):
    section_id = create_ems_section + " BAD"
    resp = TEST_CLIENT.post(f'{ep.EMS_EP}/{section_id}/articles', json={"articleName": ems.TEST_ARTICLE_NAME, "articleID": ems.TEST_ARTICLE_ID, "articleContent": ems.TEST_ARTICLE_CONTENT})
    assert resp.status_code == 406


def test_add_bad_ems_section():
    resp = TEST_CLIENT.post(ep.EMS_EP, json={"name": "", "sectionID": "", "arrayOfArticleIDs": []})
    print(resp)
    assert resp.status_code == 406


def test_add_ems_section():
    try:
        TEST_CLIENT.delete(ep.EMS_EP + "/delete/TEST_ONLY")
    except Exception as e:
        print(e)
    resp = TEST_CLIENT.post(ep.EMS_EP, json={"name": "TEST_ONLY", "sectionID": "TEST_ONLY", "arrayOfArticleIDs": []})
    print(resp)
    delete_resp = TEST_CLIENT.delete(ep.EMS_EP + "/delete/TEST_ONLY")
    print(delete_resp)
    assert resp.status_code == OK

    
def test_get_ems_article(create_ems_section):
    resp = TEST_CLIENT.get(f'{ep.EMS_EP}/{create_ems_section}/articles')
    print(resp)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)

    
def test_del_ems_article(create_ems_section):
    section_id = create_ems_section
    TEST_CLIENT.post(f'{ep.EMS_EP}/{section_id}/articles', json={"articleName": ems.TEST_ARTICLE_NAME, "articleID": ems.TEST_ARTICLE_ID, "articleContent": ems.TEST_ARTICLE_CONTENT})
    resp = TEST_CLIENT.delete(f'{ep.EMS_EP}/delete/{section_id}/{ems.TEST_ARTICLE_ID}')
    assert resp.status_code == 200


def test_bad_del_ems_article(create_ems_section):
    resp = TEST_CLIENT.delete(f'{ep.EMS_EP}/delete/{create_ems_section}/{ems.TEST_ARTICLE_ID}234232342')
    print(resp)
    print(resp.get_json)
    assert resp.status_code == 404
    

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


def test_get_finances_sections():
    resp = TEST_CLIENT.get(ep.FINANCES_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_add_finances_section():
    try:
        TEST_CLIENT.delete(ep.FINANCES_EP + "/delete/TEST_ONLY")
    except Exception as e:
        print(e)
    resp = TEST_CLIENT.post(ep.FINANCES_EP, json={"name": "TEST_ONLY", "sectionID": "TEST_ONLY", "arrayOfArticleIDs": []})
    print(resp)
    delete_resp = TEST_CLIENT.delete(ep.FINANCES_EP + "/delete/TEST_ONLY")
    print(delete_resp)
    assert resp.status_code == OK


def test_add_bad_finances_section():
    resp = TEST_CLIENT.post(ep.FINANCES_EP, json={"name": "", "sectionID": "", "arrayOfArticleIDs": []})
    assert resp.status_code == NOT_ACCEPTABLE


def test_get_finances_article(create_finances_section):
    resp = TEST_CLIENT.get(f'{ep.FINANCES_EP}/{create_finances_section}/articles')
    print(resp)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


def test_add_finances_article(create_finances_section):
    section_id = create_finances_section
    resp = TEST_CLIENT.post(f'{ep.FINANCES_EP}/{section_id}/articles', json={"articleName": fin.TEST_ARTICLE_NAME, "articleID": fin.TEST_ARTICLE_ID, "articleContent": fin.TEST_ARTICLE_CONTENT})
    TEST_CLIENT.delete(f'{ep.FINANCES_EP}/delete/{section_id}/{fin.TEST_ARTICLE_ID}')
    assert resp.status_code == CREATED
    

def test_add_bad_finances_article(create_finances_section):
    section_id = create_finances_section + " BAD"
    resp = TEST_CLIENT.post(f'{ep.FINANCES_EP}/{section_id}/articles', json={"articleName": fin.TEST_ARTICLE_NAME, "articleID": fin.TEST_ARTICLE_ID, "articleContent": fin.TEST_ARTICLE_CONTENT})
    assert resp.status_code == 406

    
def test_del_finances_article(create_finances_section):
    section_id = create_finances_section
    TEST_CLIENT.post(f'{ep.FINANCES_EP}/{section_id}/articles', json={"articleName": fin.TEST_ARTICLE_NAME, "articleID": fin.TEST_ARTICLE_ID, "articleContent": fin.TEST_ARTICLE_CONTENT})
    resp = TEST_CLIENT.delete(f'{ep.FINANCES_EP}/delete/{section_id}/{fin.TEST_ARTICLE_ID}')
    assert resp.status_code == 200

    
def test_bad_del_finances_article(create_finances_section):
    resp = TEST_CLIENT.delete(f'{ep.FINANCES_EP}/delete/{create_finances_section}/{fin.TEST_ARTICLE_ID}234232342')
    print(resp)
    print(resp.get_json)
    assert resp.status_code == 404


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
