# Library Management API

A RESTful library management API built with **Python, FastAPI, SQLAlchemy, and PostgreSQL**. The project demonstrates CRUD operations, relational data modeling, database migrations, validation, and error handling.

## Features

- Manage authors: create, list, retrieve, update, and delete
- Manage books: create, list, retrieve, update, and delete
- Manage library members
- Record book loans and returns
- List loans and filter active loans
- Validate incoming requests using Pydantic
- Handle database conflicts and invalid references
- Prevent multiple active loans for the same book
- Manage database schema changes with Alembic
- Interactive API documentation with Swagger UI

## Tech Stack

- Python 3.13
- FastAPI
- Pydantic and pydantic-settings
- SQLAlchemy
- PostgreSQL
- Psycopg 3
- Alembic
- Pytest and HTTPX (for automated testing)

## Requirements

- Python 3.11 or newer
- PostgreSQL
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/ReyhaneAalami/fastapi-library-api.git
cd fastapi-library-api
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Database Configuration

Create a PostgreSQL database for the application.

Create a `.env` file in the project root and configure the database connection:

```dotenv
DATABASE_URL=postgresql+psycopg://DB_USER:DB_PASSWORD@localhost:5432/library_db
```

Replace `DB_USER` and `DB_PASSWORD` with your local PostgreSQL credentials.

**Security:** Never commit `.env` or share database credentials publicly.

## Database Migrations

Apply the database migrations:

```bash
python -m alembic upgrade head
```

## Run the API

Start the development server:

```bash
python -m uvicorn main:app --reload
```

Open the interactive documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome information |
| POST | `/authors` | Create an author |
| GET | `/authors` | List authors |
| GET | `/authors/{author_id}` | Retrieve an author |
| PATCH | `/authors/{author_id}` | Update an author |
| DELETE | `/authors/{author_id}` | Delete an author |
| GET | `/authors/{author_id}/book-count` | Count an author's books |
| POST | `/books` | Create a book |
| GET | `/books` | List books |
| GET | `/books/{book_id}` | Retrieve a book |
| PATCH | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |
| POST | `/members` | Register a member |
| GET | `/members` | List members |
| GET | `/members/{member_id}` | Retrieve a member |
| POST | `/loans` | Create a loan |
| GET | `/loans` | List loans |
| POST | `/loans/{loan_id}/return` | Return a borrowed book |

## Project Structure

```text
fastapi-library-api/
├── alembic/
│   └── versions/
├── alembic.ini
├── database.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Data Model

The application uses relational models for authors, books, members, and loans. SQLAlchemy defines the models, while Alembic manages schema migrations.

## Error Handling and Data Integrity

The API handles invalid references, missing records, and database conflicts. A PostgreSQL partial unique index helps prevent a book from having more than one active loan at a time.

## Limitations

- Authentication and authorization are not currently implemented.
- This repository is intended as a learning and portfolio project.
- Run the application against a properly configured PostgreSQL database.

## License

No license has been specified yet. Add a license before permitting others to reuse or redistribute this project.
