
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


# ---------- Authors ----------

class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    bio: str | None = None


class AuthorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    bio: str | None = None


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    bio: str | None = None


class AuthorWithBookCount(AuthorOut):
    book_count: int


# ---------- Books ----------

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=0)
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=0)
    author_id: int | None = None


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    year: int | None
    author_id: int


# ---------- Members ----------

class MemberCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    phone: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = None


class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str | None
    email: str | None


# ---------- Loans ----------

class LoanCreate(BaseModel):
    book_id: int
    member_id: int
    due_at: datetime | None = None


class LoanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    member_id: int
    loaned_at: datetime
    due_at: datetime | None
    returned_at: datetime | None
