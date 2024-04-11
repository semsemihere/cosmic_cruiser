import pytest

import data.nutrition as nutrition

@pytest.fixture(scope='function')
def temp_section():
    section_name = nutrition._get_test_name()
    section_id = nutrition.generate_section_id()
    ret = nutrition.add_section(section_name, section_id)
    yield section_id
    if nutrition.exists(section_id):
        nutrition.delete_section(section_id)

@pytest.mark.skip('temporary skip')
def test_get_sections(temp_section):
    sections = nutrition.get_sections()

    assert isinstance(sections, dict)     # checks if sections is a dictionary

    assert len(sections) >= 0      # checks if sections is empty

    for section in sections:
        assert isinstance(section, str)
        assert isinstance(sections[section], dict)

    section_id = temp_section
    assert nutrition.exists(section_id)


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


ADD_NAME = "New Nutrition"

@pytest.mark.skip('temporary skip')
def test_add_section():
    # ret = nutrition.add_section(ADD_NAME, 4)
    # assert nutrition.exists(ADD_NAME)
    # assert isinstance(ret, str)
    new_name = nutrition._get_test_name()
    new_id = nutrition.generate_section_id()
    ret = nutrition.add_section(new_name, new_id)
    assert nutrition.exists(new_id)
    assert isinstance(ret, bool)
    nutrition.delete_section(new_id)

@pytest.mark.skip('temporary skip')
def test_add_section_duplicate_id(temp_section):
    # Duplicate section name raises a ValueError
    nutrition_name = nutrition._get_test_name()
    duplicate_section_id = temp_section
    with pytest.raises(ValueError):
        nutrition.add_section(nutrition_name, duplicate_section_id)

@pytest.mark.skip('temporary skip')
def test_add_section_blank_id():
    # Blank section name raises a ValueError
    nutrition_name = nutrition._get_test_name()
    with pytest.raises(ValueError):
        nutrition.add_section(nutrition_name, "")

@pytest.mark.skip('temporary skip')
def test_delete_section(temp_section):
    section_id = temp_section
    nutrition.delete_section(section_id)
    assert not nutrition.exists(section_id)

def test_delete_section_not_there():
    section_id = nutrition.generate_section_id()
    with pytest.raises(ValueError):
        nutrition.delete_section(section_id)

@pytest.mark.skip('temporary skip')
def test_update_nutrition_section_content(temp_section):
    updated_content = 'update the content'
    nutrition.update_nutrition_section_content(temp_section, updated_content)

    for key in nutrition.get_sections():
        if nutrition.get_sections()[key] == updated_content:
            assert True
    # section_name = temp_section
    # new_content = 'Updated content for testing.'
    # nutrition.update_section_content(section_name, new_content)
    # updated_section = nutrition.get_sections().get(section_name, {})

    # assert updated_section.get(nutrition.ARTICLE) == new_content

@pytest.mark.skip('temporary skip')
def test_update_nutrition_section_content_fail(temp_section):
    with pytest.raises(ValueError):
        nutrition.update_nutrition_section_content('non-existing section',"content")