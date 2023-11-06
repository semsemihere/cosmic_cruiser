"""
categories.py: the interface to our categories data.
"""
import random

ID_LEN = 24
BIG_NUM = 100000000000000000000

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