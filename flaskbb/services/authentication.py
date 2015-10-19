# -*- coding: utf-8 -*-
"""
    flaskbb.services.authentication
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Authentication services for FlaskBB

    :copyright: (c) 2015 by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""

from ..exceptions import ValidationError


class PasswordAuth(object):
    """Handles password based authentication

    :param checker callable: Callable to check password
    :param finder callable: Callable to locate the presumed user,
        receives the login attribute and is expected to return a User
    """
    def __init__(self, checker, finder):
        self._checker = checker
        self._finder = finder

    def authenticate(self, login, password, **kwargs):
        user = self._finder(login)
        if not self._checker(user.password, password):
            raise ValidationError('Bad login credentials')
        return user


class AfterAuth(object):
    """Class matching Authenicate's protocol to provide handling
    for any post-authentication behavior.

    :param authenticator Authenicator: Object to delegate authentication to
    :param after callable: Callable to handle post-authentication,
        receives the retrieved user and all keyword arguments passed to it
    """
    def __init__(self, authenticator, after):
        self._authenticator = authenticator
        self._after = after

    def authenticate(self, **kwargs):
        user = self._authenticator.authenticate(**kwargs)
        self._after(user, **kwargs)
        return user
