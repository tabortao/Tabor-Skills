# Personal Skills Collection for Claude Code

A curated library of 20+ productivity-enhancing skills designed to streamline your work and learning efficiency. This collection focuses on practical, immediately useful tools across content creation, development automation, knowledge management, and media processing.

## 🎯 Purpose

This is a **personal productivity toolkit** built for Claude Code, containing hand-picked skills that enhance daily workflows. Each skill is carefully selected for real-world utility and optimized for immediate use in:

- **Content Creation & Publishing**: WeChat articles, social media optimization
- **Development & Automation**: Browser automation, web development tools
- **Knowledge Management**: Note-taking, research, information organization
- **Media Processing**: Video downloading, content extraction, file handling

## 📊 Collection Overview

### 📝 Content & Publishing (6 Skills)

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| **wechat-article-writer** | End-to-end article creation | Research → Write → Title → Optimize |
| **wechat-title-optimizer** | Viral title generation | Technical content optimization |
| **wechat-content-optimizer** | Content enhancement | Chinese social media format |
| **wechat-converter** | Format conversion | General → WeChat optimized |
| **wechat-publisher-yashu** | Publishing automation | Direct WeChat platform integration |
| **generate-cover-prompt** | Visual content creation | AI image prompt generation |

### 🔧 Development & Automation (4 Skills)

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| **agent-browser** | Browser automation | CDP-based, form filling, scraping |
| **chrome-devtools-skill** | Web development | Chrome DevTools integration |
| **skill-creator-yashu** | Skill development | Enhanced creation workflow |
| **skill-optimizer-yashu** | Quality assurance | Performance analysis & optimization |

### 📚 Knowledge Management (4 Skills)

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| **obsidian-cli** | Note management | Complete Obsidian vault control |
| **obsidian-bases** | Data organization | Database-like note views |
| **obsidian-markdown** | Content processing | Obsidian-flavored markdown |
| **siyuan-notes-skill** | Platform integration | 思源笔记 (SiYuan) support |

### 🎥 Media & File Processing (3 Skills)

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| **video-downloader-skill** | Media download | YouTube, Bilibili, Twitter support |
| **defuddle** | Content extraction | Clean web content parsing |
| **json-canvas** | Visual organization | JSON Canvas file handling |

### ⚡ Productivity & Utilities (3 Skills)

| Skill | Purpose | Key Features |
|-------|---------|-------------|
| **find-skills** | Skill discovery | Find and install new skills |
| **skill-laws** | Design principles | Skill creation guidelines |
| **save_to_dinox** | Note integration | Dinox platform saving |

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/personal-skills.git
   cd personal-skills/skills
   ```

2. **Initialize submodules**:
   ```bash
   git submodule update --init --recursive
   ```

3. **Configure environment**:
   - Update `.claude/settings.json` with your API credentials
   - Verify model configuration (LongCat-Flash-Chat recommended)

### Usage Examples

#### Content Creation Workflow
```
1. Research topic → wechat-article-writer
2. Generate viral title → wechat-title-optimizer
3. Optimize content → wechat-content-optimizer
4. Create cover image → generate-cover-prompt
5. Publish article → wechat-publisher-yashu
```

#### Research & Note-Taking Workflow
```
1. Extract web content → defuddle
2. Download media → video-downloader-skill
3. Save to notes → obsidian-cli
4. Organize data → obsidian-bases
5. Convert formats → obsidian-markdown
```

#### Development & Automation Workflow
```
1. Automate browser tasks → agent-browser
2. Debug web apps → chrome-devtools-skill
3. Create new skills → skill-creator-yashu
4. Optimize performance → skill-optimizer-yashu
```

## 🏗️ Architecture

### Core Infrastructure

- **`.claude/`**: Configuration and skill management framework
- **Skill Development Tools**: Creation, testing, and optimization utilities
- **Git Submodules**: Version-controlled skill dependencies

### Skill Structure

Each skill follows a standardized pattern:

```
skill-name/
├── SKILL.md                 # Core documentation with metadata
├── scripts/                 # Executable automation scripts
├── references/              # Detailed guides and documentation
├── assets/                  # Templates, images, static files
└── evals/                   # Testing and evaluation data
```

## 🔧 Development & Customization

### Adding New Skills

1. **Use the built-in skill creator**:
   ```bash
   cd .claude/skills/skill-creator
   python -m scripts.create_skill "my-new-skill"
   ```

2. **Follow the guided workflow** for documentation and testing
3. **Add comprehensive test cases** for reliability
4. **Optimize descriptions** for better triggering accuracy

### Skill Quality Standards

- **Progressive Disclosure**: Organized loading (metadata → docs → resources)
- **Objective Testing**: Quantifiable assertions and benchmarks
- **Performance Monitoring**: Token usage and execution time tracking
- **User Experience**: Clear documentation and examples

## 📈 Performance & Optimization

### Built-in Evaluation System

- **Parallel Testing**: Compare skills against baselines
- **Quantitative Metrics**: Pass rates, performance benchmarks
- **Visual Analysis**: Interactive comparison tools
- **Description Optimization**: AI-powered triggering improvements

### Key Performance Indicators

- **Trigger Accuracy**: Skill invocation precision
- **Execution Speed**: Response time optimization
- **Token Efficiency**: Resource usage minimization
- **Success Rate**: Task completion reliability

## 🤝 Contributing

### Adding Skills to Collection

1. Fork the repository
2. Create your skill using the skill-creator workflow
3. Include comprehensive test cases and documentation
4. Optimize for performance and user experience
5. Submit a pull request with detailed description

### Quality Guidelines

- Follow progressive disclosure principles
- Include objective evaluation criteria
- Maintain clear, concise documentation
- Ensure cross-platform compatibility
- Provide practical usage examples

## 📄 License

This personal skills collection is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built for productivity, optimized for efficiency** 🚀

For detailed development guidance and operational instructions, see [CLAUDE.md](CLAUDE.md).
