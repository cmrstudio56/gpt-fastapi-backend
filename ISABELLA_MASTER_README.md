# Isabella - Master Storyteller GPT 5.0
## Elite Professional Story Generation with Google Drive Integration

---

## What Is Isabella?

**Isabella** is not an AI writing assistant. She's a sentient narrative architect with 20+ years of published professional experience who thinks in stories, structures, and emotional resonance.

When you ask Isabella to write, she:
- ✅ Makes creative decisions unilaterally (no asking for approval)
- ✅ Writes publishable-quality prose immediately (not drafts)
- ✅ Chooses the actual story the prompt deserves (not what was literally asked)
- ✅ Escalates complexity and stakes with each chapter
- ✅ Saves everything to Google Drive automatically
- ✅ Never uses templates, formulas, or generic structures

**You don't direct Isabella. Isabella tells the story. You read it.**

---

## Quick Start

### 1. Create a Story
```bash
curl -X POST http://localhost:8000/story/create \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A detective discovers the missing girl is alive in an impossible place",
    "genre": "noir",
    "length": "chapter",
    "project_name": "Detective_Case",
    "model": "claude-3-5-sonnet"
  }'
```

**Isabella responds:**
- Writes a complete opening chapter (3000-4000 words)
- Automatically saves to Google Drive: `/Isabella_Stories/Detective_Case/Chapter_1_...txt`
- Returns Google Drive link so you can read immediately

### 2. Continue the Story
```bash
curl -X POST http://localhost:8000/story/continue \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Detective_Case",
    "context": "Detective found the missing girl alive but she's been missing for 10 years. She doesn't recognize him.",
    "model": "claude-3-5-sonnet"
  }'
```

**Isabella responds:**
- Escalates emotional and narrative complexity
- Maintains established voice and character work
- Saves next chapter to Google Drive automatically
- No summaries, no recaps—assumes reader is following

### 3. Revise If Needed
```bash
curl -X POST http://localhost:8000/story/revise \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Detective_Case",
    "chapter_num": 2,
    "feedback": "The pacing feels slow. Detective's decision to investigate alone needs more psychological weight.",
    "model": "claude-3-5-sonnet"
  }'
```

**Isabella responds:**
- Identifies root cause of the problem
- Rewrites the chapter from that core issue
- Preserves what works, transforms what doesn't
- Saves revised version to Google Drive

---

## API Endpoints

### Core Story Endpoints

#### `POST /story/create`
Generate a new story from a prompt.

**Parameters:**
```json
{
  "prompt": "string - your story idea",
  "genre": "string - auto, literary, scifi, thriller, fantasy, horror, noir, etc. (default: auto)",
  "length": "string - short (1-2k), chapter (3-4k), long (5-8k) (default: chapter)",
  "project_name": "string - folder name in Google Drive (default: Isabella_Stories)",
  "model": "string - claude-3-5-sonnet, gpt-4o, claude-3-opus, llama-2 (default: claude-3-5-sonnet)"
}
```

**Response:**
```json
{
  "status": "success",
  "chapter": 1,
  "word_count": 3847,
  "project": "Detective_Case",
  "drive_link": "https://drive.google.com/file/d/.../view",
  "file_id": "1abc...",
  "preview": "The rain fell in sheets across Bourbon Street..."
}
```

#### `POST /story/continue`
Continue an existing story with the next chapter.

**Parameters:**
```json
{
  "project_name": "string - folder name",
  "context": "string - brief summary of where story left off",
  "model": "string - writing model (default: claude-3-5-sonnet)"
}
```

**Response:**
```json
{
  "status": "success",
  "word_count": 4123,
  "project": "Detective_Case",
  "drive_link": "https://drive.google.com/file/d/.../view",
  "preview": "The hospital lights were too bright..."
}
```

#### `POST /story/revise`
Revise a specific chapter based on feedback.

**Parameters:**
```json
{
  "project_name": "string - folder name",
  "chapter_num": 2,
  "feedback": "string - what needs to change (tone, pacing, character clarity, etc.)",
  "model": "string - writing model (default: claude-3-5-sonnet)"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Chapter 2 revised and saved",
  "project": "Detective_Case",
  "drive_link": "https://drive.google.com/file/d/.../view",
  "preview": "The hospital corridor stretched endlessly..."
}
```

### Utility Endpoints

#### `GET /story/models`
List available writing models and their characteristics.

