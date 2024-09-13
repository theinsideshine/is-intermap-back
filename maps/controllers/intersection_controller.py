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

# Configurar logging
log_file_path = 'logs/intersercion_controller.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Guarda los logs en un archivo
        logging.StreamHandler()  # También imprime los logs en la consola
    ]
)
logger = logging.getLogger(__name__)
#bp = Blueprint('intersection', __name__)
bp = Blueprint('intersection', __name__, url_prefix='/maps')


# Ruta al archivo KML original
KML_FILE_PATH = 'cables.kml'
linestrings_info = extract_linestrings(KML_FILE_PATH)
logger.debug(f"Linestrings info extraído: {linestrings_info}")

# Crear instancia de GCPBucketService (solo se necesita una)
bucket_service = GCPBucketService()

# Nombre del bucket de GCP
bucket_name = 'mi-bucket-para-kml'  # Reemplaza esto con tu bucket de GCP

def generate_random_filename():
    """Genera un nombre de archivo aleatorio usando UUID."""
    return f"cable_polygon_{uuid.uuid4().hex}.kml"

def get_relative_file_path(filename):
    """Obtiene la ruta relativa al directorio del proyecto."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'output', filename)

def generate_and_upload_kml(polygon):
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

@bp.route('/check_intersection_with_tolerance', methods=['POST'])
def check_intersection_with_tolerance():
    logger.debug("Request recibida en /check_intersection_with_tolerance")
    data = request.get_json()
    
    if not data or 'coord' not in data or 'tolerance' not in data:
        logger.warning("Datos faltantes en la solicitud")
        return jsonify({'error': 'Coordinates and tolerance must be provided'}), 400

    try:
        latitude = float(data['coord'][0])
        longitude = float(data['coord'][1])
        tolerance_meters = float(data['tolerance'])
        logger.info(f"Parámetros recibidos - Latitud: {latitude}, Longitud: {longitude}, Tolerancia: {tolerance_meters} metros")
    except (ValueError, TypeError) as e:
        logger.error(f"Error en el formato de coordenadas o tolerancia: {str(e)}")
        return jsonify({"error": "Invalid coordinates or tolerance format"}), 400

    polygon = create_square_polygon(latitude, longitude, tolerance_meters)
    intersections = check_polygon_intersection(polygon, linestrings_info)

    try:
        kml_filename, point = generate_and_upload_kml(polygon)
    except Exception as e:
        logger.error(f"Error al generar y subir el KML: {str(e)}")
        return jsonify({"error": str(e)}), 500

    response = build_response(intersections, kml_filename, point)

    logger.debug(f"Respuesta generada: {response}")
    return jsonify(response)

@bp.route('/check_intersection', methods=['POST'])
def check_intersection():
    logger.debug("Request recibida en /check_intersection")
    data = request.get_json()
    
    if not data or 'polygon_coords' not in data:
        logger.warning("No se proporcionaron coordenadas del polígono")
        return jsonify({'error': 'No polygon coordinates provided'}), 400

    polygon = create_polygon_from_coords(data['polygon_coords'])
    if not polygon:
        logger.error("Formato de coordenadas inválido")
        return jsonify({"error": "Invalid coordinates format"}), 400

    intersections = check_polygon_intersection(polygon, linestrings_info)

    try:
        kml_filename, point = generate_and_upload_kml(polygon)
    except Exception as e:
        logger.error(f"Error al generar y subir el KML: {str(e)}")
        return jsonify({"error generate and upload_kml": str(e)}), 500

    response = build_response(intersections, kml_filename, point)

    logger.debug(f"Respuesta generada: {response}")
    return jsonify(response)

