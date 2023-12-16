import pytest

import data.nutrition as nutrition

@pytest.fixture(scope='function')
def temp_section():
    section_name = nutrition._get_test_name()
    section_id = nutrition.generate_section_id()
    ret = nutrition.add_section(section_name, section_id, "article")
    yield section_name
    if nutrition.exists(section_name):
        nutrition.delete_section(section_name)


def test_get_sections(temp_section):
    sections = nutrition.get_sections()

    assert isinstance(sections, dict)     # checks if sections is a dictionary

    assert len(sections) >= 0      # checks if sections is empty

    for section in sections:
        assert isinstance(section, str)
        assert isinstance(sections[section], dict)

    assert nutrition.exists(temp_section)


def test_get_test_name():
    name = nutrition._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_get_test_section():
    assert isinstance(nutrition.get_test_section(), dict)


def test_generate_section_id():
    _id = nutrition.generate_section_id()
    assert isinstance(_id, str)
    assert len(_id) == nutrition.ID_LEN


ADD_NAME = "New Section"

def test_add_section():
    # ret = nutrition.add_section(ADD_NAME, 4)
    # assert nutrition.exists(ADD_NAME)
    # assert isinstance(ret, str)
    new_name = nutrition._get_test_name()
    new_id = nutrition.generate_section_id()
    ret = nutrition.add_section(new_name, new_id, "article")
    assert nutrition.exists(new_name)
    assert isinstance(ret, bool)
    nutrition.delete_section(new_name)

def test_add_section_duplicate_name(temp_section):
    # Duplicate section name raises a ValueError
    duplicate_name = temp_section
    section_id = nutrition.generate_section_id()
    with pytest.raises(ValueError):
        nutrition.add_section(duplicate_name, section_id, "article")

def test_add_section_blank_name():
    # Blank section name raises a ValueError
    section_id = nutrition.generate_section_id()
    with pytest.raises(ValueError):
        nutrition.add_section("", section_id, "article")

def test_delete_section(temp_section):
    section_name = temp_section
    nutrition.delete_section(section_name)
    assert not nutrition.exists(section_name)

def test_delete_section_not_there():
    section_name = nutrition._get_test_name()
    with pytest.raises(ValueError):
        nutrition.delete_section(section_name)

def test_update_section_content(temp_section):
    section_name = temp_section
    new_content = 'Updated content for testing.'
    nutrition.update_section_content(section_name, new_content)
    updated_section = nutrition.get_sections().get(section_name, {})

    assert updated_section.get(nutrition.ARTICLE) == new_content
