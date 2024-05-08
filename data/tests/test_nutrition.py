import pytest

import data.nutrition as nutrition

@pytest.fixture(scope='function')
def temp_section():
    section_name = nutrition._get_test_name()
    section_id = nutrition.generate_id()
    article_ids = []
    ret = nutrition.add_section(section_name, section_id, article_ids)
    yield section_id
    if nutrition.exists(section_id):
        nutrition.delete_section(section_id)

@pytest.fixture(scope='function')
def temp_article(temp_section):
    section_id = temp_section
    article_name = "Temporary Article"
    article_id = nutrition.generate_id()
    article_content = "This is a temporary article."
    nutrition.add_article(section_id, article_name, article_id, article_content)
    yield article_id
    nutrition.delete_article(section_id, article_id)

def test_get_sections(temp_section):
    # Test get sections with a temp_section
    sections = nutrition.get_sections()

    assert isinstance(sections, dict)     # checks if sections is a dictionary

    assert len(sections) >= 0      # checks if sections is empty

    for section in sections:
        assert isinstance(section, str)
        assert isinstance(sections[section], dict)

    section_id = temp_section
    assert nutrition.exists(section_id)

def test_get_sections():
    # Test get sections
    sections = nutrition.get_sections()
    assert isinstance(sections, dict) 
    assert len(sections) >= 0 

def test_get_articles():
    # Test get articles
    section_id = "mock_section_id"
    articles = nutrition.get_articles(section_id)
    assert isinstance(articles, dict)

def test_delete_non_existing_article(temp_section, temp_article):
    # Test delete a non-existing article
    section_id = temp_section
    non_existing_article_id = nutrition.generate_id()
    result = nutrition.delete_article(section_id, non_existing_article_id)
    assert result is False


def test_get_test_name():
    # Test get test name
    name = nutrition._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_get_test_section():
    # Test get test section
    assert isinstance(nutrition.get_test_section(), dict)


def test_generate_id():
    # Test generate id
    _id = nutrition.generate_id()
    assert isinstance(_id, str)
    assert len(_id) == nutrition.ID_LEN


ADD_NAME = "New Nutrition"

def test_add_section():
    # Test add a section
    new_name = nutrition._get_test_name()
    new_section_id = nutrition.generate_id()
    new_article_id = nutrition.generate_id()
    ret = nutrition.add_section(new_name, new_section_id, new_article_id)
    assert nutrition.exists(new_section_id)
    assert isinstance(ret, bool)
    nutrition.delete_section(new_section_id)

def test_add_section_duplicate_id(temp_section):
    # Duplicate section id raises a ValueError
    new_name = nutrition._get_test_name()
    duplicate_section_id = temp_section
    duplicate_article_ids = [temp_section]
    with pytest.raises(ValueError):
        nutrition.add_section(new_name, duplicate_section_id, duplicate_article_ids)

def test_add_section_blank_id():
    # Blank section id raises a ValueError
    nutrition_name = nutrition._get_test_name()
    with pytest.raises(ValueError):
        nutrition.add_section(nutrition_name, "", [])

def test_add_article_section_fail():
    # Test unsuccessfull article section
    section_id = "non_existent_section_id" 
    article_name = "Article Name"
    article_id = nutrition.generate_id()
    article_content = ""

    with pytest.raises(ValueError) as excinfo:
        nutrition.add_article(section_id, article_name, article_id, article_content)

    assert str(excinfo.value) == f'Section not found: {section_id}'

def test_add_article_duplicate_id(temp_section):
    # Duplicate article id raises a ValueError
    new_name = nutrition._get_test_name()
    section_id = nutrition.generate_id()
    duplicate_article_id = temp_section
    new_content = ''
    with pytest.raises(ValueError):
        nutrition.add_article(new_name, section_id, duplicate_article_id, new_content)

def test_add_article_blank_id():
    # Blank article id raises a ValueError
    new_name = nutrition._get_test_name()
    section_id = nutrition.generate_id()
    new_content = ''
    with pytest.raises(ValueError):
        nutrition.add_article(new_name, section_id, "", new_content)

def test_delete_article_success(temp_section):
    # Test successful delete for a article
    section_id = temp_section
    article_name = "Article Name"
    article_id = nutrition.generate_id()
    article_content = []
    
    nutrition.add_article(section_id, article_name, article_id, article_content)

    nutrition.delete_article(section_id, article_id)

    assert not nutrition.exists_article(article_id)

def test_delete_article_fail():
    # Test unsuccessful delete of a article
        with pytest.raises(ValueError):
            nutrition.delete_article('non-existing section id',"non-existing article id")

def test_delete_section_not_there():
    # Tests delete section not there
    section_id = nutrition.generate_id()
    with pytest.raises(ValueError):
        nutrition.delete_section(section_id)
