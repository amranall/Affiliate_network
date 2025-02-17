from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Transaction, func
from sqlalchemy.orm import relationship, Session

from app.db_models.models import Referral, User
from .db_models.db import Base, engine, SessionLocal, get_db
import uuid

app = FastAPI()

# Database Models


# Database setup
Base.metadata.create_all(bind=engine)


# Pydantic Schemas
class UserCreate(BaseModel):
    username: str
    referral_code: str = None

class Purchase(BaseModel):
    user_id: int
    amount: float

# API Endpoints
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if user.referral_code:
        referrer = db.query(User).filter(User.referral_code == user.referral_code).first()
        if referrer:
            referral = Referral(referrer_id=referrer.id, referred_user_id=new_user.id)
            db.add(referral)
            db.commit()
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/purchase/")
def make_purchase(purchase: Purchase, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == purchase.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transaction = Transaction(user_id=user.id, amount=purchase.amount)
    db.add(transaction)
    db.commit()
    
    referral = db.query(Referral).filter(Referral.referred_user_id == user.id).first()
    if referral:
        referrer = db.query(User).filter(User.id == referral.referrer_id).first()
        if referrer:
            referrer.balance += purchase.amount * 0.1  # 10% commission
            db.commit()
    
    return {"message": "Purchase recorded successfully"}
