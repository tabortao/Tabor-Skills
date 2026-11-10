# 工具链与已知坑

## 环境

- **DWG 读取必须用装有 pywin32 的解释器**：本机为 `F:\Program Files\Python312\python.exe`（`python` 默认是 WorkBuddy 内置 3.13，无 pywin32）。`scripts/extract_dwg.py` 会自动探测，也可用 `--python` 显式指定。
- 其余脚本（docx / 表格解析）用系统默认 `python` 即可，只用标准库 `zipfile` + `xml.etree.ElementTree`。
- AutoCAD 需已启动并加载天正等插件；通过 `win32com.client.GetActiveObject('AutoCAD.Application')` 连接现有会话，不要另起实例。

## DWG 文字提取（`scripts/extract_dwg.py`）

要点（都是踩过的坑）：

1. **不能用 `for e in ModelSpace`**，天正环境下报「不支持枚举」。必须用 `ModelSpace.Count` + `Item(i)` 索引遍历；PaperSpace 同理。
2. 文字来源三处都要取：
   - `AcDbText` → `TextString`
   - `AcDbMText` → `TextString`（含格式码，必须清洗）
   - `AcDbBlockReference` → `HasAttributes` / `GetAttributes()` 的 `TextString`
   - 另外遍历 `doc.Blocks` 中每个块定义内的 TEXT/MTEXT（块内文字往往是说明正文，数量可达数千条）
3. `app.Documents.Open(path)` 在天正环境可能抛 `AttributeError: Open.Name`（返回的是方法对象），但**文档实际已打开并成为 ActiveDocument**。遇此错不要重试，直接 `app.ActiveDocument` 继续。
4. 设计总说明是**多栏排版**：导出后按 `y` 降序 / `x` 升序排序，再按 x 聚类分栏展开，配合关键词检索最高效。
5. **MTEXT 清洗**：正文常是每栏一条 2000+ 字符的 MTEXT，含 `\P`（换行）、`{\C7;}`、`\pi..;` 等格式码，Read 工具会截断看不到后半段：
   ```python
   s = s.replace('\\P', '\n').replace('\\~', ' ')
   s = re.sub(r'\\[A-Za-z][^;]{0,40};', '', s)
   s = re.sub(r'\{\\[^;]{0,40};', '', s).replace('{', '').replace('}', '')
   ```
6. **图号映射**：多张说明图平铺在同一模型空间时，按 x 区间映射到图号。例：电气 `<109000 → 0-EW-0001`、`<181000 → 0-EW-0002`、其余 → `0-EW-0003`；通过 `--drawing-map` 传 JSON 规则。
7. 大图纸（暖通 15045 实体）COM 遍历约 8 分钟，**用后台任务跑**，不要在前台等。
8. 图纸文字临时产物统一放 `<工作区>/.workbuddy/tmp/`，命名 `<专业>_图纸文字.txt`、`<专业>_图纸_展开.txt`。

## DOCX 读取（`scripts/extract_docx.py`）

- 用 `zipfile` 解 `word/document.xml` + `xml.etree.ElementTree`，按 `w:p`（段落）/ `w:tbl`（表格行）输出纯文本，不依赖 python-docx。
- **必须同时导出 `word/media/*` 图片**：暖通设计建议 V3.1 内含 3 张规范限值表截图（GB 55016 表 2.1.4 睡眠 33dB、GB 55038-2025 表 6.1.1 结构噪声），漏看会漏判噪声指标；电气参考模板把表 8.2.7-1 / 8.2.7-2 限值表截图贴在意见单元格内。
- 表格结构（行数、`gridSpan`、`vMerge`）用 `scripts/inspect_form.py` 单独解析，不要凭印象写死。

## 审图记录单生成（editor_sdk / `edsdk.py`）

**唯一稳妥做法：复制参考 docx → `doc_set_table_cells` 批量填表 → `save_file`**，格式 100% 保真，不要用 python-docx 重建表格。

- `edsdk.py` 路径：`F:\Program Files\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\workbuddy-local-office-edit\edsdk.py`
- 命令：`python edsdk.py list` / `schema <工具名>` / `call <工具名> --json-file args.json`
- **强制流程**：调用任一 `doc_*` 工具前先跑 `edsdk.py schema <工具名>`，不要凭摘要猜参数。
- 流程：`build_form.py`（复制模板 + 生成参数）→ `open_file`（返回 `file_id`）→ `doc_list_tables`（拿 `table_id`）→ **`build_form.py --no-copy --file-id ... --table-id ...` 重生成参数** → `doc_set_table_cells --json-file set_cells.json` → `save_file`。
- **`--no-copy` 是必须的**：成品一旦被 editor_sdk 打开就持有文件锁，重跑 `build_form.py` 若默认复制模板会报 `PermissionError: [WinError 32] 另一个程序正在使用此文件`。二次生成只重算参数，不要碰磁盘上的 docx。
- `file_id` 是一切编辑的入口；`open_file` 默认 fresh open，返回的 `file_id` 常是路径字符串本身。
- 需要**重新复制**一个已被编辑器占用的 docx 时，先 `close_file` 释放文件锁；重开后 `table_id` 会变，必须重新 `doc_list_tables`。
- 保存后不要主动 `close_file`（会关掉用户正在看的视图），除非为了释放锁。
- `doc_set_table_cells` **重写单元格会清空单元格内嵌图片**：电气模板的 2 张限值表截图会丢失（成品部件数 24 vs 模板 26）。按精简口径可只保留标准表号；若要保图需另行 `doc_insert_image` 或直接注入 OOXML，并在交付说明中提示。
- 要让用户看到成品，用 `present_files`；`open_file` 不会在预览面板打开文档。

## 表格填充参数（`scripts/build_form.py`）

`doc_set_table_cells` 的 args 结构（已验证）：

```json
{
  "file_id": "<成品 docx 绝对路径>",
  "table_id": "<doc_list_tables 返回的 id>",
  "cells": [
    {"row": 7, "col": 1, "text": "0-AW-0001"},
    {"row": 7, "col": 3, "text": "设计说明增加：……（第X.X.X条）"},
    {"row": 7, "col": 7, "text": "✓"}
  ]
}
```

`row` / `col` 均为 **1-based 网格坐标**（含合并单元格的网格列，不是可见单元格序号）。

## 其他

- 临时提取文本放 `.workbuddy/tmp/`，`.workbuddy` 目录是项目数据不是缓存，**不要删除**。
- 成品统一输出到项目根目录；`参考审图意见/` 下若存在同名文件，是旧项目已填处理/验证栏的归档件，**勿覆盖**。
