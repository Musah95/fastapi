from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

my_posts = [
    {
        "title":"title1",
        "content":"content of post1",
        "id":1
    },
    {
        "title":"title2",
        "content":"content of post2",
        "id":2
    },
    {
        "title":"title3",
        "content":"content of post3",
        "id":3
    },
]

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='fastapi', cursor_factory=RealDictCursor)
        db_driver = conn.cursor()
        print('database connection was successful')
        break

    except Exception as error:
        print('connection to database failed')
        print('Error:', error)
        time.sleep(4)



def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
        
       
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/posts")
def get_posts():
    db_driver.execute("""SELECT * FROM posts""")
    posts = db_driver.fetchall()
    return{"all_posts": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    db_driver.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    post = db_driver.fetchone()
    conn.commit()
    return{"created_post": post}

    # data = post.model_dump()
    # data["id"] = randrange(0,100000)
    # my_posts.append(data)
 

@app.get("/posts/{id}")
def get_post(id: int):
    db_driver.execute("""SELECT * FROM posts WHERE id = {} """ .format(str(id)))
    post = db_driver.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"post_details": post}



@app.delete("/posts/{id}")
def delete_post(id: int):
    db_driver.execute("""DELETE FROM posts WHERE id = {} RETURNING * """ .format(str(id)))
    post = db_driver.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"deleted_post":post}   
    
@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    db_driver.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (str(id))))
    post = db_driver.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return{"updated_post":post}

