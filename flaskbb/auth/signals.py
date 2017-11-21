# -*- coding: utf-8 -*-
"""
    flaskbb.auth.signals
    ~~~~~~~~~~~~~~~~~~~~~~~

    Signals related to auth and registration

    :copyright: (c) 2017 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask.signals import Namespace

auth_signals = Namespace()

auth_failed = auth_signals.signal('auth-failed')
auth_succeeded = auth_signals.signal('auth-succeeded')
login_failed = auth_signals.signal('login-failed')
reauth_failed = auth_signals.signal('reauth-failed')
reauth_succeeded = auth_signals.signal('reauth-succeeded')
user_logged_in = auth_signals.signal('user-logged-in')
user_logged_out = auth_signals.signal('user-logged-out')
user_registered = auth_signals.signal('user-registered')
