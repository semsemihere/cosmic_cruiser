"""
categories.py: the interface to our categories data.
"""
import random
import data.db_connect as dbc

CATEGORIES_COLLECT = 'categories'


ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

NAME = 'name'
CATEGORY_ID = 'categoryID'
NUM_SECTIONS = "numSections"

TEST_CATEGORY_NAME = "Nutrition/Cooking"

categories = {}

# categories = {
#     'Emergency Services/Resources': {
#         NUM_SECTIONS: 3,
#     },
#     'Financial Literacy': {
#         NUM_SECTIONS: 4,
#     },
#     TEST_CATEGORY_NAME: {
#         NUM_SECTIONS: 5,
#     },
# }


def get_categories() -> dict:
    # return categories
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, CATEGORIES_COLLECT)


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(CATEGORIES_COLLECT, {NAME: name})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_category():
    test_category = {}
    test_category[NAME] = _get_test_name()
    test_category[CATEGORY_ID] = generate_category_id()
    test_category[NUM_SECTIONS] = 0
    return test_category


def generate_category_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id


def add_category(category_name: str, category_id: str,
                 num_sections: int) -> bool:
    if exists(category_name):
        raise ValueError(f'Duplicate category name: {category_name=}')
    if not category_name:
        raise ValueError("Category name cannot be blank!")

    # categories[category_name] = {NUM_SECTIONS: num_sections}
    # category_id = generate_category_id()
    # return category_id

    category = {}
    category[NAME] = category_name
    category[CATEGORY_ID] = category_id
    category[NUM_SECTIONS] = num_sections
    dbc.connect_db()
    _id = dbc.insert_one(CATEGORIES_COLLECT, category)
    return _id is not None


def delete_category(category_name: str):
    # check if the category to delete is in the database
    if exists(category_name):
        # del categories[category_name]
        # dbc.del_one(CATEGORIES_COLLECT, {NAME: category_name})
        return dbc.del_one(CATEGORIES_COLLECT, {NAME: category_name})
    else:
        raise ValueError(f'Delete failure: {category_name} not in database.')


# def exists(category_name: str) -> bool:
#     return category_name in get_categories()


# def main():
#     print(get_categories())


# if __name__ == '__main__':
#     main()
