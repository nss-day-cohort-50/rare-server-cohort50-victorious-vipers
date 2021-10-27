import json
import sqlite3
from models import Comments, Posts

def get_comments_by_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT 
            Comments.id,
            Comments.post_id,
            Comments.author_id,
            Comments.content,
            Comments.created_on, 
            Posts.user_id,
            Posts.category_id,
            Posts.title,
            Posts.content,
            Users.username
        FROM Comments
        JOIN Posts
        ON Posts.id = Comments.post_id
        JOIN Users
        ON Users.id = Posts.user_id
        WHERE Comments.post_id = ?
        """, (id, )) 
        data = db_cursor.fetchall()
        comments = []
        for row in data:
            comment = Comments(row['id'], row['post_id'], row['author_id'], row['content'], row['created_on'])
            comment.post= {"id":row['post_id'], "user_id":row['user_id'], "category_id":row['category_id'], "title":row['title'], "content":row['content']}
            comment.user = {"id":row['user_id'], "username": row['username']}
            comments.append(comment.__dict__)
        return json.dumps(comments)
