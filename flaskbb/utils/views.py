from flask.views import View
from .helpers import render_template


class RenderableView(View):
    def __init__(self, template, view):
        self.template = template
        self.view = view

    def dispatch_request(self, *args, **kwargs):
        context = self.view(*args, **kwargs)
        return render_template(self.template, **context)

    def __repr__(self):
        return "<{0} template={1!r} view={2!r}>".format(self.__class__.__name__,
                                                        self.template,
                                                        self.view)
