from interferences.models.entities.interference_entity import Interference
from interferences.models.dtos import InterferenceRequestDTO, InterferenceResponseDTO
from interferences.models.mappers.interference_mapper import InterferenceMapper
from interferences.repositories.interference_repository import Database

class InterferenceService:
    def __init__(self, db_path):
        self.interference_repository = Database(db_path)  # Inicializamos con el path de la base de datos

    def get_all_interferences(self):
        # Llamamos al método del repositorio para obtener todas las interferencias
        interferences = self.interference_repository.get_all_interferences()
        return [InterferenceMapper.EntityTo_ResponseDto(interference) for interference in interferences]

    def create_interference(self, interference_request_dto: InterferenceRequestDTO):
        # Convierte el DTO a entidad
        interference = InterferenceMapper.RequestDtoTo_entity(interference_request_dto)
        # Llama al repositorio para guardar la entidad y obtener el ID generado
        created_interference = self.interference_repository.create_interference(interference)
        # Convierte la entidad creada a DTO y retorna
        return InterferenceMapper.EntityTo_ResponseDto(created_interference)


    def get_interference(self, id):
        interference = self.interference_repository.get_interference(id)
        if interference:
            return InterferenceMapper.EntityTo_ResponseDto(interference)
        return None

    def update_interference(self, id, interference_request_dto: InterferenceRequestDTO):
        # Obtén la interferencia existente
        interference = self.interference_repository.get_interference(id)
        if interference:
            # Actualiza la interferencia existente con los datos del DTO
            updated_interference = InterferenceMapper.RequestDtoTo_entity(interference_request_dto, existing_interference=interference)
            # Actualiza la interferencia en el repositorio y obtén la entidad actualizada
            updated_interference = self.interference_repository.update_interference(updated_interference)
            updated_interference.id = id
            # Devuelve la entidad actualizada convertida a DTO
            return InterferenceMapper.EntityTo_ResponseDto(updated_interference)
        return None




    def delete_interference(self, id):
        interference = self.interference_repository.get_interference(id)
        if interference:
            self.interference_repository.delete_interference(id)
            return True
        return False
