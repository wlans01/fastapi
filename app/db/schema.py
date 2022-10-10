from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.utils.time_format import TimeFormat
from app.db.conn import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, nullable=False, default=TimeFormat.ktc_datetime())
    updated_at = Column(String, nullable=False, default=TimeFormat.ktc_datetime(), onupdate=TimeFormat.ktc_datetime())
    status = Column(Enum("active", "deleted", "blocked"), default="active")
    email = Column(String(length=255))
    password = Column(String(length=2000))
    username = Column(String(length=255))
    refreshToken = Column(String(length=255), nullable=True)
    items = relationship('Cups', back_populates='user')


class Cups(Base):
    __tablename__ = "cups"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, nullable=False, default=TimeFormat.ktc_datetime())
    updated_at = Column(String, nullable=False, default=TimeFormat.ktc_datetime(), onupdate=TimeFormat.ktc_datetime())
    status = Column(Enum("available", "using", "returned","cleanse","loss"), default="available")
    usedCount = Column(Integer,default = 0)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates='items')
    