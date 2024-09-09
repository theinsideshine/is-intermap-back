from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            jwt = get_jwt()
            if not jwt or jwt['sub'].get('role') != role:
                return jsonify({"error": "Acceso denegado: Rol no autorizado"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
