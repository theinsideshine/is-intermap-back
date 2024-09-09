from users.models.dto.user_request_dto import UserRequestDto
from users.models.dto.user_response_dto import UserResponseDto
from users.models.entities.user_entity import User

class UserMapper:
    @staticmethod
    def to_entity(user_request_dto: UserRequestDto) -> User:
        return User(
            username=user_request_dto.username,
            password=user_request_dto.password,
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
    def to_dto(user: User) -> UserResponseDto:
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
