from fastapi import FastAPI
from database import init_db
from routers.categories import router as categories_router
from routers.recipes import router as recipes_router

init_db()

app = FastAPI(title="Online Recipe Book")

app.include_router(categories_router)
app.include_router(recipes_router)
