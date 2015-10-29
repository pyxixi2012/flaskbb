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


class AfterAuth(AuthenticationBoundary):
    """Implements AuthenticationBoundary to perform some side-effect
    after a successful or failed Authentication. This allows for pieces to
    be easily glued together, such as performing a login or updating a
    failed authentication count.

    :param listener AuthenticationBoundary: The next listener in the chain
    :param success callable: Callable to invoke after a successful authentication,
        must accept a user object as well as any *args and **kwargs passed to the
        authentication_succeeded method
    :param fail callable: Callable to invoke after a failed authentication,
        must accept an exception object as well as any *args and **kwargs
        passed to the authentication_failed method.
    """

    def __init__(self, listener, success=None, fail=None):
        self._listener = listener
        self._success = success
        self._fail = fail

    def authentication_succeeded(self, user, *args, **kwargs):
        if self._success:
            self._success(user, *args, **kwargs)
        return self._listener.authentication_succeeded(user, *args, **kwargs)

    def authentication_failed(self, error, *args, **kwargs):
        if self._fail:
            self._fail(error, *args, **kwargs)
        return self._listener.authentication_failed(error, *args, **kwargs)
