# Python Project with .env and Google Cloud Storage Support

This project demonstrates how to set up a Python application that reads configuration from `.env` files using `python-dotenv` and integrates with Google Cloud Storage (GCS) using the `google-cloud-storage` library.

## Project Structure

```
.
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration (gitignored)
├── .gitignore           # Git ignore rules for Python projects
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- `python-dotenv`: For loading environment variables from `.env` files
- `google-cloud-storage`: For interacting with Google Cloud Storage

### 2. Configure Environment Variables

1. Copy the sample `.env` file to create your own configuration:
   ```bash
   cp .env .env.local  # Or rename/edit .env directly
   ```

2. Edit `.env` (or `.env.local`) and add your Google Cloud project details:
   ```
   # Google Cloud Storage Configuration
   GCS_PROJECT_ID=your-gcp-project-id
   GCS_CREDENTIALS_PATH=/path/to/your/service-account-key.json
   ```

   - **GCS_PROJECT_ID**: Your Google Cloud project ID.
   - **GCS_CREDENTIALS_PATH**: (Optional) Full path to your service account JSON key file. If not provided, the script will attempt to use default authentication (e.g., via `gcloud auth application-default login`).

   **Important**: Download a service account key from the Google Cloud Console:
   - Go to IAM & Admin > Service Accounts
   - Create or select a service account with Storage permissions
   - Generate a JSON key file and update the path in `.env`

   **Security Note**: Never commit your `.env` file with real credentials to version control. It's already gitignored.

### 3. Authentication Setup

Ensure you have the necessary permissions for GCS. If using service account keys, make sure the service account has roles like `roles/storage.admin` or appropriate granular permissions.

Alternatively, for local development, you can use Application Default Credentials:
```bash
gcloud auth application-default login
```

### 4. Run the Application

Execute the main script:

```bash
python main.py
```

**Expected Output** (if configured correctly):
```
Successfully connected to Google Cloud Storage project: your-project-id
Buckets in project:
 - bucket-name-1
 - bucket-name-2
```

**If authentication fails**:
```
Error accessing GCS: [error details]
Make sure to set up authentication properly.
```

### 5. Testing and Development

- The `main.py` script demonstrates:
  - Loading `.env` variables
  - Creating a GCS client with or without explicit credentials
  - Listing buckets in your project
- Extend the code to upload/download files, manage objects, etc., using the GCS client.

### Troubleshooting

- **ModuleNotFoundError**: Ensure dependencies are installed in the correct Python environment.
- **GCP Authentication Errors**: Verify your project ID, credentials path, and service account permissions.
- **No Buckets Listed**: Ensure the service account has `storage.buckets.list` permission.
- **Windows Path Issues**: Use raw strings or forward slashes for `GCS_CREDENTIALS_PATH`.

## Next Steps

- Add more GCS operations (upload, download, delete objects).
- Implement error handling for production use.
- Consider using a virtual environment (`venv`) for dependency isolation.

For more information:
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [Google Cloud Storage Client Library](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)