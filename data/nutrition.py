"""
nutrition.py: the interface to our data for the cooking/nutrition category
"""
import random
import data.db_connect as dbc

NUTRITION_COLLECT = 'nutrition'  # name of collections


ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

NAME = 'name'
SECTION_ID = 'sectionID'
ARTICLE_ID = 'articleID'
# NUM_SECTIONS = "numSections"
ARTICLE = 'nutritionContent'

# TEST_CATEGORY_NAME = "Nutrition/Cooking"

# nutrition = {
#     'health': {
#         ARTICLE: "api",
#         ARTICLE: "api",
#     },
#     'cooking': {
#         ARTICLE: "api",
#     },
# }


def get_sections() -> dict:
    # return nutrition sections, by id
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, NUTRITION_COLLECT)


def get_articles(section_id: str) -> dict:
    # return nutrition articles
    dbc.connect_db()
    return dbc.fetch_all(NUTRITION_COLLECT, {SECTION_ID: section_id})


def exists(section_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(NUTRITION_COLLECT, {SECTION_ID: section_id})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_section():
    test_section = {}
    test_section[NAME] = _get_test_name()
    test_section[SECTION_ID] = generate_section_id()
    test_section[ARTICLE] = 'article'
    return test_section


def generate_section_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id


def add_section(section_name: str, section_id: str) -> bool:
    if exists(section_id):
        raise ValueError(f'Duplicate section id: {section_id=}')
    if not section_id:
        raise ValueError("Nutrition id cannot be blank!")

    # section_id = generate_section_id()
    # return section_id

    section = {}
    section[NAME] = section_name
    section[SECTION_ID] = section_id
    dbc.connect_db()
    _id = dbc.insert_one(NUTRITION_COLLECT, section)
    return _id is not None


def delete_section(section_id: str):
    # check if the section to delete is in the database
    if exists(section_id):
        return dbc.del_one(NUTRITION_COLLECT, {SECTION_ID: section_id})
    else:
        raise ValueError(f'Delete failure: {section_id} not in database.')


def update_nutrition_section_content(section_id: str,
                                     new_content: str) -> bool:
    if exists(section_id):
        # the article content
        article = {}
        article[ARTICLE] = new_content

        # update existing section with new article content
        filter_query = {SECTION_ID: section_id}
        update_query = {'$set': article}

        dbc.connect_db()
        _id = dbc.update_one(NUTRITION_COLLECT, filter_query, update_query)

        # check if the update was successful
        return _id is not None
    else:
        raise ValueError(f'Update failed: {section_id} not in database.')


def add_article(article_name: str,
                article_id: str,
                article_content: str) -> bool:
    if exists(article_id):
        raise ValueError(f'Duplicate section id: {article_id=}')
    if not article_id:
        raise ValueError("Nutrition id cannot be blank!")

    # section_id = generate_section_id()
    # return section_id

    article = {}
    article[NAME] = article_name
    article[ARTICLE_ID] = article_id
    article[ARTICLE] = article_content
    dbc.connect_db()
    _id = dbc.insert_one(NUTRITION_COLLECT, article)
    return _id is not None

# def main():
#     print(get_sections())


# if __name__ == '__main__':
#     main()
