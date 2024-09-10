from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Regexp

class UserRequestSchema(Schema):
    username = fields.Str(required=True, validate=Length(min=4, max=20))    
   
    
    # Validación de CUIT con longitud exacta y expresión regular para formato
    cuit = fields.Str(required=True, validate=[
        Length(equal=13, error="El CUIT debe tener exactamente 13 caracteres."),
        Regexp(r'^\d{2}-\d{8}-\d$', error="El CUIT debe tener el formato XX-XXXXXXXX-X.")
    ])
    
    role = fields.Str(required=True, validate=[
        Regexp(r'^(user|admin|superuser)$', error="El rol debe ser 'user' o 'admin'.")
    ])
    
    email = fields.Email(required=True)
    
    name = fields.Str(
        required=True, 
        error_messages={
            "required": "El nombre es obligatorio."
        }
    )
    
    address = fields.Str()
    phone = fields.Str()
    mobile = fields.Str()
    contact = fields.Str()

    @validates('username')
    def validate_username(self, value):
        if "admin" in value.lower():
            raise ValidationError("El nombre de usuario no puede contener 'admin'.")

# Instancia del esquema
user_request_schema = UserRequestSchema()

