"""
ems.py: the interface to our emergency services data.
"""
import random
import data.db_connect as dbc

EMS_COLLECT = 'ems'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

EMS_SECTION_NAME = 'emsName'
EMS_SECTION_ID = 'emsID'
EMS_ARTICLES = 'emsArticle'

ems_sections = {}


def get_ems_sections() -> dict:
    # return all ems sections
    dbc.connect_db()
    return dbc.fetch_all_as_dict(EMS_SECTION_NAME, EMS_COLLECT)


def add_ems_section(ems_section_name: str, ems_section_id: str,
                    ems_articles: dict) -> bool:
    if exists(ems_section_id):
        raise ValueError(f'Duplicate EMS section: {ems_section_id=}')
    if not ems_section_id:
        raise ValueError("EMS section ID cannot be blank!")

    ems_section = {}
    ems_section[EMS_SECTION_NAME] = ems_section_name
    ems_section[EMS_SECTION_ID] = ems_section_id
    ems_section[EMS_ARTICLES] = ems_articles

    dbc.connect_db()
    _id = dbc.insert_one(EMS_COLLECT, ems_section)
    return _id is not None


def update_ems_section_content(ems_section_id: str, new_content: str) -> bool:
    if exists(ems_section_id):
        article = {}
        article[EMS_ARTICLES] = new_content

        filter_query = {EMS_SECTION_ID: ems_section_id}
        update_query = {'$set': article}

        dbc.connect_db()
        _id = dbc.update_one(EMS_COLLECT, filter_query, update_query)
        return _id is not None
    else:
        raise ValueError(f'Update failed: {ems_section_id} not in database.')


def delete_ems_section(ems_section_id: str):
    # Deletes EMS section by id
    if exists(ems_section_id):
        return dbc.del_one(EMS_COLLECT, {EMS_SECTION_ID: ems_section_id})
    else:
        raise ValueError(f'Delete failure: {ems_section_id} not in database.')


def exists(section_id: str) -> bool:
    # Checks ems section by id
    dbc.connect_db()
    return dbc.fetch_one(EMS_COLLECT, {EMS_SECTION_ID: section_id})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def generate_section_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id
