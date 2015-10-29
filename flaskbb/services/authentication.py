# -*- coding: utf-8 -*-
"""
    flaskbb.services.authentication
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Authentication services for FlaskBB

    :copyright: (c) 2015 by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""

from ..exceptions import ValidationError
from ..utils.helpers import with_metaclass
from abc import ABCMeta, abstractmethod


class Authenticator(with_metaclass(ABCMeta, object)):
    """Generic interface for Authenticators to implement.
    The contract for Authenticators is they must either return some user object
    or raise a flaskbb.exceptions.ValidationError if the user cannot be authenticated
    """
    @abstractmethod
    def authenticate(self, *args, **kwargs):
        pass


class PasswordAuth(Authenticator):
    """Handles password based authentication

    :param checker callable: Callable to check password
    :param finder callable: Callable to locate the presumed user,
        receives the login attribute and is expected to return a User
    """
    def __init__(self, checker, finder):
        self._checker = checker
        self._finder = finder

    def authenticate(self, login, password, *args, **kwargs):
        user = self._finder(login)
        if not user or not self._checker(user.password, password):
            raise ValidationError('Bad login credentials')
        return user
