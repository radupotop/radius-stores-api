from marshmallow import Schema, fields, validate


class PostcodeSchema(Schema):
    name = fields.Str()
    postcode = fields.Str()
    longitude = fields.Float()
    latitude = fields.Float()
    eastings = fields.Int()
    northings = fields.Int()
