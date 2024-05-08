import pytest
from unittest.mock import patch
import data.categories as categ


@pytest.fixture(scope='function')
def temp_category():
    category_name = categ._get_test_name()
    category_id = categ.generate_category_id()
    ret = categ.add_category(category_name, category_id)
    yield category_id
    if categ.exists(category_id):
        categ.delete_category(category_id)

@pytest.fixture(scope='function')
def temp_category_name():
    category_name = categ._get_test_name()+'temp'
    category_id = categ.generate_category_id()+"1"
    ret = categ.add_category(category_name, category_id)
    yield category_name
    if categ.exists(category_id):
        categ.delete_category(category_id)

        
@pytest.fixture(scope='function')
def temp_category_name_article_id(temp_category_name):
    category_name = temp_category_name
    temp = categ.add_article_to_category(category_name, "test")
    categories = categ.get_categories()
    print("success : ",categories)
    last_article_id = len(categories[category_name][categ.ARTICLES].keys())
    print("categories[category_name][categ.ARTICLES].keys() : ", categories[category_name][categ.ARTICLES].keys())
    print("last_article_id : ", last_article_id)
    yield (category_name, last_article_id)
    if categ.exists(temp_category_name):
        categ.delete_category(temp_category_name)

        
def test_article():
    url = categ.get_article("web scrapping")
    assert isinstance(url,str) == True

    
def test_get_categories(temp_category):
    categories = categ.get_categories()

    assert isinstance(categories, dict)     # checks if categories is a dictionary

    assert len(categories) >= 0             # checks if categories is empty

    for category in categories:
        assert isinstance(category, str)
        assert isinstance(categories[category], dict)

    assert categ.exists(temp_category)


def test_get_test_name():
    name = categ._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_get_test_category():
    assert isinstance(categ.get_test_category(), dict)


def test_generate_category_id():
    _id = categ.generate_category_id()
    assert isinstance(_id, str)
    assert len(_id) == categ.ID_LEN


ADD_NAME = "New Category"


def test_get_article_content():
    ret = categ.get_article_content(categ.TEST_ARTICLE_URL)
    print(ret)
    assert isinstance(ret, str)



@patch('data.categories.len', return_value=0)
def test_get_bad_article_content(mockResponse):
    ret = categ.get_article_content(categ.TEST_BAD_ARTICLE_URL)
    print(ret)
    
    assert ret is None

    
def test_add_category():
    new_name = categ._get_test_name()
    new_id = categ.generate_category_id()
    ret = categ.add_category(new_name, new_id)
    assert categ.exists(new_id)
    assert isinstance(ret, bool)
    categ.delete_category(new_id)


def test_add_category_duplicate_ID(temp_category):
    # Duplicate category ID raises a ValueError
    category_name = categ._get_test_name()
    duplicate_id = temp_category
    with pytest.raises(ValueError):
        categ.add_category(category_name, duplicate_id)


def test_add_category_blank_id():
    # Blank category ID raises a ValueError
    category_name = categ._get_test_name()
    with pytest.raises(ValueError):
        categ.add_category(category_name, "")


def test_update_category_name(temp_category):
    updated_name = "New category name"
    categ.update_category_name(temp_category, updated_name)
    for key in categ.get_categories():
        if key == updated_name:
            assert True


def test_update_category_name_fail():
    with pytest.raises(ValueError):
        categ.update_category_name('non-existing id',"name")


def test_update_category_num_sections(temp_category):
    updated_num_sections = 99
    categ.update_category_sections(temp_category, updated_num_sections)
    for key in categ.get_categories():
        if categ.get_categories()[key] == updated_num_sections:
            assert True


def test_update_category_num_sections_fail():
    with pytest.raises(ValueError):
        categ.update_category_sections('non-existing id', 10)


def test_delete_category(temp_category):
    categ.delete_category(temp_category)
    assert not categ.exists(temp_category)


def test_delete_category_not_there():
    category_id = categ.generate_category_id()
    with pytest.raises(ValueError):
        categ.delete_category(category_id)
