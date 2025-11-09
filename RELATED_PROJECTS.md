# Related Rocketbook Projects on GitHub

A comprehensive analysis of GitHub repositories offering useful functionality for Rocketbook users.

**Analysis Date:** November 9, 2025
**Total Repositories Analyzed:** 50+

---

## 🌟 Top Tier - Most Useful

### 1. openscan (54⭐ - C++)
**URL:** https://github.com/ryanpeach/openscan

**Functionality:**
- Generate printable custom scanning templates (QR codes, business cards, receipts, notes, drawings)
- Scanning API with quality control (border detection, sharpness, image size)
- Cloud integration with automatic categorization
- Multi-format document scanning
- Video frame analysis for optimal scan quality
- Modular design supporting various document types

**Status:** ⚠️ Archived (read-only as of September 2024)

**Use Cases:**
- Creating custom Rocketbook-compatible pages
- Advanced scanning workflows with quality control
- Custom template generation

**Technical Details:**
- Desktop implementation in C++
- Complex developer options with sensible defaults
- Context-specific applications

---

### 2. RocketBookPages (37⭐ - Python)
**URL:** https://github.com/FranciscodeMaussion/RocketBookPages

**Functionality:**
- Generate custom QR-coded numbered pages for Rocketbook
- Multiple page sizes: A4, Mini, Letter
- Four template types: DotGrid, Graph, Lined, Music
- CLI interface for easy customization
- Template sharing capabilities
- Optional page numbering

**Use Cases:**
- Creating unlimited custom Rocketbook pages without buying official notebooks
- Sharing custom templates between users
- Quick page generation via CLI

**Technical Details:**
- Command-line interface powered by Click
- Interactive menu system (console-menu)
- Dependencies: Pillow, PyPDF2, qrcode, reportlab
- JSON-based template configuration

**Example Usage:**
```bash
rocketqr create -q 5 -f A4 -t 0 -n True
```

---

### 3. notion-rocket (18⭐ - JavaScript)
**URL:** https://github.com/andresromerodev/notion-rocket

**Functionality:**
- CLI tool to sync Rocketbook notes with Notion
- Google Drive integration as sync mechanism
- Automated transfer from handwritten to Notion workspace
- OAuth authentication for Google Drive

**Use Cases:**
- Notion users wanting automated Rocketbook sync
- Maintaining handwritten notes in Notion ecosystem

**Technical Details:**
- Node.js/JavaScript implementation
- Requires Google Cloud Platform project
- Google Drive API integration
- OAuth credentials for desktop app
- MIT licensed

---

### 4. rocketbook by hirendra (12⭐ - Python)
**URL:** https://github.com/hirendra/rocketbook

**Functionality:**
- Google Vision API for handwriting OCR
- Converts handwritten notes to searchable text
- Creates merged PDFs (original + recognized text)
- Mac-based workflow with Scanner Pro integration
- DevonThink integration for document management

**Use Cases:**
- High-quality OCR conversion
- PDF enhancement with searchable text
- Mac-based automation workflows
- DevonThink users

**Technical Details:**
- Python (73.1%) and Shell scripts (26.9%)
- Google Vision API integration
- macOS optimized
- Works with any scanning app

---

## 💎 Second Tier - Specialized Use Cases

### 5. rocketbook-github (9⭐ - Python)
**URL:** https://github.com/MathiasSven/rocketbook-github

**Functionality:**
- Monitors Gmail for Rocketbook emails
- Automatically pushes PDFs/JPEGs to GitHub repository
- Runs every 3 minutes with auto-cleanup
- Web dashboard for management
- Password-protected interface for credentials
- Manual trigger capability

**Use Cases:**
- Git-based note management
- Version control for handwritten notes
- Obsidian users with Git sync
- GitHub-centric workflows

**Technical Details:**
- Python implementation
- Gmail API integration
- GitHub API integration
- Heroku deployment option (free tier)
- PM2 and virtual environment support
- Customizable via environment variables

**Configuration:**
- GitHub token
- Target repository and branch
- Destination folders
- Email processing intervals

---

### 6. rocketbook-to-obsidian (3⭐ - Python)
**URL:** https://github.com/jamesg31/rocketbook-to-obsidian

**Functionality:**
- Direct upload to Obsidian vault in iCloud
- Python-based automation
- Database schema for tracking processed files
- Cloud storage compatibility

