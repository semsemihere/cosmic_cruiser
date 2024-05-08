"""
categories.py: the interface to our categories data.
"""
import random
import data.db_connect as dbc
import requests
import json
from bs4 import BeautifulSoup


CATEGORIES_COLLECT = 'categories'


ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN
ARTICLE_NAME = "articleName"
NAME = 'name'
CATEGORY_ID = 'categoryID'
NUM_SECTIONS = "numSections"
ARTICLES = "articles"

TEST_ARTICLE_URL = "https://en.wikipedia.org/wiki/Test"

TEST_BAD_ARTICLE_URL = "https://en.wikipedia.org/wiki/Test234124124312"

TEST_CATEGORY_NAME = "Nutrition/Cooking"
TEST_BAD_URL_RESP = "Other reasons this message may be displayed:"


categories = {}

# categories = {
#     'Emergency Services/Resources': {
#         articles: [(title,url),(title2,url2)]
#     },
#     'Financial Literacy': {
#         NUM_SECTIONS: 4,
#     },
#     TEST_CATEGORY_NAME: {
#         NUM_SECTIONS: 5,
#     },
# }


def get_article(article_name: str):
    language_code = 'en'
    number_of_results = 1

    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': article_name, 'limit': number_of_results}
    response = requests.get(url, params=parameters)
    response = json.loads(response.text)
    # display_title, article_description = "", ""
    for page in response['pages']:
        # display_title = page['title']

        article_url = 'https://'
        article_url += language_code
        article_url += '.wikipedia.org/wiki/'
        article_url += str(page['key'])
    return article_url


def get_article_content(article_url: str):
    page = requests.get(article_url)
    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    list(soup.children)
    all = soup.find_all('p')
    res = ""
    paragraph = 0

    for i in range(len(all)):
        if all[i].get_text().strip() and paragraph < 3:
            print(all[i].get_text().strip())
            res += all[i].get_text().strip()
            paragraph += 1
    return res
    # return None


def get_categories() -> dict:
    # return categories
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, CATEGORIES_COLLECT)


def exists(category_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(CATEGORIES_COLLECT, {CATEGORY_ID: category_id})


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


# def add_article_to_category(category_id: str,
#                             article_name: str) -> bool:
#     categories = get_categories()
#     if category_id in categories:
#         articleId = str(len(categories[category_id][ARTICLES].keys())+1)
#         articleDict = {articleId: {"name": article_name,
#                                    "url": get_article(article_name)}}
#         dbc.connect_db()
#         dbc.insert_deep(CATEGORIES_COLLECT,
#         category_id, ARTICLES, articleDict)
#         return True
#     else:
#         return False


# def delete_article_from_category(category_id: str,
#                                  article_id: str) -> bool:
#     if exists(category_id):
#         dbc.connect_db()
#         dbc.del_one
#         return True
#     else:
#         return False


def add_category(category_name: str, category_id: str,
                 num_sections: int) -> bool:
    if exists(category_id):
        raise ValueError(f'Duplicate category ID: {category_id=}')
    if not category_id:
        raise ValueError("Category ID cannot be blank!")

    # categories[category_name] = {NUM_SECTIONS: num_sections}
    # category_id = generate_category_id()
    # return category_id

    category = {}
    category[NAME] = category_name
    category[CATEGORY_ID] = category_id
    category[NUM_SECTIONS] = num_sections
    category[ARTICLES] = {}
    dbc.connect_db()
    _id = dbc.insert_one(CATEGORIES_COLLECT, category)
    return _id is not None


def update_category_name(category_id: str, new_category_name: str) -> bool:
    if exists(category_id):
        category = {}
        category[NAME] = new_category_name

        filter_query = {CATEGORY_ID: category_id}
        update_query = {'$set': category}

        dbc.connect_db()
        _id = dbc.update_one(CATEGORIES_COLLECT, filter_query, update_query)
        return _id is not None
    else:
        raise ValueError(f'Update failed: {category_id} not in database.')


def update_category_sections(category_id: str,
                             updated_num_sections: str) -> bool:
    if exists(category_id):
        category = {}
        category[NUM_SECTIONS] = int(updated_num_sections)

        filter_query = {CATEGORY_ID: category_id}
        update_query = {'$set': category}

        dbc.connect_db()
        _id = dbc.update_one(CATEGORIES_COLLECT, filter_query, update_query)
        return _id is not None
    else:
        raise ValueError(f'Update failed: {category_id} not in database.')


def delete_category(category_id: str):
    # check if the category to delete is in the database
    if exists(category_id):
        # del categories[category_name]
        # dbc.del_one(CATEGORIES_COLLECT, {NAME: category_name})
        return dbc.del_one(CATEGORIES_COLLECT, {CATEGORY_ID: category_id})
    else:
        raise ValueError(f'Delete failure: {category_id} not in database.')


# def exists(category_name: str) -> bool:
#     return category_name in get_categories()


# def main():
#     print(get_categories())


# if __name__ == '__main__':
#     main()
