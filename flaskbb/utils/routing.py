# -*- coding: utf-8 -*-
"""
    flaskbb.utils.routing
    ~~~~~~~~~~~~~~~~~~~~~

    Routing helpers for FlaskBB

    :copyright: (c)  2017 by the FlaskBB Team
    :license: BSD, see LICENSE for more details
"""

from werkzeug.routing import UnicodeConverter, BaseConverter


class ModelConverter(BaseConverter):
    """
        Converts an integer user id in a URL path to an instance of User
    """

    def __init__(self, url_map, app, model, attr, *a, **k):
        self.app = app
        self.model = model
        self.attr = attr
        super(ModelConverter, self).__init__(url_map, *a, **k)

    def to_python(self, value):
        value = super(ModelConverter, self).to_python(value)

        with self.app.app_context():
            return self.model.query.filter(getattr(self.model, self.attr) == value).first_or_404()

    def to_url(self, value):
        return super(ModelConverter, self).to_url(getattr(value, self.attr))


def model_converter(app, model, attr, base=UnicodeConverter):
    class ModelConverter_(ModelConverter, base):
        def __init__(self, *a, **k):
            super(ModelConverter_, self).__init__(app=app, model=model, attr=attr, *a, **k)

    ModelConverter_.__name__ = "{}Converter".format(model.__name__)
    return ModelConverter_
