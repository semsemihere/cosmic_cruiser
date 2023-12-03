import pytest

import data.categories as categ


@pytest.fixture(scope='function')
def temp_category():
    category_name = categ._get_test_name()
    category_id = categ.generate_category_id()
    ret = categ.add_category(category_name, category_id, 0)
    yield category_name
    if categ.exists(category_name):
        categ.delete_category(category_name)


def test_get_categories(temp_category):
    categories = categ.get_categories()

    assert isinstance(categories, dict)     # checks if categories is a dictionary

    assert len(categories) >= 0      # checks if categories is empty

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

def test_add_category():
    # ret = categ.add_category(ADD_NAME, 4)
    # assert categ.exists(ADD_NAME)
    # assert isinstance(ret, str)
    new_name = categ._get_test_name()
    new_id = categ.generate_category_id()
    ret = categ.add_category(new_name, new_id, 4)
    assert categ.exists(new_name)
    assert isinstance(ret, bool)
    categ.delete_category(new_name)

def test_add_category_duplicate_name(temp_category):
    # Duplicate category name raises a ValueError
    duplicate_name = temp_category
    category_id = categ.generate_category_id()
    with pytest.raises(ValueError):
        categ.add_category(duplicate_name, category_id, 4)

def test_add_category_blank_name():
    # Blank category name raises a ValueError
    category_id = categ.generate_category_id()
    with pytest.raises(ValueError):
        categ.add_category("", category_id, 4)

def test_delete_category(temp_category):
    category_name = temp_category
    categ.delete_category(category_name)
    assert not categ.exists(category_name)

def test_delete_category_not_there():
    category_name = categ._get_test_name()
    with pytest.raises(ValueError):
        categ.delete_category(category_name)
