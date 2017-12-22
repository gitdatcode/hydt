from datetime import datetime
from uuid import uuid4

from peewee import *

import peeweedbevolve

from .config import options


def get_database():
    return SqliteDatabase(options.db_location)


DATABASE = get_database()


class BaseModel(Model):
    date_created = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE


class User(BaseModel):
    active = BooleanField(default=True)
    slack_id = IntegerField(null=True)
    notification_hour = IntegerField(null=True)
    notification_minute = IntegerField(null=True)
    admin = BooleanField(default=False)


class UserDay(BaseModel):
    user = ForeignKeyField(User)
    day = DateField(default=datetime.now)
    notes = TextField(null=True)
    sentiment = FloatField(null=True, default=0)
    code = CharField(null=True)
    emoji = CharField(null=True)
    color = CharField(null=True)
    color_shifted = CharField(null=True)


def create_tables():
    tables = [UserDay, User]

    DATABASE.connect()
    DATABASE.create_tables(tables)


def migrate_tables():
    DATABASE.evolve()
