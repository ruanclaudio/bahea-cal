import boto3
import os
from botocore.exceptions import ClientError
import json


def get_secret(secret_name, region_name="sa-east-1"):
    if "dev" in secret_name:
        try:
            with open(os.path.join(os.getcwd(), 'webapp/secrets.json'), 'r') as f:
                secrets = json.load(f)
                return secrets[secret_name]
        except Exception as e_:
            raise e_ from e_
    else:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e
        
        return json.loads(json.loads(get_secret_value_response['SecretString'])['credentials'])