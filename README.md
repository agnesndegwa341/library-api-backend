# Library API Backend

This project is a FastAPI-based backend application for a library management system, developed as part of Lab 4. 

## Features
- **Database**: PostgreSQL integration using SQLModel.
- **ORM**: SQLModel for database interactions and Pydantic models for data validation.
- **Endpoints**:
  - `POST /books`: Create new books.
  - `GET /books`: List books with optional filtering.
  - `POST /categories`: Create library categories.
  - `GET /books/search`: Search books by author or title.
  - `PATCH /books/{book_id}`: Update existing book details.

1. Ensure Docker is running.
2. Start the database:
   ```bash
   docker compose up -d
   Run Application: 
   uvicorn main:app --reload
   Open http://127.0.0.1:8000/docs in your browser to test all endpoints 



