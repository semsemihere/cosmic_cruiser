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
# NUM_SECTIONS = "numSections"
CONTENT = 'nutritionContent'

# TEST_CATEGORY_NAME = "Nutrition/Cooking"

# nutrition = {
#     'health': {
#         CONTENT: "api",
#     },
#     'cooking': {
#         CONTENT: "api",
#     },
# }


def get_nutrition() -> dict:
    # return nutrition, by name
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, NUTRITION_COLLECT)


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(NUTRITION_COLLECT, {NAME: name})


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_section():
    test_section = {}
    test_section[NAME] = _get_test_name()
    test_section[SECTION_ID] = generate_section_id()
    test_section[CONTENT] = 'content'
    return test_section


def generate_section_id() -> str:
    # generates a 24 digit id with leading 0's
    _id = str(random.randint(0, BIG_NUM)).rjust(ID_LEN, "0")
    return _id


def add_section(section_name: str, section_id: str,
                section_content: str) -> bool:
    if exists(section_name):
        raise ValueError(f'Duplicate section name: {section_name=}')
    if not section_name:
        raise ValueError("Category name cannot be blank!")

    # section_id = generate_section_id()
    # return section_id

    section = {}
    section[NAME] = section_name
    section[SECTION_ID] = section_id
    section[CONTENT] = section_content
    dbc.connect_db()
    _id = dbc.insert_one(NUTRITION_COLLECT, section)
    return _id is not None


def delete_section(section_name: str):
    # check if the section to delete is in the database
    if exists(section_name):
        # del nutrition[section_name]
        # dbc.del_one(NUTRITION_COLLECT, {NAME: section_name})
        return dbc.del_one(NUTRITION_COLLECT, {NAME: section_name})
    else:
        raise ValueError(f'Delete failure: {section_name} not in database.')


# def exists(section_name: str) -> bool:
#     return section_name in get_nutrition()


def main():
    print(get_nutrition())


if __name__ == '__main__':
    main()
