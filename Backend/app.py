
from fastapi import FastAPI, Depends, HTTPException
from typing import Union
from .schema import UserPayload, ExpensePayload, LoginPayload
from models import User, ExpenseInfo
from db_connection import get_db
from sqlalchemy.orm import Session
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domain in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()  # Store as a string in DB


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


@app.post("/register_user/")
async def register_user(payload: UserPayload, db: Session = Depends(get_db)):
    if payload:
        hashed_password = hash_password(payload.password)  # Hash the password
        new_user = User(username=payload.username, name=payload.name, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return {"message": "New user registered successfully"}


@app.post("/login/")
async def login(payload: LoginPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    
    if not user or not verify_password(payload.password, user.password):
        return {"error": "Invalid username or password"}
    
    return {"message": "Login successful"}


@app.post("/save_expenses/")
async def save_expenses(payload: ExpensePayload, db: Session = Depends(get_db)):
    new_expense = ExpenseInfo(**payload.__dict__)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return {"message": "User expenses saved successfully"}


@app.post("/edit_expenses/{user_name}")
async def edit_expenses(user_name: str, payload: ExpensePayload, db: Session = Depends(get_db)):
    expense = db.query(ExpenseInfo).filter(ExpenseInfo.username == user_name).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense record not found")

    # Update only the provided fields
    for key, value in payload.__dict__.items():
        if value is not None:
            setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return {"message": "Data updated successfully"}


@app.delete("/delete_data/{user_name}")
async def delete(user_name: str, db: Session = Depends(get_db)):
    expense = db.query(ExpenseInfo).filter(ExpenseInfo.username == user_name).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense record not found")

    db.delete(expense)
    db.commit()
    return {"message": "Record deleted successfully"}


@app.get("/search_data/{user_name}")
async def get(user_name: str, db: Session = Depends(get_db)):
    expenses = db.query(ExpenseInfo).filter(ExpenseInfo.username == user_name).all()

    if not expenses:
        raise HTTPException(status_code=404, detail="No records found")

    return [
        {
            "username": exp.username,
            "amount": exp.amount,
            "category": exp.category,
            "date": exp.date
        }
        for exp in expenses
    ]
