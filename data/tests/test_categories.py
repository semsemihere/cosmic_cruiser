import pytest

import data.categories as categ


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