# Tabor-Skills

A collection of powerful AI skills and tools designed to enhance productivity and streamline workflows. This repository contains specialized skills for note management and media downloading, built to integrate seamlessly with AI assistants like Claude.

## 🚀 Available Skills

### 📚 Siyuan Notes Query Skill
A sophisticated Node.js tool for intelligent querying and management of 思源笔记 (Siyuan Notes) using advanced SQL capabilities.

**Key Features:**
- 🔍 **Advanced Content Search** - Query any content within your notes using natural language
- 🔗 **Smart Relationship Discovery** - Automatically discover connections and references between notes
- 📋 **Task Management Integration** - Direct querying and management of note-based to-do items
- 🏷️ **Tag & Attribute Queries** - Precise filtering based on tags and custom attributes
- 📊 **Time-based Analysis** - Query daily notes, tasks, and documents by time ranges
- 🎯 **Zero Learning Curve** - Natural language queries without needing to learn SQL

**Use Cases:**
- "Find all notes about artificial intelligence"
- "Show me my unfinished tasks from this week"
- "What notes reference this document?"
- "List all documents with high priority tags"

**Tech Stack:** Node.js, SQL querying, RESTful API integration

**Documentation:** [siyuan-notes-skill/README.md](siyuan-notes-skill/README.md)

### 🎬 Video Downloader Skill
A powerful Python-based tool for downloading videos and audio from multiple platforms including YouTube, Bilibili, and Twitter.

**Key Features:**
- **🌐 Wide Platform Support** - Download from YouTube, Bilibili, Twitter, and 100+ other sites
- **📊 Real-time Progress** - Live download progress with detailed information display
- **🪟 Windows Optimized** - Enhanced UTF-8 support for Chinese paths and robust Windows compatibility
- **🎚️ Quality Selection** - Choose from best to worst quality, including specific resolutions (1080p, 720p, etc.)
- **🔄 Format Conversion** - Save in MP4, WebM, MKV, or extract audio as MP3
- **🛡️ Enhanced Bilibili Support** - Special anti-blocking protection and optimized download strategies
- **🍪 Cookie Support** - Download content that requires authentication
- **🔧 Auto Dependency Management** - Automatically installs required tools

**Use Cases:**
- Download educational videos for offline viewing
- Extract audio from music videos
- Archive important content from social media
- Create local backups of online media

**Tech Stack:** Python, yt-dlp integration, cross-platform compatibility

**Documentation:** [video-downloader-skill/README.md](video-downloader-skill/README.md)

## 🛠️ Development Setup

### Prerequisites

**For Siyuan Notes Skill:**
- Node.js 14.0.0 or higher
- npm package manager
- Siyuan Notes instance with API access

**For Video Downloader Skill:**
- Python 3.x
- pip package manager

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/your-org/Tabor-Skills.git
cd Tabor-Skills
```

2. **Set up Siyuan Notes Skill:**
```bash
cd siyuan-notes-skill
npm install
# Configure your .env file with Siyuan API credentials
```

3. **Set up Video Downloader Skill:**
```bash
cd video-downloader-skill
# Dependencies are automatically managed
```

## 📖 Usage Examples

### Siyuan Notes Skill
```bash
cd siyuan-notes-skill

# Test connection
npm test

# Search for notes containing specific keywords
node index.js search "machine learning"

# List all documents
node index.js docs

# Find tasks from the last 7 days
node index.js tasks "[ ]" 7
```

### Video Downloader Skill
```bash
cd video-downloader-skill

# Download video in best quality
python scripts/video_download.py "https://youtube.com/watch?v=..."

# Download Bilibili video in 1080p
python scripts/video_download.py "https://bilibili.com/video/..." -q 1080p

# Extract audio only
python scripts/video_download.py "https://youtube.com/watch?v=..." -a

# Download to specific directory
python scripts/video_download.py "https://youtube.com/watch?v=..." -o "/path/to/downloads"
```

## 🏗️ Architecture

This repository follows a modular architecture where each skill is self-contained:

```
Tabor-Skills/
├── siyuan-notes-skill/      # Node.js skill for note management
│   ├── index.js             # Main entry point
│   ├── package.json         # Dependencies and scripts
│   └── README.md           # Skill-specific documentation
├── video-downloader-skill/   # Python skill for media downloading
│   ├── scripts/
│   │   └── video_download.py  # Main downloader script
│   └── README.md           # Skill-specific documentation
├── CLAUDE.md               # Claude Code integration guide
└── README.md              # This file
```

## 🤝 Contributing

Each skill is developed independently with its own:
- Documentation
- Configuration
- Dependencies
- Testing procedures

When contributing:
1. Work within the specific skill directory
2. Follow the existing code style and patterns
3. Update the skill-specific README.md with new features
4. Ensure cross-platform compatibility where applicable

## 📄 License

This project is licensed under the MIT License. See individual skill directories for specific licensing information.

## 🔗 Related Links

- [CLAUDE.md](CLAUDE.md) - Integration guide for Claude Code
- [Siyuan Notes Official](https://github.com/siyuan-note/siyuan) - The note-taking application
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video download engine

---

**Start enhancing your productivity with AI-powered skills!** 🚀

Choose a skill from the list above and begin exploring its capabilities.