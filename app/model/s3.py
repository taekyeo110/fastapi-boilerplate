import os
import boto3

# S3
S3_CLIENT = boto3.client('s3', region_name='ap-northeast-1')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
