# -*- coding: utf-8 -*-
"""
    flaskbb.auth.views
    ~~~~~~~~~~~~~~~~~~~~

    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, flash, redirect, url_for, request
from flask_login import (current_user, login_user, login_required,
                         logout_user, confirm_login, login_fresh)
from flask_babelex import gettext as _

from flaskbb.utils.helpers import render_template
from flaskbb.email import send_reset_token
from flaskbb.auth.forms import (LoginForm, ReauthForm, ForgotPasswordForm,
                                ResetPasswordForm)
from flaskbb.user.models import User
from flaskbb.services.registrar import AfterRegister
from flaskbb.services.authentication import AfterAuth
from flaskbb.dependencies import (registrar as BaseRegistrar,
                                  password_auth as BasePasswordAuth)
from .controllers import RegisterUser, LoginUser
from .utils import disallow_authenticated, determine_register_form


auth = Blueprint("auth", __name__)


registrar = AfterRegister(
    AfterRegister(BaseRegistrar,
                  lambda u: flash(_('Thanks for registering!'), 'success')),
    login_user)

password_auth = AfterAuth(
    BasePasswordAuth,
    lambda u, **k: login_user(u, remember=k.get('remember_me', False)))

auth.add_url_rule(
    rule='/register', endpoint='register',
    view_func=disallow_authenticated(
        RegisterUser.as_view(name='register',
                             template='auth/register.html',
                             redirect_url='user.profile',
                             registrar=registrar,
                             form=determine_register_form)))


auth.add_url_rule(
    rule='/login', endpoint='login',
    view_func=disallow_authenticated(
        LoginUser.as_view(name='login',
                          template='auth/login.html',
                          redirect_endpoint='forum.index',
                          form=LoginForm,
                          authenticator=password_auth)))

@auth.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    """
    Reauthenticates a user
    """

    if not login_fresh():
        form = ReauthForm(request.form)
        if form.validate_on_submit():
            confirm_login()
            flash(_("Reauthenticated."), "success")
            return redirect(request.args.get("next") or
                            url_for("user.profile"))
        return render_template("auth/reauth.html", form=form)
    return redirect(request.args.get("next") or
                    url_for("user.profile", username=current_user.username))


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
