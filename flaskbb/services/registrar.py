# -*- coding: utf-8 -*-
"""
    flaskbb.services.registrar
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides services for creating and registering users

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""


class Registrar(object):
    def __init__(self, hasher, validator, repository, factory):
        self._hasher = hasher
        self._validator = validator
        self._repository = repository
        self._factory = factory

    def register(self, username, email, password, **kwargs):
        password = self._hasher(password)
        user = self._factory(username=username, email=email, password=password, **kwargs)
        self._validator(user)
        self._repository.persist(user)
