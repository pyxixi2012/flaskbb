from flaskbb.auth.controllers import RegisterUser, LoginUser
from flaskbb.boundaries import AuthenticatorBridge
from flaskbb.services.authentication import Authenticator
from flaskbb.exceptions import ValidationError

try:
    from unittest import mock
except ImportError:
    import mock


class FakeField(object):
    def __init__(self, data):
        self.data = data
        self.errors = []


class FakeForm(object):
    def validate_on_submit(self):
        return self.valid

    def __call__(self):
        return self


class FakeRegisterForm(FakeForm):
    def __init__(self, username, email, password, valid=True):
        self.username = FakeField(username)
        self.password = FakeField(password)
        self.email = FakeField(email)
        self.valid = valid

    @property
    def errors(self):
        errors = {'username': self.username.errors,
                  'email': self.email.errors,
                  'password': self.password.errors}

        return {k: v for k, v in errors.items() if v}

    @property
    def data(self):
        return {'username': self.username.data,
                'email': self.email.data,
                'password': self.password.data}


class FakeLoginForm(FakeForm):
    def __init__(self, login, password, remember_me=False, valid=True):
        self.login = FakeField(login)
        self.password = FakeField(password)
        self.remember_me = FakeField(remember_me)
        self.valid = valid

    @property
    def data(self):
        return {'login': self.login.data,
                'password': self.password.data,
                'remember_me': self.remember_me.data}

    def errors(self):
        errors = {'login': self.login.errors,
                  'password': self.password.errors}

        return {k: v for k, v in errors.items() if v}


def stingy_registrar(username, email, password):
    raise ValidationError('Fails validation', 'username')


class TestRegisterUser(object):
    def setup(self):
        self.form = FakeRegisterForm('fred', 'fred', 'fred')
        self.generous_registrar = lambda *a, **k: None
        self.stingy_registrar = stingy_registrar

    def test_submit_invalid_form_data(self):
        self.form.valid = False
        controller = RegisterUser(self.form, self.generous_registrar, None, None)

        with mock.patch.object(RegisterUser, '_render') as render:
            controller.post()

        assert render.call_count == 1

    def test_submit_valid_form_data(self):
        controller = RegisterUser(self.form, self.generous_registrar, None, None)

        with mock.patch.object(RegisterUser, '_register_user') as register:
            controller.post()

        assert register.call_count == 1

    def test_fail_registration_validation(self):
        controller = RegisterUser(self.form, self.stingy_registrar, None, None)

        with mock.patch.object(RegisterUser, '_render') as render:
            controller.post()

        assert self.form.errors == {'username': ['Fails validation']}
        assert render.call_count == 1

    def test_pass_registration_validation(self):
        controller = RegisterUser(self.form, self.generous_registrar, None, None)

        with mock.patch.object(RegisterUser, '_redirect') as redirect:
            controller.post()

        assert redirect.call_count == 1


class TestLoginUser(object):
    def setup(self):
        self.form = FakeLoginForm('fred', 'fred')
        self.authenticator = mock.create_autospec(Authenticator)
        self.bridge = lambda l: AuthenticatorBridge(self.authenticator, l)

    def test_submit_valid_data(self):
        controller = LoginUser(self.form, self.bridge, None, None)
        self.authenticator.authenticate.return_value = 'Fred'

        with mock.patch.object(controller, 'authentication_succeeded') as succeed:
            controller.post()

        assert succeed.call_args == mock.call('Fred', **self.form.data)

    def test_submit_invalid_data(self):
        self.form.valid = False
        controller = LoginUser(self.form, self.bridge, None, None)

        with mock.patch.object(controller, '_render') as render:
            controller.post()

        assert render.call_count == 1

    def test_authenticator_fails(self):
        error = ValidationError('Failed')
        self.authenticator.authenticate.side_effect = error
        controller = LoginUser(self.form, self.bridge, None, None)

        with mock.patch.object(controller, 'authentication_failed') as failed:
            controller.post()

        assert failed.call_args == mock.call(error, **self.form.data)
