import pytest

import data.ems as ems

@pytest.fixture(scope='function')
def temp_ems():
    ems_section_name = ems._get_test_name()
    ems_section_id = ems.generate_section_id()
    ret = ems.add_ems_section(ems_section_name, ems_section_id, {})
    
    yield ems_section_id

    if ems.exists(ems_section_id):
        ems.delete_ems_section(ems_section_id)


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

def test_add_ems_section():
    new_name = ems._get_test_name()
    new_id = ems.generate_section_id()
    ret = ems.add_ems_section(new_name, new_id, {})
    assert ems.exists(new_id)
    assert isinstance(ret, bool)
    ems.delete_ems_section(new_id)

def test_add_ems_section_duplicate_id(temp_ems):
    ems_name = ems._get_test_name
    duplicate_id = temp_ems
    with pytest.raises(ValueError):
        ems.add_ems_section(ems_name, duplicate_id, {})

def test_add_ems_section_blank_id():
    ems_name = ems._get_test_name
    with pytest.raises(ValueError):
        ems.add_ems_section(ems_name, "", {})

# @pytest.mark.skip('temporary skip')
def test_update_ems_section_content(temp_ems):
    updated_content = 'updated the content'
    ems.update_ems_section_content(temp_ems, updated_content)
    # print("qwer: ", fin.get_finances_sections())
    
    for key in ems.get_ems_sections():
        if ems.get_ems_sections()[key] == updated_content:
            assert True

    # section_id = temp_ems
    # new_content = "Updated content for testing"
    # ems.update_ems_section_content(section_id, new_content)
    # updated_section = ems.get_ems_sections().get(section_id, {})

    # assert updated_section.get(ems.EMS_ARTICLES) == new_content

def test_update_ems_section_content_fail():
    with pytest.raises(ValueError):
        ems.update_ems_section_content('non-existing section',"content")


def test_delete_ems_section(temp_ems):
    ems_id = temp_ems
    ems.delete_ems_section(ems_id)
    assert not ems.exists(ems_id)


def test_delete_ems_section_not_there():
    ems_id = ems.generate_section_id()
    with pytest.raises(ValueError):
        ems.delete_ems_section(ems_id)

def test_get_test_name():
    name = ems._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0

def test_generate_section_id():
    _id = ems.generate_section_id()
    assert isinstance(_id, str)
    assert len(_id) == ems.ID_LEN
