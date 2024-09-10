from users.models.entities.user_entity import User
from users.models.dto.user_dto import UserDTO
from flask_jwt_extended import create_access_token
import bcrypt

class AuthService:
    def __init__(self, db):
        self.db = db

    def user_exists(self, username):
        user = self.db.get_user(username)
        return user is not None
    
    def email_exists(self, email):
        email = self.db.get_email(email)
        return email is not None

    def register_user(self, user_dto: UserDTO):
        hashed_password = bcrypt.hashpw(user_dto.password.encode('utf-8'), bcrypt.gensalt())
        user = User(
            username=user_dto.username,
            password=hashed_password.decode('utf-8'),
            role=user_dto.role,
            cuit=user_dto.cuit,
            name=user_dto.name,
            address=user_dto.address,
            phone=user_dto.phone,
            mobile=user_dto.mobile,
            contact=user_dto.contact,
            email=user_dto.email
        )
        self.db.create_user(user)

    def login_user(self, username, password):
        user = self.db.get_user(username)
        if user:
            stored_password_bytes = user.password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_bytes):
                return user  # Devuelve el objeto User en lugar de un booleano
        return None  # Devuelve None si las credenciales son incorrectas

    def create_token(self, user: User):
        return create_access_token(identity={'username': user.username, 'role': user.role})