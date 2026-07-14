from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
app = FastAPI(
    title="Bookstore API",
    description="A simple API to manage a bookstore inventory",
    version="1.0.0"
)
# In-memory "database"
books_db = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 12.99, "stock": 
10},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 14.99, "stock": 5},
    {"id": 3, "title": "1984", "author": "George Orwell", "price": 9.99, "stock": 15},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "price": 11.99, "stock": 7},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "price": 10.99, "stock": 
8},
]
# Pydantic model for creating a new book
class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, le=10000)
    stock: int = Field(ge=0, le=1000)
# Pydantic model for updating an existing book
class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=10000)
    stock: Optional[int] = Field(None, ge=0, le=1000)
      
@app.get("/books")
def get_books():
    """
    Retrieve a list of all books in the inventory.
    """
    return books_db
      
@app.get("/books/{book_id}")
def get_book(book_id: int):
    """
    Retrieve a single book by its ID.
    """
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
      
@app.get("/books/search")
def search_books(q: str, author: Optional[str] = None):
    """
    Search for books by title or author.
    """
    results = []
    for book in books_db:
        # Check if the query string matches the title or author
        if q.lower() in book["title"].lower() or q.lower() in book["author"].lower():
            # Further filter by author if provided
            if author:
                if author.lower() in book["author"].lower():
                    results.append(book)
            else:
                results.append(book)
    return results
     
@app.post("/books")
def add_book(book: BookCreate):
    """
Add a new book to the inventory.
    """
    # Check if a book with the same title and author already exists
    for existing_book in books_db:
        if existing_book["title"].lower() == book.title.lower() and existing_book["author"].lower()== book.author.lower():
            raise HTTPException(status_code=400, detail="Book already exists")
    # Generate a new ID
    new_id = max([b["id"] for b in books_db]) + 1 if books_db else 1
    # Create the new book
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "stock": book.stock
    }
    # Add to the database
    books_db.append(new_book)
    return {"message": "Book added successfully", "book": new_book}
     
@app.put("/books/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
    """
    Update an existing book's details.
    """
    # Find the book
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            # Update fields that are provided
            if book_update.title is not None:
                books_db[index]["title"] = book_update.title
            if book_update.author is not None:
                books_db[index]["author"] = book_update.author
            if book_update.price is not None:
                books_db[index]["price"] = book_update.price
            if book_update.stock is not None:
                books_db[index]["stock"] = book_update.stock
            return {"message": "Book updated successfully", "book": books_db[index]}
    raise HTTPException(status_code=404, detail="Book not found")
     
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """
    Delete a book from the inventory.
    """
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            # Remove the book from the list
            deleted_book = books_db.pop(index)
            return {"message": "Book deleted successfully", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")
