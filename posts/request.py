import json
import sqlite3
from models import Posts, Category, User
db_connect = "./rare.db"

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
