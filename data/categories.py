"""
categories.py: the interface to our categories data.
"""
# import random

ID_LEN = 24
BIG_NUM = 100000000000000000000

MOCK_ID = '0' * ID_LEN

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
