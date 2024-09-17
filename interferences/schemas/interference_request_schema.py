from marshmallow import fields, Schema, post_load, validates, ValidationError

import json

class InterferenceRequestSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    company = fields.Str(required=True)
    address_ref = fields.Str(required=True)
    status = fields.Str(required=True)
    last = fields.Date(required=True)
    start = fields.Date(required=True)
    polygon_coords = fields.List(fields.List(fields.Float()), required=True)  # Lista de listas de floats
    coord = fields.List(fields.Float(), required=True)  # Lista de floats
    tolerance = fields.Int(required=True)
    url_file = fields.Str(required=True)  # Cambio a Str para almacenar el nombre del archivo

    @validates('url_file')
    def validate_url_file(self, value):
        # Verificar si el nombre del archivo termina con '.kml'
        if not value.lower().endswith('.kml'):
            raise ValidationError('El nombre del archivo debe terminar con .kml.')

    @post_load
    def process_input(self, data, **kwargs):
        # Convertir 'polygon_coords' y 'coord' de cadena JSON a listas, si es necesario
        if isinstance(data.get('polygon_coords'), str):
            data['polygon_coords'] = json.loads(data['polygon_coords'])
        if isinstance(data.get('coord'), str):
            data['coord'] = json.loads(data['coord'])
        return data

