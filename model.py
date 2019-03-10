import peewee as pw

db = pw.SqliteDatabase('postcodes.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class Postcodes(BaseModel):
    name = pw.CharField(unique=True)
    postcode = pw.CharField()
    longitude = pw.FloatField(null=True)
    latitude = pw.FloatField(null=True)
    eastings = pw.IntegerField(null=True)
    northings = pw.IntegerField(null=True)