**Use Cases:**
- Obsidian users with iCloud sync
- Automated vault updates
- Similar functionality to our project

**Technical Details:**
- 100% Python codebase
- Main application file (app.py)
- SQLite schema (schema.sql)
- Requirements file for dependencies

---

### 7. Rocketbook-to-Markdown (5⭐ - Ruby)
**URL:** https://github.com/meagerfindings/Rocketbook-to-Markdown

**Functionality:**
- Watches directory for OCR text files from Rocketbook
- Converts to organized Markdown files
- Smart filtering and pattern matching
- Appends to existing files (reading lists, sermon notes, etc.)
- Scheduled execution (20-second checks)
- Processed file management

**Use Cases:**
- Markdown-based workflows
- Automated organization by category
- Content appending to existing documents
- macOS automation

**Technical Details:**
- Ruby 2.4.1 or later required
- .plist configuration for scheduling
- Lunchy scheduling tool
- FileUtils for file management
- Predefined filter matching

---

### 8. rocketbook-markdown by wooni005 (2⭐ - Python)
**URL:** https://github.com/wooni005/rocketbook-markdown

**Functionality:**
- IMAP IDLE monitoring for instant processing (no polling!)
- Email-to-Markdown conversion
- Tag-based folder routing
- Preserves PDF links in Markdown
- Systemd service support
- Configurable date formatting in filenames

**Use Cases:**
- Email-based workflows
- Instant processing (vs polling)
- Tag-based organization
- Linux server deployment

**Technical Details:**
- Python implementation
- IMAP IDLE command for immediate response
- Subject line becomes filename
- Tag-to-path mappings
- Optional line ending removal
- Debug mode for troubleshooting

**Advantages:**
- Immediate response to new emails
- No resource-intensive polling
- Flexible organization system

---

### 9. RocketCheck (3⭐ - Python)
**URL:** https://github.com/SALLstice/RocketCheck

**Functionality:**
- Monitors Outlook inbox for Rocketbook scans
- Detects "TODO:" tags in documents
- Auto-creates Outlook tasks from scanned notes
- Continuous monitoring

**Use Cases:**
- Microsoft Outlook users
- Task automation from handwritten notes
- Corporate/enterprise workflows

**Technical Details:**
- Python (100%)
- Single file implementation (RocketCheck.py)
- Outlook API integration
- Active development (5 commits)

---

## 🛠️ Third Tier - Niche/Utility

### 10. jetbook (19⭐ - Java)
**URL:** https://github.com/nalch/jetbook

**Functionality:**
- Generates printable PDFs compatible with Rocketbook app
- Java/JavaScript implementation

**Use Cases:**
- Custom page generation
- Alternative to RocketBookPages

---

### 11. rocketbook-archiver (4⭐ - Python)
**URL:** https://github.com/suchir1/rocketbook-archiver

**Functionality:**
- Takes PDFs with embedded text from Rocketbook
- Stores them in Google Drive with organization

**Use Cases:**
- Simple Google Drive archival
- Organized storage without analysis

---

### 12. azfirefighter/rocketbook-paper (8⭐)
**URL:** https://github.com/azfirefighter/rocketbook-paper

**Functionality:**
- Repository of custom paper templates
- Ready-to-print designs
- No coding required

**Use Cases:**
- Pre-made custom templates
- Quick printing without generation

---

### 13. wajohnson43/rocketbook_automation (4⭐ - Python)
**URL:** https://github.com/wajohnson43/rocketbook_automation

**Description:** "Some handy tools to automate rocketbook backups and aggregation."

---

### 14. rocketnotion (4⭐ - Jupyter Notebook)
**URL:** https://github.com/mak9su4roi/rocketnotion

**Functionality:**
- Service for Rocketbook-Notion integration
- Jupyter Notebook based
- Related web app: rocketnotionApp

---

### 15. RocketBookWall (4⭐ - C#)
**URL:** https://github.com/kris701/RocketBookWall

**Functionality:**
- Application for Rocketbook Fusion
- Puts notes on your screen
- Display automation

---

### 16. obsidian-rocketbook-plugin (1⭐ - TypeScript)
**URL:** https://github.com/meagerfindings/obsidian-rocketbook-plugin

**Functionality:**
- Native Obsidian plugin for Rocketbook integration
- TypeScript implementation

---

## 📊 Comparison with Our Project

### Our Project: rocketbook-automation
**URL:** https://github.com/nathanLittle-Rea/rocketbook-automation

