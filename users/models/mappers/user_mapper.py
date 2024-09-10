from users.models.dto.user_request_dto import UserRequestDto
from users.models.dto.user_response_dto import UserResponseDto
from users.models.entities.user_entity import User
from users.models.dto.user_dto import UserDTO

class UserMapper:
    @staticmethod
    def UserRequestDtoTo_entity(user_request_dto: UserRequestDto, existing_user: User) -> User:
        # Solo se cambia el password si se proporciona uno nuevo en el DTO, caso contrario se conserva el existente.
        return User(
            username=user_request_dto.username,
            password=existing_user.password,  # Conserva el password existente
            role=user_request_dto.role,
            cuit=user_request_dto.cuit,
            name=user_request_dto.name,
            address=user_request_dto.address,
            phone=user_request_dto.phone,
            mobile=user_request_dto.mobile,
            contact=user_request_dto.contact,
            email=user_request_dto.email
        )
    
    @staticmethod
    def UserDtoTo_entity(user_dto: UserDTO) -> User:
        return User(
            username=user_dto.username,
            password=user_dto.password,
            role=user_dto.role,
            cuit=user_dto.cuit,
            name=user_dto.name,
            address=user_dto.address,
            phone=user_dto.phone,
            mobile=user_dto.mobile,
            contact=user_dto.contact,
            email=user_dto.email
        )

    @staticmethod
    def EntityTo_UserResponseDto(user: User) -> UserResponseDto:
        return UserResponseDto(
            username=user.username,
            role=user.role,
            cuit=user.cuit,
            name=user.name,
            address=user.address,
            phone=user.phone,
            mobile=user.mobile,
            contact=user.contact,
            email=user.email
        )
