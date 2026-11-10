---
name: green-spec-cad
display_name: 绿色专篇 CAD 版制作
display_name_en: Green Building Spec to CAD (A1 Sheet Set)
description: 把 Word 版《深圳市建设工程项目绿色专篇（民用建筑·设计阶段）》批量转成 AutoCAD 里的 A1 多页图纸（DWG）。当用户给出「绿色专篇 .docx + A1图框.dwg」并要求「做成 CAD 版 / 出图 / 排到图框里 / 生成 DWG 绿色专篇」，或要求修改已生成的绿色专篇图纸（改图签子项名称、增删页眉、补图号图名、换字体）时使用。脚本按 measure-then-place 流式三栏排版，连续段落合并成单个多行文本便于后期编辑，输出自带 0 越界 / 0 重叠 / 字高统一 3.5 的自检报告。
description_zh: 一键把 Word 绿色专篇排版进 A1 图框，生成可编辑的多页 CAD 图纸：MTEXT 连续段落合并、三栏流式排版、图签子项名称与图号图名自动填写、出图自检（越界/重叠/字高）。
description_en: Convert a Word green-building design specification into an editable multi-sheet A1 AutoCAD DWG: merged MTEXT paragraphs, 3-column flow layout, title-block numbering, and built-in QA checks.
category: design
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Glob
---

# 绿色专篇 CAD 版制作

## 这个 skill 解决什么

用户手里有一份 **Word 版绿色专篇**（几十张表、几万字）和一张 **A1 图框.dwg**，要把它排成能在
AutoCAD 里出图、又能被其他专业接着编辑的 **多页 DWG**。手工排版要几天，本 skill 全流程脚本化，
一次跑完约 1~2 分钟，并且每条验收指标都有脚本自检。

首例：`P26-07领亚项目` —— 833 段落 + 39 张表（约 4 万字）→ 5 张 A1、1061 个 MTEXT、
0 越界、0 重叠、字高全 3.5。

## 触发场景

- 「把这份绿色专篇 Word 做成 CAD 版 / 排进 A1 图框 / 生成 DWG」
- 「换一个项目的绿色专篇，照上次的样子再做一份」
- 「图签子项名称改成 xx」「页眉去掉」「图号从 AW-0020 开始」「字改成国标字体」
- 需要把专篇并入建筑专业图纸出图（此时子项名称要写「通用图」）

## 前置条件（先自检，别硬跑）

1. **AutoCAD 必须在运行**（AutoCAD 2022 + 天正 T30 环境已验证；ZWCAD 不行，用户明确只用 AutoCAD）。
   至少开着一个文档——关闭最后一个文档会让天正 COM 整体断连。
2. **需要一个带 pywin32 的 Python**。本机可用：
   `D:/Code/Python/multiCAD-mcp/.venv/Scripts/python.exe`
   换机器时先用 `python -c "import win32com.client"` 确认，不行就 `pip install pywin32`。
   （`extract_docx.py` / `make_layout.py` 只用标准库，任何 Python 3 都行。）
3. 图框是 **1:1 的 A1（841×594）dwg**，图签文字是模型空间里的 MTEXT（本 skill 靠替换这些文字填子项名称/专业）。

## 标准流程（四步 + 一步自检）

```bash
PY="D:/Code/Python/multiCAD-mcp/.venv/Scripts/python.exe"      # 带 pywin32 的解释器
SK="C:/Users/yaole/.workbuddy/skills/green-spec-cad/scripts"
PROJ="D:/WorkBuddySpace/绿色专篇/P26-07领亚项目"                 # 项目目录
mkdir -p "$PROJ/work"

# 1) Word -> 结构化 JSON（段落 + 表格，保持文档顺序，纯标准库）
$PY "$SK/extract_docx.py" "$PROJ/20261030 …绿色专篇…2026版.docx" "$PROJ/work/content.json"

# 2) JSON -> 排版块（连续段落合并、算列宽、长串硬断）
$PY "$SK/make_layout.py" "$PROJ/work/content.json" "$PROJ/work/blocks.json" \
    --cols 3 --height 3.5 --x0 30 --x1 740 --y-top 566 --y-bot 18 --step 861

# 3) 探图签格位（换了图框才需要；数字对不上就别往下走）
$PY "$SK/probe_frame.py" --frame "$PROJ/A1图框.dwg"

# 4) 画图（AutoCAD 里生成多页 A1）
$PY "$SK/draw_cad.py" \
    --frame "$PROJ/A1图框.dwg" --blocks "$PROJ/work/blocks.json" \
    --out  "$PROJ/项目名_绿色专篇(设计阶段)_CAD版.dwg" \
    --subitem 通用图 --no-prefix AW- --no-start 10 \
    --title "深圳市设计阶段绿色专篇"

# 5) 自检（必须「结论: 通过」才交付）
$PY "$SK/verify_dwg.py" --dwg "$PROJ/项目名_绿色专篇(设计阶段)_CAD版.dwg"
```

