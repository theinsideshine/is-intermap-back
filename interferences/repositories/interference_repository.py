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
        cursor.execute('''SELECT username, email, company, address_ref, status, last, start, point_reference, url_file, interference 
                          FROM interferences WHERE id=?''', (id,))
        interference = cursor.fetchone()
        conn.close()

        if interference:
            # Asigna cada valor explícitamente para evitar problemas de desempaquetado
            username = interference[0]
            email = interference[1]
            company = interference[2]
            address_ref = interference[3]
            status = interference[4]
            last = interference[5]
            start = interference[6]
            
            # Convertir los campos JSON de vuelta a listas
            point_reference = json.loads(interference[7])
            url_file = interference[8]
            interference_boolean = interference[9]

            # Devuelve la entidad Interference con valores explícitos
            return Interference(
                id=id,
                username=username,
                email=email,
                company=company,
                address_ref=address_ref,
                status=status,
                last=last,
                start=start,
                point_reference=point_reference,
                url_file=url_file,
                interference=interference_boolean  # Nuevo campo booleano
            )

        return None

    def get_all_interferences(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT id, username, email, company, address_ref, status, last, start, point_reference, url_file, interference 
                          FROM interferences''')
        interferences = cursor.fetchall()
        conn.close()
        return [Interference(interference[0], interference[1], interference[2], interference[3], interference[4], interference[5],
                             interference[6], json.loads(interference[7]), interference[8], interference[9])
                for interference in interferences]

    def create_interference(self, interference: Interference):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO interferences (username, email, company, address_ref, status, last, start, point_reference, url_file, interference) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (interference.username, interference.email, interference.company, interference.address_ref, interference.status, 
                interference.last, interference.start, json.dumps(interference.point_reference), interference.url_file, 
                interference.interference)
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
            SET username=?, email=?, company=?, address_ref=?, status=?, last=?, start=?, point_reference=?, url_file=?, interference=? 
            WHERE id=?''',
            (interference.username, interference.email, interference.company, interference.address_ref, interference.status, interference.last, 
            interference.start, json.dumps(interference.point_reference), interference.url_file, interference.interference, interference.id)
        )
        conn.commit()
        conn.close()
        return interference  # Devuelve la entidad actualizada

    def get_interferences_by_page(self, page, page_size):
        offset = page * page_size
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT id, username, email, company, address_ref, status, last, start, point_reference, url_file, interference 
                        FROM interferences 
                        LIMIT ? OFFSET ?''', (page_size, offset))
        interferences = cursor.fetchall()
        conn.close()

        # Asegúrate de desempaquetar todos los elementos necesarios
        return [
            Interference(
                id=interference[0],  # id
                username=interference[1],  # username
                email=interference[2],  # email
                company=interference[3],  # company
                address_ref=interference[4],  # address_ref
                status=interference[5],  # status
                last=interference[6],  # last
                start=interference[7],  # start
                point_reference=json.loads(interference[8]),  # point_reference
                url_file=interference[9],  # url_file
                interference=interference[10]  # interference
            ) for interference in interferences
        ]


    def count_interferences(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM interferences''')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    

    def count_interferences_by_username(self, username):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM interferences WHERE username = ?''', (username,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_interferences_by_username_and_page(self, username, page, page_size):
        offset = page * page_size
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''SELECT id, username, email, company, address_ref, status, last, start, point_reference, url_file, interference 
                        FROM interferences 
                        WHERE username = ? 
                        LIMIT ? OFFSET ?''', (username, page_size, offset))
        interferences = cursor.fetchall()
        conn.close()

        # Asegúrate de desempaquetar todos los elementos necesarios
        return [
            Interference(
                id=interference[0],  # id
                username=interference[1],  # username
                email=interference[2],  # email
                company=interference[3],  # company
                address_ref=interference[4],  # address_ref
                status=interference[5],  # status
                last=interference[6],  # last
                start=interference[7],  # start
                point_reference=json.loads(interference[8]),  # point_reference
                url_file=interference[9],  # url_file
                interference=interference[10]  # interference
            ) for interference in interferences
        ]


    def delete_interference(self, id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM interferences WHERE id=?", (id,))
        conn.commit()
        conn.close()
