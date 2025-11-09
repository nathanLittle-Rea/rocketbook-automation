# Rocketbook Automation - Project Overview

## What This Does

Automatically processes your handwritten Rocketbook notes with AI to:
- Extract tasks and action items
- Identify patterns and recurring themes
- Generate insights and summaries
- Track long-running tasks across time
- Create searchable, linked notes in Obsidian

## How It Works

```
┌─────────────────────┐
│   Write in          │
│   Rocketbook        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Scan with         │
│   Rocketbook App    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Google Drive      │ ◄── Temporary storage (30 days)
│   /Rocketbook       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Daily Sync        │
│   (8 PM via cron)   │
│                     │
│  1. Download PDFs   │
│  2. Extract text    │
│  3. Analyze (Claude)│
│  4. Create notes    │
│  5. Clean up old    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Obsidian Vault    │
│   /Rocketbook/      │
│   ├── Scans/        │
│   ├── PDFs/         │
│   └── Insights/     │
└─────────────────────┘
```

## Project Structure

```
rocketbook-automation/
├── config/                          # Configuration files
│   ├── analysis_config.yaml         # AI analysis settings
│   ├── credentials.json             # Google Drive credentials (you add this)
│   ├── token.pickle                 # Google auth token (auto-generated)
│   └── processed_files.txt          # Track processed files
│
├── scripts/                         # Python modules
│   ├── sync.py                      # Main sync orchestrator
│   ├── google_drive.py              # Google Drive API client
│   ├── claude_analyzer.py           # Claude AI analysis
│   └── obsidian_writer.py           # Obsidian note writer
│
├── logs/                            # Log files
│   ├── sync_YYYYMMDD.log           # Daily sync logs
│   └── cron.log                     # Cron execution logs
│
├── temp/                            # Temporary file storage
│
├── venv/                            # Python virtual environment
│
├── .env                             # Environment variables (you configure this)
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Setup script
├── install_cron.sh                  # Cron installation script
├── README.md                        # Full documentation
├── QUICKSTART.md                    # Quick start guide
└── PROJECT_OVERVIEW.md              # This file
```

## Key Components

### 1. Google Drive Client (`google_drive.py`)
- Authenticates with Google Drive API
- Downloads PDF files from Rocketbook folder
- Deletes files older than 30 days
- Tracks which files have been processed

### 2. Claude Analyzer (`claude_analyzer.py`)
- Sends note text to Claude AI
- Extracts structured insights:
  - Tasks and action items
  - Key themes and topics
  - Questions and uncertainties
  - Patterns and observations
- Generates relevant tags
- Creates weekly summaries

### 3. Obsidian Writer (`obsidian_writer.py`)
- Creates formatted markdown notes
- Embeds original PDF scans
- Adds metadata and tags
- Maintains task tracker
- Generates weekly insight summaries

### 4. Sync Orchestrator (`sync.py`)
- Coordinates the entire process
- Handles errors and logging
- Manages temporary files
- Tracks processing state

## Configuration Files

### `.env` - Environment Variables
```bash
CLAUDE_API_KEY=sk-ant-...           # Your Anthropic API key
OBSIDIAN_VAULT_PATH=/path/to/vault  # Obsidian vault location
GOOGLE_DRIVE_FOLDER_NAME=Rocketbook # Google Drive folder name
GOOGLE_DRIVE_RETENTION_DAYS=30     # How long to keep files
LOG_LEVEL=INFO                      # Logging verbosity
```

### `analysis_config.yaml` - AI Analysis Settings
Controls what Claude looks for:
- Task detection patterns
- Theme identification
- Tag generation rules
- Weekly summary settings

## Output in Obsidian

