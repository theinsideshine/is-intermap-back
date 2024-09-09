import sqlite3
import os
import sys

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

    # Crear la tabla users con todas las columnas necesarias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            cuit TEXT,
            name TEXT,
            address TEXT,
            phone TEXT,
            mobile TEXT,
            contact TEXT,
            email TEXT
        )
    ''')

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print(f"Base de datos y tabla 'users' creadas en '{db_path}' con todas las columnas.")

except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos o crear la tabla: {e}")

finally:
    if conn:
        conn.close()
