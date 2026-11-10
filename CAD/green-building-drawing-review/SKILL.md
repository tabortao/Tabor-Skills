---
name: green-building-drawing-review
description: 绿色建筑施工图内审（绿建审查意见 / 审图记录单 / 提资意见）自动生成。本技能用于当用户提供项目 CAD 图纸目录、绿建设计建议目录（各专业《XX绿色建筑设计建议 V3.x》），要求为建筑、给排水、暖通、电气等专业出具绿建施工图审查意见，或要求核对图纸对绿建条文的落实情况、填写《审图记录单-施工图-绿建提XX.docx》时。覆盖资料扫描、DWG/DOCX 文字提取、逐条判定、按参考模板 100% 保真填表、成品校验与交付。触发词：绿建施工图审查、施工图内审、审图记录单、绿建提建筑/给排水/暖通/电气、提资意见、落实情况、设计建议 V3.1。
agent_created: true
---

# 绿色建筑施工图内审

## 用途与输出

把「项目 CAD 图纸目录 + 项目设计建议目录」变成各专业可直接发设计院的《审图记录单-施工图-绿建提XX.docx》。判定由模型按口径逐条完成，脚本负责目录扫描、文字提取、模板解析、批量填表与校验。

**输出**：每个 `ready` 专业一份 docx，位于项目根目录，命名 `<YYYYMMDD> 审图记录单-施工图-绿建提<专业>.docx`。

## 输入契约

必需：`--cad-dir`（项目 CAD 图纸目录）、`--advice-dir`（项目设计建议目录）。
可选：`--template-dir`（参考模板目录，默认工作区 `参考审图意见/`）、指定专业列表、项目名、设计号、审核人、日期。

**自动推断，不要反复追问用户**：

- 项目名 = CAD 目录父文件夹名去掉「项目绿建审查」等后缀。
- 设计号 = 从建议书 / 图纸文本 / 模板表头用正则 `S\d{2}-[A-Z]{2}\d{4}(-\d+)?` 提取。
- 审核人 = 参考模板签署行「审核 人 XXX」。
- 日期与 `YYYYMMDD` 前缀 = 用 `date` 命令取当天，**禁止手算或硬编码**。
- 仅当设计号、审核人确实无法推断时，一次性问齐（用 AskUserQuestion），不要中断流程多次询问。

## 硬性口径（动手前先读 `references/review-rules.md`）

1. 权威顺序：用户审核后的「内审意见最终版」> 本项目设计建议 V3.x 原文 > 本项目图纸 > 参考模板（**模板里的规范版本、指标数值、旧项目信息一律不可信**）。
2. **5 类意见永久不提给各专业**（可循环材料＞10%、全装修交付、装饰性构件≤2%、集中绿地 GB 55038 强条、楼梯间采光/自行车位/绿化率 105%），由用户自行出专项报告；内部台账仍如实写「需补充修改」。
3. 一条意见只对应一个条款，照抄建议书原文用「设计说明增加：……」+ 条文号；**不追加计算书、使用部位、甲方决策、厂家报告、规范体系核查**等衍生要求。例外：设计依据/标准版本类不写条文号；同一条文号下多项指标可合并为「1、2、」；提缺档要写项目事实依据（如「因项目有幼儿园」）。
4. 图纸已有等效表述即「已落实」，不提；只提缺档 / 数值不符 / 标准版本旧 / 完全缺失。复合条款拆多条。
5. 增删意见后**必须重算小计**、每行恰好勾一个分类；处理、验证列留空。
6. 跨专业去重按归口，不按「谁先写」：电梯节能归建筑；CO 监测暖通改说明 / 电气补图纸；光伏建筑算比例 / 电气出图；**海绵城市类条文（8.2.2 年径流总量控制率等）归海绵专项，不提给排水**；**设备能效（7.2.7.3）按设备找证据——水泵 GB 19762、风机 GB 19761、变压器 GB 20052，三专业图纸都有即全部不提，缺哪个专业才补哪个专业**。禁止按条文号在多个专业机械重复出条。交付时提示用户可择一。

分类惯例与项目级技术修正见 `references/review-rules.md` §4/§6；基准条数与措辞样板见 `references/case-zhenxi.md`；模板结构见 `references/form-templates.md`；工具与已知坑见 `references/toolchain.md`。

下文把 skill 目录记为 `$SKILL_DIR`（`~/.workbuddy/skills/green-building-drawing-review`），临时产物统一放 `<工作区>/.workbuddy/tmp/`。

## 工作流

### Step 1 · 建立输入映射

```bash
python "$SKILL_DIR/scripts/scan_inputs.py" \
  --cad-dir "<项目>/CAD" --advice-dir "<项目>/01 绿建设计建议" \
  --template-dir "<工作区>/参考审图意见" --out "<工作区>/.workbuddy/tmp/inputs.json"
```

