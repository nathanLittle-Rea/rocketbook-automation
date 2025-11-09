# Quick Start Guide

Get your Rocketbook automation up and running in 15 minutes!

## Prerequisites

- macOS (the paths are configured for your system)
- Python 3.8 or higher
- Google account
- Rocketbook app installed on iPhone
- Obsidian installed

## Step 1: Get Your Claude API Key (5 minutes)

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in with your email
3. Click on "API Keys" in the left sidebar
4. Click "Create Key"
5. Give it a name like "Rocketbook Automation"
6. Copy the API key (starts with `sk-ant-...`)
7. **Save this key** - you won't be able to see it again!

**Pricing**: Claude API is pay-as-you-go. Each note analysis costs about $0.01-0.03.
For typical usage (5-10 notes per day), expect ~$5-15/month.

## Step 2: Set Up Google Drive API (10 minutes)

### Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Rocketbook Automation"
4. Click "Create"

### Enable Google Drive API

1. In the search bar, type "Google Drive API"
2. Click on "Google Drive API"
3. Click "Enable"

### Create OAuth Credentials

1. In the left sidebar, go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Rocketbook Automation"
   - User support email: your email
   - Developer contact: your email
   - Click "Save and Continue"
   - Skip scopes (click "Save and Continue")
   - Add your email as a test user
   - Click "Save and Continue"
4. Back to Create OAuth Client ID:
   - Application type: "Desktop app"
   - Name: "Rocketbook Sync"
   - Click "Create"
5. Click "Download JSON"
6. Rename the downloaded file to `credentials.json`
7. Move it to the `config/` folder in this project

## Step 3: Install and Configure (2 minutes)

```bash
# Navigate to the project
cd /Users/nathanlittle-rea/projects/2ndBrain/rocketbook-automation

# Run setup
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Create a Python virtual environment
- Install all dependencies
- Create a `.env` file for configuration

## Step 4: Configure Environment Variables

Edit the `.env` file:

```bash
nano .env
```

Add your Claude API key (the one you got in Step 1):

```
CLAUDE_API_KEY=sk-ant-your-key-here
```

The other settings should already be correct:
- `OBSIDIAN_VAULT_PATH=/Users/nathanlittle-rea/Documents/Obsidian Vault`
- `GOOGLE_DRIVE_FOLDER_NAME=Rocketbook`

Save and exit (Ctrl+X, then Y, then Enter)

## Step 5: Configure Rocketbook App

On your iPhone:

1. Open the Rocketbook app
2. Go to Settings → Destinations
3. Set up Google Drive:
   - Choose "Google Drive"
   - Authenticate with your Google account
   - Set destination folder to: `Rocketbook`
   - Choose format: **PDF** (important!)
   - Enable "Send both PDF and text" if available
4. Configure your notebook symbols to point to this destination

## Step 6: First Sync (Test)

```bash
# Activate the virtual environment
cd /Users/nathanlittle-rea/projects/2ndBrain/rocketbook-automation
source venv/bin/activate

# Run the first sync
python scripts/sync.py
```

**What happens on first run:**
1. A browser will open asking you to authenticate with Google
2. Choose your Google account
3. Click "Allow" to grant access to Google Drive
4. The browser will show "Authentication successful"
5. The sync will run and process any PDFs in your Rocketbook folder

**Expected output:**
```
Initializing Rocketbook Sync...
Google Drive authentication successful
Found X files in Google Drive
Processing Y new files
...
Sync complete!
```

## Step 7: Set Up Daily Automation

```bash
chmod +x install_cron.sh
./install_cron.sh
```

This will create a cron job that runs every day at 8:00 PM.

**To change the time:**
```bash
crontab -e
```

Change the time in the cron expression:
- `0 20 * * *` = 8:00 PM (20:00)
- `0 8 * * *` = 8:00 AM
- `0 12 * * *` = Noon
- `0 0 * * *` = Midnight

## Step 8: Test the Complete Workflow

1. Write something in your Rocketbook
2. Scan it with the Rocketbook app
3. Wait a few seconds for upload to Google Drive
4. Run the sync manually:
   ```bash
   source venv/bin/activate
   python scripts/sync.py
   ```
5. Open Obsidian and navigate to `Rocketbook/Scans/`
6. You should see a new note with:
   - The PDF embedded
   - AI analysis with tasks, themes, insights
   - Auto-generated tags

## Troubleshooting

### "credentials.json not found"
- Make sure you downloaded it from Google Cloud Console
- Place it in the `config/` directory
- Rename it to exactly `credentials.json`

### "CLAUDE_API_KEY not set"
- Edit `.env` file
- Add the line: `CLAUDE_API_KEY=sk-ant-your-actual-key`
- Save the file

### "No files found"
- Check that your Rocketbook app is configured to send to Google Drive
- Verify the folder name matches (default: "Rocketbook")
- Make sure you've scanned at least one page

### Authentication errors
- Delete `config/token.pickle`
- Run sync again to re-authenticate

## Daily Usage

Once set up, your workflow is:

1. ✍️ Write notes in Rocketbook
2. 📱 Scan with Rocketbook app (sends to Google Drive)
3. 🤖 Automation runs daily at 8 PM:
   - Downloads new scans
   - Analyzes with Claude
   - Creates Obsidian notes
   - Deletes files older than 30 days from Google Drive
4. 📖 Review insights in Obsidian

## What You Get in Obsidian

Each scan creates:

```
Obsidian Vault/
├── Rocketbook/
│   ├── Scans/
│   │   └── 2025-11-08-200015.md      ← Your analyzed note
│   ├── PDFs/
│   │   └── 2025-11-08-200015.pdf     ← Original scan
│   ├── Insights/
│   │   └── 2025-11-week-45.md        ← Weekly summary
│   └── Task-Tracker.md                ← All tasks from notes
```

Each note includes:
- 📄 Embedded PDF of your handwritten note
- ✅ Extracted tasks and to-dos
- 🎯 Key themes and topics identified
- ❓ Questions you wrote down
- 💡 Insights and patterns
- 🏷️ Auto-generated tags
- 📝 Original OCR text

## Customization

### Change what Claude looks for

Edit `config/analysis_config.yaml` to customize:
- Task detection patterns
- Tag generation rules
- Insight types
- Weekly summary content

### Change sync frequency

Edit the cron job:
```bash
crontab -e
```

### Change retention period

Edit `.env`:
```
GOOGLE_DRIVE_RETENTION_DAYS=30  # Change to any number of days
```

## Support

- Check logs: `logs/sync_YYYYMMDD.log`
- View cron logs: `logs/cron.log`
- Manual sync: `source venv/bin/activate && python scripts/sync.py`

## Next Steps

Once you're comfortable:
1. Customize the analysis prompts in `scripts/claude_analyzer.py`
2. Adjust the Obsidian note format in `scripts/obsidian_writer.py`
3. Add custom tag rules in `config/analysis_config.yaml`
4. Set up weekly review of insights

Enjoy your automated note-taking system! 🚀
