# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this personal skills collection repository.

## Project Overview

This repository is a **Personal Skills Collection** for Claude Code - a curated library of 20+ productivity-enhancing skills designed to streamline work and learning efficiency. Each skill is carefully selected and optimized for real-world usage scenarios, from content creation and research to development tools and automation.

The collection focuses on practical, immediately useful skills that enhance daily workflows across multiple domains:

- **Content Creation & Publishing** (6 skills): WeChat article writing, optimization, and publishing tools
- **Development & Automation** (4 skills): Browser automation, DevTools integration, and skill development utilities
- **Knowledge Management** (4 skills): Obsidian and note-taking platform integrations
- **Media & File Processing** (3 skills): Video downloading, content extraction, and file handling
- **Productivity & Utilities** (3 skills): Skill discovery, design principles, and utility functions

## Repository Structure

```
.skills-manager/skills/
├── .claude/                           # Core Infrastructure
│   ├── settings.json                  # Environment & API Configuration
│   └── skills/                        # Skill Development Tools
│       ├── skill-creator/             # Primary skill development framework
│       └── find-skills/               # Skill discovery and installation
│
├── Content & Publishing (6 skills)
│   ├── wechat-article-writer/         # 公众号文章自动化写作流程
│   ├── wechat-title-optimizer/        # 公众号标题优化专家
│   ├── wechat-content-optimizer/      # 公众号内容优化工具
│   ├── wechat-converter/              # 通用内容转换工具
│   ├── wechat-publisher-yashu/        # 公众号发布助手
│   └── generate-cover-prompt/         # 文章封面图AI提示词生成
│
├── Development & Automation (4 skills)
│   ├── agent-browser/                 # Browser automation CLI
│   ├── chrome-devtools-skill/         # Chrome DevTools integration
│   ├── skill-creator-yashu/           # Enhanced skill creation
│   └── skill-optimizer-yashu/         # Skill quality optimization
│
├── Knowledge Management (4 skills)
│   ├── obsidian-cli/                  # Obsidian vault management
│   ├── obsidian-bases/                # Obsidian database views
│   ├── obsidian-markdown/             # Obsidian markdown processing
│   └── siyuan-notes-skill/            # 思源笔记集成
│
├── Media & File Processing (3 skills)
│   ├── video-downloader-skill/        # Multi-platform video/audio downloader
│   ├── defuddle/                      # Clean web content extraction
│   └── json-canvas/                   # JSON Canvas file handling
│
├── Productivity & Utilities (3 skills)
│   ├── find-skills/                   # Skill discovery tool
│   ├── skill-laws/                    # Skill design principles
│   └── save_to_dinox/                 # Dinox note saving
│
└── Infrastructure
    ├── claude-plugins-official/        # Official plugin collection
    ├── tts-skill/                     # Text-to-speech functionality
    ├── docs/                          # Documentation and guides
    └── CLAUDE.md                      # This operational guide
```

## Skill Categories & Usage

### 📝 Content & Publishing Skills

**WeChat Ecosystem (5 skills)**
- `wechat-article-writer`: End-to-end article creation with research, writing, title generation
- `wechat-title-optimizer`: Generate viral titles for technical content
- `wechat-content-optimizer`: Optimize articles for Chinese social media
- `wechat-converter`: Convert general content to WeChat format
- `wechat-publisher-yashu`: Publish articles to WeChat platform

**Visual Content**
- `generate-cover-prompt`: Create AI image prompts for article covers

### 🔧 Development & Automation Skills

**Browser Tools**
- `agent-browser`: Full browser automation with CDP, form filling, scraping
- `chrome-devtools-skill`: Chrome DevTools integration for web development

**Skill Development**
- `skill-creator-yashu`: Enhanced skill creation workflow
- `skill-optimizer-yashu`: Analyze and optimize skill quality

### 📚 Knowledge Management Skills

**Obsidian Ecosystem (3 skills)**
- `obsidian-cli`: Complete Obsidian vault management via CLI
- `obsidian-bases`: Create database-like views for notes
- `obsidian-markdown`: Process Obsidian-flavored markdown

**Note Platforms**
- `siyuan-notes-skill`: Integration with 思源笔记 (SiYuan Notes)

### 🎥 Media & File Processing Skills

**Download & Extraction**
- `video-downloader-skill`: Download videos/audio from YouTube, Bilibili, Twitter
- `defuddle`: Extract clean content from web pages

**File Management**
- `json-canvas`: Handle JSON Canvas files for visual organization

### ⚡ Productivity & Utilities

**Skill Management**
- `find-skills`: Discover and install new skills
- `skill-laws`: Design principles for skill creation

**Utilities**
- `save_to_dinox`: Save content to Dinox note-taking app

## Key Technologies and Frameworks

- **Claude Code**: Primary development environment and skill execution platform
- **Git Submodules**: Used for managing external skill dependencies (see `docs/使用Submodules增加Skil.md`)
- **Anthropic API**: LongCat model integration for skill execution
- **Python**: Primary scripting language for skill automation
- **JSON**: Configuration and data exchange format

