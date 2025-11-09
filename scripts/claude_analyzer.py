"""
Claude AI analyzer for Rocketbook notes.
Extracts insights, tasks, patterns, and generates structured output.
"""

import logging
from typing import Dict, List, Optional
import yaml
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeAnalyzer:
    """Analyzes notes using Claude AI."""

    def __init__(self, api_key: str, config_path: str):
        """
        Initialize Claude analyzer.

        Args:
            api_key: Anthropic API key
            config_path: Path to analysis_config.yaml
        """
        self.client = Anthropic(api_key=api_key)

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.model = self.config['claude']['model']
        self.max_tokens = self.config['claude']['max_tokens']
        self.temperature = self.config['claude']['temperature']

        logger.info("Claude analyzer initialized")

    def analyze_note(self, text_content: str, filename: str) -> Dict:
        """
        Analyze a single note and extract insights.

        Args:
            text_content: OCR text from Rocketbook scan
            filename: Original filename for reference

        Returns:
            Dictionary containing analysis results
        """
        logger.info(f"Analyzing note: {filename}")

        prompt = self._build_analysis_prompt(text_content)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            analysis_text = response.content[0].text
            logger.info("Analysis completed successfully")

            # Parse the response into structured format
            analysis = self._parse_analysis(analysis_text, text_content)
            return analysis

        except Exception as e:
            logger.error(f"Error during Claude analysis: {e}")
            return {
                "error": str(e),
                "raw_text": text_content
            }

    def _build_analysis_prompt(self, text_content: str) -> str:
        """Build the prompt for Claude based on configuration."""

        patterns_config = self.config.get('patterns', {})
        insights_config = self.config.get('insights', {})
        tagging_config = self.config.get('tagging', {})

        prompt = f"""You are analyzing handwritten notes that have been digitized using OCR from a Rocketbook notebook.
The OCR may contain errors or unclear text. Please analyze the following note and provide structured insights.

**Original OCR Text:**
```
{text_content}
```

**Please provide the following analysis:**

## 1. TASKS & ACTION ITEMS
- Identify all tasks, action items, or to-dos mentioned
- Mark if they appear complete [x] or incomplete [ ]
- Note any deadlines or time sensitivity
- Flag tasks that seem to be recurring across multiple notes (if context suggests this)

## 2. KEY THEMES & TOPICS
- Identify main topics discussed
- Note recurring themes or patterns
- Highlight important concepts or decisions

## 3. QUESTIONS & UNCERTAINTIES
- List any questions posed in the notes
- Identify areas where more information is needed
- Note unresolved issues

## 4. INSIGHTS & OBSERVATIONS
- Pattern recognition: Are there habits, recurring activities, or behaviors?
- Decisions made or needed
- Ideas or brainstorming points
- Important information to remember

## 5. SUGGESTED TAGS
Based on the content, suggest {tagging_config.get('max_tags_per_note', 10)} relevant tags from these categories:
{', '.join(tagging_config.get('categories', []))}

Also consider custom tags based on specific content.

## 6. SUMMARY
Provide a concise 2-3 sentence summary of the note's main content.

## 7. METADATA
- Estimated note type (meeting, brainstorm, task list, journal, learning, etc.)
- Priority level (high/medium/low) based on content urgency
- Suggested related topics or notes to link to

**Format your response as structured markdown that can be easily parsed.**
Use clear section headers and bullet points.
"""

        return prompt

    def _parse_analysis(self, analysis_text: str, original_text: str) -> Dict:
        """
        Parse Claude's analysis response into structured format.

        Args:
            analysis_text: Claude's response
            original_text: Original OCR text

        Returns:
            Structured analysis dictionary
        """
        # Extract sections from markdown response
        result = {
            "full_analysis": analysis_text,
            "original_text": original_text,
            "tasks": self._extract_section(analysis_text, "TASKS & ACTION ITEMS"),
            "themes": self._extract_section(analysis_text, "KEY THEMES & TOPICS"),
            "questions": self._extract_section(analysis_text, "QUESTIONS & UNCERTAINTIES"),
            "insights": self._extract_section(analysis_text, "INSIGHTS & OBSERVATIONS"),
            "tags": self._extract_tags(analysis_text),
            "summary": self._extract_section(analysis_text, "SUMMARY"),
            "metadata": self._extract_section(analysis_text, "METADATA"),
        }

        return result

    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from the analysis text."""
        lines = text.split('\n')
        section_lines = []
        in_section = False

        for line in lines:
            # Check if we're entering the section
            if section_name.upper() in line.upper() and line.strip().startswith('#'):
                in_section = True
                continue

            # Check if we're entering a new section
            if in_section and line.strip().startswith('#'):
                break

            # Collect lines in the section
            if in_section and line.strip():
                section_lines.append(line)

        return '\n'.join(section_lines).strip()

    def _extract_tags(self, text: str) -> List[str]:
        """Extract tags from the analysis."""
        tags_section = self._extract_section(text, "SUGGESTED TAGS")

        # Simple extraction - look for hashtags or words after bullets
        tags = []
        for line in tags_section.split('\n'):
            # Remove bullets and common punctuation
            cleaned = line.strip('- *#').strip()
            if cleaned and len(cleaned) < 30:  # Reasonable tag length
                # Split on commas if multiple tags per line
                for tag in cleaned.split(','):
                    tag = tag.strip().lower().replace(' ', '-')
                    if tag:
                        tags.append(tag)

        return tags[:self.config['tagging'].get('max_tags_per_note', 10)]

    def generate_weekly_summary(self, notes_data: List[Dict]) -> str:
        """
        Generate a weekly summary from multiple notes.

        Args:
            notes_data: List of analyzed note dictionaries

        Returns:
            Weekly summary markdown
        """
        if not self.config.get('weekly_insights', {}).get('enabled', False):
            return ""

        logger.info(f"Generating weekly summary from {len(notes_data)} notes")

        # Compile all analyses
        all_tasks = []
        all_themes = []
        all_questions = []

        for note in notes_data:
            if 'tasks' in note:
                all_tasks.append(note['tasks'])
            if 'themes' in note:
                all_themes.append(note['themes'])
            if 'questions' in note:
                all_questions.append(note['questions'])

        prompt = f"""Please analyze these notes from the past week and provide a comprehensive summary.

**Notes Summary:**
Total notes analyzed: {len(notes_data)}

**All Tasks Identified:**
{chr(10).join(all_tasks)}

**All Themes:**
{chr(10).join(all_themes)}

**All Questions:**
{chr(10).join(all_questions)}

**Please provide:**

1. **Task Summary**
   - Open tasks (uncompleted)
   - Completed tasks
   - Long-running tasks (appearing multiple times)
   - Blocked or unclear tasks

2. **Recurring Patterns**
   - Topics that appeared multiple times
   - Habits or behaviors noted
   - Decision patterns

3. **Top Themes**
   - Main focus areas this week
   - Important developments

4. **Open Questions**
   - Unresolved questions
   - Areas needing investigation

5. **Recommendations**
   - Suggested priorities for next week
   - Tasks that need attention
   - Patterns to be aware of
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Error generating weekly summary: {e}")
            return f"Error generating summary: {e}"
