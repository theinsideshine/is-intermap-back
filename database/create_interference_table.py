import sqlite3
import os
import sys
import json

"""
{
  "username": "user1",
  "email": "user1@example.com",
  "company": "Company A",
  "address_ref": "123 Main St",
  "status": "active",
  "last": "2024-09-16",
  "start": "2024-09-01",
  "polygon_coords": "[[-34.9011, -56.1645], [-34.9025, -56.1622], [-34.9045, -56.1642], [-34.9031, -56.1665], [-34.9011, -56.1645]]",
  "coord": "[-34.620423798981946, -58.449699592590335]",
  "tolerance": 1000,
  "url_file": "http://example.com/file"
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

    # Crear la tabla interferences con todas las columnas necesarias
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
            polygon_coords TEXT,  -- Almacenar el polígono como un string JSON
            coord TEXT,           -- Almacenar las coordenadas como un string JSON
            tolerance INTEGER,
            url_file TEXT
        )
    ''')

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print(f"Base de datos y tabla 'interferences' creadas en '{db_path}' con todas las columnas.")

except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos o crear la tabla: {e}")

finally:
    if conn:
        conn.close()

