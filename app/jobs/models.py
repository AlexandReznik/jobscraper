from sqlalchemy import Column, Integer, String
from ..common.database import Base
    

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    date_posted = Column(String)
    url = Column(String, unique=True)
    location = Column(String)

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title})>"
    
    def meets_preferences(self, preferences):
        preferences_list = [preference.strip() for preference in preferences]
        for preference in preferences_list:
            if (preference.lower() in self.title.lower()
                or preference.lower() in self.location.lower()):
                return True
        return False