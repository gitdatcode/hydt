from .config import options
from .model.sql import create_tables, migrate_tables


def start():
    pass


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
