#!/usr/bin/env python3
"""
Main sync script for Rocketbook automation.
Downloads scans from Google Drive, analyzes with Claude, and saves to Obsidian.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from google_drive import GoogleDriveClient
from claude_analyzer import ClaudeAnalyzer
from obsidian_writer import ObsidianWriter

# Load environment variables
load_dotenv()

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"
TEMP_DIR = PROJECT_ROOT / "temp"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Setup logging
log_file = LOGS_DIR / f"sync_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RocketbookSync:
    """Main sync orchestrator."""

    def __init__(self):
        """Initialize sync components."""
        logger.info("Initializing Rocketbook Sync...")

        # Load configuration
        self.gdrive_folder = os.getenv('GOOGLE_DRIVE_FOLDER_NAME', 'Rocketbook')
        self.retention_days = int(os.getenv('GOOGLE_DRIVE_RETENTION_DAYS', 30))
        self.obsidian_path = os.getenv('OBSIDIAN_VAULT_PATH')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')

        # Validate configuration
        self._validate_config()

        # Initialize components
        self.gdrive = GoogleDriveClient(
            credentials_path=str(CONFIG_DIR / "credentials.json"),
            token_path=str(CONFIG_DIR / "token.pickle")
        )

        self.analyzer = ClaudeAnalyzer(
            api_key=self.claude_api_key,
            config_path=str(CONFIG_DIR / "analysis_config.yaml")
        )

        self.writer = ObsidianWriter(vault_path=self.obsidian_path)

        # Track processed files
        self.processed_log = CONFIG_DIR / "processed_files.txt"
        self.processed_files = self._load_processed_files()

        logger.info("Initialization complete")

    def _validate_config(self):
        """Validate required configuration."""
        if not self.obsidian_path:
            raise ValueError("OBSIDIAN_VAULT_PATH not set in .env")

        if not self.claude_api_key:
            raise ValueError("CLAUDE_API_KEY not set in .env")

        if not (CONFIG_DIR / "credentials.json").exists():
            raise FileNotFoundError(
                "Google Drive credentials.json not found in config/ directory. "
                "Please follow setup instructions in README.md"
            )

    def _load_processed_files(self) -> set:
        """Load list of already processed file IDs."""
        if self.processed_log.exists():
            with open(self.processed_log, 'r') as f:
                return set(line.strip() for line in f)
        return set()

    def _mark_processed(self, file_id: str):
        """Mark a file as processed."""
        self.processed_files.add(file_id)
        with open(self.processed_log, 'a') as f:
            f.write(f"{file_id}\n")

    def sync(self):
        """Run the sync process."""
        logger.info("=" * 60)
        logger.info("Starting Rocketbook sync")
        logger.info("=" * 60)

        try:
            # Find Google Drive folder
            folder_id = self.gdrive.find_folder(self.gdrive_folder)
            if not folder_id:
                logger.error(f"Folder '{self.gdrive_folder}' not found in Google Drive")
                logger.info("Please create the folder or update GOOGLE_DRIVE_FOLDER_NAME in .env")
                return

            # Get list of files
            files = self.gdrive.list_files(folder_id)
            logger.info(f"Found {len(files)} files in Google Drive")

            # Filter to unprocessed files
            new_files = [f for f in files if f['id'] not in self.processed_files]
            logger.info(f"Processing {len(new_files)} new files")

            # Process each file
            processed_count = 0
            for file in new_files:
                try:
                    if self._process_file(file):
                        processed_count += 1
                        self._mark_processed(file['id'])
                except Exception as e:
                    logger.error(f"Error processing {file['name']}: {e}", exc_info=True)
                    continue

            logger.info(f"Successfully processed {processed_count} files")

            # Clean up old files from Google Drive
            if self.retention_days > 0:
                logger.info(f"Cleaning up files older than {self.retention_days} days...")
                deleted_count = self.gdrive.delete_old_files(folder_id, self.retention_days)
                logger.info(f"Deleted {deleted_count} old files from Google Drive")

            logger.info("Sync complete!")

        except Exception as e:
            logger.error(f"Sync failed: {e}", exc_info=True)
            raise

    def _process_file(self, file: dict) -> bool:
        """
        Process a single file.

        Args:
            file: File metadata from Google Drive

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Processing: {file['name']}")

        # Download file to temp directory
        temp_pdf = TEMP_DIR / f"{file['id']}.pdf"
        if not self.gdrive.download_file(file['id'], str(temp_pdf)):
            logger.error(f"Failed to download {file['name']}")
            return False

        # Extract text from PDF (using basic text extraction for now)
        # In production, you might want to use proper OCR for scanned PDFs
        text_content = self._extract_text_from_pdf(temp_pdf)

        if not text_content:
            logger.warning(f"No text extracted from {file['name']}, using filename")
            text_content = f"Rocketbook scan: {file['name']}\n\nNote: Text extraction failed. Please review the PDF manually."

        # Analyze with Claude
        logger.info("Analyzing note with Claude...")
        analysis = self.analyzer.analyze_note(text_content, file['name'])

        # Write to Obsidian
        timestamp = datetime.fromisoformat(file['createdTime'].replace('Z', '+00:00'))
        note_path = self.writer.write_note(
            filename=file['name'],
            analysis=analysis,
            pdf_path=str(temp_pdf),
            timestamp=timestamp
        )

        logger.info(f"Created note: {note_path}")

        # Clean up temp file
        temp_pdf.unlink()

        return True

    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from PDF.
        For Rocketbook scans, this may require OCR.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        try:
            # Try simple text extraction first
            import PyPDF2

            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'

            if text.strip():
                logger.debug("Extracted text using PyPDF2")
                return text.strip()

        except Exception as e:
            logger.debug(f"PyPDF2 extraction failed: {e}")

        # If PyPDF2 fails, the PDF likely needs OCR
        # For now, return empty and let Claude work with the filename
        # You could add pytesseract or pdf2image + OCR here later
        logger.warning("PDF text extraction failed - may need OCR")
        return ""


def main():
    """Main entry point."""
    try:
        sync = RocketbookSync()
        sync.sync()
        sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Sync interrupted by user")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
