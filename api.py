from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware # Required import for CORS
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Import database models and CRUD functions
import models
import crud

# --- Database Setup ---

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable is not set!")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables
# This command creates the 'books' table if it doesn't exist
models.Base.metadata.create_all(bind=engine)


# --- FastAPI Application ---

app = FastAPI(
    title="Library API with Database",
    description="A library management API powered by a PostgreSQL database.",
    version="2.0.0"
)

# --- CORS Middleware Settings ---
# We add these settings to allow browsers to make requests to our API from different origins.

# List of allowed origins. "*" allows requests from any origin.
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, DELETE, etc.)
    allow_headers=["*"], # Allow all headers
)


# --- Pydantic Models ---
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

    class Config:
        from_attributes = True

class ISBNModel(BaseModel):
    isbn: str


# --- Dependency ---
def get_db():
    """
    A FastAPI dependency that creates a new database session for each request
    and closes it when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---

@app.get("/books", response_model=List[BookModel])
def get_all_books(db: Session = Depends(get_db)):
    """
    Fetches a list of all books from the database.
    """
    books = crud.get_all_books(db)
    return books


@app.post("/books", response_model=BookModel, status_code=201)
def add_book_by_isbn(item: ISBNModel, db: Session = Depends(get_db)):
    """
    Adds a new book to the library using its ISBN.
    """
    existing_book = crud.get_book_by_isbn(db, isbn=item.isbn)
    if existing_book:
        raise HTTPException(
            status_code=409,  # Conflict
            detail=f"A book with this ISBN ({item.isbn}) already exists in the library."
        )

    new_book = crud.create_book(db, isbn=item.isbn)
    if new_book is None:
        raise HTTPException(
            status_code=404, # Not Found
            detail=f"A book with this ISBN ({item.isbn}) could not be found via the Open Library API."
        )
    return new_book


@app.delete("/books/{isbn}", status_code=200)
def delete_book(isbn: str, db: Session = Depends(get_db)):
    """
    Deletes a book from the library by its ISBN.
    """
    was_removed = crud.remove_book(db, isbn=isbn)
    if not was_removed:
        raise HTTPException(
            status_code=404, # Not Found
            detail=f"A book with this ISBN ({isbn}) was not found in the library."
        )
    return {"message": "Book successfully deleted", "isbn": isbn}

