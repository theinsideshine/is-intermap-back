from users.models.entities.user_entity import User
from users.models.dtos.user_dto import UserDTO
from users.models.mappers.user_mapper import UserMapper
from users.repositories.user_repository import Database
import bcrypt

class UserService:
    def __init__(self, db_path):
        self.user_repository = Database(db_path)  # Inicializamos con el path de la base de datos

    def get_all_users(self):
        # Llamamos al método del repositorio para obtener todos los usuarios
        users = self.user_repository.get_all_users()
        return [UserMapper.EntityTo_UserResponseDto(user) for user in users]


    def get_user(self, username):
        user = self.user_repository.get_user(username)
        if user:
            return UserMapper.EntityTo_UserResponseDto(user)
        return None

    def update_user(self, username, user_request_dto):
        user = self.user_repository.get_user(username)
        if user:
            # Pasamos el usuario existente para conservar la contraseña si no se proporciona una nueva
            updated_user = UserMapper.UserRequestUpdateDtoTo_entity(user_request_dto, existing_user=user)
            self.user_repository.update_user(updated_user)
            return UserMapper.EntityTo_UserResponseDto(updated_user)
        return None


    def delete_user(self, username):
        user = self.user_repository.get_user(username)
        if user:
            self.user_repository.delete_user(username)
            return True
        return False
