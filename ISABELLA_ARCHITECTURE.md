# Isabella Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ISABELLA v1.0.0                        │
│            Intelligent Personal Assistant                │
│                                                          │
│  System Instructions → Personality, Values, Behavior    │
│  Skill Coordinator → Routes requests to right skill     │
│  Context Manager → Remembers conversation history       │
└─────────────────────────────────────────────────────────┘
              │                 │                  │
              ▼                 ▼                  ▼
    ┌──────────────────┐ ┌──────────────┐ ┌─────────────┐
    │  Skill 1: GDM    │ │ Skill 2: SW  │ │ Skill 3: T  │
    │ (ACTIVE v4.0.0)  │ │  (PLANNED)   │ │  (PLANNED)  │
    │                  │ │              │ │             │
    │ Browse & Manage  │ │ Write        │ │ Teach       │
    │ Google Drive     │ │ Stories      │ │ & Learn     │
    └──────────────────┘ └──────────────┘ └─────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌──────────────┐  ┌─────────────────┐
│ Google Drive │  │   OpenRouter    │
│  (Storage)   │  │ (AI Models)     │
└──────────────┘  └─────────────────┘
```

---

## Information Flow

### Single Skill Request
```
User Request
    ↓
Isabella (Route to correct skill)
    ↓
Skill (Execute)
    ↓
Result (Return to user)
```

### Multi-Skill Workflow
```
User Request (Complex)
    ↓
Isabella (Analyze, plan workflow)
    ↓
Skill 1 (Research/Learn)
    ↓
Skill 2 (Create/Write)
    ↓
Skill 1 (Save to Drive)
    ↓
Result (Integrated output)
```

---

## Deployment Model

### Current: Hybrid
- **Skill 1** (GDM): FastAPI microservice on Railway
- **Skills 2-3**: Deployed as Custom GPT or additional services

### Future: Unified
- All skills as integrated microservices
- Central orchestrator (Isabella Hub)
- Shared authentication and storage

---

## Data Flow

### Read Flow
```
User Query
  ↓
Isabella (Understands intent)
  ↓
Skill 1: Google Drive Manager
  ├─ /search → Find files
  ├─ /list-recursive → Browse structure
  └─ /read → Get content
  ↓
Result (Back to Isabella for formatting)
  ↓
User (Receives organized response)
```

### Write Flow
```
User Request (Write/Create)
  ↓
Isabella (Plan)
  ↓
Skill 2: Story Writer
  ├─ Generate content
  └─ Refine as needed
  ↓
Skill 1: Google Drive Manager
  ├─ /write → Create file
  └─ /append → Add to file
  ↓
User (Confirmation + link to file)
```

---

## Authentication & Authorization

### Skill 1: Google Drive Manager
```
┌─────────────────────────────────┐
│ Railway Environment Variables   │
├─────────────────────────────────┤
│ GOOGLE_OAUTH_TOKEN_JSON         │ → Drive Access
│ OPENROUTER_API_KEY              │ → AI Models
└─────────────────────────────────┘
```

### Skills 2-3 (Planned)
```
┌──────────────────────────────────┐
│ OpenAI/Custom GPT Configuration  │
├──────────────────────────────────┤
│ API Key                          │ → Model Access
│ Custom System Prompt             │ → Skill Behavior
│ Available Functions              │ → Integration
└──────────────────────────────────┘
```

---

## State Management

### Session Context
Isabella remembers across conversation:
- What skills have been used
- Files that were accessed
- Projects being worked on
- Learning topics covered
- Writing projects in progress

### Persistence
- User files stored in Google Drive
- Conversation history (if logging enabled)
- Preferences (if configured)

---

## Error Handling

### Skill Level
Each skill handles its own errors:
- Skill 1: Drive connection issues → `/diagnose` recommended
- Skills 2-3: Model errors → Clear explanation + fallback

### Isabella Level
Coordinates recovery:
- Try alternative approach
- Suggest manual action if needed
- Maintain conversation continuity

---

## Performance Considerations

### Skill 1 (GDM)
- **Response time:** ~200-500ms per request
- **Limits:** 100 items per list, recursion depth 10
- **Caching:** None (always fresh from Drive)

### Skills 2-3 (Planned)
- **Response time:** 5-30 seconds (depends on model, length)
- **Limits:** Token limits per model
- **Caching:** Model responses

---

## Security Model

### Data Protection
- ✅ Google Drive credentials never exposed
- ✅ OpenRouter key stored securely
- ✅ No local file storage on server
- ✅ Encrypted HTTPS only

### Access Control
- One user (you)
- One Drive
- Skill-based capability separation

---

## Skill Communication Protocol

### Request Format (Skills 2-3)
```json
{
  "skill": "story_writer|tutor",
  "action": "write|explain|quiz",
  "context": {
    "topic": "...",
    "previous_results": {...},
    "constraints": {...}
  },
  "request": "..."
}
```

### Response Format
```json
{
  "status": "success|error",
  "skill": "...",
  "result": "...",
  "related_actions": [...],
  "next_steps": [...]
}
```

---

## Integration Patterns

### Pattern 1: Sequential
```
Skill 3 (Learn)
  → Skill 2 (Write about it)
  → Skill 1 (Save to Drive)
