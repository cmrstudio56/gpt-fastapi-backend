# Action Schemas - GPT Writer API

This directory contains OpenAPI/Swagger schemas for integrating the GPT Writer API with AI systems like OpenAI's Custom GPT Actions.

## 📄 Files

### `openapi.yaml`
- **Format**: YAML (human-readable)
- **Use**: Ideal for reading, editing, and version control
- **Size**: Compact and easy to navigate
- **Best for**: Development and documentation

### `openapi.json`
- **Format**: JSON (programmatic)
- **Use**: Direct integration with API tools and Custom GPT
- **Best for**: Production deployments and automation

## 🚀 How to Use

### Option 1: Custom GPT Actions (OpenAI)

1. Go to [OpenAI Platform](https://platform.openai.com/account/assistants)
2. Create or edit a GPT
3. Navigate to **Actions** → **Create new action**
4. Under **Authentication**, select **API Key** (if needed)
5. Paste the contents of `openapi.json` into the **Schema** section
6. Click **Validate Schema**
7. Save and test

### Option 2: Swagger UI (Local Testing)

Use Swagger UI to visualize and test endpoints:

```bash
# Online Swagger Editor
https://editor.swagger.io

# Paste either openapi.yaml or openapi.json content
```

### Option 3: Your FastAPI Auto-Generated Docs

Your FastAPI app already generates OpenAPI docs at:
- **Swagger UI**: `https://web-production-99e37.up.railway.app/docs`
- **ReDoc**: `https://web-production-99e37.up.railway.app/redoc`
- **OpenAPI JSON**: `https://web-production-99e37.up.railway.app/openapi.json`

## 📋 Endpoint Categories

### File Operations (4 endpoints)
- `POST /write` - Create files
- `GET /read` - Read file content
- `POST /append` - Append to files
- `GET /list` - List files and folders

### AI Features (2 endpoints)
- `POST /summarize` - AI-powered summarization with 6 models
- `GET /models` - List available OpenRouter models

### Book Management (5 endpoints)
- `POST /book/create` - Create book with metadata
- `GET /book/metadata` - Get book info
- `POST /book/update-metadata` - Update metadata
- `GET /series/list` - List books by series
- `GET /book/chapter-count` - Get chapter count

### System (1 endpoint)
- `GET /` - Health check

## 🔑 Environment Variables Required

For production deployment, configure these on Railway:

```
GOOGLE_OAUTH_TOKEN_JSON=<your-google-oauth-token-as-json>
OPENROUTER_API_KEY=sk-or-v1-...
```

## 📚 Example Usage

### Create a File
```bash
curl -X POST https://web-production-99e37.up.railway.app/write \
  -H "Content-Type: application/json" \
  -d '{
    "title": "my_story",
    "content": "Chapter 1: The Beginning",
    "project": "default"
  }'
```

### Summarize with AI
```bash
curl -X POST https://web-production-99e37.up.railway.app/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "title": "my_story",
    "project": "default",
    "model": "claude-3-5-sonnet",
    "max_length": 300
  }'
```

### Create a Book
```bash
curl -X POST https://web-production-99e37.up.railway.app/book/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Last Kingdom",
    "author": "Bernard Cornwell",
    "series": "Saxon Series",
    "book_number": 1,
    "status": "completed",
    "chapters": 45
  }'
```

## 🤖 Available AI Models

Using OpenRouter integration, you can choose from:

- **claude-3-5-sonnet** - Latest Claude, best for summarization
- **claude-3-opus** - Most powerful reasoning
- **gpt-4o** - OpenAI multimodal model
- **gpt-4-turbo** - Faster GPT-4
- **llama-2** - Open-source 70B
- **mistral** - Cost-effective 7B

## 🔍 Schema Features

✅ **Fully Documented**
- Clear descriptions for all endpoints
- Parameter explanations
- Response schemas

✅ **Type-Safe**
- Strict schema validation
- Enum values for constrained fields
- Required vs optional parameters marked

✅ **Production-Ready**
- Error handling documented
- Proper HTTP status codes
- Security schemes defined

✅ **Easy Integration**
- Compatible with OpenAI Custom GPT
- Works with Swagger/OpenAPI tools
- RESTful design patterns

## 📝 Notes

- Schemas are auto-generated from FastAPI code
- Always use the latest schema from `openapi.json` for production
- Update schemas when adding new endpoints
- Test in Swagger UI before deploying to Custom GPT

## 🔗 Related

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [OpenAPI Specification](https://swagger.io/specification)
- [OpenAI Custom GPT Actions](https://platform.openai.com/docs/assistants/tools/function-calling)
- [OpenRouter Documentation](https://openrouter.io/docs)
