import pytest

import data.finances as fin

@pytest.fixture(scope='function')
def temp_section():
    finances_section_name = fin._get_test_name()
    finances_section_id = fin.generate_finances_section_id()
    ret = fin.add_finances_section(finances_section_name, finances_section_id, "article")
    yield finances_section_name
    if fin.exists(finances_section_name):
        fin.delete_finances_section(finances_section_name)


def test_get_finances_finances_sections(temp_section):
    finances_sections = fin.get_finances_finances_sections()

    assert isinstance(finances_sections, dict)     # checks if finances_sections is a dictionary

    assert len(finances_sections) >= 0      # checks if finances_sections is empty

    for section in finances_sections:
        assert isinstance(section, str)
        assert isinstance(finances_sections[section], dict)

    assert fin.exists(temp_section)


def test_get_test_name():
    name = fin._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_get_test_section():
    assert isinstance(fin.get_test_section(), dict)


def test_generate_finances_section_id():
    _id = fin.generate_finances_section_id()
    assert isinstance(_id, str)
    assert len(_id) == fin.ID_LEN


ADD_NAME = "New Finances Section"

def test_add_finances_section():
    # ret = fin.add_finances_section(ADD_NAME, 4)
    # assert fin.exists(ADD_NAME)
    # assert isinstance(ret, str)
    new_name = fin._get_test_name()
    new_id = fin.generate_finances_section_id()
    ret = fin.add_finances_section(new_name, new_id, "article")
    assert fin.exists(new_name)
    assert isinstance(ret, bool)
    fin.delete_finances_section(new_name)

def test_add_finances_section_duplicate_name(temp_section):
    # Duplicate section name raises a ValueError
    duplicate_name = temp_section
    finances_section_id = fin.generate_finances_section_id()
    with pytest.raises(ValueError):
        fin.add_finances_section(duplicate_name, finances_section_id, "article")

def test_add_finances_section_blank_name():
    # Blank section name raises a ValueError
    finances_section_id = fin.generate_finances_section_id()
    with pytest.raises(ValueError):
        fin.add_finances_section("", finances_section_id, "article")

def test_delete_finances_section(temp_section):
    finances_section_name = temp_section
    fin.delete_finances_section(finances_section_name)
    assert not fin.exists(finances_section_name)

def test_delete_finances_section_not_there():
    finances_section_name = fin._get_test_name()
    with pytest.raises(ValueError):
        fin.delete_finances_section(finances_section_name)
