# -*- coding: utf-8 -*-
"""
    flaskbb.services.registrar
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides services for creating and registering users

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""


class Registrar(object):
    def __init__(self, validator, repository, factory):
        self._validator = validator
        self._repository = repository
        self._factory = factory

    def register(self, username, email, password, **kwargs):
        user = self._factory(username=username, email=email, password=password, **kwargs)
        self._validator(user)
        self._repository.persist(user)
        return user

    def __call__(self, username, email, password, **kwargs):
        return self.register(username, email, password, **kwargs)
