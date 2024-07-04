import boto3
from media_service.settings import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)

def create_bucket():
    s3_client.create_bucket(Bucket=settings.S3_BUCKET_NAME)
