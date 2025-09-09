from typing import List
import os
import logging

from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def set_bucket_public_iam(
    storage_client,
    bucket_name: str = "your-bucket-name",
    members: List[str] = ["allUsers"],
):
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    
    # Check if already public
    for binding in policy.bindings:
        if binding['role'] == 'roles/storage.objectViewer' and 'allUsers' in binding['members']:
            logger.info(f"Bucket {bucket.name} is already publicly readable. No changes needed.")
            return
    
    policy.bindings.append(
        {"role": "roles/storage.objectViewer", "members": members}
    )

    bucket.set_iam_policy(policy)

    logger.info(f"Bucket {bucket.name} is now publicly readable")

def main():
    # Get GCS credentials from environment variables
    project_id = os.getenv('GCS_PROJECT_ID')
    credentials_path = os.getenv('GCS_CREDENTIALS_PATH')  # Path to service account JSON
    
    if not project_id:
        logger.error("Error: GCS_PROJECT_ID not set in .env file")
        return
    
    try:
        # If credentials_path is provided, use it; otherwise, assume default authentication
        if credentials_path and os.path.exists(credentials_path):
            client = storage.Client.from_service_account_json(credentials_path, project=project_id)
        else:
            client = storage.Client(project=project_id)
        
        logger.info(f"Successfully connected to Google Cloud Storage project: {project_id}")
        
        bucket_name = os.getenv('GCS_BUCKET_NAME')
        if not bucket_name:
            logger.error("Error: GCS_BUCKET_NAME not set in .env file")
            return
        set_bucket_public_iam(client, bucket_name)
            
    except Exception as e:
        logger.error(f"Error accessing GCS: {e}")
        logger.error("Make sure to set up authentication properly.")

if __name__ == "__main__":
    main()
