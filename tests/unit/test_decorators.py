import pytest

from flaskbb.exceptions import AuthorizationRequired
from flaskbb.user.models import Guest
from flaskbb.utils.decorators import admin_required


def test_admin_required_raises_with_guest():
    def stub(): return None

    stub = admin_required(stub, current_user=Guest())

    with pytest.raises(AuthorizationRequired) as excinfo:
        stub()

    assert "You are not authorized to access this area." == excinfo.value.description
    assert 403 == excinfo.value.code
