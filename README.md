# Library Management API

A simple REST API for managing library books, built with Python and FastAPI.

## Features

- List all books
- Create a book
- Retrieve a book by ID
- Update book information
- Delete a book
- Automatic request validation
- Interactive Swagger documentation
- In-memory storage without a database

## Technologies

- Python 3.13
- FastAPI
- Pydantic

## Installation

Clone this repository:

```bash
git clone YOUR_REPOSITORY_URL
cd fastapi-library-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the API

```bash
fastapi dev main.py
```

Open the interactive documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books` | List all books |
| POST | `/books` | Create a book |
| GET | `/books/{book_id}` | Retrieve a book |
| PATCH | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |

## Example Request

Send a POST request to `/books`:

```json
{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "year": 2008
}
```

## Data Storage

Book records are stored in a Python list in memory. No database is used. All records are lost when the application restarts.

## Purpose

This project demonstrates REST API development, HTTP methods, CRUD operations, input validation, and error handling using FastAPI.