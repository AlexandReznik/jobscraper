from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    preferences = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    date_posted = Column(String)
    url = Column(String)

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title})>"