import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError
import json


def get_secret(secret_name, region_name="sa-east-1"):
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
            
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
    except (ClientError, NoCredentialsError):
        try:
            with open(os.path.join(os.getcwd(), 'webapp/secrets.json'), 'r') as f:
                secrets = json.load(f)
                return secrets[secret_name]
        except Exception as e_:
            raise e_

    return json.loads(json.loads(get_secret_value_response['SecretString'])['credentials'])
