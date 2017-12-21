from . import BaseHandler


class HomeHandler(BaseHandler):

    async def get(self):
        self.write('HOMEPAGE')
