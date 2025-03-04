
from fastapi import FastAPI, Depends, HTTPException
from typing import Union
from .schema import UserPayload, ExpensePayload, LoginPayload
from models import User, ExpenseInfo
from db_connection import get_db
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import os

app = FastAPI()

# Store and retrieve encryption key
key = os.getenv("FERNET_KEY", Fernet.generate_key())
fernet = Fernet(key)


@app.post("/register_user/")
async def register_user(payload: UserPayload, db: Session = Depends(get_db)):
    if payload:
        payload.password = fernet.encrypt(payload.password.encode()).decode()
        new_user = User(**payload.__dict__)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return {"message": "New user registered successfully"}


@app.post("/login_user/")
async def login_user(payload: LoginPayload, db: Session = Depends(get_db)):
    get_user = db.query(User).filter(User.username == payload.username).first()

    if not get_user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        decrypt_password = fernet.decrypt(get_user.password.encode()).decode()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid password")

    if decrypt_password != payload.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful", "user": payload.username}


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
    expense = db.query(ExpenseInfo).filter(ExpenseInfo.username == user_name).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Record not found")

    return {
        "username": expense.username,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date
    }
