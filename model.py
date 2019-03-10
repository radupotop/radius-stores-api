import peewee as pw

db = pw.SqliteDatabase('postcodes.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Postcodes(BaseModel):
    name = pw.CharField()
    postcode = pw.CharField()
    latitude = pw.FloatField(null=True)
    longitude = pw.FloatField(null=True)
