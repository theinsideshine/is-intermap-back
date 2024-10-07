from interferences.models.entities.interference_entity import Interference
from interferences.models.dtos import InterferenceRequestDTO, InterferenceResponseDTO
from interferences.models.mappers.interference_mapper import InterferenceMapper
from interferences.repositories.interference_repository import Database
from datetime import datetime

class InterferenceService:
    def __init__(self, db_path):
        self.interference_repository = Database(db_path)  # Inicializamos con el path de la base de datos

    def get_all_interferences(self):
        # Llamamos al método del repositorio para obtener todas las interferencias
        interferences = self.interference_repository.get_all_interferences()
        return [InterferenceMapper.EntityTo_ResponseDto(interference) for interference in interferences]

    def create_interference(self, interference_request_dto: InterferenceRequestDTO):
        # Aquí puedes establecer las fechas a la fecha actual
        current_date = datetime.now().strftime('%Y-%m-%d')  # O el formato que necesites
        interference = InterferenceMapper.RequestDtoTo_entity(interference_request_dto)
        
        # Establecer fechas en la entidad
        interference.last = current_date
        interference.start = current_date
        interference.status = "open"

        created_interference = self.interference_repository.create_interference(interference)
        return InterferenceMapper.EntityTo_ResponseDto(created_interference)




    def get_interference(self, id):
        interference = self.interference_repository.get_interference(id)
        if interference:
            return InterferenceMapper.EntityTo_ResponseDto(interference)
        return None

    def update_interference(self, id, interference_request_dto: InterferenceRequestDTO):
        # Debug para verificar el DTO recibido
        print(f"Service - url_file: {interference_request_dto.url_file}")

        # Aquí puedes establecer las fechas a la fecha actual
        current_date = datetime.now().strftime('%Y-%m-%d')  # O el formato que necesites

        # Obtén la interferencia existente
        interference = self.interference_repository.get_interference(id)

        print(f"Service - interference.last: {interference.last}")
        print(f"Service - interference.start: {interference.start}")
         # Establecer fechas en la entidad
      
        interference_request_dto.start = interference.start 
        interference_request_dto.last =  current_date
        print(f"Service - get_interference(id): {interference}")

        if interference:
            # Actualiza la interferencia existente con los datos del DTO
            updated_interference = InterferenceMapper.RequestDtoTo_entity(interference_request_dto, existing_interference=interference)
            
            # Debug para verificar que el mapeo fue correcto
            print(f"Mapped Entity - url_file: {updated_interference.url_file}")

            # Actualiza la interferencia en el repositorio
            updated_interference = self.interference_repository.update_interference(updated_interference)
            updated_interference.id = id
            
            # Devuelve la entidad actualizada convertida a DTO
            return InterferenceMapper.EntityTo_ResponseDto(updated_interference)
        return None

    
    def get_interferences_paginated(self, page, page_size):
        # Obtener el número total de interferencias
        total_interferences = self.interference_repository.count_interferences()
        print("total interferencias:",total_interferences)
        total_pages = (total_interferences + page_size - 1) // page_size  # Calcular el total de páginas
        print("total paginas:",total_pages)
        # Calcular si esta es la última página
        is_last = (page + 1) >= total_pages

        # Obtener las interferencias paginadas
        interferences = self.interference_repository.get_interferences_by_page(page, page_size)

        print(interferences)

        # Convertir las interferencias a ResponseDto y luego a diccionarios en una sola línea
        interferences_response = [
            InterferenceMapper.ResponseDtoToDict(InterferenceMapper.EntityTo_ResponseDto(interference))
            for interference in interferences
        ]

        return {
            "interferences": interferences_response,
            "total_pages": total_pages,
            "total_elements": total_interferences,
            "is_last": is_last
        }

    def get_interferences_by_username_paginated(self, username, page, page_size):
        # Obtener el número total de interferencias para el usuario específico
        total_interferences = self.interference_repository.count_interferences_by_username(username)
        print("Total interferencias para el usuario:", total_interferences)
        
        total_pages = (total_interferences + page_size - 1) // page_size  # Calcular el total de páginas
        print("Total páginas para el usuario:", total_pages)
        
        # Calcular si esta es la última página
        is_last = (page + 1) >= total_pages

        # Obtener las interferencias paginadas para el usuario
        interferences = self.interference_repository.get_interferences_by_username_and_page(username, page, page_size)

        print(interferences)

        # Convertir las interferencias a ResponseDto y luego a diccionarios en una sola línea
        interferences_response = [
            InterferenceMapper.ResponseDtoToDict(InterferenceMapper.EntityTo_ResponseDto(interference))
            for interference in interferences
        ]

        return {
            "interferences": interferences_response,
            "total_pages": total_pages,
            "total_elements": total_interferences,
            "is_last": is_last
        }





    def delete_interference(self, id):
        interference = self.interference_repository.get_interference(id)
        if interference:
            self.interference_repository.delete_interference(id)
            return True
        return False
