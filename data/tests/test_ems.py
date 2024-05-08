import pytest

import data.ems as ems

@pytest.fixture(scope='function')
def temp_ems():
    ems_section_name = ems._get_test_name()
    ems_section_id = ems.generate_id()
    article_id = ems.generate_id()
    ret = ems.add_section(ems_section_name, ems_section_id, [])
    
    yield ems_section_id

    if ems.exists(ems_section_id):
        ems.delete_ems_section(ems_section_id)

def test_get_articles(temp_ems):
    ems_section_id = temp_ems
    res = ems.get_articles(ems_section_id)
    assert isinstance(res, dict)

def test_get_ems_sections(temp_ems):
    ems_sections = ems.get_ems_sections()
    
    assert isinstance(ems_sections, dict)

    assert len(ems_sections) >= 0

    for section in ems_sections:
        assert isinstance(section, str)
        assert isinstance(ems_sections[section], dict)

    ems_section_id = temp_ems
    assert ems.exists(ems_section_id)

def test_get_test_section():
    assert isinstance(ems.get_test_section(), dict)

ADD_NAME = "New EMS"

def test_add_section():
    new_name = ems._get_test_name()
    new_section_id = ems.generate_id()
    ret = ems.add_section(new_name, new_section_id, [])
    assert ems.exists(new_section_id)
    assert isinstance(ret, bool)
    ems.delete_ems_section(new_section_id)

def test_add_section_duplicate_id(temp_ems):
    # Duplicate section name raises a ValueError
    new_name = ems._get_test_name()
    duplicate_section_id = temp_ems
    duplicate_article_ids = [temp_ems]
    with pytest.raises(ValueError):
        ems.add_section(new_name, duplicate_section_id, duplicate_article_ids)

def test_add_ems_section_blank_id():
    ems_name = ems._get_test_name
    with pytest.raises(ValueError):
        ems.add_section(ems_name, "", {})

def test_add_article_success(temp_ems):
    ems_section_name = temp_ems
    ems_section_id = temp_ems
    article_id = ems.generate_id()
    new_content = 'content'
    ems.add_article(ems_section_id, ems_section_name, article_id, new_content)
    assert ems.exists(ems_section_id)

def test_add_article_duplicate_id(temp_ems):
    # Duplicate section name raises a ValueError
    new_name = ems._get_test_name()
    section_id = ems.generate_id()
    duplicate_article_id = temp_ems
    new_content = ''
    with pytest.raises(ValueError):
        ems.add_article(new_name, section_id, duplicate_article_id, new_content)

def test_add_article_blank_id():
    # Duplicate section name raises a ValueError
    new_name = ems._get_test_name()
    section_id = ems.generate_id()
    new_content = ''
    with pytest.raises(ValueError):
        ems.add_article(new_name, section_id, "", new_content)

def test_add_article_section_fail():
    section_id = "non_existent_section_id" 
    article_name = "Article Name"
    article_id = ems.generate_id()
    article_content = ""

    with pytest.raises(ValueError) as excinfo:
        ems.add_article(section_id, article_name, article_id, article_content)

    assert str(excinfo.value) == f'Section not found: {section_id}'

def test_update_ems_section_content(temp_ems):
    updated_content = 'updated the content'
    ems.update_ems_section_content(temp_ems, updated_content)
    
    for key in ems.get_ems_sections():
        if ems.get_ems_sections()[key] == updated_content:
            assert True


def test_update_ems_section_content_fail():
    with pytest.raises(ValueError):
        ems.update_ems_section_content('non-existing section',"content")


def test_delete_ems_section(temp_ems):
    ems_id = temp_ems
    ems.delete_ems_section(ems_id)
    assert not ems.exists(ems_id)


def test_delete_ems_section_not_there():
    ems_id = ems.generate_id()
    with pytest.raises(ValueError):
        ems.delete_ems_section(ems_id)

def test_get_test_name():
    name = ems._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_generate_id():
    _id = ems.generate_id()
    assert isinstance(_id, str)
    assert len(_id) == ems.ID_LEN

def test_delete_article_success(temp_ems):
    section_id = temp_ems
    article_name = "Article Name"
    article_id = ems.generate_id()
    article_content = ""
    
    ems.add_article(section_id, article_name, article_id, article_content)

    ems.delete_article(section_id, article_id)

    assert not ems.exists_article(article_id)

def test_delete_article_fail_invalid_section_id(temp_ems):
    article_id = temp_ems
    with pytest.raises(ValueError):
        ems.delete_article('non-existing section id',article_id)

def test_delete_article_fail_invalid_article_id(temp_ems):
    section_id = temp_ems
    with pytest.raises(ValueError):
        ems.delete_article(section_id,"non-existing article id")

# def test_delete_section(temp_ems):
#     section_id = temp_ems
#     ems.delete_article(section_id)
#     assert not ems.exists(section_id)

# def test_delete_section_not_there():
#     section_id = ems.generate_id()
#     with pytest.raises(ValueError):
#         ems.delete_article(section_id)