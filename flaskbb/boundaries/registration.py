"""
    flaskbb.boundaries.registration
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Registration boundary for FlaskBB

    :copyright: 2015 (c) by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""


from ..exceptions import ValidationError


class RegistrationBoundary(object):
    def registration_succeeded(self, user, *args, **kwargs):
        raise NotImplementedError

    def registration_failed(self, error, *args, **kwargs):
        raise NotImplementedError


class AfterRegistration(RegistrationBoundary):
    def __init__(self, listener, success=None, failure=None):
        self._listener = listener
        self._success = success
        self._failure = failure

    def registration_succeeded(self, user, *args, **kwargs):
        if self._success:
            self._success(user, *args, **kwargs)
        return self._listener.registration_succeeded(user, *args, **kwargs)

    def registration_failed(self, error, *args, **kwargs):
        if self._failure:
            self._failure(error, *args, **kwargs)
        return self._listener.registration_failed(error, *args, **kwargs)


class RegistrationBridge(object):
    def __init__(self, registrar, listener):
        self._registrar = registrar
        self._listener = listener

    def register(self, *args, **kwargs):
        try:
            user = self._registrar.register(*args, **kwargs)
        except ValidationError as e:
            return self._listener.registration_failed(e, *args, **kwargs)
        else:
            return self._listener.registration_succeeded(user, *args, **kwargs)
