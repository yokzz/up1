from typing import Union
from db import models, schemas, crud
from db.engine import SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
import sqlite3

from fastapi import FastAPI

app = FastAPI()
models.Base.metadata.create_all(bing=engine)

connect = sqlite3.connect('library.db')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_id(db, user_id)
    if user:
        return user
    else:
        return "User not found"


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/create_user")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    user = schemas.UserCreate(username=username, email=email)
    crud.create_user(db, user)
    return user