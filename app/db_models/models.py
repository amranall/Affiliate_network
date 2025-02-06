from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db_models.db import Base


class AffiliateNetwork(Base):
    __tablename__ = "affiliate_networks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    affiliate_link = Column(String, nullable=False)
    reward = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="affiliate_networks")
