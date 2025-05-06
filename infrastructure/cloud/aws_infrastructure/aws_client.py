import logging
from enum import Enum
import boto3
import yaml


class AwsService(Enum):
    SQS = 'sqs'
    S3 = 's3'
    STS = 'sts'
    SECRETS_MANAGER = 'secretsmanager'

class AWSClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def create_connection_via_token(
        service_name: AwsService,
        region_name: str,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None
    ) -> boto3.client:
        return boto3.client(
            service_name=service_name.value,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

    @staticmethod
    def assumed_role(sts_client: boto3.client, role_arn: str, role_session_name: str) -> dict:
        return sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )

    def read_secret(self, secret_manager_client: boto3.client, secret_name: str):
        secret = secret_manager_client.get_secret_value(SecretId=secret_name)
        return yaml.safe_load(secret['SecretString'])

    def get_bucket_content(self, s3_ins: boto3.client, bucket_name: str) -> boto3.client:
        return s3_ins.Bucket(bucket_name)

    def create_session(self, aws_region: str, role: dict) -> boto3.Session:
        return boto3.Session(
            region_name=aws_region,
            aws_access_key_id=role['Credentials']['AccessKeyId'],
            aws_secret_access_key=role['Credentials']['SecretAccessKey'],
            aws_session_token=role['Credentials']['SessionToken'],
        )
