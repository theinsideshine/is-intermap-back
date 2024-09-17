from marshmallow import Schema, fields

class InterferenceResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    company = fields.Str(dump_only=True)
    address_ref = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    start = fields.Date(dump_only=True)
    last = fields.Date(dump_only=True)
    polygon_coords = fields.List(fields.List(fields.Float()), dump_only=True)
    coord = fields.List(fields.Float(), dump_only=True)
    tolerance = fields.Float(dump_only=True)
    url_file = fields.Str(dump_only=True)
