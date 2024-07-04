from fastapi import FastAPI
from app.users.endpoints import router as user_router
from app.jobs.endpoints import router as jobs_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])


@app.get("/")
def read_root():
    return {"Hello": "World"}