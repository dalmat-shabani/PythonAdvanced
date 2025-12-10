from typing import Optional
from pydantic import BaseModel

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: str
    instructions: str
    cuisine: Optional[str] = None
    difficulty: Optional[int] = None
    category_id: Optional[int] = None


class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: int

    class Config:
        orm_mode = True