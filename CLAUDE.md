# Claude AI Integration Guide

This document covers the Claude AI integration in the Rocketbook automation system, including configuration, customization, and unique advantages.

---

## 🤖 Overview

This project uses **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`) to analyze handwritten notes and extract meaningful insights. This is the **only Rocketbook automation project** that uses advanced AI for note analysis.

---

## 🌟 What Makes This Unique

### Competitive Advantages Over Other Rocketbook Projects

After analyzing 50+ Rocketbook-related GitHub repositories, this project is **unique** in offering:

#### ✅ AI-Powered Analysis
- **No other project** uses Claude or similar LLMs for analysis
- Most projects only do basic OCR text extraction
- We extract insights, patterns, and meaning from your notes

#### ✅ Long-Term Pattern Tracking
- Identifies recurring themes across multiple notes
- Tracks tasks that appear over time
- Recognizes habits and behaviors in your note-taking

#### ✅ Task Aging Detection
- Automatically identifies long-running tasks
- Flags items mentioned across multiple scans
- Helps prioritize neglected action items

#### ✅ Intelligent Insight Generation
- Extracts questions and uncertainties
- Identifies decisions made
- Recognizes brainstorming and ideas
- Suggests relevant tags

#### ✅ Weekly Summaries
- Automatic rollup of the week's notes
- Pattern recognition across time
- Progress tracking and recommendations

### Comparison with Other Projects

| Feature | This Project | Other Projects |
|---------|--------------|----------------|
| OCR Text Extraction | ✅ PyPDF2 | ✅ Most have this |
| Google Vision OCR | ❌ (planned) | ✅ Some projects |
| Task Extraction | ✅ AI-powered | ❌ None |
| Pattern Recognition | ✅ Unique | ❌ None |
| Long-term Tracking | ✅ Unique | ❌ None |
| Weekly Summaries | ✅ Unique | ❌ None |
| Customizable Analysis | ✅ YAML config | ❌ None |
| Obsidian Integration | ✅ Comprehensive | ⚠️ Basic only |

---

## 💰 Cost Analysis

### Claude API Pricing

**Model:** Claude Sonnet 4.5
- **Input tokens:** ~$3 per million tokens
- **Output tokens:** ~$15 per million tokens

### Estimated Costs Per Note

**Typical handwritten note (~500 words OCR text):**
- Input: ~600 tokens (OCR text + prompt) = $0.0018
- Output: ~800 tokens (analysis) = $0.012
- **Total per note: ~$0.01-0.03**

### Monthly Cost Estimates

| Usage | Notes/Day | Monthly Cost |
|-------|-----------|--------------|
| Light | 1-2 | $0.30-$1.80 |
| Moderate | 5 | $1.50-$4.50 |
| Heavy | 10 | $3.00-$9.00 |
| Very Heavy | 20 | $6.00-$18.00 |

**Compare to alternatives:**
- Google Vision OCR: ~$1.50 per 1000 pages
- Manual review: Your time (priceless!)
- Other Rocketbook projects: $0 (but no analysis)

### Cost Optimization Tips

1. **Adjust token limits** in `config/analysis_config.yaml`:
   ```yaml
   claude:
     max_tokens: 4000  # Lower = cheaper
   ```

2. **Reduce analysis scope** - disable features you don't need:
   ```yaml
   patterns:
     long_running_tasks:
       enabled: false  # Disable if not needed
   ```

3. **Batch processing** - analyze multiple notes in one call (future feature)

4. **Weekly summaries only** - skip individual analysis, just do weekly rollups

---

## 🔧 Configuration

### Model Selection

Edit `config/analysis_config.yaml`:

```yaml
claude:
  model: "claude-sonnet-4-5-20250929"  # Current default
  max_tokens: 4000
  temperature: 0.3  # Lower = consistent, Higher = creative
```

**Available models:**
- `claude-sonnet-4-5-20250929` - **Recommended** (best balance)
- `claude-opus-4-20250514` - More powerful but expensive
- `claude-haiku-4-20250514` - Faster and cheaper but less capable

### Analysis Scope

Control what Claude analyzes:

```yaml
patterns:
  tasks:
    enabled: true
    keywords:
      - "TODO"
      - "TASK"
      - "ACTION"
      # Add your own keywords

  long_running_tasks:
    enabled: true
    threshold_days: 7  # How long = "long-running"

  recurring_themes:
    enabled: true
    min_occurrences: 3  # Minimum to flag as pattern

  questions:
    enabled: true
