from sqlalchemy.orm import sessionmaker
from app.common.database import get_db
from app.jobs.models import Job
from app.common.database import engine
from sqlalchemy.orm import Session
from app.common.database import SessionLocal


class DatabasePipeline:
    def __init__(self):
        self.create_table()

    def create_table(self):
        from app.common.database import engine, Base
        Base.metadata.create_all(bind=engine)

    def open_spider(self, spider):
        self.session = SessionLocal()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        job = Job(
            title=item.get('title').strip(),
            company=item.get('company').strip(),
            location=item.get('location').strip(),
            date_posted=item.get('date_posted').strip(),
            url=item.get('url').strip()
        )
        self.session.add(job)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error processing item: {e}")
        return item