from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from users.auth.auth_decorators import role_required

bp = Blueprint('status', __name__)

@bp.route('/status', methods=['GET'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@role_required('user')  # Asegúrate de que el rol sea 'admin'
def status():
    return "Estoy vivo", 200

