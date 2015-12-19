import sqlite3
import datetime
from peewee import *

db = SqliteDatabase("database.db")

class Image(Model):
    image_name = CharField(unique=True)
    image_location = CharField(unique=True)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def create_tables():
    db.connect()
    try:
        Image.create_table()
    except:
        pass


