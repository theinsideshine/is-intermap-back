import sqlite3
from users.models.entities.user_entity import User

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_user(self, username):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role, cuit, name, address, phone, mobile, contact, email FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(*user)
        return None

    def get_email(self, email):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role, cuit, name, address, phone, mobile, contact, email FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(*user)
        return None

    def get_all_users(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role, cuit, name, address, phone, mobile, contact, email FROM users")
        users = cursor.fetchall()
        conn.close()
        return [User(*user) for user in users]

    def create_user(self, user: User):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO users (username, password, role, cuit, name, address, phone, mobile, contact, email) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (user.username, user.password, user.role, user.cuit, user.name, user.address, user.phone, user.mobile, user.contact, user.email)
        )
        conn.commit()
        conn.close()

    def delete_user(self, username):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
