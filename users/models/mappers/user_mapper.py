from users.models.dtos.user_request_dto import UserRequestDto
from users.models.dtos.user_response_dto import UserResponseDto
from users.models.entities.user_entity import User
from users.models.dtos.user_dto import UserDTO

class UserMapper:
    @staticmethod
    def UserRequestDtoTo_entity(user_request_dto: UserRequestDto, existing_user: User) -> User:
        return User(
            username=user_request_dto.username,
            password=existing_user.password,
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
    def UserRequestUpdateDtoTo_entity(user_request_dto: UserRequestDto, existing_user: User) -> User:
        return User(
            id=existing_user.id,
            username=user_request_dto.username,
            password=existing_user.password,
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
    def EntityTo_UserResponseDto(user: User) -> UserResponseDto:
        return UserResponseDto(
            id=user.id,
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
    
    # Nuevo método para convertir UserResponseDto en un diccionario serializable
    @staticmethod
    def UserResponseDtoToDict(user_response_dto: UserResponseDto) -> dict:
        return {
            "id": user_response_dto.id,
            "username": user_response_dto.username,
            "role": user_response_dto.role,
            "cuit": user_response_dto.cuit,
            "name": user_response_dto.name,
            "address": user_response_dto.address,
            "phone": user_response_dto.phone,
            "mobile": user_response_dto.mobile,
            "contact": user_response_dto.contact,
            "email": user_response_dto.email
        }
