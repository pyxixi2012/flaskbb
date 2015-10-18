from flaskbb.repository.sqla import SQLAUserRepository
import pytest

try:
    from unittest import mock
except ImportError:
    import mock


@pytest.fixture
def cls_db(request, database, user):
    request.cls.db = database


@pytest.mark.usefixtures('cls_db')
class TestSQLAUserRepository(object):
    def setup(self):
        self.repository = SQLAUserRepository(self.db)

    def test_find_by_users(self):
        assert self.repository.find_by_username('test_normal')

    def test_find_by_email(self):
        assert self.repository.find_by_email('test_normal@example.org')

    def test_persist(self, user):
        with mock.patch.object(self.db, 'session') as session:
            self.repository.persist(user)

        assert session.add.call_args == mock.call(user)
        assert session.commit.call_count == 1
