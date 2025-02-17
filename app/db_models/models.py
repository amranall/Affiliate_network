import uuid
from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db_models.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    referral_code = Column(String, unique=True, default=lambda: str(uuid.uuid4())[:8])
    balance = Column(Float, default=0.0)
    referrals = relationship("Referral", back_populates="referrer")
    transactions = relationship("Transaction", back_populates="user")

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_user_id = Column(Integer, ForeignKey("users.id"))
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referrals")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="transactions")
