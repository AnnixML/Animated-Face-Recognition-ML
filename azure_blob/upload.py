import os
import ntpath
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# Credentials for connection string
# KEEP THIS PRIVATE!!!
account_name = 'anniximagestorage'
account_key = 'wYjZ2aeHMDX+pyUHmwFtV4LYkHgP7tKHa+TKIuBinVOU1Sa76L8stmoLDh51XvSnkPBxn/J62QED+AStowt7iA=='
container_name = 'images'
connection_string = 'DefaultEndpointsProtocol=https;AccountName=' + account_name + ';AccountKey=' + account_key + ';EndpointSuffix=core.windows.net'
# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create a container client
container_client = blob_service_client.get_container_client(container_name)

blobs_list = container_client.list_blobs()

for blob in blobs_list:
    print(blob.name)
    sas_token = generate_blob_sas(account_name = account_name,
                                container_name = container_name,
                                blob_name = blob,
                                account_key=account_key,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=1))
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas_token}"
    print(sas_url)

# Change local directory to the folder where the files are located
os.chdir('azure_blob/')

def download_file(path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=path)
    with open(file=os.path.join(r'filepath', 'filename'), mode="wb") as sample_blob:
        download_stream = blob_client.download_blob()
        sample_blob.write(download_stream.readall())

def upload_file(path, image=True):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=path)
    with open(path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

def delete_file(path):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=path)
    blob_client.delete_blob()

# TODO - create tag system for tokenization

# upload_file("test.txt")