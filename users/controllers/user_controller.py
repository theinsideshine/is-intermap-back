from flask import Blueprint, jsonify, request, current_app
from users.models.mappers.user_mapper import UserMapper
from users.models.dtos.user_request_dto import UserRequestDto
from users.models.dtos.user_dto import UserDTO
from users.schemas.user_create_schema import user_create_schema  # Importamos el esquema
from users.schemas.user_request_schema import user_request_schema  # Importamos el esquema
from marshmallow import ValidationError
from users.auth.auth_service import AuthService
from users.repositories.user_repository import Database

from users.models.dtos.user_response_dto import UserResponseDto
from users.services.user_service import UserService
from flask_jwt_extended import jwt_required
from users.auth.auth_decorators import roles_required
import os

# Definir el Blueprint
bp = Blueprint('user_controller', __name__)

# Este método se ejecuta antes de cada solicitud en este blueprint
@bp.before_app_request  
def setup():
    current_dir = os.path.dirname(__file__)  # Directorio actual
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Subir 2 niveles
    db_name = current_app.config['DB_NAME']
    db_path = os.path.join(project_root, 'database', db_name)

    # Imprime la ruta para depuración
    print(f"Database path: {db_path}")

    global user_service, db , auth
    user_service = UserService(db_path)
    db = Database(db_path)
    auth = AuthService(db)

# Endpoint para obtener todos los usuarios
@bp.route('/users', methods=['GET'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def get_users():
    try:
        response_dtos = user_service.get_all_users()        
        return jsonify([response_dto.__dict__ for response_dto in response_dtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para obtener usuarios paginados
@bp.route('/users/page/<int:page>', methods=['GET'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def get_users_paginated(page):
    try:
        page_size = 5  # Tamaño de la página, puedes hacerlo dinámico si lo prefieres
        paginated_result = user_service.get_users_paginated(page, page_size)

        response = {
            "content": paginated_result["users"],  # Lista de usuarios
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
            "sort": {
                "empty": True,
                "sorted": False,
                "unsorted": True
            },
            "first": page == 0,
            "numberOfElements": len(paginated_result["users"]),
            "empty": len(paginated_result["users"]) == 0
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/users/<username>', methods=['GET'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def get_user(username):
    try:
        user_response_dto = user_service.get_user(username)
        if user_response_dto:
            return jsonify(user_response_dto.__dict__), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para crear un usuario
@bp.route('/users', methods=['POST'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def create():
    try:
        # Validar los datos recibidos
        data = user_create_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data.get('username')
    email = data.get('email')

    if auth.user_exists(username):
        return jsonify({"error": "El usuario ya existe"}), 400
    
    if auth.email_exists(email):
        return jsonify({"error": "El email ya existe"}), 400

    # Crear el UserDTO usando el diccionario 'data'
    user_dto = UserDTO(**data)   

    auth.register_user(user_dto)
    return jsonify({"message": "Usuario registrado exitosamente"}), 201


@bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def update_user(id):
    try:
        # Validar los datos recibidos
        data = request.json  # Obtener los datos sin validación aún
        print(f"Datos recibidos en el request: {data}")  # Imprimir los datos crudos del request
        data = user_request_schema.load(data)  # Validar los datos
        print(f"Datos validados: {data}")  # Imprimir los datos validados
    except ValidationError as err:
        print(f"Errores de validación: {err.messages}")  # Imprimir los errores de validación
        return jsonify(err.messages), 400    

    try: 
        user_request_dto = UserRequestDto(**data)
        print(f"DTO para actualización: {user_request_dto}")  # Imprimir el objeto DTO
        user_response_dto = user_service.update_user(id, user_request_dto)
        if user_response_dto:
            print(f"Usuario actualizado: {user_response_dto}")  # Imprimir el usuario actualizado
            return jsonify(user_response_dto.__dict__), 200
        print("Usuario no encontrado")  # Mensaje si no se encuentra el usuario
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"Error durante la actualización: {str(e)}")  # Imprimir cualquier excepción
        return jsonify({'error': str(e)}), 400
  



@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def delete_user(user_id):
    try:
        success = user_service.delete_user(user_id)
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
