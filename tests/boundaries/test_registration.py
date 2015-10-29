from flaskbb.boundaries.registration import (RegistrationBoundary, AfterRegistration,
                                             RegistrationBridge)
from flaskbb.services.registrar import Registrar
from flaskbb.exceptions import ValidationError

try:
    from unittest import mock
except ImportError:
    import mock


class TestRegistrationBridge(object):
    def setup(self):
        self.registrar = mock.create_autospec(Registrar)
        self.listener = mock.create_autospec(RegistrationBoundary)
        self.bridge = RegistrationBridge(self.registrar, self.listener)

    def test_registration_succeeds(self):
        self.registrar.register.return_value = 'Fred'
        self.bridge.register()
        assert self.listener.registration_succeeded.call_args == mock.call('Fred')

    def test_registration_fails(self):
        error = ValidationError('Nope')
        self.registrar.register.side_effect = error
        self.bridge.register()
        assert self.listener.registration_failed.call_args == mock.call(error)


class TestAfterRegistration(object):
    def test_recieves_success_with_handler(self):
        listener = mock.create_autospec(RegistrationBoundary)
        success = mock.MagicMock()
        after_reg = AfterRegistration(listener, success=success)

        after_reg.registration_succeeded('fred')

        assert success.call_args == mock.call('fred')

    def test_recieves_failure_with_handler(self):
        listener = mock.create_autospec(RegistrationBoundary)
        failure = mock.MagicMock()
        after_reg = AfterRegistration(listener, failure=failure)
        error = ValidationError('Nope')

        after_reg.registration_failed(error)

        assert failure.call_args == mock.call(error)
