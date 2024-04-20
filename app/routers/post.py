from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import database, models, utils, schemas
from sqlalchemy.orm import Session
from ..database import get_db, engine, cursor, conn

router = APIRouter()




@router.get("/post")
def get_post():

    cursor.execute(""" SELECT * FROM posts;""")
    posts  = cursor.fetchall()
    return {
        "message": "GET all Post",
        "data": posts
    }
@router.get("/post/{id}")
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
@router.get("/post/latest")
def get_latest_post():
    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC""")
    post = cursor.fetchone()
    return {
        "message": "GET latest post",
        "data": post
    }
@router.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.Post):

    cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content))
    post = cursor.fetchone()
    conn.commit()
    return {
        "message": "Created  New Post was Successfully",
        "data": post
    }
@router.put("/post/{id}")
def update_post(post:schemas.Post, id:str):
    cursor.execute("""UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *;""", (post.title, post.content, str(id)))
    post = cursor.fetchone()
    conn.commit()
    return {
        "message": f"Update post with {id} was successfully",
        "data": post,
    }
@router.delete("/post/{id}")
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

# CRUD operation with ORM 


@router.get("/posts/orm")
def posts_ORM(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {
        "message": "GET All The posts",
        "data": posts,
    }
@router.get("/posts/orm/{id}")
def post_ORM_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    return {
        "message": "Get specific post with id",
        "data": post,
    }

@router.post("/posts/orm", status_code=status.HTTP_201_CREATED, response_model=schemas.BasePost)
async def create_post(post:schemas.BasePost, db:Session=Depends(get_db)):
    # you can replace this with
    new_post =  models.Post(**post.dict())
    # new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "message": "Post Created",
        "data": new_post,
    }

@router.delete("/posts/orm/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_orm(id:int, db:Session=Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id==id).first()
    db.delete(delete_post)
    db.commit()
    
    return {
        "message": "Delete this post is successfully",
        "data": delete_post,
    }
@router.put("/posts/orm/{id}")
def update_post_orm(id:int,update_post:schemas.UpdatePost ,db:Session=Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post With id:{id} Does not exist")
    # post_query.update(post.dict(),synchronize_session=False)
    # post_query.title = post.title
    # post_query.content = post.content
    # db.add(post_query)
    # post_query.update({'title': post.title, 'content': post.content}, synchronize_session=False)
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return {
        "message": "Update this post is successfully",
        "data": post_query.first(),
    }
