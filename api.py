# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# We import our existing Library class. The API will use its logic.
from library import Library
from book import Book  # Needed for type hinting if we use it

# --- 1. Create the FastAPI application ---
# This is the main object that will run our API.
app = FastAPI(
    title="Simple Library API",
    description="An API for managing a small book library using the Open Library API.",
    version="1.0.0"
)

# --- 2. Create a single, shared instance of our Library ---
# Our entire API will use this one object to interact with the library logic and the JSON file.
# This is efficient as it loads the books from the file only once when the server starts.
lib = Library()


# --- 3. Define Pydantic Data Models ---
# These models define the "contract" for our API. They ensure that the data
# we receive (input) and send (output) has the correct structure and data types.
# FastAPI uses these models for automatic data validation and documentation.

class BookModel(BaseModel):
    """Data model for a Book to be sent as an API response."""
    title: str
    author: str
    isbn: str


class ISBNModel(BaseModel):
    """Data model for receiving an ISBN in a POST request body."""
    isbn: str


# --- 4. Create the API Endpoints (Path Operations) ---

@app.get("/books", response_model=List[BookModel])
def get_books():
    """
    Endpoint to retrieve a list of all books in the library.
    Corresponds to the "list_books" functionality.
    """
    # The list_books method in our Library class returns a list of Book objects.
    # FastAPI will automatically convert these objects into JSON that matches the BookModel.
    return lib.books


@app.post("/books", response_model=BookModel, status_code=201)
def add_book_by_isbn(item: ISBNModel):
    """
    Endpoint to add a new book to the library using its ISBN.
    This reuses the logic from Stage 2.
    """
    # We get the ISBN from the request body, which is validated by Pydantic's ISBNModel.
    new_book = lib.add_book(item.isbn)

    # If the book wasn't found in the external API or already exists,
    # lib.add_book returns None. We should return a proper HTTP error in that case.
    if new_book is None:
        raise HTTPException(
            status_code=404,  # 404 Not Found is a suitable error code
            detail=f"Book with ISBN {item.isbn} could not be found or already exists in the library."
        )

    # If successful, return the newly created book object.
    # FastAPI handles converting it to JSON and sends a 201 Created status code.
    return new_book


@app.delete("/books/{isbn}", status_code=200)
def delete_book(isbn: str):
    """
    Endpoint to delete a book from the library by its ISBN.
    The ISBN is passed as part of the URL path.
    """
    was_removed = lib.remove_book(isbn)

    if not was_removed:
        # If remove_book returns False, it means no book with that ISBN was found.
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {isbn} not found in the library."
        )

    # If successful, return a confirmation message.
    # FastAPI automatically converts this dictionary to JSON.
    return {"message": "Book successfully deleted", "isbn": isbn}
