import pytest

from flaskbb import create_app
from flaskbb.extensions import db
from flaskbb.configs.testing import TestingConfig as Config
from flaskbb.utils.populate import create_default_groups, \
    create_default_settings


@pytest.fixture(scope='session')
def app():
    """application with context."""
    return create_app(Config)


@pytest.yield_fixture()
def app_context(app):
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def default_groups(database):
    """Creates the default groups"""
    return create_default_groups()


@pytest.fixture()
def default_settings(database):
    """Creates the default settings"""
    return create_default_settings()


# maybe even do it once per session...
# can't use the app_context fixture because a "scope mismatch"
# we manually instate context ourselves
@pytest.yield_fixture()
def database(app_context, request):
    db.create_all()

    yield db

    db.drop_all()
