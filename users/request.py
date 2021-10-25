import json
import sqlite3
from models import User


def create_new_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Users
            (first_name, last_name, email, username, password)
        VALUES (?, ?, ?, ?, ?);
        """, (new_user['first_name'], new_user['last_name'], new_user['email'], new_user['username'], new_user['password'], ))
       
    return json.dumps(new_user)


def found_user(object):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT id, email
        FROM Users
        WHERE email = ?

        """, (object['username'], ))

        found_email = db_cursor.fetchone() 

        if found_email:
            return json.dumps({"valid":True, "token": found_email['id']})

        else:
            return json.dumps({"valid":False})

def get_users():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            users.id,
            users.first_name,
            users.last_name,
            users.email,
            users.bio,
            users.username,
            users.password,
            users.created_on,
            users.active
        FROM Users
        """)
        users = []
        data = db_cursor.fetchall()
        for row in data:
            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'], row['username'], row['password'], row['created_on'], row['active'] )
            users.append(user.__dict__)
        return json.dumps(users)