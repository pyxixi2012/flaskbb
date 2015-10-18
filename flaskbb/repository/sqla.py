# -*- coding: utf-8 -*-
"""
    flaskbb.repositories.sqla
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    SQLAlchemy aware repository implementations

    :copyright: (c) 2015 by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""

from . import AbstractUserRepository
from ..user.models import User


class SQLAUserRepository(AbstractUserRepository):
    def __init__(self, SQLA):
        self.db = SQLA

    def find_by_username(self, username):
        return self.db.session.query(User).filter(User.username == username).first()

    def find_by_email(self, email):
        return self.db.session.query(User).filter(User.email == email).first()

    def persist(self, user):
        self.db.session.add(user)
        self.db.session.commit()
