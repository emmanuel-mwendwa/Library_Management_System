from pydantic import BaseModel

from typing import Optional


class BookInput(BaseModel):
    title: str
    author: str
    publication_date: Optional[str] = None
    isbn: Optional[str] = None
    total_copies: int