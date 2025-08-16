# library.py

import json
from book import Book  # Import from the new file name


class Library:
    """
    Manages the collection of books, including loading from and saving to a file.
    """

    def __init__(self, filename="library.json"):
        """
        Initializes the Library.

        Args:
            filename (str): The name of the file to store book data.
        """
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        """
        Loads the books from the JSON file.
        Handles the case where the file does not exist.

        Returns:
            list: A list of Book objects.
        """
        try:
            with open(self.filename, 'r') as f:
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

    def add_book(self, book):
        """
        Adds a new book to the library and saves the updated list to the file.

        Args:
            book (Book): The Book object to add.
        """
        self.books.append(book)
        self.save_books()
        print(f"Book added: {book}")

    def remove_book(self, isbn):
        """
        Removes a book from the library by its ISBN.

        Args:
            isbn (str): The ISBN of the book to remove.

        Returns:
            bool: True if the book was found and removed, False otherwise.
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

        Finds a book in the library by its ISBN.

        Args:
            isbn (str): The ISBN of the book to find.

        Returns:
            Book or None: The found Book object, or None if not found.
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def list_books(self):
        """
        Prints all the books currently in the library.
        """
        if not self.books:
            print("The library is empty.")
        else:
            print("\n--- Library Books ---")
            for book in self.books:
                print(book)
            print("---------------------\n")
