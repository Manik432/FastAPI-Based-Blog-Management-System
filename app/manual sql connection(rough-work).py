from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    caption: str
    content: str
    published : bool = True


while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'Backend FastAPI',user = 'postgres',password = 'Vehere@1234', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully!")
        break
    except Exception as error:
        print(f"The database Failed to connect\nError : {error}")
        time.sleep(5)



# created_posts = []

# def find_post(id):
#     for p in created_posts:
#         if p['id'] == id:
#             return p
        
# def find_index(id):
#     for i in range(len(created_posts)):
#         if created_posts[i]['id'] == id:
#             return i

# def find_index(id):
#     for i,post in enumerate(created_posts):
#         if post['id'] == id:
#             return i


@app.get("/")

def root():
    return {"message":"Hello!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"Result": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title,caption,content) Values (%s,%s,%s) RETURNING *""",(post.title,post.caption,post.content))
# We didnt do the following command because that could have lead to SQL injection Attack: f"""INSERT INTO posts (title,caption,content) Values {post.title},{post.caption},{post.content}
    posts=cursor.fetchone()
    conn.commit()

    return {"message":posts}


@app.get('/posts/{id}')
def getapost(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,)) # Here the id is set as a tuple by doing '(id,)'because on converting
                                                                    #id as a string by doing str(id) the interpreter thinks you're giving it multiple parameters — one for each character! ('1', '2')of coverting that 
                                                                    # value into no. of input separate values and will break the execution. 
    found_post = cursor.fetchone()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The post with {id} was not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"The post with {id} was not found."}
    return {"Result":found_post}


@app.delete("/posts/{id}")#,status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts Where id = %s RETURNING *""",(id,))
    found_post = cursor.fetchone()
    conn.commit()

    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id {id} does not exist.")

    return {"message":f"The post with id {id} has been deleted."}


@app.put("/posts/{id}")
def update_post(id:int,post :Post):
    cursor.execute("""UPDATE posts SET title = %s,caption = %s,content = %s WHERE ID = %s RETURNING *""",(post.title,post.caption,post.content,id,))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing to delete")

    return {"message":updated_post}
