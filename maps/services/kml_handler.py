import re
import os
import logging
from fastkml import kml
from shapely.geometry import shape, Polygon
from maps.helpers.geo_utils import meters_to_degrees

# Configuración del logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Crear un manejador de archivo para guardar los logs en un archivo
file_handler = logging.FileHandler('logs/kml_handler.log')
file_handler.setLevel(logging.DEBUG)

# Crear un formato para los logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Agregar el manejador al logger
logger.addHandler(file_handler)

class KMLHandler:
    def __init__(self, kml_file_path):
        self.kml_file_path = kml_file_path
        self.kml = None
        logger.info(f"Inicializando KMLHandler con archivo KML: {self.kml_file_path}")
        self._load_kml()

    def _load_kml(self):
        try:
            with open(self.kml_file_path, 'rb') as file:
                content = file.read()
            logger.info(f"Archivo KML {self.kml_file_path} cargado correctamente.")
            
            # Eliminamos la línea de declaración de encoding del contenido
            content = re.sub(b'<\?xml.*encoding=".*"\?>', b'', content)
            self.kml = kml.KML()
            self.kml.from_string(content)
            logger.info(f"Contenido del archivo KML procesado correctamente.")
        
        except FileNotFoundError:
            logger.error(f"El archivo {self.kml_file_path} no se encontró.")
        except Exception as e:
            logger.error(f"Error al cargar el archivo KML: {e}")

    def add_polygon(self, polygon, output_file_path):
        logger.info(f"Vamos a agregar el polígono al archivo: {output_file_path}")
        
        # Verificar si el directorio de salida existe, si no, crearlo
        output_dir = os.path.dirname(output_file_path)
        if not os.path.exists(output_dir):
            logger.warning(f"El directorio {output_dir} no existe. Creándolo.")
            os.makedirs(output_dir)

        try:
            new_polygon = kml.Placemark()
            new_polygon.geometry = polygon

            document = list(self.kml.features())[0]
            folder = list(document.features())[0]
            folder.append(new_polygon)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(self.kml.to_string(prettyprint=True))
            logger.info(f"Archivo KML actualizado con el polígono y guardado en: {output_file_path}")
        
        except Exception as e:
            logger.error(f"Error al agregar el polígono o al guardar el archivo: {e}")
            raise

        # Retornar un punto representativo del polígono (el primer punto)
        if polygon.is_empty:
            logger.warning(f"El polígono proporcionado está vacío.")
            return None
        
        point = polygon.exterior.coords[0]  # Retorna la primera coordenada del polígono
        logger.info(f"Punto representativo del polígono: {point}")
        return point



