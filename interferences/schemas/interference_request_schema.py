from marshmallow import fields, Schema, post_load, validates, ValidationError
import json

class InterferenceRequestSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    company = fields.Str(required=True)
    address_ref = fields.Str(required=True)
    status = fields.Str(allow_none=True)
    last = fields.Date(allow_none=True)  # Campo opcional (puede ser null)
    start = fields.Date(allow_none=True)  # Campo opcional (puede ser null)
    point_reference = fields.List(fields.Float(), required=True)  # Lista de floats para point_reference
    url_file = fields.Str(required=True)  # Campo para almacenar el nombre del archivo
    interference = fields.Bool(required=True)  # Campo booleano agregado

    @validates('url_file')
    def validate_url_file(self, value):
        # Verificar si el nombre del archivo termina con '.kml'
        if not value.lower().endswith('.kml'):
            raise ValidationError('El nombre del archivo debe terminar con .kml')

    @post_load
    def process_input(self, data, **kwargs):
        # Debug para verificar el campo `url_file`
        print(f"Schema - url_file: {data.get('url_file')}")
        
        # Convertir 'point_reference' de cadena JSON a lista, si es necesario
        if isinstance(data.get('point_reference'), str):
            data['point_reference'] = json.loads(data['point_reference'])
        return data