```

### Pattern 2: Parallel
```
Skill 3 (Research topic)  ┐
Skill 2 (Draft chapter)   ├─ Combine results
Skill 1 (Find references) ┘
```

### Pattern 3: Feedback Loop
```
Skill 2 (Write)
  ↓
User Feedback
  ↓
Skill 3 (Teach for improvement)
  ↓
Skill 2 (Rewrite)
  ↓
Skill 1 (Save version)
```

---

## Extensibility

### Adding a New Skill
1. Define capability matrix
2. Design API/interface
3. Implement skill module
4. Register with Isabella
5. Update system instructions
6. Document in ISABELLA_SKILLS.md

### Skill Template
```markdown
## Skill X: [Name]

**Status:** [Status]
**Version:** [Version]

### Capabilities
- [Capability 1]
- [Capability 2]

### Integration Points
- With Skill Y: [How]
- With Skill Z: [How]

### Example Workflow
[Example showing usage]
```

---

## Roadmap

### Phase 1: Foundation (Current)
- ✅ Architecture defined
- ✅ Skill 1: Google Drive Manager (Production)
- ✅ System instructions created
- Skills 2-3: Designed

### Phase 2: Expansion (Next)
- Deploy Skill 2: Story Writer
- Deploy Skill 3: Tutor
- Create unified dashboard
- Add skill management UI

### Phase 3: Intelligence
- Skill recommendation engine
- Auto-workflow generation
- Learning from user patterns
- Predictive assistance

### Phase 4: Ecosystem
- Community skill marketplace
- Third-party integrations
- Plugin system
- Mobile app

---

## Support & Troubleshooting

### Quick Checks
```bash
# Check all systems
https://web-production-99e37.up.railway.app/diagnose

# Check available models
https://web-production-99e37.up.railway.app/models

# Check health
https://web-production-99e37.up.railway.app/
```

### Common Issues

**"Skill not responding"**
- Check endpoint status
- Verify credentials
- Use `/diagnose`

**"Unexpected result"**
- Clarify your request
- Provide more context
- Try alternative phrasing

**"Integration failed"**
- Check skill order
- Verify dependencies
- Simplify request

---

## Documentation Index

| Document | Purpose |
|----------|---------|
| [ISABELLA_SYSTEM_INSTRUCTIONS.md](ISABELLA_SYSTEM_INSTRUCTIONS.md) | Core personality & behavior |
| [ISABELLA_SKILLS.md](ISABELLA_SKILLS.md) | Skill registry & capabilities |
| [BROWSE_DRIVE.md](BROWSE_DRIVE.md) | Skill 1 usage guide |
| [ACTION_SCHEMAS.md](ACTION_SCHEMAS.md) | OpenAPI schema |
| [openapi.json](openapi.json) | API specification |

---

## Version History

**v1.0.0** (February 2026)
- Initial architecture
- Skill 1 active
- Skills 2-3 planned
- Full documentation

