import json
import os
from book import Book  # Import the Book class from our book.py file


class Library:
    """
    Manages all library operations, including saving and loading books
    from a JSON file.
    """

    def __init__(self, filename="library.json"):
        """
        Initializes the Library object.

        Args:
            filename (str): The name of the file used for storing book data.
                            Defaults to "library.json".
        """
        self.filename = filename
        self.books = self.load_books()  # Load existing books from the file on startup.

    def load_books(self):
        """
        Loads the list of books from the JSON file.
        Handles cases where the file doesn't exist or is empty.

        Returns:
            list[Book]: A list of Book objects.
        """
        # Ensure the file exists before trying to read it.
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, 'r') as f:
                # Handle the case of an empty file to prevent JSONDecodeError
                if os.path.getsize(self.filename) == 0:
                    return []
                data = json.load(f)
                # Convert each dictionary in the JSON file back into a Book object.
                return [Book(item['title'], item['author'], item['isbn']) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file is not found or corrupted, start with an empty library.
            return []

    def save_books(self):
        """
        Saves the current list of books to the JSON file.
        This method is called whenever a change is made (add/remove).
        """
        with open(self.filename, 'w') as f:
            # Convert the list of Book objects into a list of dictionaries using the to_dict method.
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def add_book(self, book):
        """
        Adds a new Book object to the library and saves the updated list to the file.

        Args:
            book (Book): The Book object to add to the library.
        """
        # Check for duplicates before adding.
        if self.find_book(book.isbn):
            print(f"Error: Book with ISBN {book.isbn} already exists.")
            return

        self.books.append(book)
        self.save_books()
        print(f"Book added: {book}")

    def remove_book(self, isbn):
        """
        Removes a book from the library by its ISBN and saves the changes.

        Args:
            isbn (str): The ISBN of the book to remove.

        Returns:
            bool: True if the book was removed, False otherwise.
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

        Args:
            isbn (str): The ISBN of the book to find.

        Returns:
            Book or None: The found Book object, or None if no book is found.
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
            print(book)  # This will automatically use the __str__ method of the Book class.
