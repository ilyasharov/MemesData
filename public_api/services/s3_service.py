import boto3
from botocore.exceptions import NoCredentialsError
import os
from fastapi import UploadFile
from media_service.settings import settings
from dotenv import load_dotenv

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)

def upload_image_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ACL": "public-read"}
        )
        return f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{filename}"
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Could not upload file")

def delete_image_from_s3(image_url):
    try:
        bucket_key = image_url.replace(f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/", "")
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=bucket_key)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Could not delete file")
