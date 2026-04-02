# Claude Code 个人技能集合

一个精心策划的 Claude Code 技能库，包含 20+ 个提升工作效率的实用技能。本集合专注于内容创作、开发自动化、知识管理和媒体处理等实际应用场景。

## 🎯 项目目的

这是一个为 **Claude Code 打造的个人效率工具包**，包含精心挑选的技能，旨在增强日常工作流程。每个技能都经过精心选择，具有实际效用并针对以下场景进行了优化：

- **内容创作与发布**: 微信公众号文章、社交媒体优化
- **开发与自动化**: 浏览器自动化、Web 开发工具
- **知识管理**: 笔记记录、研究、信息组织
- **媒体处理**: 视频下载、内容提取、文件处理

## 📊 技能集合概览

### 📝 内容创作与发布 (6 个技能)

| 技能 | 用途 | 主要特性 |
|------|------|----------|
| **wechat-article-writer** | 全流程文章创作 | 研究 → 写作 → 标题 → 优化 |
| **wechat-title-optimizer** | 爆款标题生成 | 技术内容优化 |
| **wechat-content-optimizer** | 内容增强 | 中文社交媒体格式 |
| **wechat-converter** | 格式转换 | 通用 → 微信优化 |
| **wechat-publisher-yashu** | 发布自动化 | 直接微信平台集成 |
| **generate-cover-prompt** | 视觉内容创作 | AI 图像提示词生成 |

### 🔧 开发与自动化 (4 个技能)

| 技能 | 用途 | 主要特性 |
|------|------|----------|
| **agent-browser** | 浏览器自动化 | 基于 CDP，表单填写，数据抓取 |
| **chrome-devtools-skill** | Web 开发 | Chrome DevTools 集成 |
| **skill-creator-yashu** | 技能开发 | 增强的创建工作流程 |
| **skill-optimizer-yashu** | 质量保证 | 性能分析与优化 |

### 📚 知识管理 (4 个技能)

| 技能 | 用途 | 主要特性 |
|------|------|----------|
| **obsidian-cli** | 笔记管理 | 完整的 Obsidian 仓库控制 |
| **obsidian-bases** | 数据组织 | 类数据库笔记视图 |
| **obsidian-markdown** | 内容处理 | Obsidian 风格 Markdown |
| **siyuan-notes-skill** | 平台集成 | 思源笔记支持 |

### 🎥 媒体与文件处理 (3 个技能)

| 技能 | 用途 | 主要特性 |
|------|------|----------|
| **video-downloader-skill** | 媒体下载 | YouTube、Bilibili、Twitter 支持 |
| **defuddle** | 内容提取 | 干净的网页内容解析 |
| **json-canvas** | 视觉组织 | JSON Canvas 文件处理 |

### ⚡ 效率工具与实用程序 (3 个技能)

| 技能 | 用途 | 主要特性 |
|------|------|----------|
| **find-skills** | 技能发现 | 查找和安装新技能 |
| **skill-laws** | 设计原则 | 技能创建指南 |
| **save_to_dinox** | 笔记集成 | Dinox 平台保存 |

## 🚀 快速开始

### 安装步骤

1. **克隆仓库**:
   ```bash
   git clone https://github.com/your-org/personal-skills.git
   cd personal-skills/skills
   ```

2. **初始化子模块**:
   ```bash
   git submodule update --init --recursive
   ```

3. **配置环境**:
   - 使用您的 API 凭据更新 `.claude/settings.json`
   - 验证模型配置（推荐使用 LongCat-Flash-Chat）

### 使用示例

#### 内容创作工作流程
```
1. 研究主题 → wechat-article-writer
2. 生成爆款标题 → wechat-title-optimizer
3. 优化内容 → wechat-content-optimizer
4. 创建封面图 → generate-cover-prompt
5. 发布文章 → wechat-publisher-yashu
```

#### 研究与笔记工作流程
```
1. 提取网页内容 → defuddle
2. 下载媒体 → video-downloader-skill
3. 保存到笔记 → obsidian-cli
4. 组织数据 → obsidian-bases
5. 转换格式 → obsidian-markdown
```

#### 开发与自动化工作流程
```
1. 自动化浏览器任务 → agent-browser
2. 调试 Web 应用 → chrome-devtools-skill
3. 创建新技能 → skill-creator-yashu
4. 优化性能 → skill-optimizer-yashu
```

## 🏗️ 架构设计

### 核心基础设施

- **`.claude/`**: 配置和技能管理框架
- **技能开发工具**: 创建、测试和优化工具
- **Git 子模块**: 版本控制的技能依赖

### 技能结构

每个技能遵循标准化模式：

```
skill-name/
├── SKILL.md                 # 带有元数据的核心文档
├── scripts/                 # 可执行自动化脚本
├── references/              # 详细指南和文档
├── assets/                  # 模板、图片、静态文件
└── evals/                   # 测试和评估数据
```

## 🔧 开发与定制

### 添加新技能

1. **使用内置技能创建器**:
   ```bash
   cd .claude/skills/skill-creator
   python -m scripts.create_skill "my-new-skill"
   ```

2. **遵循引导工作流程**进行文档编写和测试
3. **添加综合测试用例**确保可靠性
4. **优化描述**以提高触发准确性

### 技能质量标准

- **渐进式披露**: 有组织的加载（元数据 → 文档 → 资源）
- **客观测试**: 可量化的断言和基准
- **性能监控**: 令牌使用和执行时间跟踪
- **用户体验**: 清晰的文档和示例

## 📈 性能与优化

### 内置评估系统

- **并行测试**: 与基准比较技能
- **量化指标**: 通过率、性能基准
- **可视化分析**: 交互式比较工具
- **描述优化**: AI 驱动的触发改进

### 关键性能指标

- **触发准确性**: 技能调用精度
- **执行速度**: 响应时间优化
- **令牌效率**: 资源使用最小化
- **成功率**: 任务完成可靠性

## 🤝 贡献指南

### 向集合添加技能

1. Fork 仓库
2. 使用技能创建器工作流程创建您的技能
3. 包含综合测试用例和文档
4. 针对性能和用户体验进行优化
5. 提交包含详细描述的拉取请求

### 质量指南

- 遵循渐进式披露原则
- 包含客观评估标准
- 维护清晰简洁的文档
- 确保跨平台兼容性
- 提供实用使用示例

## 📄 许可证

此个人技能集合采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

**为效率而生，为生产力而优化** 🚀

有关详细的开发指导和操作说明，请参阅 [CLAUDE.md](CLAUDE.md)。
