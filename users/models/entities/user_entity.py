class User:
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
