from fastapi import FastAPI, status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import time
app = FastAPI()

class Post(BaseModel):
    name: str
    content: str

while True:
    try:
        conn = psycopg2.connect(host="localhost", user="postgres", database='fastapi', 
                                password="Omar1234567890", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE Connetion was Successfully")
        break
    except:
        print("Can't connection with DATABASE")
        time.sleep(2)

@app.get("/post")
def get_post():

    cursor.execute(""" SELECT * FROM posts;""")
    posts  = cursor.fetchall()
    return {
        "message": "GET all Post",
        "data": posts
    }
@app.get("/post/{id}")
def get_post_id(id:str):
    try:
        cursor.execute(""" SELECT * FROM posts WHERE id=%s""",(str(id)))
        post = cursor.fetchone()
    except:
        post = "Can't found this post"
    return {
        "message": "GET specific post with Id",
        "data": post,
    }
@app.get("/post/latest")
def get_latest_post():
    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC""")
    post = cursor.fetchone()
    return {
        "message": "GET latest post",
        "data": post
    }
@app.post("/post")
def create_post(post:Post):

    cursor.execute(""" INSERT INTO posts (name, content) VALUES (%s, %s) RETURNING * """, (post.name, post.content))
    post = cursor.fetchone()
    conn.commit()
    return {
        "message": "Created  New Post was Successfully",
        "data": post
    }
@app.put("/post/{id}")
def update_post(post:Post, id:str):
    cursor.execute("""UPDATE posts SET name=%s, content=%s WHERE id=%s RETURNING *;""", (post.name, post.content, str(id)))
    post = cursor.fetchone()
    conn.commit()
    return {
        "message": f"Update post with {id} was successfully",
        "data": post,
    }
@app.delete("/post/{id}")
def delete_post(id:str):
    try:
        cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""", str(id))
        post = cursor.fetchone()
    except:
        post = f"Can't not found this post with {id}"
    return {
        "message": f"Delete post with {id} was successfully",
        "data": post,
    }
