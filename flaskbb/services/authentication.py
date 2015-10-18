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
    """
    def __init__(self, checker, finder):
        self._checker = checker
        self._finder = finder

    def authenticate(self, username_or_email, password):
        user = self._finder(username_or_email)
        if not self._checker(user.password, password):
            raise ValidationError('Bad login credentials')
        return user