**Unique Advantages:**
- ✅ Claude AI integration (most advanced AI analysis available)
- ✅ Comprehensive insight extraction (tasks, patterns, themes, questions)
- ✅ Weekly summaries and long-term tracking
- ✅ Self-hosted with local processing
- ✅ Automated 30-day cleanup from Google Drive
- ✅ Cross-note task tracking to identify long-running items
- ✅ Pattern recognition across multiple notes
- ✅ Customizable analysis configuration
- ✅ Rich Obsidian integration with metadata

**Features Not Found Elsewhere:**
- Long-term pattern analysis
- Task aging detection
- AI-powered insight generation
- Weekly rollup summaries
- Customizable analysis prompts
- Task tracker consolidation

---

## 🔄 Potential Integrations to Consider

### 1. Enhance OCR Quality
**Source:** hirendra/rocketbook
**Integration:** Add Google Vision API as fallback/alternative to PyPDF2
```python
# Current: PyPDF2 for text extraction
# Enhancement: Google Vision API for better handwriting recognition
```

### 2. Add Custom Page Generation
**Source:** RocketBookPages
**Integration:** Include script to generate custom Rocketbook pages
```bash
# Add to setup.sh
pip install pillow pypdf2 qrcode reportlab
```

### 3. Instant Email Processing
**Source:** wooni005/rocketbook-markdown
**Integration:** Replace polling with IMAP IDLE for instant processing
```python
# Current: Daily cron job
# Enhancement: IMAP IDLE for immediate processing when email arrives
```

### 4. Git-Based Backup
**Source:** rocketbook-github
**Integration:** Add optional Git commit/push after Obsidian note creation
```python
# After note creation
if config['git_backup']:
    git_commit_and_push(note_path)
```

---

## 🎯 Best Alternatives by Use Case

### By Platform:
- **Notion users:** notion-rocket, rocketnotion
- **Git/GitHub users:** rocketbook-github
- **Outlook users:** RocketCheck
- **DevonThink users:** hirendra/rocketbook
- **Obsidian users:** rocketbook-to-obsidian, obsidian-rocketbook-plugin
- **Markdown workflows:** Rocketbook-to-Markdown, rocketbook-markdown

### By Workflow:
- **Custom page generation:** RocketBookPages, jetbook, openscan
- **OCR enhancement:** hirendra/rocketbook (Google Vision)
- **Instant processing:** wooni005/rocketbook-markdown (IMAP IDLE)
- **Version control:** rocketbook-github
- **Task automation:** RocketCheck
- **Simple archival:** rocketbook-archiver

### By Complexity:
- **Simple/Beginner:** azfirefighter/rocketbook-paper (templates only)
- **Intermediate:** notion-rocket, rocketbook-to-obsidian
- **Advanced:** openscan, hirendra/rocketbook, our project

---

## 💡 Feature Ideas from Other Projects

### From openscan:
- Quality control checks (border detection, sharpness)
- Template generation capabilities
- Support for multiple document types

### From RocketBookPages:
- CLI interface for page generation
- Template sharing system
- Multiple page size support

### From hirendra/rocketbook:
- Google Vision API integration
- Merged PDF output (original + OCR)
- Scanner app integration

### From rocketbook-github:
- Web dashboard for management
- Manual trigger capability
- Email monitoring with cleanup

### From wooni005/rocketbook-markdown:
- IMAP IDLE for instant processing
- Tag-based routing system
- Flexible file organization

### From Rocketbook-to-Markdown:
- Content appending to existing files
- Pattern-based filtering
- Scheduled monitoring

---

## 📈 Repository Statistics Summary

**Total repositories found:** 50+

**By Stars:**
- 50+ stars: 1 (openscan)
- 10-49 stars: 4
- 5-9 stars: 2
- 1-4 stars: 12
- 0 stars: 30+ (mostly unrelated projects)

