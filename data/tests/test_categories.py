import pytest

import data.categories as categ


@pytest.fixture(scope='function')
def temp_category():
    category_name = categ._get_test_name()
    ret = categ.create_category(category_name, 0)
    yield category_name
    if categ.exists(category_name):
        categ.delete_category(category_name)


def test_get_categories():
    categories = categ.get_categories()

    assert isinstance(categories, dict)     # checks if categories is a dictionary

    assert len(categories) > 0      # checks if categories is empty

    for category in categories:
        assert isinstance(category, str)
        assert isinstance(categories[category], dict)

    assert categ.TEST_CATEGORY_NAME in categories

# def test_get_games():
#     games = gms.get_games()
#     assert isinstance(games, dict)
#     assert len(games) > 0
#     for game in games:
#         assert isinstance(game, str)
#         assert isinstance(games[game], dict)
#     assert gms.TEST_GAME_NAME in games


def test_get_test_name():
    name = categ._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_get_test_category():
    assert isinstance(categ.get_test_category(), dict)

def test_delete_category(temp_category):
    category_name = temp_category
    categ.delete_category(category_name)
    assert not categ.exists(category_name)
