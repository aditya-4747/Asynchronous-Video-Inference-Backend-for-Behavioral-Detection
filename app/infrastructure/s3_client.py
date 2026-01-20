import boto3
from app.core.config import AWS_REGION, S3_BUCKET_NAME

s3 = boto3.client("s3", region_name=AWS_REGION)

def upload_file(local_path: str, s3_key: str):
    s3.upload_file(local_path, S3_BUCKET_NAME, s3_key)

def download_file(s3_key: str, local_path: str):
    s3.download_file(S3_BUCKET_NAME, s3_key, local_path)

def generate_presigned_url(s3_key: str, expires=3600):
    return s3.generate_presigned_url(
        "get-object",
        Params={"Bucket": S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=expires
    )