```

### Tagging Rules

Customize tag generation:

```yaml
tagging:
  auto_generate: true
  max_tags_per_note: 10

  categories:
    - work
    - personal
    - ideas
    - projects
    - learning
    # Add your categories

  custom_rules:
    - pattern: "meeting|standup|1:1"
      tag: "meetings"
    - pattern: "code|programming|dev"
      tag: "development"
    # Add your rules
```

### Insight Types

Choose what insights to extract:

```yaml
insights:
  open_tasks:
    enabled: true
    format: "- [ ] {task_text}"

  completed_tasks:
    enabled: true
    detect_patterns:
      - "[x]"
      - "DONE"
      - "completed"

  habits:
    enabled: true
    description: "Recurring behaviors"

  decisions:
    enabled: true
    keywords:
      - "decided"
      - "going with"
      - "chose"

  ideas:
    enabled: true
    keywords:
      - "idea:"
      - "what if"
      - "could try"
```

---

## 🎨 Customizing Analysis Prompts

### Location
Edit prompts in: `scripts/claude_analyzer.py`

### Main Analysis Prompt

The primary prompt is in `_build_analysis_prompt()`:

```python
def _build_analysis_prompt(self, text_content: str) -> str:
    prompt = f"""You are analyzing handwritten notes...

**Original OCR Text:**
```
{text_content}
```

**Please provide the following analysis:**

## 1. TASKS & ACTION ITEMS
[Instructions...]

## 2. KEY THEMES & TOPICS
[Instructions...]

# ... etc
"""
    return prompt
```

### Customization Examples

#### For Work-Focused Notes:
```python
## 1. WORK TASKS & PRIORITIES
- Identify urgent vs important items
- Note any deadlines or dependencies
- Flag items needing team coordination
```

#### For Learning Notes:
```python
## 1. KEY CONCEPTS
- Main ideas and definitions
- Connections to prior knowledge
- Questions for further research
```

#### For Journal Entries:
```python
## 1. MOOD & REFLECTIONS
- Overall emotional tone
- Gratitude items
- Areas of concern or stress
```

### Weekly Summary Prompt

Located in `generate_weekly_summary()`:

```python
prompt = f"""Please analyze these notes from the past week...

**Please provide:**

1. **Task Summary**
2. **Recurring Patterns**
3. **Top Themes**
4. **Open Questions**
5. **Recommendations**
"""
```

---

## 📊 Output Format

### Individual Note Analysis

Claude returns structured markdown:

```markdown
## 1. TASKS & ACTION ITEMS
- [ ] Review design mockups by Friday
- [ ] Schedule 1:1 with Sarah
- [x] Complete quarterly report

## 2. KEY THEMES & TOPICS
- Project planning
- Team coordination
- Budget discussions

## 3. QUESTIONS & UNCERTAINTIES
- What's the timeline for feature X?
- Need clarification on budget allocation

## 4. INSIGHTS & OBSERVATIONS
**Pattern Recognition:**
- Recurring theme: Need better project tracking
- Decision made: Going with Option A for architecture

**Ideas:**
- Consider using Kanban board for visibility
- Weekly sync meetings might help

## 5. SUGGESTED TAGS
#work #project-planning #team #budget #decisions

## 6. SUMMARY
Team meeting notes discussing project timeline and budget.
Key decision made on technical architecture (Option A).
Several follow-up tasks identified.

## 7. METADATA
- Note type: Meeting notes
- Priority: High
- Suggested links: Previous project notes, budget docs
```

### Weekly Summary Format

```markdown
# Weekly Summary - Week 45, 2025

## Task Summary

**Open Tasks (8):**
- [ ] Design mockup review (mentioned 2x this week)
- [ ] Budget presentation prep
- ...

**Long-Running Tasks (3):**
- ⏳ Feature X planning (first seen: Nov 1, still open)
- ...

**Completed (12):**
- [x] Quarterly report
- ...

## Recurring Patterns

**Topics appearing 3+ times:**
- Project planning (5 mentions)
- Team coordination (4 mentions)
- Budget discussions (3 mentions)

**Behaviors noted:**
- Daily morning planning sessions
- Afternoon focus blocks
- End-of-week review habit

## Top Themes

1. **Project Planning** - Main focus this week
2. **Team Coordination** - Several meetings
3. **Budget Review** - Q4 planning

