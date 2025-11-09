"""
Google Drive integration for Rocketbook automation.
Handles authentication, file listing, downloading, and deletion.
"""

import os
import pickle
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

logger = logging.getLogger(__name__)


class GoogleDriveClient:
    """Client for interacting with Google Drive API."""

    def __init__(self, credentials_path: str, token_path: str):
        """
        Initialize Google Drive client.

        Args:
            credentials_path: Path to credentials.json file
            token_path: Path to save/load token.pickle
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Drive API."""
        creds = None

        # Load token if it exists
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing Google Drive credentials...")
                creds.refresh(Request())
            else:
                logger.info("Starting Google Drive authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)
        logger.info("Google Drive authentication successful")

    def find_folder(self, folder_name: str) -> Optional[str]:
        """
        Find folder by name in Google Drive.

        Args:
            folder_name: Name of folder to find

        Returns:
            Folder ID if found, None otherwise
        """
        try:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()

            files = results.get('files', [])
            if files:
                logger.info(f"Found folder '{folder_name}' with ID: {files[0]['id']}")
                return files[0]['id']
            else:
                logger.warning(f"Folder '{folder_name}' not found in Google Drive")
                return None

        except Exception as e:
            logger.error(f"Error finding folder: {e}")
            return None

    def list_files(self, folder_id: str) -> List[Dict]:
        """
        List all PDF files in a folder.

        Args:
            folder_id: Google Drive folder ID

        Returns:
            List of file metadata dicts
        """
        try:
            query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, createdTime, modifiedTime, size)',
                orderBy='createdTime desc'
            ).execute()

            files = results.get('files', [])
            logger.info(f"Found {len(files)} PDF files in folder")
            return files

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []

    def download_file(self, file_id: str, destination_path: str) -> bool:
        """
        Download a file from Google Drive.

        Args:
            file_id: Google Drive file ID
            destination_path: Local path to save file

        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.service.files().get_media(fileId=file_id)

            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            with io.FileIO(destination_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        logger.debug(f"Download progress: {int(status.progress() * 100)}%")

            logger.info(f"Downloaded file to: {destination_path}")
            return True

        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return False

    def get_file_text(self, file_id: str) -> Optional[str]:
        """
        Export file as plain text (for Google Docs).
        For PDFs, this won't work - we'll use local OCR instead.

        Args:
            file_id: Google Drive file ID

        Returns:
            Text content if available, None otherwise
        """
        try:
            # Try to export as text (works for Google Docs)
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType='text/plain'
            )

            text_content = request.execute().decode('utf-8')
            return text_content

        except Exception as e:
            # This is expected for PDFs
            logger.debug(f"Cannot export as text (expected for PDFs): {e}")
            return None

    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file from Google Drive.

        Args:
            file_id: Google Drive file ID

        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"Deleted file with ID: {file_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

    def delete_old_files(self, folder_id: str, retention_days: int) -> int:
        """
        Delete files older than retention period.

        Args:
            folder_id: Google Drive folder ID
            retention_days: Number of days to retain files

        Returns:
            Number of files deleted
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
            cutoff_str = cutoff_date.isoformat() + 'Z'

            query = (
                f"'{folder_id}' in parents and "
                f"createdTime < '{cutoff_str}' and "
                f"trashed=false"
            )

            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, createdTime)'
            ).execute()

            files = results.get('files', [])
            deleted_count = 0

            for file in files:
                if self.delete_file(file['id']):
                    deleted_count += 1
                    logger.info(
                        f"Deleted old file: {file['name']} "
                        f"(created: {file['createdTime']})"
                    )

            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting old files: {e}")
            return 0
