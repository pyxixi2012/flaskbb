"""Tests for the utils/fields.py file."""
import pytest
from wtforms.form import Form
from flask_login import login_user
from flaskbb.utils.fields import BirthdayField, HiddenUsernameField


def test_birthday_field():
    class F(Form):
        birthday = BirthdayField(format='%d %m %Y')

    a = ["04 02 2015"]
    b = ["None", "None", "2015"]  # this one should fail
    c = ["None", "None", "None"]

    form = F()

    assert form.birthday.process_formdata(a) is None
    assert form.birthday.process_formdata(c) is None

    with pytest.raises(ValueError):
        form.birthday.process_formdata(b)


def test_hidden_username_field(user, application):

    class F(Form):
        username = HiddenUsernameField()

    with application.test_request_context():
        login_user(user)
        f = F()
        f.username.process_formdata(None)

    assert f.username.data == user.username
