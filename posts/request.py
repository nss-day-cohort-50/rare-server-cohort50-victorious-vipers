import json
import sqlite3
from models import Posts, Category, User, category
db_connect = "./rare.db"
def get_single_post(id):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            c.id,
            c.label,
            u.first_name,
            u.last_name 
        FROM Posts as p
        LEFT JOIN Categories as c
            ON c.id = p.category_id
        Left JOIN Users as u
            ON u.id = p.user_id
        WHERE p.id = ?
        """,(id,))
        data = db_cursor.fetchone()
        post = Posts(data["id"], data["user_id"], data["category_id"], data["title"], data["publication_date"], data["content"])
        post.category = Category(data["id"], data["label"]).__dict__
        post.user = {"first_name": data["first_name"], "last_name": data["last_name"]}
        return json.dumps(post.__dict__)
def get_users_post(id):
    with sqlite3.connect(db_connect) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            c.id,
            c.label,
            u.first_name,
            u.last_name 
        FROM Posts as p
        LEFT JOIN Categories as c
            ON c.id = p.category_id
        Left JOIN Users as u
            ON u.id = p.user_id
        WHERE p.user_id = ?
        """,(id,))

        posts = []
        data = db_cursor.fetchall()
        for row in data:
            post = Posts(row["id"], row["user_id"], row["category_id"], row["title"], row["publication_date"], row["content"])
            post.category = Category(row["id"], row["label"]).__dict__
            post.user = {"first_name": row["first_name"], "last_name": row["last_name"]}
            posts.append(post.__dict__)
        return json.dumps(posts)

def add_Post(object):
    with sqlite3.connect(db_connect) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Posts
            (user_id,category_id, title, publication_date, content)
        VALUES
            (?,?,?,?,?)
        """, (object["user_id"], object["category_id"], object["title"], object["publication_date"], object["content"]))
        return json.dumps(object)

def delete_post(id):
    with sqlite3.connect(db_connect) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """,(id,))

def edit_post(id, post):
    with sqlite3.connect(db_connect) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id =?,
                category_id =?,
                title =?,
                publication_date = ?,
                content = ?
        WHERE id = ?
        """, (post["user_id"], post["category_id"], post["title"], post["publication_date"], post["content"], id,))

        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            return False
        else:
            return True