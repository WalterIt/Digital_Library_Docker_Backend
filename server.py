import psycopg2

from typing import List
from pydantic import BaseModel

import uvicorn

from fastapi import FastAPI, status

from fastapi.middleware.cors import  CORSMiddleware


# Creating a Model
class Book(BaseModel):
    id: int = None
    volume_id: str
    title: str
    authors: str = None
    thumbnail: str = None
    state: int     # Completed, Reading, Finished
    rating: int = None

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
@app.get("/books", response_model= List[Book], status_code=status.HTTP_200_OK)
async def get_books():
    conn = psycopg2.connect(
        database = "exampledb",
        user = "docker",
        password = "docker",
        host = "0.0.0.0",
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
        database = "exampledb",
        user = "docker",
        password = "docker",
        host = "0.0.0.0",
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO book (volume_id, title, authors, thumbnail, state) VALUES (%s, %s, %s, %s, %s)", (book.volume_id, book.title, book.authors, book.thumbnail, book.state))
    conn.commit()
    cur.close()
    conn.close()
    return 


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
