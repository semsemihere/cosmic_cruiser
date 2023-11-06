"""
categories.py: the interface to our categories data.
"""
# import random

ID_LEN = 24
BIG_NUM = 100000000000000000000

MOCK_ID = '0' * ID_LEN

NUM_SECTIONS = "numSections"

categories = {
    'Emergency Services/Resources': {
        NUM_SECTIONS: 3,
    },
    'Financial Literacy': {
        NUM_SECTIONS: 4,
    },
    'Nutrition/Cooking': {
        NUM_SECTIONS: 5,
    },
}


def get_categories() -> dict:
    return categories
