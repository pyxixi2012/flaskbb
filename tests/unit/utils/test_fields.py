"""Tests for the utils/fields.py file."""
import pytest
from wtforms.form import Form
from flaskbb.utils.fields import BirthdayField
from datetime import date


class TestForm(Form):
    birthday = BirthdayField(format='%d %m %Y')


@pytest.mark.parametrize('date, expected', [
    (["23 01 1989"], date(1989, 1, 23)),
    (["04", "04", "2015"], date(2015, 4, 4)),
    (["29", "02", "2004"], date(2004, 2, 29))
])
def test_birthday_field_with_good(date, expected):
    f = TestForm()
    f.birthday.process_formdata(date)

    assert f.birthday.data == expected


def test_birthday_field_with_all_none():
    f = TestForm()
    f.birthday.process_formdata(["None"]*3)

    assert f.birthday.data is None


@pytest.mark.parametrize('date', [
    ["None", "None", "2015"],
    ["1989 01 23"], ["29", "02", "2013"]
])
def test_birthday_with_bad_data(date):
    f = TestForm()

    with pytest.raises(ValueError) as excinfo:
        f.birthday.process_formdata(date)

    assert str(excinfo.value) == "Not a valid date value"
