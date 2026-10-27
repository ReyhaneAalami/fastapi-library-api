
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Author, Book, Loan, Member
from schemas import (
    AuthorCreate,
    AuthorOut,
    AuthorUpdate,
    AuthorWithBookCount,
    BookCreate,
    BookOut,
    BookUpdate,
    LoanCreate,
    LoanOut,
    MemberCreate,
    MemberOut,
)

app = FastAPI(
    title="Library Management API",
    description="Library API with PostgreSQL, SQLAlchemy and Alembic",
    version="2.0.0",
)


def commit_or_conflict(db: Session, message: str = "Data conflicts with an existing record"):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=message)


# ---------- Home ----------

@app.get("/")
def home():
    return {
        "message": "Welcome to the Library Management API",
        "docs": "/docs",
    }


# ---------- Authors ----------

@app.post("/authors", response_model=AuthorOut, status_code=201)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    author = Author(name=data.name.strip(), bio=data.bio)
    if not author.name:
        raise HTTPException(status_code=422, detail="Author name cannot be empty")

    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@app.get("/authors", response_model=list[AuthorOut])
def get_authors(db: Session = Depends(get_db)):
    return db.scalars(select(Author).order_by(Author.id)).all()


@app.get("/authors/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.patch("/authors/{author_id}", response_model=AuthorOut)
def update_author(
    author_id: int,
    data: AuthorUpdate,
    db: Session = Depends(get_db),
):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    changes = data.model_dump(exclude_unset=True)
    if "name" in changes:
        if changes["name"] is None or not changes["name"].strip():
            raise HTTPException(status_code=422, detail="Author name cannot be empty")
        changes["name"] = changes["name"].strip()

    for field, value in changes.items():
        setattr(author, field, value)

    db.commit()
    db.refresh(author)
    return author


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    if db.scalar(select(func.count(Book.id)).where(Book.author_id == author_id)):
        raise HTTPException(
            status_code=409,
            detail="Cannot delete an author who has books",
        )

    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}


@app.get("/authors/{author_id}/book-count", response_model=AuthorWithBookCount)
def get_author_book_count(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    count = db.scalar(
        select(func.count(Book.id)).where(Book.author_id == author_id)
    ) or 0

    return {
        "id": author.id,
        "name": author.name,
        "bio": author.bio,
        "book_count": count,
    }


# ---------- Books ----------

@app.post("/books", response_model=BookOut, status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    author = db.get(Author, data.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Book title cannot be empty")

    book = Book(title=title, year=data.year, author_id=data.author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db)):
    return db.scalars(select(Book).order_by(Book.id)).all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.patch("/books/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    changes = data.model_dump(exclude_unset=True)

    if "title" in changes:
        if changes["title"] is None or not changes["title"].strip():
            raise HTTPException(status_code=422, detail="Book title cannot be empty")
        changes["title"] = changes["title"].strip()

    if "author_id" in changes:
        if changes["author_id"] is None:
            raise HTTPException(status_code=422, detail="author_id cannot be null")
        if db.get(Author, changes["author_id"]) is None:
            raise HTTPException(status_code=404, detail="Author not found")

    for field, value in changes.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if db.scalar(select(func.count(Loan.id)).where(Loan.book_id == book_id)):
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a book that has loan history",
        )

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


# ---------- Members ----------

@app.post("/members", response_model=MemberOut, status_code=201)
def create_member(data: MemberCreate, db: Session = Depends(get_db)):
    member = Member(
        full_name=data.full_name.strip(),
        phone=data.phone.strip() if data.phone else None,
        email=str(data.email) if data.email else None,
    )
    if not member.full_name:
        raise HTTPException(status_code=422, detail="Member name cannot be empty")

    db.add(member)
    commit_or_conflict(db, "Phone or email already exists")
    db.refresh(member)
    return member


@app.get("/members", response_model=list[MemberOut])
def get_members(db: Session = Depends(get_db)):
    return db.scalars(select(Member).order_by(Member.id)).all()


@app.get("/members/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


# ---------- Loans ----------

@app.post("/loans", response_model=LoanOut, status_code=201)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    if db.get(Book, data.book_id) is None:
        raise HTTPException(status_code=404, detail="Book not found")

    if db.get(Member, data.member_id) is None:
        raise HTTPException(status_code=404, detail="Member not found")

    active_loan = db.scalar(
        select(Loan).where(
            Loan.book_id == data.book_id,
            Loan.returned_at.is_(None),
        )
    )
    if active_loan:
        raise HTTPException(status_code=409, detail="Book is already on loan")

    if data.due_at is not None and data.due_at.tzinfo is None:
        raise HTTPException(
            status_code=422,
            detail="due_at must include a timezone, e.g. +00:00",
        )

    loan = Loan(
        book_id=data.book_id,
        member_id=data.member_id,
        due_at=data.due_at,
    )
    db.add(loan)
    commit_or_conflict(db, "Book is already on loan")
    db.refresh(loan)
    return loan


@app.get("/loans", response_model=list[LoanOut])
def get_loans(
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    query = select(Loan).order_by(Loan.id)
    if active_only:
        query = query.where(Loan.returned_at.is_(None))
    return db.scalars(query).all()


@app.post("/loans/{loan_id}/return", response_model=LoanOut)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.get(Loan, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.returned_at is not None:
        raise HTTPException(status_code=409, detail="Loan has already been returned")

    loan.returned_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(loan)
    return loan
