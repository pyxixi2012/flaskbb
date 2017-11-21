# -*- coding: utf-8 -*-
"""
    flaskbb.auth.interfaces
    ~~~~~~~~~~~~~~~~~~~~~~~

    Provides the contracts for user authentication,
    registration, resetting passwords and other
    similar user management needs.

    If you're looking to implement custom user
    authentication, this is the place for you
    to look.

    :copyright: (c) 2017 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from abc import abstractmethod
from functools import wraps

from flaskbb._compat import ABC


def do_not_super(f):

    @abstractmethod
    @wraps(f)
    def _(*args, **kwargs):
        raise NotImplementedError("Do not super into base class")

    return _


class UserActivator(ABC):
    """
    Handles the user activation flow
    """

    @do_not_super
    def send_token(self, user):
        """
        Handles sending the user an activation token
        """
        pass

    @abstractmethod
    def activate_user(self, user, token):
        """
        Activates a user using their token
        """
        user.activated = True


class UserAuthenicator(ABC):
    """
    Used to authenticate a user and mark them acceptable to login
    """

    @abstractmethod
    def authenticate(self, user, password):
        return False


class UserAuthenticationService(ABC):

    @do_not_super
    def authenticate(self, username_or_email, password):
        pass

class UserAvailablityChecker(ABC):
    """
    Used to check if a username or email is available
    """

    @abstractmethod
    def is_username_available(self, username):
        """
        Returns a boolean representing if the username is available
        """
        return False

    @abstractmethod
    def is_email_available(self, email):
        """
        Returns a boolean representing if the email is available
        """
        return False


class UserLoginService(ABC):

    @do_not_super
    def login(self, username_or_email, password, remember=False):
        pass

    @do_not_super
    def logout(self, user):
        pass

    @do_not_super
    def refresh(self, username, password):
        pass

    @abstractmethod
    def has_fresh_login(self, user):
        return False


class UserRegistrator(ABC):
    """
    Facility for registering a user and persisting them.
    """

    @do_not_super
    def register(self, userblob):
        pass
