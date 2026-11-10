# -*- coding: utf-8 -*-
"""把 extract_docx.py 的 content.json 转成「块」清单 blocks.json，供 draw_cad.py 流式排版。

块的两种形态：
  {"k":"para", "s": "...", "role":"body|head", "n": 合并段数}
  {"k":"trow", "cells":[...], "w":[列宽...], "head":true/false, "span":false}

排版三条铁律（都是踩过坑换来的）：
1) **连续段落合并成一个 MTEXT**：中间没有表格/标题打断的正文段落，用 MTEXT 换行码 \\P
   拼成一块，段首加两个空格缩进。用户双击一次就能改一整段，不必逐行改。
2) **标题单独成块**：标题要单独变色（GB-HEAD）+ 画下划线，且标题本身是视觉分隔，
   不与正文合并。
3) **超长 ASCII 串按列宽硬断**：AutoCAD 的 MTEXT 不会在长数字/英文串内部折行，
   300 字符放进 30mm 宽的格子仍只占 1 行横向溢出。所以生成阶段就要插 \\P。

用法：
    python make_layout.py content.json blocks.json
    python make_layout.py content.json blocks.json --cols 3 --height 3.5 \
        --x0 30 --x1 740 --y-top 566 --y-bot 18 --step 861
"""
import argparse
import json
import re
import unicodedata

SEP = "\\P"          # MTEXT 段落换行码
PARA_INDENT = "  "   # 段首缩进：两个半角空格（3.5 号字下约 4mm，≈半个汉字宽）

# 一级标题白名单：这些短句不加「一、」「（一）」前缀但确实是标题，需要单独成块变色
L1_EXACT = {
    "项目概况", "设计依据", "安全耐久", "健康舒适", "生活便利", "资源节约",
    "环境宜居", "提高与创新", "控制项", "评分项（自选）", "得分项（自选）",
    "建筑专业", "结构专业", "给排水专业", "暖通专业", "电气专业", "景观专业",
    "规划专业", "全专业", "其他", "建筑节能施工图设计说明（居住建筑）",
    "建筑节能施工图设计说明（公共建筑）", "五、绿色建筑施工图设计说明",
    "（一）绿色建筑设计自评表", "（二）绿色建筑基本规定及《深圳经济特区绿色建筑条例》有关技术要求",
    "（三）绿色建筑设计技术措施", "（四）绿色建筑增量投资及效益分析",
    "综合效益分析（经济效益、环境效益、社会效益）", "装配式建筑施工图设计说明",
    "实施装配式建筑情况", "（二）装配式建筑设计", "（三）信息化应用",
    "（四）其他要求", "（五）附表：深圳市装配式建筑技术评分施工图索引表",
    "节能评定结果", "（三）建筑节能热工设计", "（四）采暖、通风和空调节能设计",
    "（五）电气节能", "（六）给水排水与燃气节能", "（七）可再生能源应用",
    "（八）材料送检要求", "（一）节能计算软件及版本", "（二）节能评定结果",
    "（六）分项计量要求", "（七）给排水节能", "（八）可再生能源应用",
    "（九）材料送检要求",
}


def clean(s):
    s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return re.sub(r" {2,}", " ", s).strip()


def mtext_escape(s):
    """MTEXT 格式码转义：反斜杠、花括号。"""
    return s.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


WORD_RE = re.compile(r"([A-Za-z0-9_./:%+\-]+)")


def char_w(c, h):
    """字宽估算：全角按 1 个字高，半角按 0.55 个字高（3.5 号字 = 3.5 / 1.925mm）。"""
    return h if unicodedata.east_asian_width(c) in ("W", "F", "A") else h * 0.55


def wrap_cell(s, width, h):
    out = []
    for tok in WORD_RE.split(clean(s)):
        if not tok:
            continue
        if WORD_RE.fullmatch(tok) and sum(char_w(c, h) for c in tok) > width - 1.0:
            cur, w, parts = "", 0.0, []
            for ch in tok:
                c = char_w(ch, h)
                if w + c > width - 1.0 and cur:
                    parts.append(cur)
                    cur, w = "", 0.0
                cur += ch
                w += c
            if cur:
                parts.append(cur)
            out.append("\x00".join(parts))
        else:
            out.append(tok)
    return mtext_escape("".join(out)).replace("\x00", SEP)


def is_heading(s):
    if s in L1_EXACT:
        return True
    if len(s) <= 32 and (s.startswith("（") or s.startswith("(")) and any(
            c in s[:4] for c in "一二三四五六七八九十"):
        return True
    if len(s) <= 30 and re.match(r"^表\d+ ", s):
        return True
    return False


