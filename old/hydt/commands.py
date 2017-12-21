from .config import options
from .model.sql import create_tables, migrate_tables


def start():
    from .routes import ROUTES
    from .view import functions

    from tornado import httpserver, ioloop, web


    class App(web.Application):

        def __init__(self):
            settings = {
                'debug': options.debug,
                'ui_methods': functions,
            }

            web.Application.__init__(self, ROUTES, **settings)

    application = App()
    http_server = httpserver.HTTPServer(application)

    print('STARTING HYDT ON PORT: ', options.port)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()


def migrate():
    migrate_tables()


def send_notifications(hour, minute):
    from .model.sql import User

    users = User.select().where(
        User.notification_hour == hour,
        User.notification_minute == minute)

    for user in users:
        user.notify(hour=hour, minute=minute)


def build_database():
    create_tables()


def how_to():
    return """
To build the database
    {app_name}.py build_database

To migrate the database
    {app_name}.py migrate

To start the application
    {app_name}.py start

""".format(app_name=options.app_name)