只审 `status: ready` 的专业；缺 CAD / 建议书 / 模板的专业在交付说明中列出，不硬凑。**同一专业出现多个模板候选时人工确认**：模板目录里带成品日期前缀的同名文件是旧项目已填处理/验证栏的归档件，绝不可用、绝不可覆盖。

### Step 2 · 提取资料（各专业可并行）

```bash
# 设计建议 + 参考模板：文本 + word/media 图片（图片必看，常含规范限值表截图）
python "$SKILL_DIR/scripts/extract_docx.py" "<建议书.docx>" --out "<tmp>/<专业>设计建议.txt"
python "$SKILL_DIR/scripts/extract_docx.py" "<参考模板.docx>" --out "<tmp>/<专业>_参考模板.txt"

# CAD 文字：脚本自动切到带 pywin32 的解释器；大图纸放后台跑
python "$SKILL_DIR/scripts/extract_dwg.py" --file "<项目>/CAD/<专业>.dwg" \
  --out "<tmp>/<专业>图纸文字.txt" --columns
```

要点：AutoCAD 需已启动（含天正插件）；多栏说明用 `--columns` 展开；多张说明图平铺时用 `--drawing-map` 传 x 区间→图号规则；长 MTEXT 已被清洗 `\P` / 格式码。详见 `references/toolchain.md`。

### Step 3 · 逐专业判定（**模型完成，不可交给脚本**）

按 `references/review-rules.md` §1 的算法，对每个专业产出两份文件：

- `opinions_<专业>.json`：格式见 `assets/opinions.example.json`，字段 `drawing_no` / `text` / `category`（强条 / 法规 / 图面）。
- `review_log_<专业>.md`：逐条记录「模板意见 → 保留/删除 + 图纸证据」「建议书新增项 + 证据」「排除项」「跨专业去重」，供用户复核。

判定纪律：逐条给证据，不凭印象；图号用本项目图纸目录真实编号；无法定位写 `——`；建议书原文错字只做最小修正；**不要照抄模板旧数值**。

### Step 4 · 解析模板结构（每个专业一次）

```bash
python "$SKILL_DIR/scripts/inspect_form.py" "<参考模板.docx>" --out "<tmp>/layout_<专业>.json"
```

**任何新专业、新模板都必须先解析，禁止硬编码行号**（建筑 36 行、给排水 18 行、暖通/电气 23 行）。核对输出的意见行区间、容量、小计/签署行、列坐标。意见条数超过容量时分页或精简。

### Step 5 · 生成并填表（每个专业）

设 `$EDSDK` 为 `workbuddy-local-office-edit` skill 目录下的 `edsdk.py`。调用任何 `doc_*` 工具前先跑 `python "$EDSDK" schema <工具名>`。

```bash
# 1) 复制模板 + 生成参数（此时不绑定 id）
python "$SKILL_DIR/scripts/build_form.py" --template "<参考模板.docx>" \
  --layout "<tmp>/layout_<专业>.json" --opinions "<tmp>/opinions_<专业>.json" \
  --out "<项目根>/<YYYYMMDD> 审图记录单-施工图-绿建提<专业>.docx" \
  --args-out "<tmp>/set_<专业>_cells.json" --summary-out "<tmp>/summary_<专业>.json"

# 2) 打开并取 id
python "$EDSDK" call open_file file_path="<成品绝对路径>"          # file_id 常为路径本身
python "$EDSDK" call doc_list_tables file_id="<file_id>"           # 取 table_id（8 字符）

# 3) 二次生成参数：务必 --no-copy，否则文件被编辑器占用会报 WinError 32
python "$SKILL_DIR/scripts/build_form.py" --template "<参考模板.docx>" \
  --layout "<tmp>/layout_<专业>.json" --opinions "<tmp>/opinions_<专业>.json" \
  --out "<成品绝对路径>" --args-out "<tmp>/set_<专业>_cells.json" \
  --file-id "<file_id>" --table-id "<table_id>" --no-copy

# 4) 填表 → 保存
python "$EDSDK" call doc_set_table_cells --json-file "<tmp>/set_<专业>_cells.json"
python "$EDSDK" call save_file file_id="<file_id>"
```

**收表（可选，非默认）**：用户会按版面手工删减空白意见行，但各专业留白不一致（建筑删光、给排水留 2 行、电气留 4 行、暖通未动），没有统一规律。**默认保留模板原行数**；仅在用户要求或版面过长时，在填表保存之后执行：

```bash
python "$SKILL_DIR/scripts/trim_rows.py" --layout "<tmp>/layout_<专业>.json" \
  --count <条数> --keep-blank 1 --out "<tmp>/trim_<专业>.json"
# 按输出的 delete_rows 从大到小逐行删：
python "$EDSDK" call doc_delete_table_row file_id="<file_id>" table_id="<table_id>" row=<行号>
```

