import boto3
from app.core.config import AWS_REGION, SQS_QUEUE_URL

sqs = boto3.client("sqs", region_name=AWS_REGION)

def send_message(message_body: str):
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=message_body
    )

def receive_messages(max_messages=1, wait_time=20):
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time
    )
    return response.get("Messages", [])

def delete_message(receipt_handle: str):
    sqs.delete_message(
        QueueUrl=SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle
    )