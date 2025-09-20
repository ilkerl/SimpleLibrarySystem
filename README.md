# Simple Library System

This project is a three-stage library management system developed as part of the Global AI Hub Python 202 Bootcamp. The application evolves from a simple command-line tool into a web service with its own API.

## Project Stages

**Stage 1: OOP Terminal Application** - A console-based application built using Object-Oriented Programming principles to manage a local library stored in a JSON file.

**Stage 2: External API Integration** - The application is enhanced to fetch book details (title, author) automatically from the Open Library API using just an ISBN.

**Stage 3: Web Service with FastAPI** - The core logic is exposed as a web API using the FastAPI framework, allowing programmatic access to the library.

## Features

- **Add books**: Add new books to the library manually (Stage 1) or automatically via ISBN (Stage 2 & 3).
- **Remove books**: Delete books from the library using their ISBN.
- **List all books**: View a list of all books currently in the library.
- **Find a book**: Search for a specific book by its ISBN.
- **Data Persistence**: All book data is saved locally in a `library.json` file.
- **Web API**: A RESTful API provides endpoints for listing, adding, and deleting books.
- **Automatic Documentation**: The API includes auto-generated, interactive documentation via Swagger UI.

## Installation

Follow the steps below to run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/ilkerl/SimpleLibrarySystem.git
cd SimpleLibrarySystem
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required libraries for the project using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Usage

The project can be run in two different ways: as a terminal application or as an API server.

### Terminal Application (Stage 1 & 2)

The command-line interface allows you to manage the library directly from your terminal.

To run the application:

```bash
python main.py
```

You will be presented with a menu to add, remove, list, or find books.

### API Server (Stage 3)

To run the library logic as a web service, start the Uvicorn server.

```bash
uvicorn api:app --reload
```

Once the server starts, the API will be accessible at `http://127.0.0.1:8000`.

## API Documentation

While the API server is running, you can access the interactive documentation and testing interface in your browser by navigating to:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### 1. List All Books

- **Endpoint**: `GET /books`
- **Description**: Returns a list of all books in the library in JSON format.
- **Success Response (200 OK)**:

```json
[
  {
    "title": "Dune",
    "author": "Frank Herbert",
    "isbn": "9780441013593"
  }
]
```

### 2. Add a Book via ISBN

- **Endpoint**: `POST /books`
- **Description**: Finds a book using the provided ISBN via the Open Library API and adds it to the library.
- **Request Body**:

```json
{
  "isbn": "9780743273565"
}
```

- **Success Response (201 Created)**: Returns the details of the added book.

### 3. Delete a Book

- **Endpoint**: `DELETE /books/{isbn}`
- **Description**: Deletes the book with the specified ISBN from the library.
- **URL Parameter**: `isbn` (string)
- **Success Response (200 OK)**:

```json
{
  "message": "Book successfully deleted",
  "isbn": "9780441013593"
}
```