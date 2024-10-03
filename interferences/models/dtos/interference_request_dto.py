class InterferenceRequestDTO:
    def __init__(self, username, email, company, address_ref, point_reference, url_file, interference, last=None, start=None , status=None,):
        self.username = username
        self.email = email
        self.company = company
        self.address_ref = address_ref
        self.status = status    
        self.last = last  # Campo opcional para la última fecha
        self.start = start  # Campo opcional para la fecha de inicio    
        self.point_reference = point_reference  # Cambiado de `coord` a `point_reference`
        self.url_file = url_file
        self.interference = interference  # Nuevo campo booleano
        

        # Debug para el campo `url_file`
        print(f"DTO - url_file: {self.url_file}")


