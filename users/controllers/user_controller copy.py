from flask import Blueprint, jsonify, request, current_app
from users.models.mappers.user_mapper import UserMapper
from users.models.dto.user_request_dto import UserRequestDto
from users.models.dto.user_dto import UserDTO
from users.schemas.user_schema import user_schema  # Importamos el esquema
from marshmallow import ValidationError

from users.models.dto.user_response_dto import UserResponseDto
from users.services.user_service import UserService
from flask_jwt_extended import jwt_required
from users.auth.auth_decorators import role_required
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

    global user_service
    user_service = UserService(db_path)

# Endpoint para obtener todos los usuarios
@bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = user_service.get_all_users()
        response_dtos = [UserMapper.to_dto(user) for user in users]
        return jsonify([response_dto.__dict__ for response_dto in response_dtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para crear un usuario
@bp.route('/users', methods=['POST'])
def create_user():
    try:
        # Validar los datos recibidos
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        data = request.get_json()
        user_dto = UserDTO(**data)
        user = user_service.create_user(user_dto)
        response_dto = UserMapper.EntityTo_UserResponseDto(user)
        return jsonify(response_dto.__dict__), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para obtener un usuario por su username
@bp.route('/users/<username>', methods=['GET'])
def get_user(username):
    try:
        user = user_service.get_user(username)
        if user:
            response_dto = UserMapper.to_dto(user)
            return jsonify(response_dto.__dict__), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para actualizar un usuario
@bp.route('/users/<username>', methods=['PUT'])
def update_user(username):
    try:
        data = request.get_json()
        user_request_dto = UserRequestDto(**data)
        user = user_service.update_user(username, user_request_dto)
        if user:
            response_dto = UserMapper.to_dto(user)
            return jsonify(response_dto.__dict__), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para eliminar un usuario
@bp.route('/users/<username>', methods=['DELETE'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@role_required('admin')  # Asegúrate de que el rol sea 'admin'
def delete_user(username):
    try:
        success = user_service.delete_user(username)
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
