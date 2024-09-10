from flask import Blueprint, jsonify
from users.auth.auth_decorators import roles_required, any_role_required
from flask_jwt_extended import jwt_required

bp = Blueprint('api', __name__)

@bp.route('/status', methods=['GET'])
@any_role_required
def status():
    return "Estoy vivo", 200

@bp.route('/admin-super-data', methods=['GET'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin', 'superuser')
def admin_super_data():
    return jsonify({"data": "Información confidencial para admins y superusuarios"}), 200

@bp.route('/admin-data', methods=['GET'])
@jwt_required()  # Asegúrate de que el JWT esté presente
@roles_required('admin')
def admin_data():
    return jsonify({"data": "Información confidencial para admins"}), 200