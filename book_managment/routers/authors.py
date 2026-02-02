import sqlite3
from sqlite3 import IntegrityError
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from book_managment.models.author import Author, AuthorCreate
from book_managment.auth.security import get_api_key
from book_managment.database import get_db_connection

router = APIRouter()

# ---------------- GET AUTHORS ----------------
@router.get("/", response_model=List[Author])
def get_authors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM authors")
    authors = cursor.fetchall()
    conn.close()

    return [
        {"id": author[0], "name": author[1]}
        for author in authors
    ]

# ---------------- CREATE AUTHOR ----------------
@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(
    author: AuthorCreate,
    _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (author.name,)
        )
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return Author(id=author_id, name=author.name)

    except IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author already exists"
        )

# ---------------- UPDATE AUTHOR ----------------
@router.put("/{author_id}", response_model=Author)
def update_author(
    author_id: int,
    author: AuthorCreate,
    _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE authors SET name = ? WHERE id = ?",
        (author.name, author_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )

    conn.commit()
    conn.close()
    return Author(id=author_id, name=author.name)

# ---------------- DELETE AUTHOR ----------------
@router.delete("/{author_id}", response_model=dict)
def delete_author(
    author_id: int,
    _: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM authors WHERE id = ?",
        (author_id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )

    conn.commit()
    conn.close()
    return {"detail": "Author deleted successfully"}
