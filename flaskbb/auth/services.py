# -*- coding: utf-8 -*-
"""
    flaskbb.auth.services
    ~~~~~~~~~~~~~~~~~~~~~

    This provides the services for user authentication, registration,
    resetting passwords for users.

    :copyright: (c) 2017 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from datetime import datetime

from flask import current_app, flash
from flask_babelplus import gettext as _
from flask_login import confirm_login, login_fresh, login_user, logout_user
from flaskbb.email import send_activation_token, send_reset_token
from flaskbb.extensions import db
from flaskbb.user.models import User
from flaskbb.utils.settings import flaskbb_config
from werkzeug.security import check_password_hash

from .exceptions import (DuplicateUser, InvalidPassword, RegistrationFailure,
                         UserDoesntExist)
from .interfaces import (UserAuthenicator, UserAuthenticationService,
                         UserAvailablityChecker, UserLoginService,
                         UserRegistrator)
from .models import UserBlob
from .signals import (auth_failed, auth_succeeded, login_failed, reauth_failed,
                      reauth_succeeded, user_logged_in, user_logged_out,
                      user_registered)


def increment_user_login_attempts(sender, user, **extras):
    user.login_attempts = 1 if user.login_attempts is None else user.login_attempts + 1
    user.last_failed_login = datetime.utcnow()
    user.save()


def reset_user_login_attempts(sender, user, **extras):
    user.login_attempts = 0
    user.last_failed_login = None
    user.save()


def flash_activation_message(sender, user, **extras):
    flash(
        _(
            "In order to use your account you have to activate it "
            "through the link we have sent to your email "
            "address."
        ), "danger"
    )


def flash_reauth_success(sender, user, **extras):
    flash(_("Reauthenticated"), "success")


def flash_logout(sender, user, **extras):
    flash(_("Logged out"), "success")


def handle_activation(sender, user, **extras):
    if flaskbb_config["ACTIVATE_ACCOUNT"]:
        send_activation_token.delay(user)
        flash(
            _(
                "An account activation email has been sent to %(email)s",
                email=user.email
            ), "success"
        )
    else:
        user.activated = True
        login_user(user)
        flash(_("Thanks for registering."), "success")


class DefaultUserAuthenticator(UserAuthenicator):

    def authenticate(self, user, password):
        return check_password_hash(user.password, password)


class DefaultUserAuthenticationService(UserAuthenticationService):

    def __init__(self):
        self.authenticator = DefaultUserAuthenticator()

    def authenticate(self, username_or_email, password):
        user = User.query.filter(
            db.or_(
                User.username.ilike(username_or_email),
                User.email.ilike(username_or_email)
            )
        ).first()

        if user is None:
            raise AuthenticationError("User does not exist")

        return self.authenticator.authenticate(user, password)


class DefaultUserAvailabiltyChecker(UserAvailablityChecker):
    """
    Checks the database to see if a username or email is available
    for use.
    """

    def is_username_available(self, username):
        return User.query.filter(User.username.ilike(username)).count() == 0

    def is_email_available(self, email):
        return User.query.filter(User.email.ilike(email)).count() == 0


class DefaultUserLoginService(UserLoginService):

    def __init__(self):
        self.authenticator = DefaultUserAuthenticator()
        self.clock = datetime.utcnow

    def login(self, username_or_email, password, remember=False):
        user = User.query.filter(
            db.or_(
                User.username.ilike(username_or_email),
                User.email.ilike(username_or_email)
            )
        ).first()

        if user is None:
            raise UserDoesntExist()

        authenticated = self.authenticator.authenticate(user, password)

        if not authenticated:
            auth_failed.send(current_app._get_current_object(), user=user)
            raise InvalidPassword()

        auth_succeeded.send(current_app._get_current_object(), user=user)
        logged_in = login_user(user, remember=remember)

        if logged_in:
            user_logged_in.send(current_app._get_current_object(), user=user)
        else:
            login_failed.send(current_app._get_current_object(), user=user)

        return logged_in

    def logout(self, user):
        if not user.authenticated:
            raise AuthenticationError(
                "Cannot logout user that is not logged in"
            )
        logout_user()
        user_logged_out.send(current_app._get_current_object(), user=user)

    def refresh(self, user, password):
        authenticated = self.authenticator.authenticate(user, password)

        if not authenticated:
            reauth_failed.send(current_app._get_current_object(), user=user)
            raise InvalidPassword()

        reauth_succeeded.send(current_app._get_current_object(), user=user)
        confirm_login()

    def has_fresh_login(self, user):
        return login_fresh()


class DefaultUserRegistrator(UserRegistrator):

    def __init__(self, clock=datetime.utcnow, default_group=4):
        self.clock = clock
        self.default_group = default_group
        self.availablity = DefaultUserAvailabiltyChecker()

    def register(self, userblob):
        if not (self.availablity.is_username_available(userblob.username)
                and self.availablity.is_email_available(userblob.email)):
            raise DuplicateUser("Username or email already in use")

        user = User(
            username=userblob.username,
            email=userblob.email,
            password=userblob.password,
            language=userblob.language,
            group=userblob.group if group is not None else self.default_group,
            date_joined=self.clock()
        )
        user.save()
        return user