需要看效果时截图（会自己把 CAD 窗口还原并放大到指定范围）：

```bash
$PY "$SK/screenshot.py" "$PROJ/work/page1.png" --win 0,0,841,594
$PY "$SK/screenshot.py" "$PROJ/work/tb.png"    --win 744,6,838,216   # 只截图签
```

## 关键参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `--cols` | 3 | 每页栏数。A1 内容区 710mm 宽、3.5 号字，3 栏是「行宽约 40 汉字」的舒适值 |
| `--height` | 3.5 | 字高，天正 3.5 号字 |
| `--x0/--x1` | 30/740 | 内容区左右边界（右侧 740 之后是图签） |
| `--y-top/--y-bot` | 566/18 | 内容区上下边界 |
| `--step` | 861 | 页间距 = A1 宽 841 + 20，多页横向并排 |
| `--subitem` | 通用图 | 图签「子项名称」。**并入建筑专业图纸出图时写「通用图」**；独立出册才写「绿色建筑专篇」 |
| `--trade-from/--trade-to` | 海绵城市(HM) → 绿色建筑(LJ) | 图框原是海绵城市图纸时改专业名 |
| `--no-prefix/--no-start` | AW- / 10 | 图号，逐页递增（AW-0010、AW-0011…） |
| `--title` | 深圳市设计阶段绿色专篇 | 图名主体，自动加（一）（二）…；传 `""` 则只写图号 |
| `--name-cell` / `--no-cell` | 751,42,829,78 / 767,12,795.5,24 | 图签「图纸名称」「图号」的正文区，换图框必须重测 |
| `--header` | 关 | 每页顶部加「标题 + 第 N 页/共 M 页」和分隔线。**默认不加**，图名图号由图签承担 |

## 验收标准（用户已认可的口径）

1. 越界 MTEXT = **0**（按 bbox 判栏位，不要按插入点判）
2. 同栏纵向重叠 = **0**
3. 正文区字高 = **3.5**（图签另有 2.6/4.5 的小字与图名，属正常）
4. 每张图框图签都有 **图号 + 图名**
5. 用户要求「并入建筑专业出图」时：**子项名称 = 通用图，且每页不出现顶部大标题和页码**

## 排版设计（为什么长这样）

- **连续段落合并成一个 MTEXT**：中间没有表格/标题打断的正文段落用 `\P` 拼成一块，段首两个半角空格缩进。
  833 段 → 239 块，用户双击一次改一整段，而不是逐行点 800 多次。
- **遇表格或标题就断开**：标题要单独变色（GB-HEAD 蓝色 + 下划线），且本身是视觉分隔。
- **建一块量一块**：每建一个 MTEXT 就 `GetBoundingBox` 拿真实高度，放不下才换栏/换页。
  不靠字宽估算——SHX 字体估算误差能到 20%，估算必然穿栏。
- **合并块按段落二分切分**：一块放不下时二分找「放得下的段落前缀」留在本栏，其余续到下一栏，
  避免整块跳栏在栏底留 150~550mm 空白（本机实测会多出 1 页）。
- **字体用国标 SHX**：`GB-标准` = `gbenor.shx` + `gbcbig.shx`，AutoCAD 自带，对方电脑不缺字，
  比宋体窄约 10%，5 页而不是 6 页。

## 坑（详细版见 references/experience.md）

- `AddMText` 新建的 MTEXT **默认字高 350**（继承 TEXTSIZE），必须显式设 3.5 并读回校验，否则包围盒十几万毫米。
- 点参数必须是 `VARIANT(VT_ARRAY|VT_R8,[x,y,z])`；`CopyObjects` 的对象数组必须 `VARIANT(VT_ARRAY|VT_DISPATCH, objs)`。
- **不要用 COM `doc.Close()`**：天正包装的 AutoCAD 会整体断连，只能 `doc.SendCommand("_.CLOSE\n")`。
- **不要按索引批量删除模型空间实体**：删一个后面的索引全部前移，会删错对象（本 skill 的教训：
  按索引删页眉，把第 2 页图签的文字删了）。要删就「扫一条 → 删一条 → 重新扫」或重新生成。
- `AttachmentPoint=5`（正中）在 COM 里不可靠，文字整体右移半宽 → 建完按 bbox 实测居中。
- 宽表跨整幅（`--span`）慎开：16 个宽表会把 6 页撑到 17 页，因为每个宽表都让一整页留白。

## 交付话术

1. 报文件路径 + 页数 + 图号区间 + 图名。
2. 报自检数字：越界 0/1061、重叠 0、字高全 3.5、图框 N 个。
3. 提醒后续改内容的正道：**内容改动走 Word 改完重跑脚本**；只在 CAD 里改个别字句，双击 MTEXT 直接改即可。
4. 若本次有人工微调（图签格位、图名文案、图号起点），把实际值写进 `references/experience.md` 的
   「项目档案」一节，下次同院图框直接用。
