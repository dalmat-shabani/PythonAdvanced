from fastapi import APIRouter, HTTPException, status
from models.recipe import RecipeCreate, RecipeResponse
from database import get_db_connection


router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/", response_model=list[RecipeResponse])
def get_recipes():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM recipes ORDER BY name;").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate):
    conn = get_db_connection()

    if recipe.category_id is not None:
        if not conn.execute(
            "SELECT 1 FROM categories WHERE id = ?;",
            (recipe.category_id,)
        ).fetchone():
            conn.close()
            raise HTTPException(400, "Category does not exist")

    cur = conn.execute("""
        INSERT INTO recipes
        (name, description, ingredients, instructions, cuisine, difficulty, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        recipe.name.strip(),
        recipe.description,
        recipe.ingredients,
        recipe.instructions,
        recipe.cuisine,
        recipe.difficulty,
        recipe.category_id
    ))

    conn.commit()
    row = conn.execute(
        "SELECT * FROM recipes WHERE id = ?;",
        (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return dict(row)

@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    conn = get_db_connection()

    if not conn.execute(
        "SELECT 1 FROM recipes WHERE id = ?;", (recipe_id,)
    ).fetchone():
        conn.close()
        raise HTTPException(404, "Recipe not found")

    if recipe.category_id is not None:
        if not conn.execute(
            "SELECT 1 FROM categories WHERE id = ?;",
            (recipe.category_id,)
        ).fetchone():
            conn.close()
            raise HTTPException(400, "Category does not exist")

    conn.execute("""
        UPDATE recipes SET
        name=?, description=?, ingredients=?, instructions=?,
        cuisine=?, difficulty=?, category_id=?
        WHERE id=?;
    """, (
        recipe.name.strip(),
        recipe.description,
        recipe.ingredients,
        recipe.instructions,
        recipe.cuisine,
        recipe.difficulty,
        recipe.category_id,
        recipe_id
    ))

    conn.commit()
    row = conn.execute(
        "SELECT * FROM recipes WHERE id = ?;", (recipe_id,)
    ).fetchone()
    conn.close()
    return dict(row)

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int):
    conn = get_db_connection()
    if not conn.execute(
        "SELECT 1 FROM recipes WHERE id = ?;", (recipe_id,)
    ).fetchone():
        conn.close()
        raise HTTPException(404, "Recipe not found")

    conn.execute("DELETE FROM recipes WHERE id = ?;", (recipe_id,))
    conn.commit()
    conn.close()
    return {"message": "Recipe deleted"}
