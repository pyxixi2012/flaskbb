"""
    flaskbb.exceptions
    ~~~~~~~~~~~~~~~~~~
    Custom exceptions designed for FlaskBB

    :copyright: (c) 2015 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details
"""

class FlaskBBError(Exception):
    "Root FlaskBB Exception"
    pass


class ValidationError(FlaskBBError):
    """Error raised for invalid data

    Includes optional field attribute if communication about what piece of data
    was invalid needs to be communicated, this is helpful for updating Form.errors
    when applying application validation to form data.
    """
    def __init__(self, msg, field=None):
        self.msg = msg
        self.field = field
        super(ValidationError, self).__init__(msg)
