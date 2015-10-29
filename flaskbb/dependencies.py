# -*- coding: utf-8 -*-
"""
    flaskbb.dependencies
    ~~~~~~~~~~~~~~~~~~~~
    Dependency creation layer for FlaskBB

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""

from .services import BasicUserRegistrar, PasswordAuth
from .validators.helpers import validate_many
from .validators.user import is_email_free, is_username_free
from .repository.sqla import SQLAUserRepository
from .extensions import db
from .user.models import User

from werkzeug.security import check_password_hash
from datetime import datetime


def create_user(**kwargs):
    kwargs = {arg: kwargs[arg] for arg in
              ['username', 'email', 'password', 'language']}
    kwargs.update({'primary_group_id': 4, 'date_joined': datetime.utcnow()})
    return User(**kwargs)


def find_by_username_or_email(user_repository):
    def finder(login):
        return (user_repository.find_by_username(login) or
                user_repository.find_by_email(login))
    return finder


UserRepository = SQLAUserRepository(db)

user_validator = validate_many(is_email_free(UserRepository),
                               is_username_free(UserRepository))

registrar = BasicUserRegistrar(user_validator, UserRepository, create_user)
password_auth = PasswordAuth(check_password_hash,
                             find_by_username_or_email(UserRepository))
