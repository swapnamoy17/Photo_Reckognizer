import boto3 
import json
import os 
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')

# Elasticsearch configuration
host = os.environ['ES_HOST'] 
region = 'us-east-1'
es_index = 'photos'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)

es = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    
    custom_labels = response['ResponseMetadata']['HTTPHeaders'].get('x-amz-meta-customlabels', '')
    if custom_labels:
        custom_labels_list = [label.strip() for label in custom_labels.lower().split(',')]
    else:
        custom_labels_list = []
    
    rekognition_response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
        MaxLabels=10
    )
    detected_labels = [label['Name'].lower() for label in rekognition_response['Labels']]
    
    labels = list(set(custom_labels_list + detected_labels))
    
    doc = {
        'objectKey': object_key,
        'bucket': bucket_name,
        'createdTimestamp': datetime.now().isoformat(),
        'labels': labels
    }
    
    es.index(index=es_index, body=doc)
    print("Muchas gracias afición, esto es para vosotros. Siuuu")
    print("Lioonel Messisidisdisidsid")
    print("Cristianoooooooooo")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Document indexed successfully.')
    }
