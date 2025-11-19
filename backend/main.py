from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from database import db

load_dotenv()

app = FastAPI(title="Code Craft API")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Code Craft API is running"}

@app.get("/test")
def test_db():
    db_url = os.getenv("DATABASE_URL")
    db_name = os.getenv("DATABASE_NAME")
    try:
        collections = db.list_collection_names() if db is not None else []
        return {
            "backend": "ok",
            "database": "connected" if db is not None else "not_configured",
            "database_url": "set" if db_url else "missing",
            "database_name": db_name or "missing",
            "connection_status": "ok" if db is not None else "unavailable",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "ok", "database": "error", "error": str(e)}

# Expose schemas for tooling (optional)
@app.get("/schema")
def get_schema():
    try:
        from schemas import User, Product
        return {
            "schemas": [
                {"name": "user", "fields": list(User.model_fields.keys())},
                {"name": "product", "fields": list(Product.model_fields.keys())},
            ]
        }
    except Exception as e:
        return {"error": str(e)}