**By Language:**
- Python: ~60% of useful repos
- JavaScript/Node: ~20%
- Java: ~5%
- Ruby: ~5%
- Other (C++, C#, TypeScript): ~10%

**By Integration Target:**
- Notion: 3 repos
- Obsidian: 3 repos
- GitHub/Git: 1 repo
- Outlook: 1 repo
- DevonThink: 1 repo
- Generic/Multiple: 6+ repos

**Status:**
- Active: Most repos
- Archived: 1 (openscan)
- Inactive/Old: Several with no recent updates

---

## 🚀 Recommendations for Enhancement

### High Priority:
1. **Add Google Vision OCR** (from hirendra/rocketbook)
   - Better handwriting recognition
   - Fallback for difficult scans
   - Cost: ~$1.50 per 1000 pages

2. **Implement IMAP IDLE** (from wooni005/rocketbook-markdown)
   - Instant processing vs daily cron
   - More responsive system
   - Better user experience

### Medium Priority:
3. **Custom page generator** (from RocketBookPages)
   - Create custom templates
   - Unlimited pages without purchase
   - Add to setup tools

4. **Git backup option** (inspired by rocketbook-github)
   - Version control for notes
   - Offsite backup
   - Easy sharing

### Low Priority:
5. **Web dashboard** (from rocketbook-github)
   - View logs via web interface
   - Manual trigger button
   - Status monitoring

6. **Quality checks** (from openscan)
   - Verify scan quality
   - Reject poor scans
   - Alert user to rescan

---

## 🎓 Lessons Learned from Analysis

### What Works Well:
- Email monitoring is most common approach
- Python is preferred language for automation
- Most focus on single platform (Notion, Obsidian, etc.)
- Custom page generation is popular

### What's Missing in Ecosystem:
- **AI-powered analysis** (only our project!)
- Long-term pattern tracking
- Cross-note intelligence
- Task aging detection
- Comprehensive insight extraction

### Our Competitive Advantages:
1. Most advanced AI integration (Claude)
2. Only project with pattern analysis
3. Only project tracking tasks over time
4. Most comprehensive Obsidian integration
5. Self-hosted privacy focus
6. Customizable analysis pipeline

---

## 📚 Additional Resources

### Official Rocketbook:
- Website: https://getrocketbook.com/
- App integrations: Google Drive, Evernote, Slack, Dropbox, Box, OneNote, OneDrive, iMessage, iCloud, Trello, Email

### Related Communities:
- r/rocketbook (Reddit)
- Rocketbook Facebook groups
- Productivity tool forums

### API Documentation:
- Google Drive API: https://developers.google.com/drive
- Google Vision API: https://cloud.google.com/vision
- Anthropic Claude API: https://console.anthropic.com/
- GitHub API: https://docs.github.com/en/rest
- Notion API: https://developers.notion.com/

---

## 🔗 Quick Reference Links

| Repository | Stars | Language | Primary Function |
|------------|-------|----------|------------------|
| [openscan](https://github.com/ryanpeach/openscan) | 54 | C++ | Custom template scanning |
| [RocketBookPages](https://github.com/FranciscodeMaussion/RocketBookPages) | 37 | Python | QR page generation |
| [jetbook](https://github.com/nalch/jetbook) | 19 | Java | PDF generation |
| [notion-rocket](https://github.com/andresromerodev/notion-rocket) | 18 | JavaScript | Notion sync |
| [rocketbook (hirendra)](https://github.com/hirendra/rocketbook) | 12 | Python | Google Vision OCR |
| [rocketbook-github](https://github.com/MathiasSven/rocketbook-github) | 9 | Python | GitHub integration |
| [rocketbook-paper](https://github.com/azfirefighter/rocketbook-paper) | 8 | - | Template repo |
| [Rocketbook-to-Markdown](https://github.com/meagerfindings/Rocketbook-to-Markdown) | 5 | Ruby | Markdown conversion |
| [rocketnotion](https://github.com/mak9su4roi/rocketnotion) | 4 | Jupyter | Notion service |
| [RocketBookWall](https://github.com/kris701/RocketBookWall) | 4 | C# | Screen display |
| [rocketbook-archiver](https://github.com/suchir1/rocketbook-archiver) | 4 | Python | Drive archival |
| [rocketbook_automation](https://github.com/wajohnson43/rocketbook_automation) | 4 | Python | Backup tools |
| [RocketCheck](https://github.com/SALLstice/RocketCheck) | 3 | Python | Outlook tasks |
| [rocketbook-to-obsidian](https://github.com/jamesg31/rocketbook-to-obsidian) | 3 | Python | Obsidian upload |
| [rocketbook-markdown](https://github.com/wooni005/rocketbook-markdown) | 2 | Python | Email to Markdown |

---

**Last Updated:** November 9, 2025
**Maintained By:** Nathan Little-Rea
**Project:** https://github.com/nathanLittle-Rea/rocketbook-automation
