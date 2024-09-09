class UserDTO:
    def __init__(self, username, password, role, cuit=None, name=None, address=None, phone=None, mobile=None, contact=None, email=None):
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

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'cuit': self.cuit,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'mobile': self.mobile,
            'contact': self.contact,
            'email': self.email
        }

