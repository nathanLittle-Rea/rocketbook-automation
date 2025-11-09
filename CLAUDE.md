# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Rocketbook automation system that syncs handwritten notes from Google Drive to Obsidian with AI-powered analysis using Claude. The system downloads PDFs, extracts text, analyzes content for tasks/patterns/insights, and creates formatted Obsidian notes.

**Workflow:** Rocketbook App → Google Drive → Local Processing (Python) → Obsidian Vault

## Development Setup

### Initial Setup
```bash
# Install dependencies in virtual environment
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Required Configuration
Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

Required environment variables:
- `CLAUDE_API_KEY` - Anthropic API key (get from console.anthropic.com)
- `OBSIDIAN_VAULT_PATH` - Full path to Obsidian vault
- `GOOGLE_DRIVE_FOLDER_NAME` - Folder name in Google Drive (default: "Rocketbook")

Required external setup:
- `config/credentials.json` - Google Drive OAuth credentials from Google Cloud Console

### Running the Sync

```bash
# Activate virtual environment
source venv/bin/activate

# Manual sync (downloads new files, analyzes, creates Obsidian notes)
python scripts/sync.py

# Test setup without running sync
python test_setup.py
```

### Authentication Flow
First run opens browser for Google Drive OAuth. Token saved to `config/token.pickle` for subsequent runs. Delete token file to re-authenticate.

## Architecture

### Component Interaction Flow
1. **sync.py** (orchestrator) initializes three main components
2. **GoogleDriveClient** (`google_drive.py`) authenticates, lists files, downloads PDFs
3. **ClaudeAnalyzer** (`claude_analyzer.py`) sends OCR text to Claude API, parses structured response
4. **ObsidianWriter** (`obsidian_writer.py`) creates markdown notes with analysis results

### State Management
- `config/processed_files.txt` - Line-delimited list of processed Google Drive file IDs (prevents reprocessing)
- `temp/` - Downloaded PDFs stored temporarily during processing, deleted after
- `logs/sync_YYYYMMDD.log` - Daily log files

### Key Data Structures

**File metadata from Google Drive:**
```python
{
    'id': str,          # Google Drive file ID
    'name': str,        # Filename
    'createdTime': str, # ISO format timestamp
    'modifiedTime': str,
    'size': str
}
```

**Analysis result from Claude:**
```python
{
    'full_analysis': str,      # Complete markdown response
    'original_text': str,      # OCR text input
    'tasks': str,              # Extracted section
    'themes': str,
    'questions': str,
    'insights': str,
    'tags': List[str],         # Parsed tag list
    'summary': str,
    'metadata': str
}
```

## Configuration System

### Analysis Behavior (`config/analysis_config.yaml`)
Controls Claude's analysis through structured configuration:

**Pattern detection** - Keywords and thresholds for identifying tasks, questions, recurring themes
**Tagging** - Category lists and regex rules for auto-tag generation
**Insights** - Enable/disable different insight types (tasks, habits, decisions, ideas)
**Claude settings** - Model, max_tokens, temperature

Changes to YAML affect prompt construction in `claude_analyzer.py:_build_analysis_prompt()`

### Environment Variables (`.env`)
Runtime configuration loaded via `python-dotenv`. All scripts use `os.getenv()` with defaults where appropriate.

## Text Extraction Pipeline

Current implementation (`sync.py:_extract_text_from_pdf`):
1. Try PyPDF2.PdfReader for embedded text
2. If extraction yields <100 chars or fails, return empty string
3. Fallback creates note with filename placeholder

**Known limitation:** Rocketbook scans may need OCR. PyPDF2 only extracts embedded text. For scanned PDFs with no text layer, extraction returns empty and Claude receives minimal context.

**Future enhancement noted in code:** Add pytesseract or Google Vision API for actual OCR.

## Claude Integration Details

### Prompt Structure
Primary prompt in `claude_analyzer.py:_build_analysis_prompt()` constructs 7-section analysis request:
1. Tasks & Action Items
2. Key Themes & Topics
3. Questions & Uncertainties
4. Insights & Observations
5. Suggested Tags
6. Summary
7. Metadata

Prompt dynamically includes configuration from YAML (keyword lists, thresholds, enabled features).

### Response Parsing
`_parse_analysis()` extracts sections using header matching:
- `_extract_section()` - Finds content between markdown headers
- `_extract_tags()` - Parses tag section, cleans formatting, limits to `max_tags_per_note`

### API Costs
Model: `claude-sonnet-4-5-20250929`
Typical cost per note: $0.01-0.03 (varies with note length and analysis depth)

## Obsidian Output Format

### Directory Structure Created
```
{OBSIDIAN_VAULT_PATH}/Rocketbook/
├── Scans/           # Individual note markdown files
├── PDFs/            # Original PDF scans
├── Insights/        # Weekly summary rollups
└── Task-Tracker.md  # Consolidated task list
```

### Note Template
Markdown with YAML frontmatter. Key elements:
- Frontmatter: created timestamp, source, type, tags
- Embedded PDF using relative path `![[../PDFs/...]]`
- Structured sections from Claude analysis
- Original OCR text in code block

Template in `obsidian_writer.py:_build_note_content()`

## Testing & Debugging

### Verify Setup
```bash
python test_setup.py
```
Checks: Python version, .env file, required directories, credentials, dependencies, vault path existence

### View Logs
```bash
# Today's sync log
tail -f logs/sync_$(date +%Y%m%d).log

