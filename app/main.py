from fastapi import FastAPI
from app.endpoints import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/main", tags=["main"])


@app.get("/")
def read_root():
    return {"Hello": "World"}