# -*- coding: utf-8 -*-
"""
    flaskbb.validators.user
    ~~~~~~~~~~~~~~~~~~~~~~~
    User validators

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""


from ..exceptions import ValidationError


def is_username_free(repository):
    def is_username_free(user):
        if repository.find_by_username(user.username):
            raise ValidationError('Username in use already', field='username')
        return True
    return is_username_free


def is_email_free(repository):
    def is_email_free(user):
        if repository.find_by_email(user.email):
            raise ValidationError('Email in use already', field='email')
        return True
    return is_email_free
