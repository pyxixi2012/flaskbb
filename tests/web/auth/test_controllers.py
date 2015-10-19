from flaskbb.auth.controllers import RegisterUser, LoginUser
from flaskbb.exceptions import ValidationError

try:
    from unittest import mock
except ImportError:
    import mock


class FakeField(object):
    def __init__(self, data):
        self.data = data
        self.errors = []


class FakeRegisterForm(object):
    def __init__(self, username, email, password, valid=True):
        self.username = FakeField(username)
        self.password = FakeField(password)
        self.email = FakeField(email)
        self.valid = valid

    def validate_on_submit(self):
        return self.valid

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

    def __call__(self):
        return self


class FakeLoginForm(object):
    def __init__(self, login, password, remember_me=False, valid=True):
        self.login = FakeField(login)
        self.password = FakeField(password)
        self.remember_me = FakeField(remember_me)
        self.valid = valid

    def validate_on_submit(self):
        return self.valid

    @property
    def data(self):
        return {'login': self.login.data,
                'password': self.password.data,
                'remember_me': self.remember_me.data}

    def __call__(self):
        return self


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
    def test_submit_valid_data(self):
        form = FakeLoginForm('fred', 'fred', False, True)
        authenticator = mock.Mock()
        controller = LoginUser(form, authenticator, None, None)

        with mock.patch.object(LoginUser, '_redirect'):
            controller.post()

        assert (authenticator.authenticate.call_args ==
                mock.call(login='fred', password='fred', remember_me=False))

    def test_submit_invalid_data(self):
        form = FakeLoginForm('fred', 'fred', False, False)
        authenticator = mock.Mock()
        controller = LoginUser(form, authenticator, None, None)

        with mock.patch.object(controller, '_render') as render:
            controller.post()

        assert render.call_count == 1

    def test_authenticator_fails(self):
        form = FakeLoginForm('fred', 'fred', False, True)
        error = ValidationError('Failed')
        authenticator = mock.Mock()
        authenticator.authenticate.side_effect = error
        controller = LoginUser(form, authenticator, None, None)

        with mock.patch.object(controller, '_handle_error') as handler, mock.patch.object(controller, '_render') as render:
            controller.post()

        assert handler.call_args == mock.call(error)
        assert render.call_count == 1
