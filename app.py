from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow  # Importar Marshmallow
from maps.controllers import intersection_controller, status_controller
from users.auth import auth_controller
from users.controllers import user_controller
from interferences.controllers import interference_controller 
from config import Config

# Inicializar la aplicación Flask
app = Flask(__name__)

# Inicializar Marshmallow
ma = Marshmallow(app)  # Inicializar Marshmallow con la aplicación

# Configuración de CORS
CORS(app)

# Cargar la configuración desde config.py
app.config.from_object(Config)

# Configuración del JWT
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(auth_controller.bp)
app.register_blueprint(user_controller.bp)
app.register_blueprint(intersection_controller.bp)
app.register_blueprint(status_controller.bp)
app.register_blueprint(interference_controller.bp)

if __name__ == '__main__':
    app.run(debug=True)
