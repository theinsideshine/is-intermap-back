from flask import Blueprint, jsonify, request, current_app
from interferences.models.mappers.interference_mapper import InterferenceMapper
from interferences.models.dtos.interference_request_dto import InterferenceRequestDTO
from interferences.schemas.interference_request_schema import InterferenceRequestSchema
from marshmallow import ValidationError
from interferences.services.interference_service import InterferenceService
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity, get_jwt
from users.auth.auth_decorators import roles_required
from datetime import datetime
import os

# Definir el Blueprint
bp = Blueprint('interference_controller', __name__)

# Este método se ejecuta antes de cada solicitud en este blueprint
@bp.before_app_request
def setup():
    current_dir = os.path.dirname(__file__)  # Directorio actual
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Subir 2 niveles
    db_name = current_app.config['DB_NAME']
    db_path = os.path.join(project_root, 'database', db_name)

    # Imprime la ruta para depuración
    print(f"Database path: {db_path}")

    global interference_service
    interference_service = InterferenceService(db_path)


# Endpoint para obtener todas las interferencias
@bp.route('/interferences', methods=['GET'])
def get_interferences():
    try:
        response_dtos = interference_service.get_all_interferences()
        return jsonify([response_dto.__dict__ for response_dto in response_dtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para obtener una interferencia por ID
@bp.route('/interferences/<int:interference_id>', methods=['GET'])
def get_interference(interference_id):
    try:
        response_dto = interference_service.get_interference(interference_id)
        if response_dto:
            return jsonify(response_dto.__dict__), 200
        return jsonify({'error': 'Interference not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


# Endpoint para crear una nueva interferencia
@bp.route('/interferences', methods=['POST'])
@jwt_required()  # Requiere un JWT para autenticar
@roles_required('admin', 'user')   
def create_interference():
    try:
        # Crear una instancia del esquema y validar los datos recibidos
        schema = InterferenceRequestSchema()
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Crear el InterferenceRequestDTO usando el diccionario 'data'
    interference_request_dto = InterferenceRequestDTO(**data)

    try:
        response_dto = interference_service.create_interference(interference_request_dto)
        return jsonify(response_dto.__dict__), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

@bp.route('/interferences/page/<int:page>', methods=['GET'])
@jwt_required()  # Requiere un JWT para autenticar
def get_interferences_paginated(page):
    try:
       # Obtiene el JWT identity, que parece contener tanto el username como el rol
        current_user = get_jwt_identity()        

        # Extrae el rol directamente desde el objeto retornado por get_jwt_identity()
        role = current_user.get('role', None)
        username = current_user.get('username', None)

        # Verifica si el usuario tiene el rol de 'admin'
        is_admin = role == 'admin'
        
        # Imprime para depuración
        print(f"Username: {username}, Admin: {is_admin}")
       

        page_size = 5  # Tamaño de la página

        # Si el usuario es admin, traer todas las interferencias
        if is_admin:
            paginated_result = interference_service.get_interferences_paginated(page, page_size)
        else:
            # Si no es admin, traer solo las interferencias del usuario actual
            paginated_result = interference_service.get_interferences_by_username_paginated(username, page, page_size)       


        response = {
            "content": paginated_result["interferences"],
            "pageable": {
                "sort": {
                    "empty": True,
                    "sorted": False,
                    "unsorted": True
                },
                "offset": page * page_size,
                "pageNumber": page,
                "pageSize": page_size,
                "paged": True,
                "unpaged": False
            },
            "last": paginated_result["is_last"],
            "totalPages": paginated_result["total_pages"],
            "totalElements": paginated_result["total_elements"],
            "size": page_size,
            "number": page,
            "first": page == 0,
            "numberOfElements": len(paginated_result["interferences"]),
            "empty": len(paginated_result["interferences"]) == 0
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para actualizar una interferencia
@bp.route('/interferences/<int:interference_id>', methods=['PUT'])
@jwt_required()  # Requiere un JWT para autenticar
@roles_required('admin')  # Solo admin puede actualizar interferencias
def update_interference(interference_id):
    try:
        # Crear una instancia del esquema y validar los datos recibidos
        schema = InterferenceRequestSchema()
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    interference_request_dto = InterferenceRequestDTO(**data)    
    try:
        response_dto = interference_service.update_interference(interference_id, interference_request_dto)
        if response_dto:
            return jsonify(response_dto.__dict__), 200
        return jsonify({'error': 'Interference not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Endpoint para eliminar una interferencia
@bp.route('/interferences/<int:interference_id>', methods=['DELETE'])
@jwt_required()  # Requiere un JWT para autenticar
@roles_required('admin')  # Solo admin puede eliminar interferencias
def delete_interference(interference_id):
    try:
        success = interference_service.delete_interference(interference_id)
        if success:
            return jsonify({'message': 'Interference deleted successfully'}), 200
        return jsonify({'error': 'Interference not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
