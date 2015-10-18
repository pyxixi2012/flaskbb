from flaskbb.services.authentication import PasswordAuth
from flaskbb.exceptions import ValidationError
from collections import namedtuple
from hashlib import md5


import pytest
try:
    from unittest import mock
except ImportError:
    import mock


FakeUser = namedtuple('User', ['username', 'password'])


def hash_password(password):
    if hasattr(password, 'encode'):
        password = password.encode()
    return md5(password).hexdigest()


def password_checker(existing_password, given_password):
    return hash_password(given_password) == existing_password


class TestPasswordAuth(object):
    def test_verify_password_is_true_with_same(self):
        user = FakeUser('fred', hash_password('fred'))
        finder = mock.Mock(return_value=user)
        authenticator = PasswordAuth(password_checker, finder)

        assert authenticator.authenticate('fred', 'fred') == user

    def test_verify_password_raises_with_different(self):
        finder = mock.Mock(return_value=FakeUser('fred', 'fred'))
        authenticator = PasswordAuth(password_checker, finder)

        with pytest.raises(ValidationError) as exc:
            authenticator.authenticate('fred', 'fred')

        assert exc.value.msg == 'Bad login credentials'
