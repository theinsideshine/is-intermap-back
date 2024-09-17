import sqlite3
from interferences.models.entities.interference_entity import Interference
import json

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_interference(self, id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT username, email, company, address_ref, status, last, start, polygon_coords, coord, tolerance, url_file 
                          FROM interferences WHERE id=?''', (id,))
        interference = cursor.fetchone()
        conn.close()
        if interference:
            # Convertir los campos JSON de vuelta a listas o diccionarios
            polygon_coords = json.loads(interference[7])
            coord = json.loads(interference[8])
            return Interference(*interference[:7], polygon_coords, coord, *interference[9:])
        return None

    def get_all_interferences(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT id, username, email, company, address_ref, status, last, start, polygon_coords, coord, tolerance, url_file 
                          FROM interferences''')
        interferences = cursor.fetchall()
        conn.close()
        return [Interference(interference[0], interference[1], interference[2], interference[3], interference[4], interference[5],
                             interference[6],interference[7], json.loads(interference[8]), json.loads(interference[9]), interference[10], interference[11])
                for interference in interferences]

    def create_interference(self, interference: Interference):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO interferences (username, email, company, address_ref, status, last, start, polygon_coords, coord, tolerance, url_file) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (interference.username, interference.email, interference.company, interference.address_ref, interference.status, 
                interference.last, interference.start, json.dumps(interference.polygon_coords), json.dumps(interference.coord), 
                interference.tolerance, interference.url_file)
            )
            conn.commit()
            interference.id = cursor.lastrowid  # Asigna el ID generado
            return interference
        except Exception as e:
            print(f"Error al crear la interferencia: {e}")
            raise
        finally:
            conn.close()  # Asegúrate de cerrar la conexión en caso de error o éxito


    def update_interference(self, interference: Interference):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE interferences 
            SET username=?, email=?, company=?, address_ref=?, status=?, last=?, start=?, polygon_coords=?, coord=?, tolerance=?, url_file=? 
            WHERE id=?''',
            (interference.username, interference.email, interference.company, interference.address_ref, interference.status, interference.last, 
            interference.start, json.dumps(interference.polygon_coords), json.dumps(interference.coord), interference.tolerance, 
            interference.url_file, interference.id)
        )
        conn.commit()
        conn.close()
        return interference  # Devuelve la entidad actualizada




    def delete_interference(self, id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM interferences WHERE id=?", (id,))
        conn.commit()
        conn.close()
