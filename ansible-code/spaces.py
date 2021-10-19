import os
import boto3

session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=os.getenv('SPACES_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('SPACES_SECRET_KEY'))


# client.create_bucket(Bucket='example-space-name')


# List All Spaces in a Region
response = client.list_buckets()
for space in response['Buckets']:
    print(space['Name'])

# List All Files in a Space
bucket_name="litecoinfullnodebackup"
response = client.list_objects(Bucket=bucket_name)
for obj in response['Contents']:
    print(obj['Key'])

# delete bucket
#file_name="backups/fullnode-20211019.tgz"

#client.delete_object(Bucket=bucket_name,
                     Key=file_name)

#client.delete_bucket(Bucket=bucket_name)