def col_widths(rows, ncols, total, min_col, h):
    """按内容长度比例分列宽：每列不小于 min_col，总和精确等于 total。"""
    w = []
    for j in range(ncols):
        m = max(min(sum(char_w(c, h) for c in (r[j] if j < len(r) else "")), 130.0)
                for r in rows)
        w.append(max(m, min_col))
    s = sum(w)
    out = [total * v / s for v in w]
    for _ in range(4):
        deficit = sum(max(0.0, min_col - v) for v in out)
        if deficit <= 0:
            break
        over = [v for v in out if v > min_col]
        scale = (sum(over) - deficit) / sum(over)
        out = [min_col if v <= min_col else v * scale for v in out]
    k = total / sum(out)
    out = [v * k for v in out]
    out[-1] += total - sum(out)
    return [round(v, 3) for v in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("blocks")
    ap.add_argument("--height", type=float, default=3.5, help="字高（天正 3.5）")
    ap.add_argument("--cols", type=int, default=3, help="每页栏数")
    ap.add_argument("--x0", type=float, default=30.0)
    ap.add_argument("--x1", type=float, default=740.0)
    ap.add_argument("--gut", type=float, default=8.0, help="栏间距")
    ap.add_argument("--y-top", type=float, default=566.0)
    ap.add_argument("--y-bot", type=float, default=18.0)
    ap.add_argument("--step", type=float, default=861.0, help="页间距（A1 841 + 20）")
    ap.add_argument("--ls-factor", type=float, default=0.96,
                    help="MTEXT 精确行距系数：0.96 x 5.83 = 5.6mm")
    ap.add_argument("--span", action="store_true",
                    help="宽表跨整幅排版（慎用：每个宽表会让一整页留白，页数翻倍）")
    ap.add_argument("--span-min-cols", type=int, default=9)
    ap.add_argument("--span-min-col", type=float, default=11.0)
    a = ap.parse_args()

    H = a.height
    X0, X1, GUT, NCOL = a.x0, a.x1, a.gut, a.cols
    CW = (X1 - X0 - GUT * (NCOL - 1)) / float(NCOL)
    TW = CW * NCOL + GUT * (NCOL - 1)

    items = json.load(open(a.content, encoding="utf-8"))
    blocks = []
    stats = {"paragraphs": 0, "headings": 0, "tables": 0, "rows": 0, "cells": 0,
             "span_tables": 0, "merged_blocks": 0, "merged_max": 0}
    buf = []

    def flush():
        nonlocal buf
        if not buf:
            return
        blocks.append({"k": "para",
                       "s": SEP.join(PARA_INDENT + s for s in buf),
                       "role": "body", "n": len(buf)})
        stats["merged_blocks"] += 1
        stats["merged_max"] = max(stats["merged_max"], len(buf))
        buf = []

    for it in items:
        if it["t"] == "p":
            s = clean(it["v"])
            if not s:
                continue
            if is_heading(s):
                flush()
                blocks.append({"k": "para", "s": mtext_escape(s),
                               "role": "head", "n": 1})
                stats["headings"] += 1
            else:
                buf.append(wrap_cell(it["v"], CW - 2.0, H))
            stats["paragraphs"] += 1
        else:
            flush()
            rows = it["rows"]
            while rows and all(not clean(c) for c in rows[-1]):
                rows = rows[:-1]
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            narrow = col_widths(rows, ncols, CW, 10.0, H)
            span = a.span and ((ncols >= a.span_min_cols)
                               or (min(narrow) < a.span_min_col))
            total = TW if span else CW
            widths = col_widths(rows, ncols, total, 12.0 if span else 10.0, H)
            for ri, row in enumerate(rows):
                cells = [wrap_cell(row[j] if j < len(row) else "",
                                   max(widths[j] - 2.0, 6.0), H)
                         for j in range(ncols)]
                blocks.append({"k": "trow", "cells": cells, "w": widths,
                               "head": ri == 0, "span": span})
                stats["rows"] += 1
                stats["cells"] += sum(1 for c in cells if c)
            stats["tables"] += 1
            stats["span_tables"] += 1 if span else 0
    flush()

    out = {"h": H, "x0": X0, "x1": X1, "gut": GUT, "cw": CW, "tw": TW,
           "y_top": a.y_top, "y_bot": a.y_bot, "step": a.step, "ncol": NCOL,
           "ls_factor": a.ls_factor, "blocks": blocks}
    json.dump(out, open(a.blocks, "w", encoding="utf-8"), ensure_ascii=False)

    n_para = sum(1 for b in blocks if b["k"] == "para")
    print("blocks =", len(blocks), "| para blocks =", n_para, "| stats =", stats)
    print("col width = %.2f mm, full width = %.2f mm" % (CW, TW))
    print("saved", a.blocks)


if __name__ == "__main__":
    main()
