from fastapi import APIRouter, HTTPException, status
from ..models.category import CategoryCreate, CategoryResponse
from ..database import get_db_connection
import sqlite3
