from flaskbb.services import Registrar
from flaskbb.exceptions import ValidationError


from collections import namedtuple
from functools import wraps
import pytest


User = namedtuple('User', ['username', 'email', 'password'])


def has_call_counter(func):
    @wraps(func)
    def counter(*args, **kwargs):
        counter.calls += 1
        return func(*args, **kwargs)
    counter.calls = 0
    return counter


def validate_user(user):
    return user


def never_validates(user):
    raise ValidationError(msg='Username exists', field='username')


def user_factory(username, email, password, **kwargs):
    return User(username=username, email=email, password=password)


class FakeUserRepository(object):
    def __init__(self):
        self.calls = []

    def persist(self, user):
        self.calls.append('persist')


class TestRegistrar(object):
    def setup(self):
        self.userdata = {'username': 'fred', 'email': 'fred@fred.com',
                         'password': 'fred'}
        self.validator = has_call_counter(validate_user)
        self.user_factory = has_call_counter(user_factory)
        self.repository = FakeUserRepository()
        self.registrar = Registrar(validator=self.validator,
                                   repository=self.repository,
                                   factory=self.user_factory)

    def test_creates_user_with_factory(self):
        self.registrar.register(**self.userdata)

        assert self.user_factory.calls == 1

    def test_validates_user(self):
        self.registrar.register(**self.userdata)

        assert self.validator.calls == 1

    def test_persists_user(self):
        self.registrar.register(**self.userdata)

        assert self.repository.calls == ['persist']

    def test_invalid_user_doesnt_persist(self):
        self.registrar._validator = never_validates

        with pytest.raises(ValidationError):
            self.registrar.register(**self.userdata)

        assert self.repository.calls == []
