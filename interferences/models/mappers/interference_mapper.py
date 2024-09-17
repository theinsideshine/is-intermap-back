from interferences.models.entities.interference_entity import Interference
from interferences.models.dtos import InterferenceRequestDTO, InterferenceResponseDTO

class InterferenceMapper:
    
    @staticmethod
    def EntityTo_ResponseDto(interference: Interference):
        return InterferenceResponseDTO(
            id=interference.id,
            username=interference.username,
            email=interference.email,
            company=interference.company,
            address_ref=interference.address_ref,
            status=interference.status,
            last=interference.last,
            start=interference.start,
            polygon_coords=interference.polygon_coords, 
            coord=interference.coord,
            tolerance=interference.tolerance,
            url_file=interference.url_file
        )

    @staticmethod
    def RequestDtoTo_entity(interference_request_dto: InterferenceRequestDTO, existing_interference: Interference = None):
        if existing_interference:
            # Actualizamos solo los campos que cambian
            existing_interference.username = interference_request_dto.username
            existing_interference.email = interference_request_dto.email
            existing_interference.company = interference_request_dto.company
            existing_interference.address_ref = interference_request_dto.address_ref
            existing_interference.status = interference_request_dto.status
            existing_interference.last = interference_request_dto.last
            existing_interference.start = interference_request_dto.start
            existing_interference.polygon_coords = interference_request_dto.polygon_coords
            existing_interference.coord = interference_request_dto.coord
            existing_interference.tolerance = interference_request_dto.tolerance
            existing_interference.url_file = interference_request_dto.url_file
            return existing_interference
        else:
            return Interference(
                username=interference_request_dto.username,
                email=interference_request_dto.email,
                company=interference_request_dto.company,
                address_ref=interference_request_dto.address_ref,
                status=interference_request_dto.status,
                last=interference_request_dto.last,
                start=interference_request_dto.start,
                polygon_coords=interference_request_dto.polygon_coords,
                coord=interference_request_dto.coord,
                tolerance=interference_request_dto.tolerance,
                url_file=interference_request_dto.url_file
            )