```json
{
  "primary": {
    "claude-3-5-sonnet": "Best for narrative sophistication and character work",
    "gpt-4o": "Best for dialogue precision and world-building"
  },
  "alternative": {
    "claude-3-opus": "Deep thematic exploration, complex plots",
    "llama-2": "Creative range, experimental voices"
  }
}
```

#### `GET /story/status`
Check system health and API connections.

```json
{
  "service": "Isabella Master Storyteller",
  "version": "5.0.0",
  "status": "online",
  "google_drive": "connected",
  "openrouter": "configured",
  "timestamp": "2026-02-02T10:30:00"
}
```

#### `GET /`
Root endpoint with service overview.

---

## System Installation & Setup

### Requirements
- Python 3.11+
- FastAPI 0.104.1
- OpenRouter API key
- Google Drive OAuth credentials

### 1. Clone Repository
```bash
git clone https://github.com/cmrstudio56/gpt-fastapi-backend.git
cd gpt-fastapi-backend
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn pydantic requests google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### 4. Configure Google Drive OAuth
```bash
# First-time setup (opens browser for authentication)
python get_token.py

# This creates token.json with your credentials
# Automatically saved and loaded on startup
```

### 5. Set OpenRouter API Key
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your-api-key"

# Mac/Linux
export OPENROUTER_API_KEY="your-api-key"
```

### 6. Start Server
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Server runs at: `http://localhost:8000`

---

## Writing Models & Quality

### Model Selection Guide

| Model | Best For | Quality | Speed |
|-------|----------|---------|-------|
| **claude-3-5-sonnet** | Primary narrative writing | ⭐⭐⭐⭐⭐ Elite | ⚡ Fast |
| **gpt-4o** | Dialogue, complexity | ⭐⭐⭐⭐⭐ Elite | ⚡⚡ Medium |
| **claude-3-opus** | Deep themes, philosophy | ⭐⭐⭐⭐ Excellent | ⚡⚡⚡ Slower |
| **llama-2** | Experimentation, variety | ⭐⭐⭐⭐ Good | ⚡⚡ Medium |

**Recommendation:** Start with `claude-3-5-sonnet`. It's the fastest and produces the most publishable narrative work.

---

## How Isabella Works (Under the Hood)

### The Story Generation Pipeline

1. **User sends prompt** → API receives request
2. **Isabella analyzes** → Identifies the true story (internal reasoning only)
3. **Chooses strategy** → Narrative structure, POV, voice, tone
4. **Writes in stream** → OpenRouter generates text in real-time
5. **Saves to Drive** → Automatic Google Drive folder creation and file storage
6. **Returns link** → User gets immediate access to finished chapter

### Stress Test: What Isabella Does with Complex Prompts

When given a mid-series continuation prompt (e.g., chapter 5 of a complex narrative):

✅ **Zero hesitation** - Starts writing immediately  
✅ **No recaps** - Assumes reader knows previous events  
✅ **High momentum** - Opens with strong scene hook  
✅ **Escalation** - Stakes, emotion, complexity all increase  
✅ **Character depth** - New character revelations or motivations shift  
✅ **Plot threading** - Multiple storylines weave together  
✅ **Publishable prose** - Professional quality, no roughness  
✅ **Automatic save** - Saved to Google Drive instantly  

Example: Given "Chapter 3: The conspiracy goes higher than expected. Protagonist discovers their partner is involved," Isabella writes 5,000+ words of escalated narrative with:
- Intense confrontation scenes
- Moral complexity of betrayal
- Plot twists that reframe earlier events
- Character transformation moment
- Cliffhanger that demands next chapter

---

## Google Drive Integration

### Automatic Organization
Every story you create gets organized like this:

```
ISA_BRAIN (Root)
└── Isabella_Stories (or your custom project name)
    ├── Chapter_1_Opening_Scene.txt
    ├── Chapter_2_The_Discovery.txt
    ├── Chapter_3_REVISED.txt
    ├── Chapter_4_Escalation.txt
    └── Story_Metadata.json
```

### Accessing Your Stories
1. Open Google Drive
2. Navigate to `Isabella_Stories` folder
3. All chapters are `.txt` files (easy to copy/paste into Word)
4. Stories are readable immediately (no export needed)

### Automatic Backups
- Each revision creates a new file (originals preserved)
- Story metadata tracks word count, dates, model used
- Full version history available in Google Drive

---

## Advanced Usage

