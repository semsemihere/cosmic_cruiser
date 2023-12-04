import pytest

import data.ems as ems

@pytest.fixture(scope='function')
def temp_ems():
    ems_section_name = ems._get_test_name()
    ems_section_id = ems.generate_section_id()
    ret = ems.add_ems_section(ems_section_name, ems_section_id, {})
    
    yield ems_section_name

    if ems.exists(ems_section_id):
        ems.delete_ems_section(ems_section_id)


def test_get_ems_sections(temp_ems):
    ems_sections = ems.get_ems_sections()

    assert isinstance(ems_sections, dict)

    assert len(ems_sections) >= 0

    # for section in ems_sections:
    #     print(section)
