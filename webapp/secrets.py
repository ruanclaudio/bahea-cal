import boto3
import os
from botocore.exceptions import ClientError
import json


def get_secret(secret_name, region_name="sa-east-1"):
        try:
            session = boto3.session.Session()
            try:
                client = session.client(
                    service_name='secretsmanager',
                    region_name=region_name
                )
            except Exception as e:
                print(e)
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            
            with open(os.path.join(os.getcwd(), 'webapp/secrets.json'), 'r') as f:
                secrets = json.load(f)
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e      
        except Exception as e:
             raise e from e
  
        return secrets[secret_name], json.loads(json.loads(get_secret_value_response['SecretString'])['credentials'])