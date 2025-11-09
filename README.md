# Rocketbook Automation System

Automated workflow to sync Rocketbook scans from Google Drive to your local Obsidian vault with AI-powered insights.

## Features

- 📥 Auto-download new scans from Google Drive
- 🤖 AI analysis with Claude (tasks, patterns, insights)
- 📝 Create formatted Obsidian notes with metadata
- 🗑️ Auto-delete files from Google Drive after 30 days
- 🏷️ Automatic tagging based on content
- ⏰ Can run on schedule or on-demand

## Architecture

```
Rocketbook App → Google Drive → Local Processing → Obsidian Vault
```

## Setup

### 1. Install Dependencies

```bash
cd rocketbook-automation
pip install -r requirements.txt
```

### 2. Configure Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Drive API
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials and save as `config/credentials.json`

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
# Edit .env with your settings
```

Required variables:
- `CLAUDE_API_KEY`: Your Anthropic API key
- `OBSIDIAN_VAULT_PATH`: Path to your Obsidian vault
- `GOOGLE_DRIVE_FOLDER_NAME`: Name of folder in Google Drive (e.g., "Rocketbook")

### 4. First Run (Authentication)

```bash
python scripts/sync.py
```

This will open a browser for Google Drive authentication. After authentication, a token will be saved for future runs.

## Usage

### Manual Sync

```bash
python scripts/sync.py
```

### Automated Sync (cron)

Add to crontab to run every 15 minutes:

```bash
# Edit crontab
crontab -e

# Add this line (adjust path as needed)
*/15 * * * * cd /Users/nathanlittle-rea/projects/2ndBrain/rocketbook-automation && python scripts/sync.py >> logs/cron.log 2>&1
```

### On-Demand with Watch Mode

```bash
python scripts/sync.py --watch
```

## Output Structure

Files are saved in your Obsidian vault:

```
Obsidian Vault/
├── Rocketbook/
│   ├── Scans/
│   │   ├── 2025-11-08-143022.md
│   │   └── 2025-11-08-150045.md
│   ├── PDFs/
│   │   ├── 2025-11-08-143022.pdf
│   │   └── 2025-11-08-150045.pdf
│   └── Insights/
│       └── 2025-11-week-45.md (weekly rollup)
```

## Configuration

Edit `config/analysis_config.yaml` to customize:
- Insight patterns to look for
- Tag generation rules
- Task tracking preferences
- Retention policies

## Troubleshooting

### Authentication Issues

Delete `config/token.pickle` and re-run to re-authenticate.

### No Files Syncing

Check `logs/sync.log` for errors and verify:
- Google Drive folder name matches config
- Credentials are valid
- API is enabled

### Claude API Errors

Verify your API key is valid and has sufficient credits.
