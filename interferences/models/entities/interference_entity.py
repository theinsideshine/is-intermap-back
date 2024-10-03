class Interference:
    def __init__(self, id=None, username=None, email=None, company=None, address_ref=None, status=None, last=None, start=None, point_reference=None, url_file=None, interference=None):
        self.id = id  # ID será opcional
        self.username = username
        self.email = email
        self.company = company
        self.address_ref = address_ref
        self.status = status
        self.last = last  # Fecha
        self.start = start  # Fecha
        self.point_reference = point_reference  # Cambiado de `coord` a `point_reference`
        self.url_file = url_file  # URL del archivo asociado
        self.interference = interference  # Nuevo campo booleano
