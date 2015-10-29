# -*- coding: utf-8 -*-
"""
    flaskbb.boundaries.authentication
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Authentication boundaries for FlaskBB

    :copyright: 2015 (c) by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""


from ..exceptions import ValidationError


class AuthenticationBoundary(object):
    """Boundary interface for Authentication. Implementers should receive some
    authenticator that can call the authentication_succeeded or authentication_failed
    based on the success of the authentication.
    """
    def authentication_succeeded(self, user, *args, **kwargs):
        raise NotImplementedError

    def authentication_failed(self, error, *args, **kwargs):
        raise NotImplementedError


class AuthenticatorBridge(object):
    """Default implementation of bridge between Authenticator objects and
    AuthenticationBoundary objects. Attempts to validate user and signals
    results appropriately to its listener.
    """
    def __init__(self, authenticator, listener):
        self._authenticator = authenticator
        self._listener = listener

    def authenticate(self, *args, **kwargs):
        try:
            user = self._authenticator.authenticate(*args, **kwargs)
        except ValidationError as e:
            return self._listener.authentication_failed(e, *args, **kwargs)
        else:
            return self._listener.authentication_succeeded(user, *args, **kwargs)
