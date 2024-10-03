import sqlite3
import os
import sys
import json

"""
{
    "username": "tavolaro",
    "email": "tavolaro@example.com",
    "company": "Rht",
    "address_ref": "Saenz 145",
    "status": "waiting",
    "point_reference": [-34.620423798981946, -58.449699592590335],  // Cambiado a lista
    "url_file": "cable_polygon_3c08fc58880f475084ecdbce312fc591.kml",
    "interference": true
}

"""

# Agregar el directorio anterior al path para importar config.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar el archivo de configuración y acceder a la clase Config
from config import Config

# Ruta al directorio actual y luego el nombre del archivo de la base de datos desde Config.DB_NAME
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, Config.DB_NAME)

try:
    # Conectar a la base de datos (esto la creará si no existe)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear la tabla interferences con las columnas actualizadas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            address_ref TEXT,
            status TEXT,
            last DATE,
            start DATE,
            point_reference TEXT,  -- Cambio de nombre de coord a point_reference
            url_file TEXT,
            interference BOOLEAN  -- Nueva columna boolean para indicar interferencia
        )
    ''')

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print(f"Base de datos y tabla 'interferences' creadas/actualizadas en '{db_path}' con las columnas necesarias.")

except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos o crear la tabla: {e}")

finally:
    if conn:
        conn.close()