## Common Commands

### Skill Development Workflow

```bash
# Create a new skill using the skill-creator
cd .claude/skills/skill-creator
python -m scripts.create_skill "skill-name"

# Test a skill with evaluation cases
python -m scripts.run_tests skill-name/evals/evals.json

# Package a skill for distribution
python -m scripts.package_skill path/to/skill-directory

# Run skill description optimization
python -m scripts.run_loop --eval-set trigger-eval.json --skill-path skill-directory
```

### Repository Management

```bash
# Add a skill as a Git submodule
git submodule add https://github.com/user/skill-name.git

# Update all submodules
git submodule update --init --recursive

# Initialize submodules after cloning
git submodule update --init --recursive
```

### Evaluation and Testing

```bash
# Run the evaluation viewer for skill testing
python eval-viewer/generate_review.py workspace/iteration-1 --skill-name "my-skill"

# Aggregate benchmark results
python -m scripts.aggregate_benchmark workspace/iteration-1 --skill-name skill-name
```

## Architecture Overview

### Skill Structure

Each skill follows a standardized structure:

```
skill-name/
├── SKILL.md                 # Required: Skill documentation with YAML frontmatter
├── scripts/                 # Optional: Executable Python scripts
├── references/              # Optional: Documentation and reference materials
├── assets/                  # Optional: Templates, images, and static files
└── evals/                   # Optional: Test cases and evaluation data
    └── evals.json          # Test prompts and expected outputs
```

### Skill Development Framework

1. **Skill Creator** (`.claude/skills/skill-creator/`): The primary tool for developing new skills, featuring:
   - Automated test case generation and execution
   - Quantitative benchmarking and evaluation
   - Description optimization for better skill triggering
   - Progressive disclosure architecture support

2. **Quality Assurance**: Skills undergo rigorous testing including:
   - Parallel execution of skill vs baseline comparisons
   - Quantitative assertion-based grading
   - Visual benchmark comparison tools
   - Performance metrics (tokens, duration, pass rates)

## Development Guidelines

### Creating New Skills

1. **Use the Skill Creator**: Always start with `.claude/skills/skill-creator/SKILL.md` for new skill development
2. **Follow the Progressive Disclosure Pattern**:
   - Keep SKILL.md under 500 lines
   - Use reference files for detailed documentation
   - Organize by domains when supporting multiple frameworks
3. **Include Test Cases**: Create realistic evaluation prompts in `evals/evals.json`
4. **Optimize Skill Descriptions**: Use the description optimization workflow for better triggering

### Skill Quality Standards

- **Progressive Disclosure**: Three-level loading system (metadata → SKILL.md → bundled resources)
- **Principle of Lack of Surprise**: Skills must not contain malware or unexpected behavior
- **Objective Evaluation**: Include quantifiable assertions for automated testing
- **Domain Organization**: Group related variants in reference files

### Configuration Management

Environment settings are managed in `.claude/settings.json`:
- Anthropic API configuration
- Model selection (LongCat-Flash-Chat as default)
- Output token limits
- Performance optimization flags

## Important Files and References

- `.claude/settings.json`: Environment configuration and API settings
- `.claude/skills/skill-creator/SKILL.md`: Complete skill development workflow
- `docs/使用Submodules增加Skil.md`: Git submodule usage guide (Chinese)
- `.claude/skills/skill-creator/references/schemas.md`: JSON schemas for evaluation data
- `.claude/skills/skill-creator/agents/`: Specialized subagent instructions

## Usage Examples

### Content Creation Workflow
```
1. Research topic with WebSearch
2. Write article using wechat-article-writer
3. Optimize title with wechat-title-optimizer
4. Enhance content with wechat-content-optimizer
5. Generate cover with generate-cover-prompt
6. Publish using wechat-publisher-yashu
```

### Research & Note-Taking Workflow
```
1. Extract content with defuddle
2. Save to Obsidian using obsidian-cli
3. Organize with obsidian-bases
4. Convert formats with obsidian-markdown
```

### Development & Automation Workflow
```
1. Automate browser tasks with agent-browser
2. Debug with chrome-devtools-skill
3. Create new skills with skill-creator-yashu
4. Optimize existing skills with skill-optimizer-yashu
```

## Troubleshooting and Support

### Common Issues

1. **Skill Not Triggering**: Run description optimization workflow
2. **Evaluation Failures**: Check assertion format in `grading.json`
3. **Submodule Issues**: Ensure proper initialization with `--recursive` flag
4. **Permission Errors**: Verify API token configuration in settings.json

### Performance Optimization

- Use `--static` flag for headless environments
- Implement caching for frequently accessed resources
- Monitor token usage and optimize skill descriptions
- Use parallel execution for multiple test cases

This personal skills collection represents a comprehensive toolkit for enhancing productivity across content creation, development, research, and knowledge management workflows. Each skill is designed for immediate practical use and continuous improvement through the built-in evaluation framework.
