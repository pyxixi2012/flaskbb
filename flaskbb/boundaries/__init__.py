# -*- coding: utf-8 -*-
"""
    flaskbb.boundaries
    ~~~~~~~~~~~~~~~~~~
    Boundaries module for FlaskBB
    :copyright: 2015 (c) by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""

from .authentication import AuthenticationBoundary, AuthenticatorBridge, AfterAuth
from .registration import RegistrationBoundary, RegistrationBridge, AfterRegistration