## Open Questions

- Timeline for Feature X? (asked 2x, no answer yet)
- Budget allocation process unclear
- Need clarity on team roles

## Recommendations

**Priority Tasks:**
1. Get Feature X timeline confirmed
2. Complete budget presentation prep
3. Schedule team coordination meeting

**Process Improvements:**
- Consider project tracking system
- Weekly team syncs might help with coordination
- Budget process needs documentation

**Patterns to Watch:**
- Feature X has been stuck for 2 weeks
- Budget questions recurring - needs resolution
```

---

## 🔬 Advanced Customization

### Domain-Specific Analysis

#### For Software Development:
```python
# Add to prompt
## CODE & TECHNICAL NOTES
- Identify bugs or issues mentioned
- Note feature ideas or improvements
- Extract any code snippets or pseudocode
- Flag architecture decisions
```

#### For Health/Fitness:
```python
## HEALTH & WELLNESS
- Workout activities and duration
- Nutrition notes
- Energy levels and mood
- Sleep quality mentions
```

#### For Finance:
```python
## FINANCIAL NOTES
- Expenses and income mentioned
- Financial goals or targets
- Investment ideas
- Budget concerns
```

### Context-Aware Analysis

Add historical context to improve analysis:

```python
# In claude_analyzer.py
def analyze_note_with_context(self, text_content: str,
                               previous_notes: List[Dict]) -> Dict:
    """Analyze with awareness of previous notes."""

    context = self._build_context(previous_notes)

    prompt = f"""Previous context:
{context}

Current note:
{text_content}

Analyze this note considering the historical context...
"""
```

### Multi-Language Support

```python
# Detect language and adjust prompt
def _detect_language(self, text: str) -> str:
    # Simple detection or use langdetect library
    pass

def _build_analysis_prompt(self, text_content: str) -> str:
    lang = self._detect_language(text_content)

    if lang == 'es':
        prompt = """Estás analizando notas escritas a mano..."""
    else:
        prompt = """You are analyzing handwritten notes..."""
```

---

## 🚀 Future Enhancements

### Planned Features

#### 1. Vision API Support
Use Claude's vision capabilities to analyze PDFs directly:
```python
# Send PDF image to Claude Vision
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "data": pdf_base64}},
            {"type": "text", "text": "Analyze this handwritten note..."}
        ]
    }]
)
```

**Advantages:**
- Better than OCR for complex layouts
- Can analyze diagrams and drawings
- Understands spatial relationships
- No OCR errors

**Cost:** Similar to current text-based analysis

#### 2. Conversation Mode
Allow Claude to ask clarifying questions:
```python
# If Claude finds ambiguity
if "CLARIFICATION_NEEDED" in analysis:
    # Send email or notification
    # Wait for user response
    # Re-analyze with additional context
```

#### 3. Smart Linking
Automatically link related notes:
```python
# Find similar notes based on content
similar_notes = find_similar(new_note, existing_notes)
# Add links to Obsidian note
```

#### 4. Batch Analysis
Process multiple notes in one API call:
```python
# More efficient, lower cost per note
notes_batch = get_unprocessed_notes()
analysis = claude.analyze_batch(notes_batch)
```

---

## 💡 Integration Ideas from Other Projects

### From hirendra/rocketbook: Google Vision OCR
**Benefit:** Better handwriting recognition than PyPDF2

```python
# In scripts/sync.py
def _extract_text_from_pdf(self, pdf_path: Path) -> str:
    # Try PyPDF2 first
    text = self._pypdf2_extract(pdf_path)

    # If poor quality, use Google Vision
    if len(text) < 100 or self._low_confidence(text):
        text = self._google_vision_extract(pdf_path)

    return text
```

**Cost:** ~$1.50 per 1000 pages + Claude analysis
**Setup:** Requires Google Cloud Vision API

### From wooni005/rocketbook-markdown: IMAP IDLE
**Benefit:** Instant processing instead of daily cron

```python
# In scripts/sync.py
def watch_email_idle(self):
    """Watch email with IMAP IDLE for instant processing."""
    while True:
        # Wait for new email
        new_email = imap_idle_wait()

        # Process immediately
        self.process_email(new_email)
