"""
Tests for form.py.
"""
import data.form as fm
import io
import sys
from unittest.mock import patch


def test_get_form():
    form = fm.get_form()
    assert isinstance(form, list)
    assert len(form) > 0
    for fld in form:
        # Every field must have a name!
        assert fm.FLD_NM in fld
        # And it can't be blank.
        assert len(fld[fm.FLD_NM]) > 0


def test_get_form_descr():
    assert isinstance(fm.get_form_descr(), dict)


def test_get_fld_names():
    assert isinstance(fm.get_fld_names(), list)

# def test_main():
#     # redirect stdout to a StringIO object
#     captured_output = io.StringIO()
#     sys.stdout = captured_output
#     # call main function
#     fm.main()
#     # printed output
#     printed_output = captured_output.getvalue()
#     # reset stdout
#     sys.stdout = sys.__stdout__
#     assert "Form:" in printed_output
#     assert "get_form_descr()=" in printed_output


# def test_main(capsys):
#     fm.main()
#     captured = capsys.readouterr()
#     assert "Form:" in captured.out
#     assert "get_form_descr()=" in captured.out
