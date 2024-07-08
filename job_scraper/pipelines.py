from app.jobs.models import Job
from app.common.database import SessionLocal
from sqlalchemy.exc import IntegrityError


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
        existing_job = self.session.query(Job).filter_by(url=item.get('url')).first()

        if existing_job:
            existing_job.title = item.get('title').strip()
            existing_job.company = item.get('company').strip()
            existing_job.location = item.get('location').strip()
            existing_job.date_posted = item.get('date_posted')
        else:
            job = Job(
                title=item.get('title').strip(),
                company=item.get('company').strip(),
                location=item.get('location').strip(),
                date_posted=item.get('date_posted'),
                url=item.get('url').strip()
            )
            self.session.add(job)
        
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            spider.logger.error(f"IntegrityError processing item: {item.get('url')}")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error processing item: {e}")

        return item