import json
import sqlite3
from models import User


def create_new_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Users
            (id, first_name, last_name, email, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['username'], new_user['password'],))