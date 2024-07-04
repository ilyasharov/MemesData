from fastapi import FastAPI
from public_api.routers import memes

app = FastAPI()

app.include_router(memes.router, prefix="/memes", tags=["memes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Meme API"}
