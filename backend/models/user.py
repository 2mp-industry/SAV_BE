# models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Text, func, Enum
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid
from db.database import Base
from core.enums import UserRole  # Correction: enums au lieu de enum

class User(Base):
    __tablename__ = "users"
    
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(Enum(UserRole, native_enum=False, length=50), nullable=False, default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UNIQUEIDENTIFIER, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"