# -*- coding: utf-8 -*-
"""
    flaskbb.auth.models
    ~~~~~~~~~~~~~~~~~~~~~~~

    Models related to auth and registration

    :copyright: (c) 2017 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from collections import namedtuple

_BLOB_FIELDS = ['username', 'password', 'email', 'language', 'group']


class UserBlob(namedtuple('UserBlob', _BLOB_FIELDS)):

    def __new__(cls, username, password, email, language, group=None):
        return super(cls, cls).__new__(
            cls, username, password, email, language, group
        )


del _BLOB_FIELDS

