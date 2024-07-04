from fastapi import FastAPI, UploadFile, File
from media_service.s3_setup import s3_client, create_bucket
from media_service.settings import settings

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_bucket()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    s3_client.upload_fileobj(file.file, settings.S3_BUCKET_NAME, file.filename)
    return {"filename": file.filename}
