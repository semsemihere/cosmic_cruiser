"""
finances.py: the interface to our data for the finances category
"""
import random
import data.db_connect as dbc

FINANCES_COLLECT = 'finances'  # name of collections


ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

SECTION_NAME = 'name'
SECTION_ID = 'sectionID'
ARTICLE_NAME = 'articleName'
ARTICLE_ID = 'articleID'
ARTICLE_IDS = 'arrayOfArticleIDs'
ARTICLE_CONTENT = 'articleContent'
# ARTICLE_IDS = {'':''}

# TEST_CATEGORY_SECTION_NAME = "Nutrition/Cooking"

# finances = {
#     'section1': {
#        'title': 'title',
#        'content': 'content',
#     },
#     'tax': {
#         'title': "What is Tax",
#         'content': "Tax is very interesting",
#     },
# }


def get_finances_sections() -> dict:
    # return finances sections, by name
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SECTION_ID, FINANCES_COLLECT)


def exists(section_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(FINANCES_COLLECT, {SECTION_ID: section_id})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_section():
    test_section = {}
    test_section[SECTION_NAME] = _get_test_name()
    test_section[SECTION_ID] = generate_section_id()
    test_section[ARTICLE_IDS] = {}
    return test_section


def generate_section_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id


def add_finances_section(section_name: str, section_id: str,
                         section_article: list) -> bool:
    if exists(section_id):
        raise ValueError(f'Duplicate section name: {section_id=}')
    if not section_id:
        raise ValueError("Finance ID cannot be blank!")

    # section_id = generate_section_id()
    # return section_id

    section = {}
    section[SECTION_NAME] = section_name
    section[SECTION_ID] = section_id
    section[ARTICLE_IDS] = section_article
    dbc.connect_db()
    _id = dbc.insert_one(FINANCES_COLLECT, section)
    return _id is not None

# def get_finance_section_article(finance_section:
# str, finance_section_id: str):
#     if exists(finance_section_id):
#         dbc.connect_db()
#         return dbc.fetch_one(FINANCES_COLLECT,
#               {SECTION_ID: section_id})
#     else:
#         raise ValueError(f'Update failed:
# {finance_section_id} not in db.')


def update_finance_section_article(finance_section: str,
                                   finance_section_id: str,
                                   article_title: str,
                                   article_content: str) -> bool:
    if exists(finance_section_id):
        # article = {}
        # article[ARTICLE_IDS] = new_content
        print("asdfaasfd")
        dbc.connect_db()
        db = dbc.fetch_all_as_dict(SECTION_NAME, FINANCES_COLLECT)
        article = db[finance_section][ARTICLE_IDS]
        print("before addign", article)
        article[article_title] = article_content
        print("after adding ", article)

        filter_query = {SECTION_ID: finance_section_id}
        update_query = {'$set': {ARTICLE_IDS: article}}

        _id = dbc.update_one(FINANCES_COLLECT, filter_query, update_query)
        return _id is not None
    else:
        raise ValueError(f'Update failed: {finance_section_id} not in db.')


def delete_finances_section(section_id: str):
    # Deletes finances section by id
    if exists(section_id):
        return dbc.del_section(section_id,
                               SECTION_ID,
                               ARTICLE_ID,
                               FINANCES_COLLECT)
    else:
        raise ValueError(f'Delete failure: {section_id} not in database.')


# def exists(section_name: str) -> bool:
#     return section_name in get_finances_sections()


# def main():
#     print(get_finances_sections())


# if __name__ == '__main__':
#     main()
