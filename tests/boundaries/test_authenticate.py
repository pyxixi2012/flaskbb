from flaskbb.boundaries import AuthenticationBoundary, AuthenticatorBridge, AfterAuth
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


class TestAfterAuth(object):
    def setup(self):
        self.listener = mock.create_autospec(AuthenticationBoundary)
        self.success_handler = mock.MagicMock()
        self.failure_handler = mock.MagicMock()
        self.after_auth = AfterAuth(self.listener, self.success_handler,
                                    self.failure_handler)

    def test_recieves_success_with_handler(self):
        self.after_auth.authentication_succeeded('Fred')
        assert self.success_handler.call_args == mock.call('Fred')

    def test_recieves_failure_with_handler(self):
        error = ValidationError('Nope')
        self.after_auth.authentication_failed(error)
        assert self.failure_handler.call_args == mock.call(error)
