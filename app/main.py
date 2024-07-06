from fastapi import FastAPI
from app.common.database import engine, Base
from app.users.endpoints import router as user_router
from app.jobs.endpoints import router as jobs_router
# from app.users import models as user_models
# from app.jobs import models as job_models

Base.metadata.create_all(bind=engine)
app = FastAPI()
# user_models.Base.metadata.create_all(bind=engine)
# job_models.Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Scraper and Alert System"}