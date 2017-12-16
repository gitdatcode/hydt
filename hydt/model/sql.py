from datetime import datetime
from uuid import uuid4

from peewee import *

import peeweedbevolve

from ..config import options


def get_database():
    return SqliteDatabase(options.db_location)


DATABASE = get_database()


class BaseModel(Model):
    date_created = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE


class Day(BaseModel):
    month = IntegerField()
    day = IntegerField()
    year = IntegerField()


class User(BaseModel):
    active = BooleanField(default=True)
    phone = CharField()
    email = CharField()
    password = CharField()
    notification_hour = IntegerField()
    notification_minute = IntegerField()
    admin = BooleanField(default=False)

    def notify(self, resend=False):
        now = datetime.now()
        day, _ = Day.get_or_create(day=now.day, month=now.month, year=now.year)
        user_day, _ = UserDay.get_or_create(day=day, user=self)

        if not user_day.notification_sent or resend:
            # send sms
            code = str(uuid4())
            user_day.code = code
            user_day.notification_sent = True
            user_day.save()


class UserDay(BaseModel):
    user = ForeignKeyField(User)
    day = ForeignKeyField(Day)
    notes = TextField(null=True)
    code = CharField()
    notification_sent = BooleanField(default=False)


class Invite(BaseModel):
    code = CharField()


class UserInvite(BaseModel):
    user = ForeignKeyField(User)
    invite = ForeignKeyField(Invite)
    invited = CharField()
    fullfilled = DateTimeField(null=True)


def create_tables():
    tables = [Day, UserDay, User, Invite, UserInvite]

    DATABASE.connect()
    DATABASE.create_tables(tables)


def migrate_tables():
    DATABASE.evolve()
