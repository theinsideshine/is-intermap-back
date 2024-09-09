# users/dto/user_request_dto.py
class UserRequestDto:
    def __init__(self, username, password, role, cuit, name, address, phone, mobile, contact, email):
        self.username = username
        self.password = password
        self.role = role
        self.cuit = cuit
        self.name = name
        self.address = address
        self.phone = phone
        self.mobile = mobile
        self.contact = contact
        self.email = email
