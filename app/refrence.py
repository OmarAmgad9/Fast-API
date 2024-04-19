from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi' ,user='postgres', 
                                password='Omar1234567890', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connet with DATABASE was successfull.")
        break
    except Exception as error:
        print("Connet with DATABASE faild.")
        print("Error", error)
        time.sleep(3)
    


@app.get("/")
async def root():
    return {"message": "Welcome to my api and test"}


my_post = [{"title": "this is post 1", "content":"content for post 1", "id":1},{"title": "this is post 1", "content":"content for post 3", "id":2},{"title": "this is post 1", "content":"content for post 3", "id":3},{"title": "this is post 1", "content":"content for post 3", "id":4},{"title": "this is post 1", "content":"content for post 3", "id":5}]
def find_index(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


@app.get("/post")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message": "test Post",
            "data": posts,
            }

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):

    cursor.execute("""INSERT INTO posts (name) values (%s) RETURNING *;""", (post.title))
    cursor.fetchone()
    return {
                "message": "Post request successe",
                "data": post
            }

@app.get("/post/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC""")
    post = cursor.fetchone()
    return {
        "messsage": "this is latest post",
        "data": post,
    }

@app.get("/post/{id}")
def get_post(id:int, response:Response):
    # post = find_post(id)
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post Not found ")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "this post with id was not found "}
    return {"post_detail": f"Here is post {id}",
            "data": post,
            }


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #deleting post logic

    # find the inde in the array has to delete
    

    return {"messsage": "delete ",
            "data": my_post,
            }