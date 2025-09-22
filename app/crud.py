from sqlalchemy.orm import Session
import httpx

# The import statement has been corrected.
# We use a relative import to tell Python to look for 'models.py'
# in the same directory (package) as this file.
from . import models


def get_book_by_isbn(db: Session, isbn: str):
    """
    Retrieves a single book from the database by its ISBN.
    """
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of all books from the database.
    """
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, isbn: str):
    """
    Fetches book data from the Open Library API and creates a new book record in the database.
    """
    # 1. Prepare the API request to Open Library.
    api_url = "https://openlibrary.org/api/books"
    params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

    # 2. Make the API call with error handling.
    try:
        with httpx.Client() as client:
            response = client.get(api_url, params=params, timeout=10.0)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()

        # 3. Process the API response.
        if not data or f"ISBN:{isbn}" not in data:
            return None  # Book not found in the external API

        book_data = data[f"ISBN:{isbn}"]
        title = book_data.get("title", "Unknown Title")
        authors_list = book_data.get("authors", [])
        author_names = ", ".join([author['name'] for author in authors_list]) if authors_list else "Unknown Author"

        # 4. Create a new Book database model instance.
        db_book = models.Book(title=title, author=author_names, isbn=isbn)

        # 5. Add the new book to the session and commit it to the database.
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    except (httpx.RequestError, httpx.HTTPStatusError):
        # If the external API call fails for any reason, return None.
        return None


def delete_book(db: Session, isbn: str):
    """
    Deletes a book from the database by its ISBN.
    """
    db_book = get_book_by_isbn(db=db, isbn=isbn)
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None
