# -*- coding: utf-8 -*-
"""
    flaskbb.auth.utils
    ~~~~~~~~~~~~~~~~~~
    Utilities specifically for flaskbb.auth

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""

from .forms import RegisterForm, RegisterRecaptchaForm
from ..fixtures.settings import available_languages
from ..utils.settings import flaskbb_config

from flask import current_app, redirect, url_for, request
from flask_login import current_user

from functools import wraps


def determine_register_form():
    if current_app.config['RECAPTCHA_ENABLED']:
        form = RegisterRecaptchaForm()
    else:
        form = RegisterForm()

    form.language.choices = available_languages()
    form.language.default = flaskbb_config['DEFAULT_LANGUAGE']
    form.process(request.form)
    return form


def disallow_authenticated(view):
    @wraps(view)
    def checker(*args, **kwargs):
        if current_user and current_user.is_authenticated():
            return redirect(url_for('user.profile', username=current_user.username))
        return view(*args, **kwargs)
    return checker
