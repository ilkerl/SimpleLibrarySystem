# test_api.py

from fastapi.testclient import TestClient
from book import Book

# Import our FastAPI app instance from the api.py file
from api import app

# Create a TestClient instance. This allows us to send HTTP requests to our app
# in our tests without needing a running server.
client = TestClient(app)


# Note on 'mocker': This is a fixture provided by the pytest-mock library.
# It allows us to replace functions or object methods with mock versions.

def test_get_all_books(mocker):
    """
    Test the GET /books endpoint.
    We'll mock the library's internal book list to test the API layer in isolation.
    """
    # 1. Prepare mock data
    mock_books = [
        Book(title="Test Book 1", author="Author 1", isbn="111").to_dict(),
        Book(title="Test Book 2", author="Author 2", isbn="222").to_dict()
    ]

    # 2. Mock the 'books' attribute of the 'lib' object inside the 'api' module.
    #    When the endpoint tries to access `lib.books`, it will get our mock data instead.
    mocker.patch('api.lib.books', mock_books)

    # 3. Make the HTTP request to the endpoint
    response = client.get("/books")

    # 4. Assert the results
    assert response.status_code == 200
    assert response.json() == [
        {"title": "Test Book 1", "author": "Author 1", "isbn": "111"},
        {"title": "Test Book 2", "author": "Author 2", "isbn": "222"}
    ]


def test_add_book_success(mocker):
    """Test the POST /books endpoint for a successful case."""
    # 1. Prepare a mock Book object that we expect `lib.add_book` to return.
    mock_book_to_return = Book(title="New Book", author="New Author", isbn="12345")

    # 2. Mock the `add_book` method of the `lib` object in the `api` module.
    mocker.patch('api.lib.add_book', return_value=mock_book_to_return)

    # 3. Make the POST request with the ISBN in the request body.
    response = client.post("/books", json={"isbn": "12345"})

    # 4. Assert the results
    assert response.status_code == 201  # Check for 201 Created status
    assert response.json() == {
        "title": "New Book",
        "author": "New Author",
        "isbn": "12345"
    }


def test_add_book_not_found(mocker):
    """Test the POST /books endpoint when the book is not found by the library."""
    # 1. Mock the `add_book` method to return None, simulating a failure.
    mocker.patch('api.lib.add_book', return_value=None)

    # 2. Make the POST request.
    response = client.post("/books", json={"isbn": "00000"})

    # 3. Assert that the API correctly returns a 404 Not Found error.
    assert response.status_code == 404
    assert "could not be found" in response.json()["detail"]


def test_delete_book_success(mocker):
    """Test the DELETE /books/{isbn} endpoint for a successful case."""
    # 1. Mock the `remove_book` method to return True, simulating success.
    mocker.patch('api.lib.remove_book', return_value=True)

    # 2. Make the DELETE request.
    response = client.delete("/books/123")

    # 3. Assert the results
    assert response.status_code == 200
    assert response.json()["message"] == "Book successfully deleted"
    assert response.json()["isbn"] == "123"


def test_delete_book_not_found(mocker):
    """Test the DELETE /books/{isbn} endpoint when the book is not found."""
    # 1. Mock the `remove_book` method to return False, simulating failure.
    mocker.patch('api.lib.remove_book', return_value=False)

    # 2. Make the DELETE request.
    response = client.delete("/books/999")

    # 3. Assert that the API correctly returns a 404 Not Found error.
    assert response.status_code == 404
    assert "not found in the library" in response.json()["detail"]
