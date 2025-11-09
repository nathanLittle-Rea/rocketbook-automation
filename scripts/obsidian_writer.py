"""
Obsidian vault writer for Rocketbook notes.
Creates formatted markdown notes with metadata and links.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class ObsidianWriter:
    """Writes analyzed notes to Obsidian vault."""

    def __init__(self, vault_path: str):
        """
        Initialize Obsidian writer.

        Args:
            vault_path: Path to Obsidian vault root
        """
        self.vault_path = Path(vault_path)

        # Create directory structure
        self.rocketbook_dir = self.vault_path / "Rocketbook"
        self.scans_dir = self.rocketbook_dir / "Scans"
        self.pdfs_dir = self.rocketbook_dir / "PDFs"
        self.insights_dir = self.rocketbook_dir / "Insights"

        self._ensure_directories()

        logger.info(f"Obsidian writer initialized at: {vault_path}")

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.scans_dir, self.pdfs_dir, self.insights_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")

    def write_note(
        self,
        filename: str,
        analysis: Dict,
        pdf_path: str,
        timestamp: datetime
    ) -> str:
        """
        Write a Rocketbook note to the Obsidian vault.

        Args:
            filename: Original filename
            analysis: Analysis results from Claude
            pdf_path: Path to the PDF file
            timestamp: Timestamp of the note

        Returns:
            Path to created markdown file
        """
        # Generate note filename based on timestamp
        note_name = timestamp.strftime("%Y-%m-%d-%H%M%S")
        note_path = self.scans_dir / f"{note_name}.md"

        # Copy PDF to vault
        pdf_dest = self.pdfs_dir / f"{note_name}.pdf"
        self._copy_pdf(pdf_path, pdf_dest)

        # Build markdown content
        content = self._build_note_content(
            note_name, analysis, pdf_dest, timestamp
        )

        # Write to file
        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created Obsidian note: {note_path}")
        return str(note_path)

    def _copy_pdf(self, source: str, destination: Path):
        """Copy PDF to Obsidian vault."""
        import shutil
        try:
            shutil.copy2(source, destination)
            logger.debug(f"Copied PDF to: {destination}")
        except Exception as e:
            logger.error(f"Error copying PDF: {e}")

    def _build_note_content(
        self,
        note_name: str,
        analysis: Dict,
        pdf_path: Path,
        timestamp: datetime
    ) -> str:
        """Build formatted markdown content for the note."""

        # Extract data from analysis
        tags = analysis.get('tags', [])
        summary = analysis.get('summary', '')
        tasks = analysis.get('tasks', '')
        themes = analysis.get('themes', '')
        questions = analysis.get('questions', '')
        insights = analysis.get('insights', '')
        metadata_section = analysis.get('metadata', '')
        original_text = analysis.get('original_text', '')

        # Build frontmatter
        tag_str = ' '.join([f'#{tag}' for tag in tags])

        # Get relative path to PDF from Scans directory
        pdf_relative = os.path.relpath(pdf_path, self.scans_dir)

        content = f"""---
created: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}
source: rocketbook
type: handwritten-note
tags: {tag_str}
---

# Rocketbook Note - {timestamp.strftime("%B %d, %Y")}

## Summary

{summary}

## PDF Scan

![[{pdf_relative}]]

---

## Tasks & Action Items

{tasks if tasks else "*No tasks identified*"}

---

## Key Themes & Topics

{themes if themes else "*No major themes identified*"}

---

## Questions & Open Items

{questions if questions else "*No open questions*"}

---

## Insights & Observations

{insights if insights else "*No additional insights*"}

---

## Metadata

{metadata_section}

---

## Original OCR Text

```
{original_text}
```

---

## AI Analysis

> This note was automatically processed and analyzed using Claude AI.
> Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Tags:** {tag_str}

---

## Related Notes

<!-- Links to related notes will appear here as they're created -->

"""

        return content

    def write_weekly_summary(self, week_start: datetime, summary_text: str) -> str:
        """
        Write a weekly insights summary.

        Args:
            week_start: Start date of the week
            summary_text: Summary content from Claude

        Returns:
            Path to created summary file
        """
        # Format: 2025-11-week-45.md
        iso_week = week_start.isocalendar()[1]
        summary_name = f"{week_start.year}-{week_start.month:02d}-week-{iso_week:02d}"
        summary_path = self.insights_dir / f"{summary_name}.md"

        content = f"""---
created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
type: weekly-summary
week-start: {week_start.strftime("%Y-%m-%d")}
tags: #weekly-summary #insights
---

# Weekly Summary - Week {iso_week}, {week_start.year}

Week of {week_start.strftime("%B %d, %Y")}

---

{summary_text}

---

## Notes This Week

<!-- Links to individual notes from this week -->

---

*Generated automatically from Rocketbook scans*
"""

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Created weekly summary: {summary_path}")
        return str(summary_path)

    def update_task_tracker(self, all_tasks: List[Dict]):
        """
        Update a master task tracker file with all tasks.

        Args:
            all_tasks: List of task dictionaries from all notes
        """
        tracker_path = self.rocketbook_dir / "Task-Tracker.md"

        # Group tasks by status
        open_tasks = []
        completed_tasks = []
        long_running = []

        for task in all_tasks:
            if task.get('status') == 'open':
                open_tasks.append(task)
            elif task.get('status') == 'completed':
                completed_tasks.append(task)
            if task.get('long_running', False):
                long_running.append(task)

        content = f"""---
updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
type: task-tracker
tags: #tasks #tracking
---

# Rocketbook Task Tracker

Auto-updated from handwritten notes.

## Open Tasks ({len(open_tasks)})

"""

        for task in open_tasks:
            content += f"- [ ] {task.get('text', '')} *({task.get('source', '')})*\n"

        content += f"\n## Long-Running Tasks ({len(long_running)})\n\n"

        for task in long_running:
            content += f"- ⏳ {task.get('text', '')} *({task.get('first_seen', '')} - {task.get('last_seen', '')})*\n"

        content += f"\n## Recently Completed ({len(completed_tasks[:10])})\n\n"

        for task in completed_tasks[:10]:  # Show last 10 completed
            content += f"- [x] {task.get('text', '')} *({task.get('source', '')})*\n"

        content += "\n---\n\n*Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*\n"

        with open(tracker_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Updated task tracker: {tracker_path}")
