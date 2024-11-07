from fastapi import FastAPI

from app.common.database import Base, engine
from app.jobs.endpoints import router as jobs_router
from app.users.endpoints import router as user_router


Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url="/")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])