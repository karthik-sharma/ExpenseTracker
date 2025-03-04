from fastapi import FastAPI, Depends, HTTPException
from typing import Union
from schema import UserPayload, ExpensePayload, LoginPayload
from models import User, ExpenseInfo
from db_connection import get_db
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet

app = FastAPI()
key = Fernet.generate_key()

# Instance the Fernet class with the key

fernet = Fernet(key)


@app.post("/register_user/")
async def register_user(payload: UserPayload, db:Session = Depends(get_db)):

    if payload:
        payload.password = fernet.encrypt(payload.password.encode())
        new_user = User(**payload.__dict__)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
    return {"new user registered"}

@app.post("/login_user/")
async def login_user(payload: LoginPayload, db:Session = Depends(get_db)):

    if payload:
        passkey = payload.password
        user_name = payload.username

        get_user = db.query(User).filter(User.username == user_name).first()
        if get_user:
            decrypt_password = fernet.decrypt(get_user.password).decode()
            if  decrypt_password != passkey:
                 raise HTTPException(status_code=404, detail="User not found")
            
            return {"message": "Login successful", "user": user_name}
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.post("/save_expenses/")
async def save_expenses(payload: ExpensePayload, db: Session = Depends(get_db)):

    if payload:
        user_expenses = ExpenseInfo(**payload.__dict__)
        db.add(user_expenses)
        db.commit()
        db.refresh(user_expenses)
    
    return {"user expenses saved"}

@app.post("/edit_expenses/{item_id}")
async def edit_expenses(item_id: int, payload: ExpensePayload, db: Session = Depends(get_db)):

    data = db.query(User).filter(User.id == item_id).first()
    if data:
        payload = payload.__dict__
        data.username = payload.get("username", data.username)
        data.category = payload.get("category", data.category)
        data.amount = payload.get("amount", data.amount)
        data.date = payload.get("date", data.date)

        db.commit()
        db.refresh(data)
        return {"data updated successfully"}

@app.delete("/delete_data/{item_id}")
async def delete(item_id: int, db: Session = Depends(get_db)):
    data = db.query(User).filter(User.id == item_id).first()
    if data:
        db.delete(data)
        db.commit()
        return {"record deleted successfully"}

@app.post("/search_data/{item_id}")
async def get(item_id: int, db: Session = Depends(get_db)):
    from db_connection import User
    data = db.query(User).filter(User.id == item_id).first()
    if data:
        data.__dict__
        return {"username": data["username"], "amount": data["amount"],
                "category": data["category"], "date": data["date"]}