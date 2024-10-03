# kml_service.py
from fastkml import kml
from shapely.geometry import shape, Polygon
from maps.helpers.geo_utils import meters_to_degrees

def extract_linestrings(kml_file_path):
    k = kml.KML()
    with open(kml_file_path, 'rb') as f:
        kml_data = f.read()

    # Eliminar la declaración de codificación (si existe)
    kml_data = kml_data.decode('utf-8')
    if kml_data.startswith('<?xml'):
        kml_data = kml_data.replace('<?xml version="1.0" encoding="UTF-8"?>', '')

    k.from_string(kml_data.encode('utf-8'))

    line_strings_info = []

    def extract_features(features):
        for feature in features:
            if isinstance(feature, kml.Document):
                extract_features(feature.features())
            elif isinstance(feature, kml.Folder):
                extract_features(feature.features())
            elif isinstance(feature, kml.Placemark):
                try:
                    if feature.geometry and hasattr(feature.geometry, 'geom_type'):
                        if feature.geometry.geom_type == 'LineString':
                            shapely_line = shape(feature.geometry)
                            name = feature.name
                            description = feature.description
                            line_strings_info.append({
                                'line': shapely_line,
                                'name': name,
                                'description': description
                            })
                except AttributeError as e:
                    print(f"AttributeError: {e} with feature: {feature}")
            else:
                print(f"Unexpected feature type: {type(feature)}")

    extract_features(k.features())

    return line_strings_info

def check_polygon_intersection(polygon, line_strings_info):
    intersecting_lines = []
    for idx, line_info in enumerate(line_strings_info):
        if polygon.intersects(line_info['line']):
            intersecting_lines.append((idx, line_info))
    return intersecting_lines

def create_polygon_from_coords(coords):
    """
    Crea un polígono a partir de una lista de coordenadas.
    """
    try:
        polygon_coords = [(float(coord[1]), float(coord[0])) for coord in coords]
        return Polygon(polygon_coords)
    except (ValueError, TypeError):
        return None

def create_square_polygon(latitude, longitude, tolerance_meters):
    """
    Crea un polígono cuadrado alrededor de un punto con una tolerancia dada en metros.
    """
    tolerance_degrees = meters_to_degrees(tolerance_meters)
    polygon_coords = [
        [latitude - tolerance_degrees, longitude - tolerance_degrees],
        [latitude - tolerance_degrees, longitude + tolerance_degrees],
        [latitude + tolerance_degrees, longitude + tolerance_degrees],
        [latitude + tolerance_degrees, longitude - tolerance_degrees],
        [latitude - tolerance_degrees, longitude - tolerance_degrees]
    ]
    return Polygon([(coord[1], coord[0]) for coord in polygon_coords])

def format_intersection_response(intersections):
    """
    Formatea la respuesta de intersección en un JSON.
    """
    if intersections:
        return {
            'intersects': True,
            'details': [
                {
                    'index': idx,
                    'name': line_info['name'],
                    'description': line_info['description'],
                    'line': list(line_info['line'].coords)
                }
                for idx, line_info in intersections
            ]
        }
    else:
        return {'intersects': False}

def add_filename_to_response(response, filename):
    """
    Agrega el nombre del archivo al response.
    
    :param response: El diccionario de respuesta original.
    :param filename: El nombre del archivo a agregar al response.
    :return: El diccionario de respuesta modificado.
    """
    response['generated_file'] = filename
    return response


def add_point_view_to_response(response, point):
 
    response['point_reference'] = {'lat': point[1], 'lng': point[0]}
    
    return response