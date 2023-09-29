import psycopg2

from typing import List
from pydantic import BaseModel

import uvicorn

from fastapi import FastAPI, status

from fastapi.middleware.cors import CORSMiddleware


# Creating a Model
class Book(BaseModel):
    id: int = None
    volume_id: str
    title: str
    authors: str = None
    thumbnail: str = None
    state: int     # 0 = Completed, 1 = Reading, 2 = Whishlist
    rating: int = 0


class UpdateRatingRequestBody(BaseModel):
    volume_id: str
    new_rating: int


class UpdateStateRequestBody(BaseModel):
    volume_id: str
    new_state: int


# Creating a FastAPI & Middleware
app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creating an Endpoint


@app.get("/status")
async def check_status():
    return "WELCOME TO FASTAPI!"


# Getting Books
@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_books():
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0",
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM book ORDER BY id DESC")
    rows = cur.fetchall()

    formatted_books = []

    for row in rows:
        # formatted_books.append(Book(**row))
        formatted_books.append(
            Book(
                id=row[0],
                volume_id=row[1],
                title=row[2],
                authors=row[3],
                thumbnail=row[4],
                state=row[5],
                rating=row[6]
            ))

    cur.close()
    conn.close()

    return formatted_books


# Post a Book
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def new_book(book: Book):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0",
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO book (volume_id, title, authors, thumbnail, state, rating) VALUES (%s, %s, %s, %s, %s, %s)",
                (book.volume_id, book.title, book.authors, book.thumbnail, book.state, book.rating))
    conn.commit()
    cur.close()
    conn.close()
    return


# Rating a Book
@app.put("/books/update_rating", status_code=status.HTTP_200_OK)
async def update_rating(update_rating_body: UpdateRatingRequestBody):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0",
    )
    cur = conn.cursor()
    cur.execute("UPDATE book SET rating = %s WHERE volume_id = %s",
                (update_rating_body.new_rating, update_rating_body.volume_id))
    conn.commit()
    cur.close()
    conn.close()
    return

# Update a Book State


@app.put("/books/update_state", status_code=status.HTTP_200_OK)
async def update_state(update_state_body: UpdateStateRequestBody):
    conn = psycopg2.connect(
        database="exampledb",
        user="docker",
        password="docker",
        host="0.0.0.0",
    )
    cur = conn.cursor()
    cur.execute("UPDATE book SET state = %s WHERE volume_id = %s",
                (update_state_body.new_state, update_state_body.volume_id))
    conn.commit()
    cur.close()
    conn.close()
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