# Cron execution log (if using automated sync)
tail -f logs/cron.log
```

### Common Issues

**No text extracted:** PDF is scanned image without text layer. PyPDF2 cannot extract. Note will be created with minimal context. Claude analysis will be limited.

**Authentication errors:** Delete `config/token.pickle` and re-run to trigger OAuth flow.

**Files not syncing:** Check `config/processed_files.txt` - file IDs already processed are skipped. Delete line to reprocess.

## Modifying Analysis Behavior

### Add New Insight Type
1. Add configuration to `config/analysis_config.yaml` under `insights:`
2. Update prompt in `claude_analyzer.py:_build_analysis_prompt()` to request new section
3. Update `_parse_analysis()` to extract new section
4. Modify Obsidian template in `obsidian_writer.py:_build_note_content()` to include new section

### Customize Prompt for Domain-Specific Notes
Edit `claude_analyzer.py:_build_analysis_prompt()`. The prompt is constructed as f-string with variables from config. Can add conditional sections based on note content or user preferences.

### Change Note Output Format
Edit `obsidian_writer.py:_build_note_content()`. Returns formatted markdown string. Modify frontmatter structure, section order, or add custom formatting.

## Automation Setup

### Cron Job Installation
```bash
./install_cron.sh
```
Creates wrapper script `run_sync.sh` and installs cron job. Default: daily at 8:00 PM (`0 20 * * *`).

### Manual Cron Configuration
```bash
crontab -e
# Add line:
0 20 * * * /path/to/rocketbook-automation/run_sync.sh
```

Cron output appends to `logs/cron.log`.

## File Retention & Cleanup

Google Drive cleanup in `sync.py`: After processing, deletes files older than `GOOGLE_DRIVE_RETENTION_DAYS` (default: 30).

Uses `google_drive.py:delete_old_files()` which queries by `createdTime < cutoff_date`.

Local PDFs in `temp/` deleted immediately after Obsidian note creation.

## Dependencies

Core libraries (see `requirements.txt`):
- `google-api-python-client` - Google Drive API
- `anthropic` - Claude API client
- `python-dotenv` - Environment variable loading
- `PyYAML` - Config file parsing
- `PyPDF2` - PDF text extraction

## Code Organization Principles

**Separation of concerns:** Each script handles single responsibility (API client, analysis, writing)

**Configuration over code:** Behavior changes via YAML/env vars rather than code edits where possible

**Error isolation:** Per-file processing wrapped in try/except. One file error doesn't stop batch processing.

**Idempotency:** Processed files tracked to prevent duplicate analysis. Safe to re-run.

**Logging:** Comprehensive logging at INFO level for operations, DEBUG for technical details, ERROR for failures.
