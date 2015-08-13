from flaskbb import exceptions as excs


def test_FlaskBBError():
    e = excs.FlaskBBError()

    assert (e.code, e.description) == (500, "An internal error has occured.")


def test_AuthorizationRequied():
    e = excs.AuthorizationRequired()

    assert (e.code, e.description) == (403, "You are not authorized to access this area.")
