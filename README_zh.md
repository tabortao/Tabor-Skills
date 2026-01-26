# Tabor-Skills

专为提升工作效率而设计的一系列强大AI技能和工具集合。本仓库包含专为笔记管理和媒体下载而设计的专业工具，可与Claude等AI助手无缝集成。

## 🚀 可用技能

### 📚 思源笔记查询技能
一个功能强大的Node.js工具，使用先进的SQL功能进行思源笔记的智能查询和管理。

**核心特性：**
- 🔍 **高级内容搜索** - 使用自然语言查询笔记中的任何内容
- 🔗 **智能关系发现** - 自动发现笔记间的连接和引用关系
- 📋 **任务管理集成** - 直接查询和管理基于笔记的待办事项
- 🏷️ **标签和属性查询** - 基于标签和自定义属性的精确筛选
- 📊 **时间维度分析** - 按时间范围查询日记、任务和文档
- 🎯 **零学习成本** - 无需学习SQL，使用自然语言即可查询

**使用场景：**
- "查找所有关于人工智能的笔记"
- "显示本周未完成的任务"
- "哪些笔记引用了这篇文档？"
- "列出所有带有高优先级标签的文档"

**技术栈：** Node.js, SQL查询, RESTful API集成

**文档：** [siyuan-notes-skill/README.md](siyuan-notes-skill/README.md)

### 🎬 视频下载器技能
一个功能强大的基于Python的工具，用于从YouTube、Bilibili、Twitter等多个平台下载视频和音频。

**核心特性：**
- **🌐 广泛平台支持** - 支持从YouTube、Bilibili、Twitter及100+其他网站下载
- **📊 实时进度显示** - 实时下载进度，详细信息展示
- **🪟 Windows优化** - 增强的UTF-8支持，适用于中文路径，强大的Windows兼容性
- **🎚️ 质量选择** - 从最佳到最差质量选择，包括特定分辨率（1080p、720p等）
- **🔄 格式转换** - 保存为MP4、WebM、MKV，或提取音频为MP3
- **🛡️ 增强的B站支持** - 特殊的防封禁保护和优化的下载策略
- **🍪 Cookie支持** - 下载需要登录验证的内容
- **🔧 自动依赖管理** - 自动安装所需工具

**使用场景：**
- 下载教育视频供离线观看
- 从音乐视频中提取音频
- 归档社交媒体上的重要内容
- 创建在线媒体的本地备份

**技术栈：** Python, yt-dlp集成, 跨平台兼容

**文档：** [video-downloader-skill/README.md](video-downloader-skill/README.md)

## 🛠️ 开发环境搭建

### 前置要求

**思源笔记技能：**
- Node.js 14.0.0或更高版本
- npm包管理器
- 支持API访问的思源笔记实例

**视频下载器技能：**
- Python 3.x
- pip包管理器

### 快速开始

1. **克隆仓库：**
```bash
git clone https://github.com/your-org/Tabor-Skills.git
cd Tabor-Skills
```

2. **设置思源笔记技能：**
```bash
cd siyuan-notes-skill
npm install
# 配置.env文件，填入思源API凭证
```

3. **设置视频下载器技能：**
```bash
cd video-downloader-skill
# 依赖项自动管理
```

## 📖 使用示例

### 思源笔记技能
```bash
cd siyuan-notes-skill

# 测试连接
npm test

# 搜索包含特定关键词的笔记
node index.js search "机器学习"

# 列出所有文档
node index.js docs

# 查找最近7天的任务
node index.js tasks "[ ]" 7
```

### 视频下载器技能
```bash
cd video-downloader-skill

# 以最佳质量下载视频
python scripts/video_download.py "https://youtube.com/watch?v=..."

# 以1080p下载B站视频
python scripts/video_download.py "https://bilibili.com/video/..." -q 1080p

# 仅提取音频
python scripts/video_download.py "https://youtube.com/watch?v=..." -a

# 下载到指定目录
python scripts/video_download.py "https://youtube.com/watch?v=..." -o "/path/to/downloads"
```

## 🏗️ 架构设计

本仓库采用模块化架构，每个技能都是独立的：

```
Tabor-Skills/
├── siyuan-notes-skill/      # 笔记管理Node.js技能
│   ├── index.js             # 主入口点
│   ├── package.json         # 依赖和脚本
│   └── README.md           # 技能特定文档
├── video-downloader-skill/   # 媒体下载Python技能
│   ├── scripts/
│   │   └── video_download.py  # 主下载脚本
│   └── README.md           # 技能特定文档
├── CLAUDE.md               # Claude Code集成指南
└── README.md              # 本文件
```

## 🤝 贡献指南

每个技能独立开发，具有自己的：
- 文档
- 配置
- 依赖项
- 测试流程

贡献时请注意：
1. 在特定技能目录内工作
2. 遵循现有的代码风格和模式
3. 使用新功能更新技能特定的README.md
4. 确保跨平台兼容性（如适用）

## 📄 许可证

本项目采用MIT许可证。请查看各个技能目录了解具体的许可信息。

## 🔗 相关链接

- [CLAUDE.md](CLAUDE.md) - Claude Code集成指南
- [思源笔记官方](https://github.com/siyuan-note/siyuan) - 笔记应用
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 视频下载引擎

---

**开始使用AI驱动的技能提升您的工作效率！** 🚀

从上面的列表中选择一个技能，开始探索其功能。