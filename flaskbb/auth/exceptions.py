# -*- coding: utf-8 -*-
"""
    flaskbb.auth.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~

    Authentication and Registration based
    exceptions in FlaskBB

    :copyright: (c) 2017 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from ..exceptions import AuthenticationError, FlaskBBError

class UserDoesntExist(AuthenticationError):
    pass


class InvalidPassword(AuthenticationError):
    pass


class RegistrationFailure(FlaskBBError):
    pass


class DuplicateUser(RegistrationFailure):
    pass
