# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This repository contains two main skills/tools:

1. **siyuan-notes-skill** - A Node.js tool for querying and managing 思源笔记 (Siyuan Notes) using SQL queries
2. **video-downloader-skill** - A Python tool for downloading videos from YouTube, Bilibili, and other platforms

## Development Commands

### Siyuan Notes Skill (Node.js)

**Installation and Setup:**
```bash
cd siyuan-notes-skill
npm install
```

**Running the tool:**
```bash
# Start the tool
npm start

# Test connection to Siyuan Notes
npm test
# or
node index.js check
```

**Available Commands:**
```bash
# Search notes containing keywords
node index.js search "keyword" [blockType]

# List all documents or documents in a specific notebook
node index.js docs [notebookId]

# Query document headings
node index.js headings "documentId" [headingType]

# Query document blocks
node index.js blocks "documentId" [blockType]

# Search by tag
node index.js tag "tagName"

# Get backlinks for a block
node index.js backlinks "blockId"

# Search tasks
node index.js tasks [status] [days]

# Query daily notes
node index.js daily "startDate" "endDate"

# Search by attribute
node index.js attr "attributeName" [attributeValue]

# Query bookmarks
node index.js bookmarks [bookmarkName]

# Get random heading from document
node index.js random "documentId"

# Get recent blocks
node index.js recent [days] [blockType]

# Get unreferenced documents
node index.js unreferenced "notebookId"
```

**Configuration:**
- Requires a `.env` file in the siyuan-notes-skill directory
- Must configure `SIYUAN_API_TOKEN` from Siyuan Notes settings
- Optional: `SIYUAN_HOST`, `SIYUAN_PORT`, `SIYUAN_USE_HTTPS`, `SIYUAN_BASIC_AUTH_USER`, `SIYUAN_BASIC_AUTH_PASS`

### Video Downloader Skill (Python)

**Running the tool:**
```bash
cd video-downloader-skill
python scripts/video_download.py <url> [options]
```

**Available Options:**
```bash
# Download with specific quality
python scripts/video_download.py "https://youtube.com/watch?v=..." -q 720p

# Download only audio as MP3
python scripts/video_download.py "https://youtube.com/watch?v=..." -a

# Specify output directory
python scripts/video_download.py "https://youtube.com/watch?v=..." -o"/path/to/output"

# Choose video format
python scripts/video_download.py "https://youtube.com/watch?v=..." -f webm

# Combined example
python scripts/video_download.py "https://bilibili.com/video/..." -q 1080p -o"./downloads" -f mp4
```

**Quality Options:** `best`, `1080p`, `720p`, `480p`, `360p`, `worst`
**Format Options:** `mp4`, `webm`, `mkv`

**Dependencies:**
- Automatically installs `yt-dlp` if not available
- Requires Python 3.x
- Supports Windows, macOS, and Linux

## Code Architecture

### Siyuan Notes Skill
- **Entry Point:** `index.js` - Main CLI interface and command router
- **Core Functions:** SQL query execution, search, document management
- **Configuration:** Environment variable management with `.env` file support
- **Authentication:** Supports both Siyuan API token and HTTP Basic Auth
- **Error Handling:** Comprehensive error handling for network, authentication, and API errors
- **Output Formatting:** Multiple formatting options for query results

**Key Features:**
- SQL-based querying of Siyuan Notes database
- Support for searching by content, tags, attributes
- Document and block management
- Task and daily note querying
- Backlink analysis
- Structured and formatted output options

### Video Downloader Skill
- **Entry Point:** `scripts/video_download.py` - Main CLI interface
- **Core Functions:** Video downloading with platform-specific optimizations
- **Platform Support:** YouTube, Bilibili (with special handling), and other yt-dlp supported platforms
- **Quality Management:** Flexible quality selection and format options
- **Error Recovery:** Automatic retry mechanisms for failed downloads
- **Real-time Progress:** Live download progress display

**Key Features:**
- Automatic yt-dlp installation and management
- Bilibili-specific optimizations with anti-blocking measures
- Smart output directory detection
- Audio-only download support (MP3)
- Comprehensive error handling and troubleshooting guidance
- Cross-platform compatibility with UTF-8 support

## Environment Setup

### For Siyuan Notes Skill:
1. Install Node.js 14.0.0 or higher
2. Navigate to `siyuan-notes-skill` directory
3. Run `npm install`
4. Create `.env` file with required configuration
5. Obtain API token from Siyuan Notes settings

### For Video Downloader Skill:
1. Ensure Python 3.x is installed
2. Navigate to `video-downloader-skill` directory
3. The tool will automatically install yt-dlp if needed

## Common Development Tasks

### Testing Siyuan Connection:
```bash
cd siyuan-notes-skill
node index.js check
```

### Testing Video Downloader:
```bash
cd video-downloader-skill
python scripts/video_download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" -q 720p
```

### Debugging:
- Both tools support debug output
- For Siyuan skill: Set `DEBUG=true` in `.env` or use `--debug` flag
- For video downloader: Use `--verbose` flag for detailed output

## Repository Management

This repository uses Git for version control. Both skills are designed to be modular and can be developed independently.

**Recent Structure:**
- Main directory contains the two skill folders
- Each skill has its own README.md and documentation
- Skills are designed to work with Claude Code's skill system