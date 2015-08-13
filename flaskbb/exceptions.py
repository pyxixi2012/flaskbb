from werkzeug import exceptions as exc


class FlaskBBError(Exception):
    """Base for all FlaskBB exceptions."""
    code = 500
    description = "An internal error has occured."


class AuthorizationRequired(exc.Forbidden, FlaskBBError):
    description = "You are not authorized to access this area."
