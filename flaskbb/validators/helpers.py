# -*- coding: utf-8 -*-
"""
    flaskbb.validators.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Validation helpers

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""


def validate_many(*validators):
    def validator(*args, **kwargs):
        return all(validator(*args, **kwargs) for validator in validators)
    return validator
