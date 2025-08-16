# test_library.py

import pytest
import os
from library import Library  # Import from the new file name
from book import Book  # Import from the new file name


@pytest.fixture
def library_fixture():
    """
    Creates a temporary Library instance for testing and cleans up the test file afterwards.
    """
    test_filename = "test_library.json"
    lib = Library(filename=test_filename)
    yield lib
    if os.path.exists(test_filename):
        os.remove(test_filename)


def test_add_book(library_fixture):
    """
    Tests if a book can be successfully added to the library.
    """
    book = Book("Test Title", "Test Author", "12345")
    library_fixture.add_book(book)
    assert len(library_fixture.books) == 1
    assert library_fixture.books[0].title == "Test Title"


def test_remove_book(library_fixture):
    """
    Tests if a book can be successfully removed from the library.
    """
    book = Book("Another Title", "Another Author", "67890")
    library_fixture.add_book(book)
    assert len(library_fixture.books) == 1

    removed = library_fixture.remove_book("67890")
    assert removed is True
    assert len(library_fixture.books) == 0

    removed_again = library_fixture.remove_book("99999")
    assert removed_again is False


def test_find_book(library_fixture):
    """
    Finds a book in the library by its ISBN.
    """
    book1 = Book("Find Me", "Author A", "find1")
    book2 = Book("Dont Find Me", "Author B", "find2")
    library_fixture.add_book(book1)
    library_fixture.add_book(book2)

    found_book = library_fixture.find_book("find1")
    assert found_book is not None
    assert found_book.title == "Find Me"

    not_found_book = library_fixture.find_book("nonexistent")
    assert not_found_book is None


def test_save_and_load_books(library_fixture):
    """
    Tests if the library data persists after saving and loading.
    """
    book = Book("Persistent Book", "Persistent Author", "persist1")
    library_fixture.add_book(book)

    new_library = Library(filename=library_fixture.filename)

    assert len(new_library.books) == 1
    assert new_library.books[0].isbn == "persist1"
