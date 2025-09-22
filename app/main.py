from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Use relative imports because crud and models are in the same package ('app')
from . import models, crud

# --- Database Setup ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This command creates the 'books' table in your Neon database if it doesn't exist.
# It runs only once when the application starts.
models.Base.metadata.create_all(bind=engine)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Simple Library API",
    description="An API for managing a book library, deployed on Fly.io with a Neon database.",
    version="1.0.0"
)

# --- CORS Middleware ---
# This is the crucial part that was missing after refactoring.
# It allows web pages from any origin (like your local index.html or GitHub Pages)
# to make requests to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# --- Dependency ---
def get_db():
    """
    Dependency that provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Pydantic Models (Data Schemas) ---
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class BookCreate(BaseModel):
    isbn: str


class Book(BookBase):
    class Config:
        from_attributes = True


# --- API Endpoints ---

@app.get("/books", response_model=List[Book], summary="Get All Books")
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all books from the library.
    """
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.post("/books", response_model=Book, status_code=201, summary="Add a New Book by ISBN")
def create_book_entry(book: BookCreate, db: Session = Depends(get_db)):
    """
    Add a new book to the library using its ISBN.
    The book details are fetched from the Open Library API.
    """
    db_book = crud.get_book_by_isbn(db, isbn=book.isbn)
    if db_book:
        raise HTTPException(status_code=400, detail=f"Book with ISBN {book.isbn} already exists.")

    new_book = crud.create_book(db=db, isbn=book.isbn)
    if new_book is None:
        raise HTTPException(status_code=404,
                            detail=f"Book with ISBN {book.isbn} could not be found via Open Library API.")

    return new_book


@app.delete("/books/{isbn}", response_model=Book, summary="Delete a Book by ISBN")
def delete_book_entry(isbn: str, db: Session = Depends(get_db)):
    """
    Delete a book from the library using its ISBN.
    """
    deleted_book = crud.delete_book(db, isbn=isbn)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail=f"Book with ISBN {isbn} not found in the library.")
    return deleted_book

