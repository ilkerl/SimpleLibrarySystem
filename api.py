# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from library import Library

# --- 1. FastAPI uygulamasını oluştur ---
app = FastAPI(
    title="Simple Library API",
    description="An API for managing a small book library.",
    version="1.0.0"
)

# --- 2. Library sınıfının tek bir örneğini oluştur ---
# API'miz veri işlemleri için bu nesneyi kullanacak
lib = Library()


# --- 3. Pydantic Veri Modellerini Tanımla ---
# Bu modeller, API'nin veri yapısını (sözleşmesini) belirler.
class BookModel(BaseModel):
    """API çıktısı için bir kitabın veri modeli."""
    title: str
    author: str
    isbn: str


class ISBNModel(BaseModel):
    """API girdisi için bir ISBN'nin veri modeli."""
    isbn: str


# --- 4. API Uç Noktaları (Endpoints) ---

@app.get("/books", response_model=List[BookModel])
def get_books():
    """
    Kütüphanedeki tüm kitapların listesini getirir.
    """
    return lib.list_books()


@app.post("/books", response_model=BookModel, status_code=201)
def add_book_by_isbn(item: ISBNModel):
    """
    ISBN numarasını kullanarak kütüphaneye yeni bir kitap ekler.
    """
    new_book = lib.add_book(item.isbn)

    if new_book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {item.isbn} not found or already exists."
        )
    return new_book


@app.delete("/books/{isbn}", status_code=200)
def delete_book(isbn: str):
    """
    ISBN numarasını kullanarak kütüphaneden bir kitap siler.
    """
    was_removed = lib.remove_book(isbn)

    if not was_removed:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN {isbn} not found."
        )
    return {"message": "Book successfully deleted", "isbn": isbn}
