from peewee import SqliteDatabase, Model, TextField, IntegerField

db = SqliteDatabase('test_db.db')


class BaseModel(Model):
    class Meta:
        database = db


class Chromosome(BaseModel):
    name = TextField()
    sequence = TextField()
    is_circular = IntegerField()
    trunc512 = TextField()
    md5 = TextField()
    size = IntegerField()
