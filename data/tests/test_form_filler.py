from unittest.mock import patch

import data.form_filler as ff



def test_get_fld_names():
    ret = ff.get_fld_names(ff.TEST_FLD_DESCRIPS)
    assert isinstance(ret, list)
    assert ff.TEST_FLD in ret


def test_get_form_descr():
    ret = ff.get_form_descr(ff.TEST_FLD_DESCRIPS)
    assert isinstance(ret, dict)
    assert ff.TEST_FLD in ret


def test_get_form_descr_with_choices():
    # list of field descriptions with choices
    field_descriptions = [
        {
            ff.FLD_NM: 'Field1',
            ff.QSTN: 'Question 1',
            ff.PARAM_TYPE: ff.QUERY_STR,
            ff.CHOICES: ['Choice1', 'Choice2', 'Choice3']
        },
        {
            ff.FLD_NM: 'Field2',
            ff.QSTN: 'Question 2',
            ff.PARAM_TYPE: ff.QUERY_STR,
            ff.CHOICES: ['Yes', 'No']
        }
    ]

    form_descr = ff.get_form_descr(field_descriptions)

    assert 'Field1' in form_descr
    assert 'Field2' in form_descr
    assert form_descr['Field1'] == 'Question 1\nChoices: [\'Choice1\', \'Choice2\', \'Choice3\']'
    assert form_descr['Field2'] == 'Question 2\nChoices: [\'Yes\', \'No\']'


def test_get_query_fld_names():
    # list of field descriptions
    field_descriptions = [
        {ff.FLD_NM: 'Field1', ff.PARAM_TYPE: ff.QUERY_STR},
        {ff.FLD_NM: 'Field2', ff.PARAM_TYPE: ff.QUERY_STR},
        {ff.FLD_NM: 'Field3', ff.PARAM_TYPE: ff.PATH},  # Not QUERY_STR
        {ff.FLD_NM: 'Field4', ff.PARAM_TYPE: ff.QUERY_STR}
    ]
    # call finction
    query_field_names = ff.get_query_fld_names(field_descriptions)
    #  check if return list
    assert isinstance(query_field_names, list)
    # chekf fields
    assert 'Field1' in query_field_names
    assert 'Field2' in query_field_names
    assert 'Field3' not in query_field_names
    assert 'Field4' in query_field_names


# @patch('data.form_filler.get_input', return_value='Y')
# def test_form(mock_get_input):
#     assert isinstance(ff.form(ff.TEST_FLD_DESCRIPS), dict)

@patch('builtins.input', return_value='User input')
def test_get_input(mock_input):
    # call get_input function with some input
    user_input = ff.get_input('Default text', '(Optional)', 'Enter your input:')
    # check if correct arguments
    mock_input.assert_called_once_with('Default text(Optional)Enter your input: ')
    # check if return value matches patched input value
    assert user_input == 'User input'
    


def test_form_with_default():
    field_descriptions = [
        {ff.FLD_NM: 'Field1', ff.QSTN: 'Enter value for Field1:', ff.DEFAULT: 'DefaultValue'}
    ]
    ff.get_input = lambda dflt, opt, qstn: 'InputValue'
    result = ff.form(field_descriptions)
    assert result['Field1'] == 'InputValue'


def test_form_without_default():
    field_descriptions = [
        {ff.FLD_NM: 'Field2', ff.QSTN: 'Enter value for Field2:'}
    ]

    ff.get_input = lambda dflt, opt, qstn: 'InputValue'
    result = ff.form(field_descriptions)
    assert result['Field2'] == 'InputValue'


def test_optional_flag_present():
    fld_descrips = [{ff.FLD_NM: 'Field1', ff.OPT: True}]
    result = ff.form(fld_descrips)
    assert any(ff.OPT in fld for fld in fld_descrips)

def test_set_default_value():
    fld_descrips = [{ff.FLD_NM: 'Field1', ff.DEFAULT: 'DefaultValue'}]    
    result = ff.form(fld_descrips)
    assert result['Field1'] == 'DefaultValue'

def test_typecast_to_int():
    fld_descrips = [{ff.FLD_NM: 'Field1', ff.TYPECAST: ff.INT, ff.QSTN: 'Enter an integer value:'}]
    ff.get_input = lambda dflt, opt, qstn: '123'
    result = ff.form(fld_descrips)
    assert 'Field1' in result
    assert isinstance(result['Field1'], int)
