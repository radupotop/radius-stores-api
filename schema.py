from marshmallow import Schema, fields, validate


class PostcodeSchema(Schema):
    name = fields.Str()
    postcode = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
