# test_library.py

import os
import pytest
import httpx  # Import httpx to use its classes for mocking
from library import Library
from book import Book


# This fixture is still useful. It creates a temporary, clean Library instance for each test.
@pytest.fixture
def library_fixture():
    """A fixture that creates a temporary library file for testing."""
    test_filename = "test_library.json"
    # Ensure the file is clean before the test
    if os.path.exists(test_filename):
        os.remove(test_filename)

    lib = Library(filename=test_filename)
    yield lib  # Provide the library instance to the test function

    # Teardown: Clean up the file after the test is done
    if os.path.exists(test_filename):
        os.remove(test_filename)


# --- NEW TESTS FOR STAGE 2 ---

def test_add_book_from_api_success(library_fixture, mocker):
    """
    Tests successfully adding a book by mocking a successful API response.
    """
    isbn = "9780345391803"

    mock_api_response_data = {
        f"ISBN:{isbn}": {
            "title": "The Hitchhiker's Guide to the Galaxy",
            "authors": [{"name": "Douglas Adams"}]
        }
    }

    # --- FIX IS HERE ---
    # We now create a dummy Request object and pass it to the Response.
    # The URL can be anything, as it's not actually used for a real request.
    mock_request = httpx.Request('GET', 'https://fake.url/api')
    mock_response = httpx.Response(
        200,
        json=mock_api_response_data,
        request=mock_request  # Associate the request with the response
    )

    mocker.patch.object(httpx.Client, 'get', return_value=mock_response)

    added_book = library_fixture.add_book(isbn)

    assert added_book is not None
    assert len(library_fixture.books) == 1
    assert library_fixture.books[0].title == "The Hitchhiker's Guide to the Galaxy"
    assert library_fixture.books[0].author == "Douglas Adams"


def test_add_book_from_api_not_found(library_fixture, mocker):
    """
    Tests the case where the API response does not contain the book data.
    """
    isbn = "0000000000000"

    mock_api_response_data = {}

    # --- FIX IS HERE ---
    # We also need to add the dummy request to this mocked response.
    mock_request = httpx.Request('GET', 'https://fake.url/api')
    mock_response = httpx.Response(
        200,
        json=mock_api_response_data,
        request=mock_request
    )

    mocker.patch.object(httpx.Client, 'get', return_value=mock_response)

    added_book = library_fixture.add_book(isbn)

    assert added_book is None
    assert len(library_fixture.books) == 0


def test_add_book_api_request_error(library_fixture, mocker):
    """
    Tests the case where the API call fails due to a network error.
    (This test was already passing and needs no changes.)
    """
    isbn = "1111111111111"

    mock_request = httpx.Request('GET', 'https://fake.url/api')
    mocker.patch.object(httpx.Client, 'get', side_effect=httpx.RequestError("Network error", request=mock_request))

    added_book = library_fixture.add_book(isbn)

    assert added_book is None
    assert len(library_fixture.books) == 0


# --- STAGE 1 TESTS (STILL VALID) ---

def test_remove_book_success(library_fixture):
    """Tests removing a book that exists."""
    book = Book("Test Title", "Test Author", "12345")
    library_fixture.books.append(book)

    was_removed = library_fixture.remove_book("12345")

    assert was_removed is True
    assert len(library_fixture.books) == 0


def test_remove_book_not_found(library_fixture):
    """Tests trying to remove a book that does not exist."""
    was_removed = library_fixture.remove_book("99999")

    assert was_removed is False


def test_find_book(library_fixture):
    """Tests finding an existing and non-existing book."""
    book = Book("Find Me", "Author", "54321")
    library_fixture.books.append(book)

    found_book = library_fixture.find_book("54321")
    not_found_book = library_fixture.find_book("00000")

    assert found_book is not None
    assert found_book.title == "Find Me"
    assert not_found_book is None