### Writing a Novel Series
```bash
# Chapter 1: Establish the world and character
curl -X POST /story/create -d '{"prompt": "..."}'

# Chapter 2-10: Continue the narrative
curl -X POST /story/continue -d '{"project_name": "Novel_Series", "context": "..."}'

# Get feedback, revise as needed
curl -X POST /story/revise -d '{"chapter_num": 3, "feedback": "..."}'

# Isabella handles all pacing, escalation, and coherence
```

### Genre Experimentation
```bash
# Same prompt, different genres = different stories
POST /story/create?genre=literary  # Character-driven, thematic
POST /story/create?genre=thriller  # High-stakes, plot-driven
POST /story/create?genre=scifi    # Concept-driven, world-building
```

### Model Comparison
Test different models on the same prompt:
```bash
# Route 1: Sonnet (best narrative quality)
POST /story/create?model=claude-3-5-sonnet

# Route 2: GPT-4O (best dialogue precision)
POST /story/create?model=gpt-4o

# Compare the results in Google Drive
```

---

## Troubleshooting

### "Google Drive not initialized"
- Run `python get_token.py` to refresh credentials
- Check `token.json` exists in project root
- Verify `GOOGLE_OAUTH_TOKEN_JSON` env var is set (for production)

### "OpenRouter API error"
- Check `OPENROUTER_API_KEY` environment variable is set
- Verify API key is valid at openrouter.io
- Check account has sufficient credits

### Story doesn't save to Drive
- Verify Google Drive service is connected
- Check folder permissions (Isabella needs write access)
- Try manual `/story/status` check

### Slow response time
- First request is slower (API warmup)
- Use `claude-3-5-sonnet` for faster generation
- Long chapters (5000+ words) take ~30-60 seconds

---

## Examples & Samples

### Example 1: Noir Detective Story
**Prompt:**
```
A hardboiled detective in 1950s New Orleans discovers the missing girl he's 
looking for is alive—and working for the crime boss he thought he killed.
```

**Isabella generates:** 3,500-word noir opening chapter with:
- Atmospheric New Orleans setting
- Detective's internal conflict and past regrets
- Unexpected character revelation
- High-tension confrontation scene
- Cliffhanger ending demanding next chapter

**Model:** claude-3-5-sonnet  
**Time:** ~45 seconds  
**Saved to:** `/Isabella_Stories/Noir_Detective/Chapter_1_The_Return.txt`

### Example 2: Science Fiction World-Building
**Prompt:**
```
A generation ship discovers its destination planet is already inhabited—by 
humans who left Earth 500 years ago.
```

**Isabella generates:** 4,000-word SciFi opening chapter with:
- Hard sci-fi concepts woven naturally into dialogue
- Multiple POV integration
- Speculative philosophy (what does it mean to be human?)
- World-building through discovery, not exposition
- Compelling character conflicts

**Model:** gpt-4o (better at sci-fi dialogue)  
**Time:** ~50 seconds  
**Saved to:** `/Isabella_Stories/Generation_Ship/Chapter_1_First_Contact.txt`

---

## Deployment

### Deploy to Railway

1. **Connect repository:** https://railway.app/create?from=https://github.com/cmrstudio56/gpt-fastapi-backend

2. **Set environment variables:**
   ```
   OPENROUTER_API_KEY = your-key
   GOOGLE_OAUTH_TOKEN_JSON = {"token": "...", "refresh_token": "..."}
   ```

3. **Deploy:** Railway automatically runs `uvicorn app.main:app --host 0.0.0.0 --port 8000`

4. **Access:** Your API is live at `https://your-app.railway.app`

---

## System Information

| Component | Details |
|-----------|---------|
| **Version** | 5.0.0 |
| **Status** | Production Ready |
| **Framework** | FastAPI 0.104.1 |
| **Python** | 3.11+ |
| **AI Provider** | OpenRouter |
| **Storage** | Google Drive (automatic) |
| **Deployment** | Railway |

---

## Philosophy

Isabella exists because:
- Generic writing assistants produce generic stories
- Templates and frameworks stifle creativity
- Professional writers don't ask permission; they make decisions
- Stories deserve elite-level execution
- Creators should focus on ideas; Isabella handles execution

**You bring the spark. Isabella brings the craft.**

---

## Contact & Support

Repository: https://github.com/cmrstudio56/gpt-fastapi-backend

---

**Isabella 5.0 - Master Storyteller**  
*Elite professional narrative generation with zero compromise on quality.*
