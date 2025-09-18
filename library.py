import json
import os
import httpx  # --- ADDED: For making HTTP requests ---
from book import Book


class Library:
    """
    Manages all library operations, now including fetching data from the Open Library API.
    """

    def __init__(self, filename="library.json"):
        """
        Initializes the Library object.
        """
        self.filename = filename
        self.books = self.load_books()

    # --- load_books and save_books methods remain the same ---

    def load_books(self):
        """
        Loads the list of books from the JSON file.
        """
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, 'r') as f:
                if os.path.getsize(self.filename) == 0:
                    return []
                data = json.load(f)
                return [Book(item['title'], item['author'], item['isbn']) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        """
        Saves the current list of books to the JSON file.
        """
        with open(self.filename, 'w') as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    # --- MODIFIED: add_book method ---

    def add_book(self, isbn):
        """
        Fetches book data from the Open Library API using its ISBN and adds it to the library.
        The method now takes an ISBN string instead of a Book object.

        Args:
            isbn (str): The ISBN of the book to fetch and add.

        Returns:
            Book or None: The added Book object if successful, otherwise None.
        """
        # 1. Check for duplicates first.
        if self.find_book(isbn):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return None

        # 2. Prepare the API request.
        print(f"Fetching book data for ISBN: {isbn}...")
        api_url = "https://openlibrary.org/api/books"
        params = {"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"}

        # 3. Make the API call with error handling.
        try:
            # Use a with statement for the client to ensure resources are managed correctly.
            with httpx.Client() as client:
                response = client.get(api_url, params=params, timeout=10.0)
                # Raise an exception for bad status codes (4xx or 5xx).
                response.raise_for_status()
                data = response.json()

            # 4. Process the API response.
            if not data or f"ISBN:{isbn}" not in data:
                print(f"Error: No book found with ISBN {isbn}.")
                return None

            book_data = data[f"ISBN:{isbn}"]
            title = book_data.get("title", "Unknown Title")

            # Handle authors list, which might be missing or empty.
            authors_list = book_data.get("authors", [])
            author_names = ", ".join([author['name'] for author in authors_list]) if authors_list else "Unknown Author"

            # 5. Create a new Book object and add it to the library.
            new_book = Book(title, author_names, isbn)
            self.books.append(new_book)
            self.save_books()
            print(f"Successfully added: {new_book}")
            return new_book

        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            print("Please check your internet connection.")
            return None
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
            print(f"The book with ISBN {isbn} might not exist in the Open Library database.")
            return None

    # --- remove_book, find_book, and list_books methods remain the same ---

    def remove_book(self, isbn):
        """
        Removes a book from the library by its ISBN and saves the changes.
        """
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"Book removed: {book_to_remove}")
            return True
        else:
            print(f"Error: Book with ISBN {isbn} not found.")
            return False

    def find_book(self, isbn):
        """
        Finds a specific book in the library by its ISBN.
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def list_books(self):
        """
        Displays all the books currently in the library.
        """
        if not self.books:
            print("\nThe library is currently empty.")
            return

        print("\n--- Books in Library ---")
        for book in self.books:
            print(book)

