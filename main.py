
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Library Management API",
    description="A simple library management API without a database.",
    version="1.0.0",
)


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int | None = Field(default=None, ge=0)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    author: str | None = Field(default=None, min_length=1)
    year: int | None = Field(default=None, ge=0)


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int | None = None


# In-memory storage: book ID -> book data
books: dict[int, dict] = {}
next_book_id = 1


@app.get("/")
def home():
    return {
        "message": "Welcome to the Library Management API",
        "docs": "/docs",
    }


@app.get("/books", response_model=list[Book])
def get_books():
    return list(books.values())


@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookCreate):
    global next_book_id

    new_book = {
        "id": next_book_id,
        **book.model_dump(),
    }

    books[next_book_id] = new_book
    next_book_id += 1

    return new_book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = books.get(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return book


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_data: BookUpdate):
    book = books.get(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    changes = updated_data.model_dump(exclude_unset=True)

    for field in ("title", "author"):
        if field in changes and changes[field] is None:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null",
            )

    book.update(changes)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted_book = books.pop(book_id, None)

    if deleted_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return {
        "message": "Book deleted successfully",
        "deleted_book": deleted_book,
    }
