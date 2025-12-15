from pydantic import BaseModel
from typing import Optional

class RecipeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: str
    instructions: str
    cuisine: Optional[str] = None
    difficulty: Optional[str] = None
    category_id: Optional[int] = None

class RecipeResponse(RecipeCreate):
    id: int
