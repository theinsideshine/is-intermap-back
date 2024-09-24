from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Regexp

class UserCreateSchema(Schema):
    username = fields.Str(
        required=True, 
        validate=Length(min=4, max=20, error="El nombre de usuario debe tener entre 4 y 20 caracteres."),
        error_messages={
            "required": "El nombre de usuario es obligatorio.",
            "invalid": "El nombre de usuario es inválido."
        }
    )
    
    password = fields.Str(
        required=True, 
        validate=Length(min=6, error="La contraseña debe tener al menos 6 caracteres."),
        error_messages={
            "required": "La contraseña es obligatoria."
        }
    )

    role = fields.Str(required=True, validate=[
        Regexp(r'^(user|admin|superuser)$', error="El rol debe ser 'user' , 'admin' o 'superuser' ")
    ])
    
    
    cuit = fields.Str(
        required=True, 
        validate=[
            Length(equal=13, error="El CUIT debe tener exactamente 13 caracteres."),
            Regexp(r'^\d{2}-\d{8}-\d$', error="El CUIT debe tener el formato XX-XXXXXXXX-X.")
        ], 
        error_messages={
            "required": "El CUIT es obligatorio."
        }
    )
    
    email = fields.Email(
        required=True,
        error_messages={
            "required": "El correo electrónico es obligatorio.",
            "invalid": "El correo electrónico no es válido."
        }
    )
    
    name = fields.Str(
        required=True, 
        validate=Length(min=2, max=50, error="El nombre debe tener entre 2 y 50 caracteres."),
        error_messages={
            "required": "El nombre es obligatorio."
        }
    )
    
    address = fields.Str(
        required=True, 
        validate=Length(min=5, max=100, error="La dirección debe tener entre 5 y 100 caracteres."),
        error_messages={
            "required": "La dirección es obligatoria.",
            "invalid": "La dirección no es válida."
        }
    )
    
    phone = fields.Str(
        required=True, 
        validate=Length(min=7, max=15, error="El teléfono debe tener entre 7 y 15 caracteres."),
        error_messages={
            "required": "El teléfono es obligatorio.",
            "invalid": "El teléfono no es válido."
        }
    )
    
    mobile = fields.Str(
        required=True, 
        validate=Length(min=7, max=15, error="El número de móvil debe tener entre 7 y 15 caracteres."),
        error_messages={
            "required": "El número de móvil es obligatorio.",
            "invalid": "El número de móvil no es válido."
        }
    )
    
    contact = fields.Str(
        required=True, 
        validate=Length(min=2, max=50, error="El contacto debe tener entre 2 y 50 caracteres."),
        error_messages={
            "required": "El contacto es obligatorio.",
            "invalid": "El contacto no es válido."
        }
    )

    @validates('username')
    def validate_username(self, value):
        if "admin" in value.lower():
            raise ValidationError("El nombre de usuario no puede contener 'admin'.")

    @validates('name')
    def validate_name(self, value):
        if not value.strip():  # Verifica si la cadena está vacía o contiene solo espacios
            raise ValidationError("El nombre no puede estar vacío.")

    @validates('address')
    def validate_address(self, value):
        if not value.strip():
            raise ValidationError("La dirección no puede estar vacía.")

    @validates('phone')
    def validate_phone(self, value):
        if not value.strip():
            raise ValidationError("El teléfono no puede estar vacío.")
            
    @validates('mobile')
    def validate_mobile(self, value):
        if not value.strip():
            raise ValidationError("El número de móvil no puede estar vacío.")

    @validates('contact')
    def validate_contact(self, value):
        if not value.strip():
            raise ValidationError("El contacto no puede estar vacío.")


# Instancia del esquema
user_create_schema = UserCreateSchema()

