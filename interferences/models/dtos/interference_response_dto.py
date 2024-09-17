class InterferenceResponseDTO:
    def __init__(self, id, username, email, company, address_ref, status, last, start, polygon_coords, coord, tolerance, url_file):
        self.id = id
        self.username = username
        self.email = email
        self.company = company
        self.address_ref = address_ref
        self.status = status
        self.last = last
        self.start = start
        self.polygon_coords = polygon_coords
        self.coord = coord
        self.tolerance = tolerance
        self.url_file = url_file
