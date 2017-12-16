from tornado import web, escape, gen, ioloop


class BaseHandler(web.RequestHandler):

    @property
    def is_ajax(self):
        return ('X-Requested-With' in self.request.headers and
            self.request.headers['X-Requested-With'] == 'XMLHttpRequest')

    def get_arg(self, name, default=None):
        """
        method used to get the argument from the request
        all requests are sent as encoded json tied to the body argument
        PUT methods do not get data from self.request.get_argument
        so direct parsing of self.request.body is used
        """

        if self.is_ajax:
            body = json.loads(self.request.body.decode('utf-8'))

            if name:
                body = body.get(name, default)
        else:
            body = self.get_argument(name, default)

        return self.strip_tags(body)
