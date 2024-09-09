from users.models.entities.user_entity import User
from users.models.mappers.user_mapper import UserMapper
from users.repositories.user_repository import Database

class UserService:
    def __init__(self, db_path):
        self.user_repository = Database(db_path)  # Inicializamos con el path de la base de datos

    def get_all_users(self):
        # Llamamos al método del repositorio para obtener todos los usuarios
        users = self.user_repository.get_all_users()
        return [UserMapper.to_dto(user) for user in users]

    def create_user(self, user_request_dto):
        user = UserMapper.to_entity(user_request_dto)
        self.user_repository.create_user(user)
        return UserMapper.to_dto(user)

    def get_user(self, username):
        user = self.user_repository.get_user(username)
        if user:
            return UserMapper.to_dto(user)
        return None

    def update_user(self, username, user_request_dto):
        user = self.user_repository.get_user(username)
        if user:
            updated_user = UserMapper.to_entity(user_request_dto)
            self.user_repository.create_user(updated_user)  # Usamos create_user para actualizar
            return UserMapper.to_dto(updated_user)
        return None

    def delete_user(self, username):
        user = self.user_repository.get_user(username)
        if user:
            self.user_repository.delete_user(username)
            return True
        return False
