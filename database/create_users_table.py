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
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Insertar los usuarios
    cursor.execute('''
        INSERT INTO users (username, password, role, cuit, name, address, phone, mobile, contact, email)
        VALUES 
        ('tavolaro', '$2b$12$VyyNDsFAv.8HKsRzDRNw9.usbTVsg6RBBilK23AtDp12s.4he8zeC', 'admin', '20-25895331-3', 'pablo oscar', 'Alberdi 1645', '+54 11 46315743', '+54 9 11 550681', 'sordeara', 'poto@example.com'),
        ('marcela', '$2b$12$9oc/TTep8SE6aFYg8VF9mu5EFE/SnGMVslRSCwzQkBwfbpKO2dv7O', 'user', '20-12345678-3', 'Guille', 'Gilar', '1146315743', '1145758963', 'marcela', 'marcela.ta@gmail.com'),
        ('rvillar', '$2b$12$B5X5DxR11Av0mPvmMngbKOVofGURbqpBsaZHeGnMkpSJ/j3WWaOOu', 'admin', '20-25563258-3', 'Rodrigo Jesus Villar', 'Lescano 917', '01139484142', '01139484142', 'rodrigo', 'rodrigo.villar@msn.com')
    ''')

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print(f"Base de datos, tabla 'users' creadas y registros insertados en '{db_path}'.")

except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos o crear la tabla: {e}")

finally:
    if conn:
        conn.close()
