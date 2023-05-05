import os

from app.model import dynamodb

# DynamoDB
DDB_TABLE = dynamodb.Table(os.environ.get('DDB_TABLE_NAME'))
