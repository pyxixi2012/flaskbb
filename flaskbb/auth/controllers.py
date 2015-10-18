# -*- coding: utf-8 -*-
"""
    flaskbb.auth.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Controllers for FlaskBB.Auth module

    :copyright: (c) 2015 by the FlaskBB Team
    :license: BSD, see LICENSE for more details.
"""


from ..exceptions import ValidationError
from flask import url_for, redirect
from flask.views import MethodView
from flaskbb.utils.helpers import render_template


class RegisterUser(MethodView):
    def __init__(self, form, registrar, template, redirect_url):
        self._form = form()
        self._registrar = registrar
        self._template = template
        self._redirect_url = redirect_url

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
        return redirect(url_for(self._redirect_url, username=self._form.username.data))

    def _handle_error(self, exc):
        field = getattr(self._form, exc.field)
        field.errors = [exc.msg]