### Individual Note Format
```markdown
---
created: 2025-11-08 20:00:15
source: rocketbook
type: handwritten-note
tags: #work #tasks #project-x
---

# Rocketbook Note - November 08, 2025

## Summary
Brief AI-generated summary of the note's content.

## PDF Scan
![[../PDFs/2025-11-08-200015.pdf]]

## Tasks & Action Items
- [ ] Review design mockups by Friday
- [ ] Schedule 1:1 with Sarah
- [x] Complete quarterly report

## Key Themes & Topics
- Project planning
- Team coordination
- Budget review

## Questions & Open Items
- What's the timeline for feature X?
- Need clarification on budget allocation

## Insights & Observations
- Recurring theme: Need better project tracking
- Decision: Going with Option A for architecture

## Original OCR Text
[Raw extracted text from the scan]
```

### Task Tracker (`Task-Tracker.md`)
Consolidated view of all tasks:
- Open tasks with source notes
- Long-running tasks (spanning multiple notes)
- Recently completed tasks

### Weekly Insights (`Insights/2025-11-week-45.md`)
AI-generated weekly summary:
- Task progress
- Recurring patterns
- Top themes
- Open questions
- Recommendations

## Customization Points

### 1. Adjust Analysis Focus
Edit `config/analysis_config.yaml`:
```yaml
patterns:
  tasks:
    keywords:
      - "TODO"
      - "ACTION"
      # Add your own keywords
```

### 2. Change Sync Schedule
Edit cron job:
```bash
crontab -e
# Change from daily to hourly, weekly, etc.
```

### 3. Modify Note Template
Edit `scripts/obsidian_writer.py`:
- Change markdown format
- Add custom sections
- Modify metadata structure

### 4. Enhance Analysis Prompt
Edit `scripts/claude_analyzer.py`:
- Add domain-specific insights
- Include custom analysis sections
- Adjust AI behavior

## Workflow Tips

### Daily Review
1. Check `Rocketbook/Task-Tracker.md` for open tasks
2. Review new notes in `Rocketbook/Scans/`
3. Update links between related notes

### Weekly Review
1. Read the weekly insights summary
2. Identify long-running tasks
3. Notice patterns in your note-taking
4. Adjust priorities based on themes

### Monthly Cleanup
1. Review and archive completed tasks
2. Update tag taxonomy if needed
3. Check logs for any errors
4. Verify Google Drive cleanup is working

## Maintenance

### Update Dependencies
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Check Sync Status
```bash
# View recent logs
tail -f logs/sync_*.log

# View cron logs
tail -f logs/cron.log

# Test sync manually
source venv/bin/activate
python scripts/sync.py
```

### Troubleshooting
1. Check logs in `logs/` directory
2. Verify `.env` configuration
3. Test Google Drive connection
4. Validate Claude API key
5. Check Obsidian vault path

## API Costs

### Claude API (Anthropic)
- Model: Claude Sonnet 4.5
- Cost per note: ~$0.01-0.03
- Estimated monthly: $5-15 (for 5-10 notes/day)

### Google Drive API
- Free tier: 1 billion queries/day
- This project uses < 100 queries/day
- **Cost: $0**

## Privacy & Security

- ✅ All processing happens locally
- ✅ Notes stored in your Obsidian vault (local)
- ✅ Google Drive used only as temporary transit
- ✅ Claude API: Notes sent to Anthropic for analysis
- ✅ No data shared with third parties
- ⚠️ Keep your API keys secure
- ⚠️ Don't commit `.env` to version control

## Future Enhancements

Possible additions:
- [ ] OCR for better text extraction (pytesseract)
- [ ] Automatic linking between related notes
- [ ] Smart tag suggestions based on vault history
- [ ] Mobile app for triggering sync on-demand
- [ ] Email notifications for important tasks
- [ ] Integration with calendar for task scheduling
- [ ] Voice note processing
- [ ] Multi-notebook support

## Support & Contributing

### Get Help
1. Check `QUICKSTART.md` for setup issues
2. Review logs for error messages
3. Open an issue with log details

### Customize
Feel free to modify any scripts to fit your workflow!

## License

This is your personal automation system. Use and modify as you wish!

---

Built with ❤️ for better note-taking
