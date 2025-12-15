from fastapi import APIRouter, HTTPException, status
from models.category import CategoryCreate, CategoryResponse
from database import get_db_connection
import sqlite3

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
def get_categories():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY name;").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    conn = get_db_connection()
    try:
        cur = conn.execute(
            "INSERT INTO categories (name) VALUES (?);",
            (category.name.strip(),)
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM categories WHERE id = ?;",
            (cur.lastrowid,)
        ).fetchone()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(400, "Category already exists")
    conn.close()
    return dict(row)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate):
    conn = get_db_connection()
    if not conn.execute(
        "SELECT 1 FROM categories WHERE id = ?;", (category_id,)
    ).fetchone():
        conn.close()
        raise HTTPException(404, "Category not found")

    conn.execute(
        "UPDATE categories SET name = ? WHERE id = ?;",
        (category.name.strip(), category_id)
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM categories WHERE id = ?;", (category_id,)
    ).fetchone()
    conn.close()
    return dict(row)

@router.delete("/{category_id}")
def delete_category(category_id: int):
    conn = get_db_connection()
    if not conn.execute(
        "SELECT 1 FROM categories WHERE id = ?;", (category_id,)
    ).fetchone():
        conn.close()
        raise HTTPException(404, "Category not found")

    conn.execute("DELETE FROM categories WHERE id = ?;", (category_id,))
    conn.commit()
    conn.close()
    return {"message": "Category deleted"}
