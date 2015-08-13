from werkzeug import exceptions as exc


class FlaskBBError(Exception):
    """Base for all FlaskBB exceptions."""
    description = "An internal error has occured."


class AuthorizationRequired(FlaskBBError, exc.Forbidden):
    description = "You are not authorized to access this area."
