"""
categories.py: the interface to our categories data.
"""
import random

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

NAME = 'name'

NUM_SECTIONS = "numSections"
TEST_CATEGORY_NAME = "Nutrition/Cooking"
categories = {
    'Emergency Services/Resources': {
        NUM_SECTIONS: 3,
    },
    'Financial Literacy': {
        NUM_SECTIONS: 4,
    },
    TEST_CATEGORY_NAME: {
        NUM_SECTIONS: 5,
    },
}


def get_categories() -> dict:
    return categories


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_category():
    test_category = {}
    test_category[NAME] = _get_test_name()
    test_category[NUM_SECTIONS] = 0
    return test_category


def generate_category_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id


def create_category(category_name: str, num_sections: int) -> str:
    if category_name in categories:
        raise ValueError(f'Duplicate category name: {category_name=}')
    if not category_name:
        raise ValueError("Category name cannot be blank!")

    categories[category_name] = {NUM_SECTIONS: num_sections}
    category_id = generate_category_id()
    return category_id


def delete_category(category_name: str):
    # check if the category to delete is in the database
    if category_name in categories:
        del categories[category_name]
    else:
        raise ValueError(f'Delete failure: {category_name} not in database.')


def exists(category_name: str) -> bool:
    return category_name in get_categories()
