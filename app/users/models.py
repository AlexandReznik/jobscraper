from sqlalchemy import Column, Integer, String
from app.common.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    preferences = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"