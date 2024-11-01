import os
import subprocess
import boto3

class S3Sync:
    def __init__(self, access_key, secret_key, region, bucket_name):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        self.bucket_name = bucket_name

    def upload_directory(self, local_folder, s3_folder):
        """
        Recursively uploads a local directory to an S3 bucket, preserving folder structure.
        
        Parameters:
        - local_folder (str): Path of the local directory to upload.
        - s3_folder (str): Base S3 path (folder) where files should be uploaded.
        """
        for root, _, files in os.walk(local_folder):
            for file in files:
                # Full local path
                local_path = os.path.join(root, file)
                local_path = local_path.replace("\\", "/")
                
                # Create S3 path with folder structure by calculating the relative path
                relative_path = os.path.relpath(local_path, local_folder)
                s3_path = os.path.join(s3_folder, relative_path).replace("\\", "/")  # S3 uses "/" as the separator
                
                # Upload file to S3
                self.s3.upload_file(local_path, self.bucket_name, s3_path)

"""
class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        os.system(command=command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync {aws_bucket_url} {folder}"
        os.system(command=command)
"""