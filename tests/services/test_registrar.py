from flaskbb.services import BasicUserRegistrar
from flaskbb.exceptions import ValidationError


from collections import namedtuple
import pytest

try:
    from unittest import mock
except ImportError:
    import mock

User = namedtuple('User', ['username', 'email', 'password'])


def validate_user(user):
    return user


def never_validates(user):
    raise ValidationError(msg='Username exists', field='username')


def user_factory(username, email, password, **kwargs):
    return User(username=username, email=email, password=password)


class TestRegistrar(object):
    def setup(self):
        self.userdata = {'username': 'fred', 'email': 'fred@fred.com',
                         'password': 'fred'}
        self.validator = mock.Mock(side_effect=validate_user)
        self.user_factory = mock.Mock(side_effect=user_factory)
        self.repository = mock.Mock()
        self.registrar = BasicUserRegistrar(
                            validator=self.validator,
                            repository=self.repository,
                            factory=self.user_factory)

    def test_creates_user_with_factory(self):
        self.registrar.register(**self.userdata)

        assert self.user_factory.call_count == 1

    def test_validates_user(self):
        self.registrar.register(**self.userdata)

        assert self.validator.call_count == 1

    def test_persists_user(self):
        self.registrar.register(**self.userdata)

        assert self.repository.persist.call_count == 1

    def test_invalid_user_doesnt_persist(self):
        self.registrar._validator = never_validates

        with pytest.raises(ValidationError):
            self.registrar.register(**self.userdata)

        assert not self.repository.call_count
