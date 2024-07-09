import subprocess
from fastapi import FastAPI
from app.common.database import engine, Base
from app.users.endpoints import router as user_router
from app.jobs.endpoints import router as jobs_router


Base.metadata.create_all(bind=engine)
app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     subprocess.Popen(["python", "run_spiders.py"])


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])