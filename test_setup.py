#!/usr/bin/env python3
"""
Setup verification script.
Tests that all components are configured correctly.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check(condition, message):
    """Check a condition and print result."""
    if condition:
        print(f"{GREEN}✓{RESET} {message}")
        return True
    else:
        print(f"{RED}✗{RESET} {message}")
        return False

def warn(message):
    """Print a warning."""
    print(f"{YELLOW}⚠{RESET} {message}")

def main():
    """Run setup verification."""
    print("=" * 60)
    print("Rocketbook Automation - Setup Verification")
    print("=" * 60)
    print()

    all_good = True

    # Check Python version
    print("1. Python Environment")
    print("-" * 60)
    python_version = sys.version_info
    all_good &= check(
        python_version >= (3, 8),
        f"Python version: {python_version.major}.{python_version.minor}"
    )
    print()

    # Check .env file
    print("2. Environment Configuration")
    print("-" * 60)
    env_path = Path(".env")
    all_good &= check(env_path.exists(), ".env file exists")

    if env_path.exists():
        load_dotenv()

        # Check required variables
        claude_key = os.getenv('CLAUDE_API_KEY')
        all_good &= check(
            claude_key and claude_key.startswith('sk-ant-'),
            "CLAUDE_API_KEY is set and valid format"
        )

        vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
        all_good &= check(vault_path is not None, "OBSIDIAN_VAULT_PATH is set")

        if vault_path:
            all_good &= check(
                Path(vault_path).exists(),
                f"Obsidian vault exists at: {vault_path}"
            )

        gdrive_folder = os.getenv('GOOGLE_DRIVE_FOLDER_NAME')
        all_good &= check(
            gdrive_folder is not None,
            f"Google Drive folder name: {gdrive_folder}"
        )

    print()

    # Check directories
    print("3. Directory Structure")
    print("-" * 60)
    required_dirs = ['config', 'scripts', 'logs', 'temp']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        all_good &= check(dir_path.exists(), f"{dir_name}/ directory exists")
    print()

    # Check configuration files
    print("4. Configuration Files")
    print("-" * 60)
    config_yaml = Path("config/analysis_config.yaml")
    all_good &= check(config_yaml.exists(), "analysis_config.yaml exists")

    credentials = Path("config/credentials.json")
    cred_exists = check(credentials.exists(), "credentials.json exists")
    all_good &= cred_exists

    if not cred_exists:
        warn("You need to download credentials.json from Google Cloud Console")
        warn("See QUICKSTART.md for instructions")

    print()

    # Check Python dependencies
    print("5. Python Dependencies")
    print("-" * 60)
    required_packages = [
        'google.auth',
        'googleapiclient',
        'anthropic',
        'yaml',
        'dotenv',
    ]

    for package in required_packages:
        try:
            __import__(package)
            check(True, f"{package} is installed")
        except ImportError:
            all_good &= check(False, f"{package} is installed")
            warn(f"Run: pip install -r requirements.txt")

    print()

    # Check scripts
    print("6. Scripts")
    print("-" * 60)
    scripts = [
        'scripts/sync.py',
        'scripts/google_drive.py',
        'scripts/claude_analyzer.py',
        'scripts/obsidian_writer.py'
    ]

    for script in scripts:
        script_path = Path(script)
        all_good &= check(script_path.exists(), f"{script} exists")

    print()

    # Test Google Drive authentication (if credentials exist)
    if credentials.exists():
        print("7. Google Drive API")
        print("-" * 60)
        token_path = Path("config/token.pickle")
        if token_path.exists():
            check(True, "Google Drive token exists (already authenticated)")
        else:
            warn("No authentication token found")
            warn("Run 'python scripts/sync.py' to authenticate")
        print()

    # Test Claude API (if key exists)
    if claude_key:
        print("8. Claude API")
        print("-" * 60)
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=claude_key)
            # Just verify the client initializes
            check(True, "Claude API client initialized")
            warn("API key format looks correct, but not tested against API")
        except Exception as e:
            all_good &= check(False, f"Claude API initialization: {e}")
        print()

    # Summary
    print("=" * 60)
    if all_good:
        print(f"{GREEN}All checks passed! ✓{RESET}")
        print()
        print("Next steps:")
        print("1. If you haven't authenticated with Google Drive yet:")
        print("   python scripts/sync.py")
        print()
        print("2. Configure Rocketbook app to send to Google Drive")
        print()
        print("3. Scan a test page and run the sync")
        print()
        print("4. Set up daily automation:")
        print("   ./install_cron.sh")
    else:
        print(f"{RED}Some checks failed ✗{RESET}")
        print()
        print("Please fix the issues above and run this test again.")
        print()
        print("For help, see:")
        print("- QUICKSTART.md for setup instructions")
        print("- README.md for detailed documentation")

    print("=" * 60)

    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
