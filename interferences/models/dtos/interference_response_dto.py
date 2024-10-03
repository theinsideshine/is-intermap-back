class InterferenceResponseDTO:
    def __init__(self, id, username, email, company, address_ref, status, last, start, point_reference, url_file, interference):
        self.id = id
        self.username = username
        self.email = email
        self.company = company
        self.address_ref = address_ref
        self.status = status
        self.last = last
        self.start = start
        self.point_reference = point_reference  # Cambiado de `coord` a `point_reference`
        self.url_file = url_file
        self.interference = interference  # Nuevo campo booleano