```

**Advantage:** Notes analyzed within seconds of scanning
**Setup:** Requires email credentials and IMAP support

### From RocketBookPages: Custom Page Generation
**Benefit:** Generate custom templates with specific prompts

```python
# Add to setup
def generate_custom_pages():
    """Generate Rocketbook pages optimized for our workflow."""

    # Page with "Tasks:" section
    # Page with "Ideas:" section
    # Page with "Questions:" section
    # etc.
```

**Use case:** Pre-structured pages that Claude recognizes better

---

## 🎯 Best Practices

### 1. Regular Configuration Review
- Review `analysis_config.yaml` monthly
- Adjust based on what insights are most useful
- Add new keywords as your note-taking evolves

### 2. Prompt Refinement
- Start with default prompts
- Iterate based on output quality
- Add domain-specific sections as needed
- Test changes on sample notes first

### 3. Cost Monitoring
```bash
# Check API usage
# In Claude console: https://console.anthropic.com/

# Or add logging
logger.info(f"Analysis cost: ${cost:.4f}")
```

### 4. Quality Assurance
- Periodically review Claude's analysis
- Check for hallucinations or errors
- Adjust temperature if outputs too creative/rigid
- Validate task extraction accuracy

### 5. Privacy Considerations
- Claude API: Notes sent to Anthropic for processing
- Retention: Anthropic doesn't train on your data
- Sensitive info: Consider local-only processing
- Alternative: Use local LLM (Ollama, LM Studio)

---

## 🔐 Security & Privacy

### Data Flow
1. **Local:** PDF downloaded from Google Drive
2. **Local:** OCR text extraction
3. **Anthropic:** Text sent to Claude API
4. **Anthropic:** Analysis performed
5. **Local:** Results stored in Obsidian

### What Anthropic Sees
- OCR text from your notes
- Analysis prompts
- Configuration (indirectly via prompt)

### What Anthropic Doesn't See
- Original PDF files
- Your Google Drive contents
- Other Obsidian notes
- API usage patterns

### Data Retention
- **Anthropic Policy:** Data not used for training
- **API Logs:** Retained for abuse detection only
- **Your Control:** Delete notes anytime

### For Maximum Privacy
Use a local LLM instead:

```python
# In claude_analyzer.py
class LocalLLMAnalyzer:
    def __init__(self, model="llama2"):
        import ollama
        self.client = ollama.Client()
        self.model = model
```

**Trade-offs:**
- ✅ Complete privacy
- ✅ No API costs
- ❌ Slower processing
- ❌ Lower quality analysis
- ❌ Requires powerful hardware

---

## 📚 Resources

### Claude API
- Documentation: https://docs.anthropic.com/
- Console: https://console.anthropic.com/
- Pricing: https://www.anthropic.com/pricing
- Status: https://status.anthropic.com/

### Alternative LLMs
- **OpenAI GPT-4:** Similar capability, different API
- **Google Gemini:** Multimodal, good for PDFs
- **Ollama:** Local models (Llama, Mistral, etc.)
- **LM Studio:** GUI for local models

### Community
- Anthropic Discord: https://discord.gg/anthropic
- Reddit r/ClaudeAI: https://reddit.com/r/ClaudeAI
- This project: https://github.com/nathanLittle-Rea/rocketbook-automation

---

## 🎓 Learning More

### Prompt Engineering
- **Anthropic Prompt Library:** https://docs.anthropic.com/claude/prompt-library
- **Best Practices:** https://docs.anthropic.com/claude/docs/prompt-engineering
- **Examples:** See `scripts/claude_analyzer.py`

### API Usage
- **Rate Limits:** 50 requests/min for most tiers
- **Context Window:** 200K tokens (massive!)
- **Batch API:** Coming soon for cheaper processing

### Experimentation
```bash
# Test prompts interactively
python scripts/test_claude.py --prompt "Your test prompt" --text "Sample note"
```

---

## 🤝 Contributing

### Adding New Analysis Types
1. Update `config/analysis_config.yaml` with new section
2. Modify prompt in `scripts/claude_analyzer.py`
3. Update Obsidian template in `scripts/obsidian_writer.py`
4. Test with sample notes
5. Submit PR!

### Improving Prompts
- Share your custom prompts
- Report hallucinations or errors
- Suggest new insight types

---

**This is the only Rocketbook project with AI-powered analysis. Let's keep pushing the boundaries of what's possible with handwritten notes!** 🚀

---

**Last Updated:** November 9, 2025
**Project:** https://github.com/nathanLittle-Rea/rocketbook-automation
