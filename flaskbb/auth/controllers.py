# -*- coding: utf-8 -*-
"""
    flaskbb.auth.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Controllers for FlaskBB.Auth module

    :copyright: (c) 2015 by the FlaskBB Team
    :license: BSD, see LICENSE for more details.
"""


from ..exceptions import ValidationError
from ..utils.helpers import render_template

from flask import url_for, redirect, flash, request
from flask.views import MethodView
from flask_babelex import gettext as _


class RegisterUser(MethodView):
    def __init__(self, form, registrar, template, redirect_endpoint):
        self._form = form()
        self._registrar = registrar
        self._template = template
        self._redirect_endpoint = redirect_endpoint

    def get(self):
        return self._render()

    def post(self):
        if not self._form.validate_on_submit():
            return self._render()
        else:
            return self._register_user()

    def _register_user(self):
        try:
            self._registrar(**self._form.data)
        except ValidationError as e:
            self._handle_error(e)
            return self._render()
        else:
            return self._redirect()

    def _render(self):
        return render_template(self._template, form=self._form)

    def _redirect(self):
        return redirect(url_for(self._redirect_endpoint,
                                username=self._form.username.data))

    def _handle_error(self, exc):
        field = getattr(self._form, exc.field)
        field.errors = [exc.msg]


class LoginUser(MethodView):
    def __init__(self, form, authenticator, template, redirect_endpoint):
        self._form = form()
        self._authenticator = authenticator
        self._template = template
        self._redirect_endpoint = redirect_endpoint

    def get(self):
        return self._render()

    def post(self):
        if not self._form.validate_on_submit():
            return self._render()
        else:
            return self._authenticate()

    def _authenticate(self):
        try:
            self._authenticator.authenticate(**self._form.data)
        except ValidationError as e:
            self._handle_error(e)
            return self._render()
        else:
            return self._redirect()

    def _render(self):
        return render_template(self._template, form=self._form)

    def _redirect(self):
        endpoint = request.args.get('next') or url_for(self._redirect_endpoint)
        return redirect(endpoint)

    def _handle_error(self, e):
        flash(_(e.msg))
