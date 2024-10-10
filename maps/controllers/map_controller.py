import uuid
import os
import logging
from flask import Blueprint, request, jsonify
from maps.services.kml_service import (
    create_square_polygon, 
    create_polygon_from_coords,
    format_intersection_response,
    check_polygon_intersection,
    extract_linestrings,
    add_filename_to_response,
    add_point_view_to_response
)
from maps.services.kml_handler import KMLHandler
from maps.services.gcp_bucket import GCPBucketService
from config import Config
from flask_jwt_extended import jwt_required
from users.auth.auth_decorators import roles_required

# Configurar logging
log_file_path = 'logs/map_controller.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Guarda los logs en un archivo
        logging.StreamHandler()  # También imprime los logs en la consola
    ]
)
logger = logging.getLogger(__name__)
bp = Blueprint('map', __name__, url_prefix='/maps')

# Ruta al archivo KML original
KML_FILE_PATH = 'cables.kml'
linestrings_info = extract_linestrings(KML_FILE_PATH)
logger.debug(f"Linestrings info extraído: {linestrings_info}")

# Crear instancia de GCPBucketService (solo se necesita una)
bucket_service = GCPBucketService()

def generate_random_filename():
    """Genera un nombre de archivo aleatorio usando UUID."""
    return f"cable_polygon_{uuid.uuid4().hex}.kml"

def get_relative_file_path(filename):
    """Obtiene la ruta relativa al directorio del proyecto."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'output', filename)

def generate_and_upload_kml(polygon, bucket_name):
    """Genera un archivo KML, lo guarda y lo sube a GCP, devolviendo el nombre del archivo y el punto representativo."""
    new_kml_filename = generate_random_filename()
    output_file_path = get_relative_file_path(new_kml_filename)
    
    logger.info(f"Generando archivo KML: {new_kml_filename} en {output_file_path}")
    
    kml_handler = KMLHandler(KML_FILE_PATH)
    point = kml_handler.add_polygon(polygon, output_file_path)
    
    try:
        bucket_service.upload_file(bucket_name, output_file_path, new_kml_filename)
        logger.info(f"Archivo {output_file_path} subido exitosamente a {bucket_name} como {new_kml_filename}")
    except Exception as e:
        logger.error(f"Error al subir el archivo a GCP: {str(e)}")
        raise Exception(f"Error al subir el archivo a GCP: {str(e)}")

    return new_kml_filename, point

def build_response(intersections, kml_filename, point):
    """Construye la respuesta JSON final con el nombre del archivo y el punto representativo."""
    response = format_intersection_response(intersections)
    response_with_filename = add_filename_to_response(response, kml_filename)
    response_with_point = add_point_view_to_response(response_with_filename, point)
    return response_with_point

def process_request_data(data, key_coords, key_tolerance=None):
    """Procesa y valida los datos de la solicitud para puntos o polígonos."""
    if key_tolerance:
        if not data or key_coords not in data or key_tolerance not in data:
            logger.warning("Datos faltantes en la solicitud")
            return None, {'error': 'Coordinates and tolerance must be provided'}, 400
        try:
            latitude = float(data[key_coords][0])
            longitude = float(data[key_coords][1])
            tolerance_meters = float(data[key_tolerance])
            return create_square_polygon(latitude, longitude, tolerance_meters), None, None
        except (ValueError, TypeError) as e:
            logger.error(f"Error en el formato de coordenadas o tolerancia: {str(e)}")
            return None, {"error": "Invalid coordinates or tolerance format"}, 400
    else:
        if not data or key_coords not in data:
            logger.warning("No se proporcionaron coordenadas del polígono")
            return None, {'error': 'No polygon coordinates provided'}, 400
        polygon = create_polygon_from_coords(data[key_coords])
        if not polygon:
            logger.error("Formato de coordenadas inválido")
            return None, {"error": "Invalid coordinates format"}, 400
        return polygon, None, None

def handle_kml_process(polygon, bucket_name):
    """Genera un KML, lo sube y devuelve la respuesta."""
    try:
        kml_filename, point = generate_and_upload_kml(polygon, bucket_name)
        return kml_filename, point, None
    except Exception as e:
        logger.error(f"Error al generar y subir el KML: {str(e)}")
        return None, None, {"error": str(e)}, 500

def handle_interference_request(data, key_coords, key_tolerance, bucket_name):
    """Función genérica para manejar solicitudes de interferencia con puntos o polígonos."""
    polygon, error_response, error_code = process_request_data(data, key_coords, key_tolerance)
    if error_response:
        return jsonify(error_response), error_code

    intersections = check_polygon_intersection(polygon, linestrings_info)
    
    kml_filename, point, error_response = handle_kml_process(polygon, bucket_name)

    if error_response:
        return jsonify(error_response), error_code
    
    response = build_response(intersections, kml_filename, point)
    logger.debug(f"Respuesta generada: {response}")
    return jsonify(response)

@bp.route('/verify_point', methods=['POST'])
@jwt_required()
@roles_required('admin', 'user') 
def check_intersection_with_tolerance():
    data = request.get_json()
    return handle_interference_request(data, 'coord', 'tolerance', Config.BUCKET_TO_CHECK)

@bp.route('/verify_polygon', methods=['POST'])
@jwt_required()
@roles_required('admin', 'user') 
def check_intersection():
    data = request.get_json()
    return handle_interference_request(data, 'polygon_coords', None, Config.BUCKET_TO_CHECK)

@bp.route('/save_point', methods=['POST'])
@jwt_required()
@roles_required('admin', 'user') 
def save_interference_point():
    data = request.get_json()
    return handle_interference_request(data, 'coord', 'tolerance', Config.BUCKET_TO_SAVE)

@bp.route('/save_polygon', methods=['POST'])
@jwt_required()
@roles_required('admin', 'user') 
def save_interference_polygon():
    data = request.get_json()
    return handle_interference_request(data, 'polygon_coords', None, Config.BUCKET_TO_SAVE)

@bp.route('/delete_bucket_interference', methods=['DELETE'])
@jwt_required()
@roles_required('admin')
def delete_bucket():
    try:
        bucket_name = Config.BUCKET_TO_SAVE
        bucket_service.clear_bucket(bucket_name)
        logger.info(f"Bucket {bucket_name} eliminado exitosamente.")
        return jsonify({"message": f"Bucket '{bucket_name}' eliminado exitosamente."}), 200
    except Exception as e:
        logger.error(f"Error al eliminar el bucket: {str(e)}")
        return jsonify({"error": f"Error al eliminar el bucket: {str(e)}"}), 500


