from flaskbb import validators
from flaskbb.exceptions import ValidationError
from collections import namedtuple


try:
    from unittest import mock
except ImportError:
    import mock

import pytest

FakeUser = namedtuple('User', ['username', 'email', 'password'])


class TestUserValidators(object):
    def test_is_username_free_raises_with_existing(self):
        repository = mock.Mock()
        repository.find_by_username.return_value = True
        checker = validators.user.is_username_free(repository)
        new_user = FakeUser('fred', 'fred@fred.com', 'fredpassword')

        with pytest.raises(ValidationError) as ex:
            checker(new_user)

        assert ex.value.msg == 'Username in use already' and ex.value.field == 'username'

    def test_is_username_free_happy_path(self):
        repository = mock.Mock()
        repository.find_by_username.return_value = False
        checker = validators.user.is_username_free(repository)
        new_user = FakeUser('fred', 'fred@fred.com', 'fredpassword')

        assert checker(new_user)

    def test_is_email_free_raises_with_existing(self):
        repository = mock.Mock()
        repository.find_by_email.return_value = True
        checker = validators.user.is_email_free(repository)
        new_user = FakeUser('fred', 'fred@fred.com', 'fredpassword')

        with pytest.raises(ValidationError) as ex:
            checker(new_user)

        assert ex.value.msg == 'Email in use already' and ex.value.field == 'email'

    def test_is_email_free_happy_path(self):
        repository = mock.Mock()
        repository.find_by_email.return_value = False
        checker = validators.user.is_email_free(repository)
        new_user = FakeUser('fred', 'fred@fred.com', 'fredpassword')

        assert checker(new_user)


class TestValidatorHelpers(object):
    def setup(self):
        self.generous_validator = lambda: True
        self.stingy_validator = lambda: False

    def test_validate_many_with_one_passing(self):
        checker = validators.helpers.validate_many(self.generous_validator)
        assert checker()

    def test_validate_many_with_one_failing(self):
        checker = validators.helpers.validate_many(self.stingy_validator)
        assert not checker()

    def test_validate_many_with_mixed_validators(self):
        checker = validators.helpers.validate_many(self.generous_validator,
                                                   self.stingy_validator)
        assert not checker()
