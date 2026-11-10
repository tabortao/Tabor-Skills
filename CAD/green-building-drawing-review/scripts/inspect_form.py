#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析审图记录单参考模板的表格结构，推断意见行/小计行/签署行与网格列坐标。

任何新专业、新模板都必须先跑本脚本，禁止硬编码行号。

用法：
  python inspect_form.py "<20250603 审图记录单-施工图-绿建提给排水.docx>" --out "<tmp>/layout_pw.json"
"""
import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DEFAULT_COLS = {
    "drawing_no": 1, "opinion": 3,
    "mandatory": 7, "regulation": 8, "drawing": 9,
    "handling": 10, "verification": 11,
}
COL_HINTS = {
    "drawing_no": ["图号", "图纸编号"],
    "opinion": ["校审意见", "审查意见", "意见"],
    "mandatory": ["强条", "强制性"],
    "regulation": ["法规", "规范"],
    "drawing": ["图面", "错漏"],
    "handling": ["处理"],
    "verification": ["验证"],
}


def para_text(p):
    parts = []
    for node in p.iter():
        if node.tag == W + "t":
            parts.append(node.text or "")
        elif node.tag in (W + "tab", W + "br", W + "cr"):
            parts.append(" ")
    return "".join(parts).strip()


def read_tables(docx: Path):
    with zipfile.ZipFile(docx) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    tables = []
    if body is None:
        return tables
    for tbl in body.iter(W + "tbl"):
        rows = []
        maxcol = 0
        for tr in tbl.findall(W + "tr"):
            col = 1
            cells = []
            for tc in tr.findall(W + "tc"):
                tcpr = tc.find(W + "tcPr")
                span, vmerge = 1, None
                if tcpr is not None:
                    gs = tcpr.find(W + "gridSpan")
                    if gs is not None:
                        span = int(gs.get(W + "val", "1") or 1)
                    vm = tcpr.find(W + "vMerge")
                    if vm is not None:
                        vmerge = vm.get(W + "val", "continue")
                txt = " ".join(para_text(p) for p in tc.findall(W + "p")).strip()
                cells.append({"col": col, "span": span, "text": txt, "vmerge": vmerge})
                col += span
            maxcol = max(maxcol, col - 1)
            rows.append({"row": len(rows) + 1, "cells": cells})
        tables.append({"grid_cols": maxcol, "rows": rows})
    return tables


def cell_at(row, col):
    for c in row["cells"]:
        if c["col"] <= col < c["col"] + c["span"]:
            return c["text"]
    return ""


def row_text(row):
    return " ".join(c["text"] for c in row["cells"])


def infer_layout(docx: Path) -> dict:
    """解析审图记录单表格，返回行号推断与网格列坐标（供 inspect/diff/verify 复用）。"""
    tpl = Path(docx).resolve()
    tables = read_tables(tpl)
    if not tables:
        raise ValueError(f"未找到表格：{tpl}")
    # 取「小计」所在且行数最多的表
    cand = [t for t in tables if any("小计" in row_text(r) for r in t["rows"])]
    table = max(cand or tables, key=lambda t: len(t["rows"]))
    rows = table["rows"]

    subtotal_rows = [r["row"] for r in rows if "小计" in row_text(r)]
    if not subtotal_rows:
        print("[WARN] 未找到「小计」行，请人工核对 layout", file=sys.stderr)
        subtotal_row = len(rows) - 1
    else:
        subtotal_row = subtotal_rows[-1]
    sign_row = min(subtotal_row + 1, len(rows))

    header_rows = [r["row"] for r in rows[: subtotal_row - 1]
                   if ("校审意见" in row_text(r) or "审查意见" in row_text(r)
                       or "校 审 意 见" in row_text(r)
                       or ("图号" in row_text(r) and "序号" in row_text(r)))]
    header_row = header_rows[-1] if header_rows else 6
    # 分类子表头行（强条/法规/图面）之后才是第一条意见行
    subheader_rows = [r["row"] for r in rows[: subtotal_row - 1]
                      if all(k in row_text(r) for k in ("强条", "法规", "图面"))]
    subheader_row = subheader_rows[-1] if subheader_rows else None
    opinion_first = (subheader_row or header_row) + 1
    opinion_last = subtotal_row - 1

    # 从表头行 / 分类子表头行反查列坐标，反查不到则用通用坐标
    cols = dict(DEFAULT_COLS)
    probe_ids = ([header_row] if header_rows else []) + ([subheader_row] if subheader_row else [])
    for hrow in [r for r in rows if r["row"] in probe_ids]:
        for key, hints in COL_HINTS.items():
            for c in hrow["cells"]:
                if any(h in c["text"] for h in hints):
                    cols[key] = c["col"]
                    break

    layout = {
        "template": str(tpl),
        "row_count": len(rows),
        "grid_cols": table["grid_cols"],
        "header_row": header_row,
        "subheader_row": subheader_row,
        "opinion_first_row": opinion_first,
        "opinion_last_row": opinion_last,
        "opinion_capacity": max(0, opinion_last - opinion_first + 1),
        "subtotal_row": subtotal_row,
        "sign_row": sign_row,
        "columns": cols,
        "row_samples": [
            {"row": r["row"], "text": row_text(r)[:120]} for r in rows
        ],
    }
    return layout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    tpl = Path(args.template).resolve()
    try:
        layout = infer_layout(tpl)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"模板：{tpl.name}")
    print(f"行数 {layout['row_count']}  网格列 {layout['grid_cols']}  "
          f"意见行 {layout['opinion_first_row']}~{layout['opinion_last_row']}"
          f"（容量 {layout['opinion_capacity']}）  小计 {layout['subtotal_row']}  签署 {layout['sign_row']}")
    print("列坐标：" + "  ".join(f"{k}={v}" for k, v in layout["columns"].items()))
    print("\n前 8 行 / 小计 / 签署行预览：")
    for r in layout["row_samples"]:
        if r["row"] <= 8 or r["row"] in (layout["subtotal_row"], layout["sign_row"]):
            print(f"  R{r['row']:>2}: {r['text'][:100]}")
    print(f"\nlayout 输出：{out}")
    print("⚠ 必须人工核对上述行号与列坐标后再填表；不同专业行数不同。")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
