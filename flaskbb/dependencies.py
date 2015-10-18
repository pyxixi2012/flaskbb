# -*- coding: utf-8 -*-
"""
    flaskbb.dependencies
    ~~~~~~~~~~~~~~~~~~~~
    Dependency creation layer for FlaskBB

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""

from .services import Registrar
from .validators.helpers import validate_many
from .validators.user import is_email_free, is_username_free
from .repository.sqla import SQLAUserRepository
from .extensions import db

from .user.models import User

from datetime import datetime


def create_user(**kwargs):
    kwargs = {arg: kwargs[arg] for arg in
              ['username', 'email', 'password', 'language']}
    kwargs.update({'primary_group_id': 4, 'date_joined': datetime.utcnow()})
    return User(**kwargs)


UserRepository = SQLAUserRepository(db)

user_validator = validate_many(is_email_free(UserRepository),
                               is_username_free(UserRepository))

registrar = Registrar(user_validator, UserRepository, create_user)
