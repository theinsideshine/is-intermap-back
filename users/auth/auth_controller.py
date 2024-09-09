from flask import Blueprint, current_app, request, jsonify
from users.auth.auth_service import Auth
from users.repositories.user_repository import Database
from users.models.dto.user_dto import UserDTO
from users.schemas.user_schema import user_schema  # Importamos el esquema
from marshmallow import ValidationError
import os

bp = Blueprint('auth', __name__)

@bp.before_app_request  
def setup():
    current_dir = os.path.dirname(__file__)  # Directorio actual
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Subir 2 niveles
    db_name = current_app.config['DB_NAME']
    db_path = os.path.join(project_root, 'database', db_name)

    # Imprime la ruta para depuración
    print(f"Database path: {db_path}")

    global db, auth
    db = Database(db_path)
    auth = Auth(db)

@bp.route('/register', methods=['POST'])
def register():
    try:
        # Validar los datos recibidos
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    username = data.get('username')
    password = data.get('password')    
    cuit = data.get('cuit')
    name = data.get('name')
    address = data.get('address')
    phone = data.get('phone')
    mobile = data.get('mobile')
    contact = data.get('contact')
    email = data.get('email')

    # Forzar el rol a 'user'
    role = 'user'

    if auth.user_exists(username):
        return jsonify({"error": "El usuario ya existe"}), 400
    
    if auth.email_exists(email):
        return jsonify({"error": "El email ya existe"}), 400
    

    user_dto = UserDTO(
        username=username,
        password=password,
        role=role,
        cuit=cuit,
        name=name,
        address=address,
        phone=phone,
        mobile=mobile,
        contact=contact,
        email=email
    )

    auth.register_user(user_dto)
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return jsonify({"error": "Username and password are required"}), 400

    user = auth.login_user(username, password)
    if user:
        access_token = auth.create_token(user)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401