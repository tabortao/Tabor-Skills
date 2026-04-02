---
name: save_to_dinox
description: Save Markdown files to Dinox note-taking app. Supports importing markdown content with or without title and tags. Use when the user asks to save content to Dinox or import markdown files.
---

# Save to Dinox

Save Markdown files to Dinox note-taking app using the Dinox Open API.

## Features

- **Markdown import**: Save markdown content directly to Dinox
- **Title and tags support**: Optionally specify title and tags
- **Auto-read from files**: Reads markdown from local files
- **Token from environment**: Uses DINOX_TOKEN environment variable

## Setup

1. **Get your Dinox API Token:**
   - Register at Dinox and obtain your API token

2. **Set environment variable:**
   ```bash
   # Add to your .env file
   DINOX_TOKEN="your_dinox_token_here"
   ```

## Usage

### Save markdown file to Dinox

```bash
python scripts/save_to_dinox.py "path/to/article.md"
```

### Save with title and tags

```bash
python scripts/save_to_dinox.py "path/to/article.md" --title "My Title" --tags "tag1,tag2"
```

### Save markdown content directly

```bash
python scripts/save_to_dinox.py --content "# Hello\n\nThis is content"
```

### Save with explicit token

```bash
python scripts/save_to_dinox.py "article.md" --token "your_token"
```

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `/api/openapi/markdown/import/{token}` | Import markdown content |
| `/api/openapi/createNote` | Create note with title and tags |

## Examples

```bash
# Save a markdown file
python scripts/save_to_dinox.py "my_notes.md"

# Save with custom title
python scripts/save_to_dinox.py "my_notes.md" --title "今日笔记"

# Save with tags
python scripts/save_to_dinox.py "my_notes.md" --tags "AI,技术,笔记"

# Save raw content
python scripts/save_to_dinox.py --content "# 标题\n\n内容..."
```

## Notes

- DINOX_TOKEN should be set in .env file or passed via --token
- The markdown import endpoint is compatible with Flomo
- Returns the noteId of the created note
- Supports full markdown syntax including headers, lists, code blocks, etc.
