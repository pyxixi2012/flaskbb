# -*- coding: utf-8 -*-
"""
    flaskbb.auth.views
    ~~~~~~~~~~~~~~~~~~~~

    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, flash, redirect, url_for
from flask_login import (current_user, login_user, login_required,
                         logout_user, confirm_login)
from flask_babelex import gettext as _

from flaskbb.utils.helpers import render_template
from flaskbb.email import send_reset_token
from flaskbb.auth.forms import (LoginForm, ReauthForm, ForgotPasswordForm,
                                ResetPasswordForm)
from flaskbb.user.models import User


from flaskbb.boundaries.authentication import AuthenticatorBridge, AfterAuth
from flaskbb.boundaries.registration import RegistrationBridge, AfterRegistration
from flaskbb.dependencies import (registrar as BaseRegistrar,
                                  password_auth as BasePasswordAuth,
                                  password_reauth as BasePasswordReauth)
from .controllers import RegisterUser, AuthenticateUser
from .utils import disallow_authenticated, determine_register_form


auth = Blueprint("auth", __name__)


def registrar(listener):
    return RegistrationBridge(
        BaseRegistrar,
        AfterRegistration(
            AfterRegistration(
                listener=listener,
                success=lambda *a, **k: flash(_('Thanks for registering!'), 'success')),
            success=lambda u, *a, **k: login_user(u)))


def auth_factory(listener):
    return AuthenticatorBridge(
        BasePasswordAuth,
        AfterAuth(
            AfterAuth(
                listener,
                success=lambda *a, **k: flash(_('Welcome back!'), 'success')),
            success=lambda u, *a, **k: login_user(u, remember=k.get('remember_me', False))
        ))


def reauth_factory(listener):
    return AuthenticatorBridge(
        BasePasswordReauth,
        AfterAuth(
            AfterAuth(
                listener,
                success=lambda *a, **k: flash(_('Reauthenticated'), 'success')),
            success=lambda *a, **k: confirm_login()))


auth.add_url_rule(
    rule='/register', endpoint='register',
    view_func=disallow_authenticated(
        RegisterUser.as_view(
            name='register',
            template='auth/register.html',
            redirect_endpoint='user.me',
            registrar=registrar,
            form=determine_register_form)))


auth.add_url_rule(
    rule='/login', endpoint='login',
    view_func=disallow_authenticated(
        AuthenticateUser.as_view(
            name='login',
            template='auth/login.html',
            redirect_endpoint='forum.index',
            form=LoginForm,
            authenticator=auth_factory)))


auth.add_url_rule(
    rule='/reauth', endpoint='reauth',
    view_func=login_required(
        AuthenticateUser.as_view(
            name='reauth',
            template='auth/reauth.html',
            redirect_endpoint='user.me',
            form=ReauthForm,
            authenticator=reauth_factory)))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(("Logged out"), "success")
    return redirect(url_for("forum.index"))


@auth.route('/resetpassword', methods=["GET", "POST"])
def forgot_password():
    """
    Sends a reset password token to the user.
    """

    if not current_user.is_anonymous():
        return redirect(url_for("forum.index"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            token = user.make_reset_token()
            send_reset_token(user, token=token)

            flash(_("E-Mail sent! Please check your inbox."), "info")
            return redirect(url_for("auth.forgot_password"))
        else:
            flash(_("You have entered a Username or E-Mail Address that is "
                    "not linked with your account."), "danger")
    return render_template("auth/forgot_password.html", form=form)


@auth.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Handles the reset password process.
    """

    if not current_user.is_anonymous():
        return redirect(url_for("forum.index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        expired, invalid, data = user.verify_reset_token(form.token.data)

        if invalid:
            flash(_("Your Password Token is invalid."), "danger")
            return redirect(url_for("auth.forgot_password"))

        if expired:
            flash(_("Your Password Token is expired."), "danger")
            return redirect(url_for("auth.forgot_password"))

        if user and data:
            user.password = form.password.data
            user.save()
            flash(_("Your Password has been updated."), "success")
            return redirect(url_for("auth.login"))

    form.token.data = token
    return render_template("auth/reset_password.html", form=form)
