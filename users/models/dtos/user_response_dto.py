# users/dto/user_response_dto.py
class UserResponseDto:
    def __init__(self, id, username, role, cuit, name, address, phone, mobile, contact, email):
        self.id = id
        self.username = username
        self.role = role
        self.cuit = cuit
        self.name = name
        self.address = address
        self.phone = phone
        self.mobile = mobile
        self.contact = contact
        self.email = email
