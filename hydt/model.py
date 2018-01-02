from datetime import datetime
from uuid import uuid4

from peewee import *

import peeweedbevolve

from .config import options


def get_database(location=None):
    location = location or options.db_location

    return SqliteDatabase(location)


class BaseModel(Model):
    date_created = DateTimeField(default=datetime.now)

    class Meta:
        database = get_database()


class User(BaseModel):
    active = BooleanField(default=True)
    slack_id = CharField(null=True)
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


def create_tables(location=None):
    tables = [UserDay, User]
    db = get_database(location)

    db.connect()
    db.create_tables(tables)


def migrate_tables(location=None):
    db = get_database(location)

    db.evolve()
