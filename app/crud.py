from sqlalchemy.orm import Session
import httpx
# CHANGED: Replaced relative import with absolute import
import models

def get_book_by_isbn(db: Session, isbn: str):
    """
    Retrieves a single book from the database by its ISBN.
    """
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def get_all_books(db: Session):
    """
    Retrieves all books from the database.
    """
    return db.query(models.Book).all()

def create_book(db: Session, isbn: str):
    """
    Fetches book data from the Open Library API and creates a new book record in the database.
    """
    # 1. Check if the book already exists in our database.
    db_book = get_book_by_isbn(db, isbn=isbn)
    if db_book:
        print(f"Error: Book with ISBN {isbn} already exists.")
        return None  # Indicate that the book already exists

    # 2. Fetch data from the external API.
    print(f"Fetching book data for ISBN: {isbn}...")
    api_url = "https://openlibrary.org/api/books"
    params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

    try:
        with httpx.Client() as client:
            response = client.get(api_url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

        if not data or f"ISBN:{isbn}" not in data:
            print(f"Error: No book found with ISBN {isbn} in Open Library.")
            return None  # Indicate that the book was not found externally

        book_data = data[f"ISBN:{isbn}"]
        title = book_data.get("title", "Unknown Title")
        authors_list = book_data.get("authors", [])
        author_names = ", ".join([author['name'] for author in authors_list]) if authors_list else "Unknown Author"

        # 3. Create a new SQLAlchemy Book model instance.
        new_book = models.Book(title=title, author=author_names, isbn=isbn)

        # 4. Add the new book to the session, commit it to the database, and refresh its state.
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        print(f"Successfully added: {new_book}")
        return new_book

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"An error occurred with the Open Library API: {e}")
        return None

def remove_book(db: Session, isbn: str):
    """
    Deletes a book from the database by its ISBN.
    """
    book_to_remove = get_book_by_isbn(db, isbn=isbn)
    if book_to_remove:
        db.delete(book_to_remove)
        db.commit()
        print(f"Book removed: {book_to_remove}")
        return True
    else:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

