import pytest
import os
from library import Library
from book import Book


@pytest.fixture
def library_fixture():
    """
    This is a pytest fixture. It sets up a temporary environment for our tests.
    It creates a Library instance with a temporary JSON file and cleans up after the test is done.
    """
    # 1. Setup: Create a temporary file name for testing
    test_filename = "test_library.json"

    # Create a Library instance using this temporary file
    lib = Library(filename=test_filename)

    # 2. Yield: Provide the Library instance to the test function
    yield lib

    # 3. Teardown: This code runs after the test function completes
    # Clean up by removing the temporary file if it exists
    if os.path.exists(test_filename):
        os.remove(test_filename)


def test_add_book(library_fixture):
    """
    Tests the functionality of adding a single book to the library.
    """
    # Arrange: Create a new book instance
    book1 = Book("The Hobbit", "J.R.R. Tolkien", "12345")

    # Act: Add the book using the library fixture
    library_fixture.add_book(book1)

    # Assert: Check if the book was actually added
    assert len(library_fixture.books) == 1
    assert library_fixture.books[0].title == "The Hobbit"


def test_remove_book(library_fixture):
    """
    Tests the functionality of removing a book from the library.
    """
    # Arrange: Add a book first so we can remove it
    book1 = Book("Dune", "Frank Herbert", "67890")
    library_fixture.add_book(book1)
    assert len(library_fixture.books) == 1  # Verify it was added

    # Act: Remove the book by its ISBN
    was_removed = library_fixture.remove_book("67890")

    # Assert: Check if the book list is now empty and the method returned True
    assert len(library_fixture.books) == 0
    assert was_removed is True


def test_remove_nonexistent_book(library_fixture):
    """
    Tests that trying to remove a book that doesn't exist doesn't crash the program
    and returns False.
    """
    # Act: Attempt to remove a book with an ISBN that is not in the library
    was_removed = library_fixture.remove_book("00000")

    # Assert: The book list should still be empty and the method should return False
    assert len(library_fixture.books) == 0
    assert was_removed is False


def test_find_book(library_fixture):
    """
    Tests finding an existing book by its ISBN.
    """
    # Arrange: Add a book to find
    book1 = Book("1984", "George Orwell", "11223")
    library_fixture.add_book(book1)

    # Act: Find the book
    found_book = library_fixture.find_book("11223")

    # Assert: Check that the correct book object was returned
    assert found_book is not None
    assert found_book.isbn == "11223"
    assert found_book.title == "1984"


def test_find_nonexistent_book(library_fixture):
    """
    Tests that searching for a book that doesn't exist returns None.
    """
    # Act: Search for a book that has not been added
    found_book = library_fixture.find_book("99999")

    # Assert: The result should be None
    assert found_book is None
