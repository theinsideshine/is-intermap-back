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
    
    def get_users_paginated(self, page, page_size):
        total_users = self.user_repository.count_users()  # Obtener el número total de usuarios
        total_pages = (total_users + page_size - 1) // page_size  # Calcular el total de páginas
        
        # Calcular si esta es la última página
        is_last = (page + 1) >= total_pages

        # Obtener los usuarios paginados
        users = self.user_repository.get_users_by_page(page, page_size)

        # Convertir los usuarios a UserResponseDto y luego a diccionarios
        users_response = [
            UserMapper.UserResponseDtoToDict(UserMapper.EntityTo_UserResponseDto(user))
            for user in users
        ]

        return {
            "users": users_response,
            "total_pages": total_pages,
            "total_elements": total_users,
            "is_last": is_last
        }



    def get_user(self, username):
        user = self.user_repository.get_user(username)
        if user:
            return UserMapper.EntityTo_UserResponseDto(user)
        return None

    def update_user_by_username(self, username, user_request_dto):
        user = self.user_repository.get_user(username)
        if user:
            # Pasamos el usuario existente para conservar la contraseña si no se proporciona una nueva
            updated_user = UserMapper.UserRequestUpdateDtoTo_entity(user_request_dto, existing_user=user)
            self.user_repository.update_user(updated_user)
            return UserMapper.EntityTo_UserResponseDto(updated_user)
        return None
    
    def update_user(self, id, user_request_dto):
        user = self.user_repository.get_user_by_id(id)
        if user:
            # Pasamos el usuario existente para conservar la contraseña si no se proporciona una nueva
            updated_user = UserMapper.UserRequestUpdateDtoTo_entity(user_request_dto, existing_user=user)
            self.user_repository.update_user(updated_user)
            return UserMapper.EntityTo_UserResponseDto(updated_user)
        return None



    def delete_user_by_username(self, username):
        user = self.user_repository.get_user(username)
        if user:
            self.user_repository.delete_user(username)
            return True
        return False

    def delete_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        
        if user:
            self.user_repository.delete_user(user_id)
            return True
        
        return False
