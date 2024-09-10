from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

def roles_required(*roles):
    """Decorator to check if the user has one of the specified roles."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            jwt = get_jwt()
            if not jwt or jwt['sub'].get('role') not in roles:
                return jsonify({"error": "Acceso denegado: Rol no autorizado"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def any_role_required(fn):
    """Decorator to ensure the user has a valid JWT, without checking roles."""
    @wraps(fn)
    @jwt_required()  # Asegúrate de que el JWT esté presente
    def wrapper(*args, **kwargs):
        user_identity = get_jwt_identity()
        # Aquí puedes realizar cualquier verificación adicional si es necesario
        # Para ahora, simplemente devolvemos el resultado
        return fn(*args, **kwargs)
    return wrapper

