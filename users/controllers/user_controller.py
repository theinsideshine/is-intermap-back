from flask import Blueprint, jsonify, request, current_app
from users.models.mappers.user_mapper import UserMapper
from users.models.dtos.user_request_dto import UserRequestDto
from users.models.dtos.user_dto import UserDTO
from users.schemas.user_schema import user_schema  # Importamos el esquema
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
def get_users():
    try:
        response_dtos = user_service.get_all_users()        
        return jsonify([response_dto.__dict__ for response_dto in response_dtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/users/<username>', methods=['GET'])
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
def create():
    try:
        # Validar los datos recibidos
        data = user_schema.load(request.json)
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


# Endpoint para actualizar un usuario
@bp.route('/users/<username>', methods=['PUT'])
def update_user(username):
    try:
        # Validar los datos recibidos
        data = user_request_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    try:
        #data = request.get_json()
        user_request_dto = UserRequestDto(**data)
        user_response_dto = user_service.update_user(username, user_request_dto)
        if user_response_dto:           
            return jsonify(user_response_dto.__dict__), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para eliminar un usuario
@bp.route('/users/<username>', methods=['DELETE'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin')  # Asegúrate de que el rol sea 'admin'
def delete_user(username):
    try:
        success = user_service.delete_user(username)
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
