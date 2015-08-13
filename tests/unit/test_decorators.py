import pytest
from flaskbb.exceptions import AuthorizationRequired
from flaskbb.utils.decorators import admin_required, moderator_required
from collections import namedtuple


User = namedtuple('User', ['is_anonymous', 'permissions'])

Guest = User(is_anonymous=lambda: True, permissions={})
Member = User(is_anonymous=lambda: False,
              permissions={'mod': False, 'super_mod': False, 'admin': False})
Mod = Member._replace(permissions={'mod': True, 'super_mod': False, 'admin': False})
SuperMod = Member._replace(permissions={'mod': False, 'super_mod': True, 'admin': False})
Admin = Member._replace(permissions={'mod': False, 'super_mod': False, 'admin': True})


@pytest.mark.parametrize('user', [Guest, Member, Mod, SuperMod])
def test_admin_required_raises_with_bad_perms(user):
    stub = admin_required(lambda: None, current_user=user)

    with pytest.raises(AuthorizationRequired) as excinfo:
        stub()

    assert "You are not authorized to access this area." == excinfo.value.description
    assert 403 == excinfo.value.code


def test_admin_required_passes_with_admin():
    assert admin_required(lambda: True, current_user=Admin)()


@pytest.mark.parametrize('user', [Guest, Member])
def test_moderator_required_raises_with_bad_perms(user):
    stub = moderator_required(lambda: None, current_user=user)

    with pytest.raises(AuthorizationRequired) as excinfo:
        stub()

    assert "You are not authorized to access this area." == excinfo.value.description
    assert 403 == excinfo.value.code


@pytest.mark.parametrize('user', [Mod, SuperMod, Admin])
def test_admin_required_passes_with_good_perms(user):
    assert admin_required(lambda: True, current_user=Admin)()
