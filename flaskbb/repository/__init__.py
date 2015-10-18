# -*- coding: utf-8 -*-
"""
    flaskbb.repository
    ~~~~~~~~~~~~~~~~~~
    Abstract repositories for FlaskBB

    :copyright: (c) 2015 by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""

from abc import abstractmethod, ABCMeta
from ..utils.helpers import with_metaclass


class ABC(with_metaclass(ABCMeta, object)):
    pass


class AbstractUserRepository(ABC):
    @abstractmethod
    def find_by_username(self, username):
        pass

    @abstractmethod
    def find_by_email(self, email):
        pass

    @abstractmethod
    def persist(self, user):
        pass
