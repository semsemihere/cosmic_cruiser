"""
nutrition.py: the interface to our data for the cooking/nutrition category
"""
import random
import data.db_connect as dbc

NUTRITION_COLLECT = 'nutrition'  # name of collections


ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

SECTION_NAME = 'name'
SECTION_ID = 'sectionID'
ARTICLE_NAME = 'articleName'
ARTICLE_ID = 'articleID'
# NUM_SECTIONS = "numSections"
ARTICLE_IDS = 'arrayOfArticleIDs'
ARTICLE_CONTENT = 'articleContent'
TEST_SECITON_ID = 'TEST ONLY'
TEST_SECITON_NAME = 'TEST ONLY'
TEST_ARTICLE_NAME = 'TEST ARTICLE ONLY'
TEST_ARTICLE_ID = 'TEST ARTICLE ONLY'
TEST_ARTICLE_CONTENT = 'TESTING CONTENT'
# TEST_CATEGORY_NAME = "Nutrition/Cooking"

# nutrition = {
#     'health': {
#         ARTICLE: "api",
#     },
#     'cooking': {
#         ARTICLE: "api",
#     },
# }


def get_sections() -> dict:
    # return nutrition sections, by id
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SECTION_ID, NUTRITION_COLLECT)


def get_articles(nutrition_section_id: str) -> dict:
    # return nutrition articles
    dbc.connect_db()
    return dbc.fetch_articles_by_section(nutrition_section_id,
                                         SECTION_ID,
                                         ARTICLE_ID,
                                         NUTRITION_COLLECT)


def exists(section_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(NUTRITION_COLLECT, {SECTION_ID: section_id})


def exists_article(article_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(NUTRITION_COLLECT, {ARTICLE_ID: article_id})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_section():
    test_section = {}
    test_section[SECTION_NAME] = _get_test_name()
    test_section[SECTION_ID] = generate_id()
    test_section[ARTICLE_IDS] = 'article'
    return test_section


def generate_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id


def add_section(section_name: str, section_id: str, article_ids: list) -> bool:
    if exists(section_id):
        raise ValueError(f'Duplicate section id: {section_id=}')
    if not section_id:
        raise ValueError("Nutrition id cannot be blank!")

    # section_id = generate_id()
    # return section_id

    section = {}
    section[SECTION_NAME] = section_name
    section[SECTION_ID] = section_id
    section[ARTICLE_IDS] = article_ids
    dbc.connect_db()
    _id = dbc.insert_one(NUTRITION_COLLECT, section)
    return _id is not None


def delete_section(section_id: str):
    # check if the section to delete is in the database
    if exists(section_id):
        return dbc.del_section(section_id,
                               SECTION_ID,
                               ARTICLE_ID,
                               NUTRITION_COLLECT)
    else:
        raise ValueError(f'Delete failure: {section_id} not in database.')


def delete_article(section_id: str, article_id: str):
    # check if article exists
    if exists(section_id):
        if exists_article(article_id):
            return dbc.del_article(section_id,
                                   article_id,
                                   SECTION_ID,
                                   ARTICLE_ID,
                                   ARTICLE_IDS,
                                   NUTRITION_COLLECT)
    else:
        raise ValueError(f'Delete failure: {article_id} not in database.')


def add_article(section_id: str,
                article_name: str,
                article_id: str,
                article_content: str) -> bool:
    if exists(article_id):
        raise ValueError(f'Duplicate section id: {article_id=}')
    if not article_id:
        raise ValueError("Nutrition id cannot be blank!")

    # section_id = generate_id()
    # return section_id

    article = {}
    article[ARTICLE_NAME] = article_name
    article[ARTICLE_ID] = article_id
    article[ARTICLE_CONTENT] = article_content

    dbc.connect_db()
    section_doc = dbc.fetch_one(NUTRITION_COLLECT, {SECTION_ID: section_id})

    if section_doc:
        dbc.update_one(NUTRITION_COLLECT,
                       {SECTION_ID: section_id},
                       {"$push": {ARTICLE_IDS: article_id}})
    else:
        raise ValueError(f'Section not found: {section_id}')

    _id = dbc.insert_one(NUTRITION_COLLECT, article)

    return _id is not None