删完行号会变：重新 `inspect_form.py` 成品生成 layout，再做 Step 6 校验。

若成品已存在且被编辑器占用：先 `close_file` 释放锁，重开后 `table_id` 会变，必须重新 `doc_list_tables`。保存后不要主动 `close_file`（会关掉用户视图），除非确实要释放资源。

### Step 6 · 校验与交付

```bash
python "$SKILL_DIR/scripts/verify_form.py" --form "<成品.docx>" \
  --layout "<tmp>/layout_<专业>.json" --template "<参考模板.docx>" \
  --old-project "<旧项目名>" --strict
```

校验条数、分类勾选、小计一致性、处理/验证列为空、旧项目信息残留。设计依据/标准版本类意见无条文号属正常，脚本只提示不判错。模板单元格内的限值表截图会被 `doc_set_table_cells` 清空（建筑 3 张、电气 2 张、给排水 2 张），交付时必须提示；用户最终版通常会保留或自行补图，需要自动补时用 `doc_set_table_cells` 的 `image` 字段。用 `present_files` 展示全部成品。

交付说明必须包含：各专业意见条数与「强条/法规/图面」小计、被删除的已落实项、5 类排除项由用户专项报告处理、跨专业重复项（可择一）、缺资料未审的专业、被清空的限值表截图。

### Step 7 · 经验回流（每个项目必做）

**这是技能持续成长的唯一入口，不要跳过。**

1. 用户返回审核后的最终版（如 `内审意见最终版/`）后，逐专业对比：

   ```bash
   python "$SKILL_DIR/scripts/diff_form.py" --ai "<AI 成品.docx>" --final "<最终版.docx>" \
     --out "<工作区>/.workbuddy/tmp/diff_<专业>.md"
   ```

   脚本自动识别两边不同的表格行数（最终版常删空白行），输出删除 / 新增 / 改写清单与小计差异。

2. 读 diff 报告，按 `references/lessons-learned.md` 文末模板追加一节：删除项及理由、新增项及分类、改写前后文与可复用规律、小计与分类是否被修正。
3. 把**已稳定、可复用**的规律回写到 `references/review-rules.md`；项目最终数据更新到 `references/case-<项目>.md`；推测项放「待确认」，不要写成规则。
4. 若发现 `verify_form.py` 误报 / 漏报，同步修脚本。
5. 在交付说明中告诉用户这次沉淀了哪几条新经验。

## 边界与故障

- **不生成 5 类专项报告内容；不填处理/验证列；不修改用户已审核的最终版；不覆盖参考模板目录内任何文件。**
- `PermissionError: WinError 32` → 用 `--no-copy` 重生成参数，或先 `close_file` 再重开并重新取 `table_id`。
- `AttributeError: Open.Name` → 文档实际已打开，脚本已自动改用 `ActiveDocument`，不要重试 `Documents.Open`。
- 意见超容量 → 分页或精简，不要挤掉模板行。
- 模板数值与建议书冲突 → 一律以本项目设计建议 V3.x 为准。
- 成品输出到项目根目录，临时提取文本放 `.workbuddy/tmp/`；`.workbuddy` 是项目数据，不要删除。

## 资源索引

| 文件 | 用途 |
|---|---|
| `scripts/scan_inputs.py` | 扫描三类目录，输出专业映射 `inputs.json` |
| `scripts/extract_docx.py` | docx → 文本 + `word/media` 图片 + 表格结构 JSON |
| `scripts/extract_dwg.py` | AutoCAD COM 提取 DWG 文字（TEXT/MTEXT/块属性/块定义），分栏、图号映射 |
| `scripts/inspect_form.py` | 解析参考模板行列/合并结构，推断意见行、小计行、列坐标 |
| `scripts/build_form.py` | 复制模板 + 生成 `doc_set_table_cells` 参数 JSON + 统计 |
| `scripts/verify_form.py` | 成品校验（条数、分类、小计、空列、旧信息、图片） |
| `scripts/diff_form.py` | 对比 AI 版与用户最终版，输出删除/新增/改写报告（经验回流） |
| `scripts/trim_rows.py` | 计算收表要删除的空白意见行（从大到小逐行删） |
| `assets/opinions.example.json` | `opinions_<专业>.json` 格式样例 |
| `references/review-rules.md` | 判定口径、5 类排除项、写作规范、分类、跨专业去重 |
| `references/lessons-learned.md` | 经验库（稳定口径 + 逐项目校准记录 + 追加模板） |
| `references/toolchain.md` | DWG/docx 提取、editor_sdk 命令、踩过的坑 |
| `references/form-templates.md` | 各专业行数、11 列网格坐标、图号与命名规则 |
| `references/case-zhenxi.md` | 臻玺宣府基准案例（4 专业条数、删减理由、最终版对比） |
