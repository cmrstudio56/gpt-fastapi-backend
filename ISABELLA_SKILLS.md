# Isabella Skills Registry

## Overview

Isabella coordinates 3 integrated skills to help with writing, learning, and file organization.

---

## Skill 1: Google Drive Manager ✅ ACTIVE

**Status:** Production Ready (v4.0.0)  
**Repository:** `https://github.com/cmrstudio56/gpt-fastapi-backend`  
**Endpoint:** `https://web-production-99e37.up.railway.app`  
**OpenAPI Schema:** `openapi.json` or `openapi.yaml`

### Capabilities
| Capability | Endpoint | Method | Purpose |
|-----------|----------|--------|---------|
| Browse Root | `/list-all` | GET | See all top-level folders |
| Browse Folder | `/list?path=X` | GET | List files in specific folder |
| Detailed View | `/list-detailed?path=X` | GET | Files with sizes and dates |
| Tree View | `/list-recursive?path=X` | GET | Complete nested structure |
| Search | `/search?query=X` | GET | Find files across drive |
| Read File | `/read?title=X` | GET | Get file content |
| Write File | `/write` | POST | Create new file |
| Append | `/append` | POST | Add to existing file |
| Summarize | `/summarize` | POST | AI-powered summary |
| AI Models | `/models` | GET | Available summarization models |
| Diagnose | `/diagnose` | GET | Connection status check |
| Health | `/` | GET | System status |

### Dependencies
- Google Drive OAuth Token
- OpenRouter API Key (for AI features)
- Network connectivity

### Response Format
```json
{
  "status": "success|error",
  "message": "...",
  "data": {...}
}
```

### Example Workflows

**Workflow 1: Find and Read**
```
GET /search?query=novel
GET /read?title=novel_outline
```

**Workflow 2: Organize and Summarize**
```
GET /list-recursive?path=Books
POST /summarize {title: "chapter1"}
POST /write {title: "summary", content: "..."}
```

---

## Skill 2: Story Writer 📝 PLANNED

**Status:** Design Phase  
**Version:** 1.0.0 (Planned)  
**Technology:** LLM-based via Custom GPT or OpenRouter

### Planned Capabilities
- Character development and profiling
- Scene writing and generation
- Chapter outlining
- Dialogue writing
- Plot brainstorming
- Writing style refinement
- Story feedback and critique
- Genre-specific templates

### Integration Points
- **With Google Drive Manager:** Save drafts and research
- **With Tutor:** Research topics for story context
- **Data Storage:** Google Drive

### Skill Inputs
- Story premise/concept
- Character descriptions
- Plot outline
- Writing preferences
- Target audience
- Genre conventions

### Skill Outputs
- Written scenes/chapters
- Character profiles
- Story outlines
- Writing suggestions
- Feedback on drafts

### Example Request
```
User: "Write a dramatic scene where Sarah discovers a secret"
Story Writer:
  - Considers character context
  - Generates emotional scene
  - Returns with dialogue and narrative
  - Saves to Google Drive
```

---

## Skill 3: Tutor 🎓 PLANNED

**Status:** Design Phase  
**Version:** 1.0.0 (Planned)  
**Technology:** LLM-based education module

### Planned Capabilities
- Concept explanation (any subject)
- Q&A and questioning
- Study material generation
- Assessment and quizzes
- Learning paths creation
- Adapted learning styles
- Research assistance
- Knowledge checking

### Integration Points
- **With Story Writer:** Research for story accuracy
- **With Google Drive Manager:** Store learning materials
- **Data Storage:** Google Drive

### Subject Coverage
- Science (Physics, Chemistry, Biology, etc.)
- History and Social Studies
- Mathematics
- Languages
- Technology and Programming
- Arts and Literature
- Business and Economics
- And more

### Example Request
```
User: "Teach me about photosynthesis"
Tutor:
  - Explains concept clearly
  - Provides visual descriptions
  - Offers examples
  - Creates study notes
  - Saves to Google Drive
```

---

## Skill Interaction Matrix

| Skill 1 | Skill 2 | Skill 3 | Use Case |
|---------|---------|---------|----------|
| ✅ | ✅ | ✅ | Write historically accurate novel |
| ✅ | ✅ | ❌ | Draft and organize writing project |
| ✅ | ❌ | ✅ | Learn and take study notes |
| ❌ | ✅ | ✅ | Learn writing craft |
| ✅ | ❌ | ❌ | Manage documents and files |
| ❌ | ✅ | ❌ | Pure creative writing |
| ❌ | ❌ | ✅ | Pure learning/tutoring |

---

## Configuration

### Required Environment Variables
```
GOOGLE_OAUTH_TOKEN_JSON=<your-google-token>
OPENROUTER_API_KEY=<your-openrouter-key>
ISABELLA_MODE=production  # or development
```

### Optional Settings
```
DEFAULT_MODEL=claude-3-5-sonnet
MAX_RECURSION_DEPTH=10
CACHE_RESPONSES=true
```

---

## API Status Check

To verify all skills are connected:

```bash
# Skill 1 Status
curl https://web-production-99e37.up.railway.app/diagnose

# Response shows:
# - Google Drive: ✓ or ✗
# - OpenRouter: ✓ or ✗
# - Storage space
# - Recommendations
```

---

## Future Skills (Roadmap)

1. **Research Assistant** - Deep research and synthesis
2. **Code Assistant** - Programming help and debugging
3. **Translator** - Multi-language support
4. **Editor** - Professional editing and proofreading
5. **Analyzer** - Data analysis and insights
6. **Designer** - Visual and UX assistance

---

## Skill Development Guidelines

### For Adding New Skills
1. Define clear capabilities
2. Document API endpoints
3. Create integration tests
4. Test with other skills
5. Add to this registry
6. Update system instructions

### Naming Convention
- Skill names: `[Noun] [Action]` (e.g., "Story Writer", "Code Assistant")
- Endpoint prefix: `/skill-{name-lowercase}`
- Version: Semantic versioning

---

## Troubleshooting

### Skill 1: Google Drive Manager
- **Issue:** "Google Drive not initialized"
  - **Solution:** Set `GOOGLE_OAUTH_TOKEN_JSON` env var
  - **Check:** Use `/diagnose` endpoint

- **Issue:** "Search returns empty"
  - **Solution:** File might be in subfolder, use `/list-recursive`
  - **Check:** Verify with `/list-all`

### Skills 2 & 3
- **Coming Soon:** Will add troubleshooting as they're deployed

---

## Version History

**v1.0.0** (February 2026)
- 1 Active Skill: Google Drive Manager (4.0.0)
- 2 Planned Skills: Story Writer, Tutor
- Architecture defined
- System instructions created

