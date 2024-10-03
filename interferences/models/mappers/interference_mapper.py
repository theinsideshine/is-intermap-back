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
            point_reference=interference.point_reference,  # Cambiado de `coord` a `point_reference`
            url_file=interference.url_file,
            interference=interference.interference  # Nuevo campo booleano
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
            existing_interference.point_reference = interference_request_dto.point_reference  # Cambiado de `coord` a `point_reference`
            existing_interference.url_file = interference_request_dto.url_file
            existing_interference.interference = interference_request_dto.interference  # Nuevo campo booleano

            # Debug para verificar la asignación de `url_file`
            print(f"Mapper - Existing Interference - url_file: {existing_interference.url_file}")
            
            return existing_interference
        else:
            interference = Interference(
                username=interference_request_dto.username,
                email=interference_request_dto.email,
                company=interference_request_dto.company,
                address_ref=interference_request_dto.address_ref,
                status=interference_request_dto.status,
                last=interference_request_dto.last,
                start=interference_request_dto.start,
                point_reference=interference_request_dto.point_reference,  # Cambiado de `coord` a `point_reference`
                url_file=interference_request_dto.url_file,
                interference=interference_request_dto.interference  # Nuevo campo booleano
            )

            # Debug para verificar la asignación de `url_file`
            print(f"Mapper - New Interference - url_file: {interference.url_file}")
            
            return interference

    @staticmethod
    def ResponseDtoToDict(response_dto):
        return {
            "id": response_dto.id,
            "username": response_dto.username,
            "email": response_dto.email,
            "company": response_dto.company,
            "address_ref": response_dto.address_ref,
            "status": response_dto.status,
            "last": response_dto.last,
            "start": response_dto.start,
            "point_reference": response_dto.point_reference,  # Cambiado de `coord` a `point_reference`
            "url_file": response_dto.url_file,
            "interference": response_dto.interference  # Nuevo campo booleano
        }
