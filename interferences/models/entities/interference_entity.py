class Interference:
    def __init__(self, id,  username, email, company, address_ref, status, last, start, polygon_coords, coord, tolerance, url_file, ):
        self.id = id  # ID será opcional, útil cuando crees una nueva interferencia
        self.username = username
        self.email = email
        self.company = company
        self.address_ref = address_ref
        self.status = status
        self.last = last  # Fecha
        self.start = start  # Fecha
        self.polygon_coords = polygon_coords  # Lista de coordenadas del polígono
        self.coord = coord  # Coordenada de un punto (latitud y longitud)
        self.tolerance = tolerance  # Tolerancia en metros
        self.url_file = url_file  # URL del archivo asociado

    def __repr__(self):
        return f"<Interference(username={self.username}, email={self.email}, company={self.company}, address_ref={self.address_ref}, status={self.status}, last={self.last}, start={self.start}, tolerance={self.tolerance}, url_file={self.url_file})>"
