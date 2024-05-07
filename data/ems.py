"""
ems.py: the interface to our emergency services data.
"""
import random
import data.db_connect as dbc

EMS_COLLECT = 'ems'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

SECTION_NAME = 'name'
SECTION_ID = 'sectionID'
ARTICLE_NAME = 'articleName'
ARTICLE_ID = 'articleID'
ARTICLE_IDS = 'arrayOfArticleIDs'
ARTICLE_CONTENT = 'articleContent'


def get_ems_sections() -> dict:
    # return all ems sections
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SECTION_NAME, EMS_COLLECT)


def get_test_section():
    test_section = {}
    test_section[SECTION_NAME] = _get_test_name()
    test_section[SECTION_ID] = generate_section_id()
    test_section[ARTICLE_IDS] = 'article'
    return test_section


def add_section(section_name: str, section_id: str, article_ids: list) -> bool:
    if exists(section_id):
        raise ValueError(f'Duplicate section id: {section_id=}')
    if not section_id:
        raise ValueError("Nutrition id cannot be blank!")

    # section_id = generate_section_id()
    # return section_id

    section = {}
    section[SECTION_NAME] = section_name
    section[SECTION_ID] = section_id
    section[ARTICLE_IDS] = article_ids
    dbc.connect_db()
    _id = dbc.insert_one(EMS_COLLECT, section)
    return _id is not None


def update_ems_section_content(ems_section_id: str, new_content: str) -> bool:
    if exists(ems_section_id):
        article = {}
        article[ARTICLE_IDS] = new_content

        filter_query = {SECTION_ID: ems_section_id}
        update_query = {'$set': article}

        dbc.connect_db()
        _id = dbc.update_one(EMS_COLLECT, filter_query, update_query)
        return _id is not None
    else:
        raise ValueError(f'Update failed: {ems_section_id} not in database.')


def delete_ems_section(ems_section_id: str):
    # Deletes EMS section by id
    if exists(ems_section_id):
        return dbc.del_one(EMS_COLLECT, {SECTION_ID: ems_section_id})
    else:
        raise ValueError(f'Delete failure: {ems_section_id} not in database.')


def exists(section_id: str) -> bool:
    # Checks ems section by id
    dbc.connect_db()
    return dbc.fetch_one(EMS_COLLECT, {SECTION_ID: section_id})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def generate_section_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id
