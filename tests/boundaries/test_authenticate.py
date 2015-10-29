from flaskbb.boundaries import AuthenticationBoundary, AuthenticatorBridge
from flaskbb.exceptions import ValidationError
from flaskbb.services.authentication import Authenticator

try:
    from unittest import mock
except ImportError:
    import mock


class TestAuthenticationBridge(object):
    def setup(self):
        self.authenticator = mock.create_autospec(Authenticator)
        self.listener = mock.create_autospec(AuthenticationBoundary)
        self.bridge = AuthenticatorBridge(self.authenticator, self.listener)

    def test_authentication_succeeds(self):
        self.authenticator.authenticate.return_value = 'Fred'

        self.bridge.authenticate()

        assert self.listener.authentication_succeeded.call_args == mock.call('Fred')

    def test_authentication_fails(self):
        error = ValidationError('Nope')
        self.authenticator.authenticate.side_effect = error

        self.bridge.authenticate()

        assert self.listener.authentication_failed.call_args == mock.call(error)
