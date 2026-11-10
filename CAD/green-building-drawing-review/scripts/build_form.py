#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复制参考模板 → 生成 editor_sdk `doc_set_table_cells` 的 args JSON。

用法：
  python build_form.py --template "<参考模板.docx>" --layout "<tmp>/layout_给排水.json" \
      --opinions "<tmp>/opinions_给排水.json" --out "<项目根>/20261109 审图记录单-施工图-绿建提给排水.docx" \
      --args-out "<tmp>/set_pw_cells.json" --file-id "<file_id>" --table-id "<table_id>"

opinions.json 格式见 assets/opinions.example.json。
脚本只生成参数文件；实际填表/保存仍走 edsdk.py（见 references/toolchain.md）。
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

CATS = {"强条": "mandatory", "法规": "regulation", "图面": "drawing"}


def load_opinions(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {}, data
    ops = data.get("opinions", [])
    meta = {k: data.get(k, "") for k in ("project", "design_no", "reviewer", "date")}
    return meta, ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--layout", required=True, help="inspect_form.py 输出的 layout JSON")
    ap.add_argument("--opinions", required=True)
    ap.add_argument("--out", required=True, help="成品 docx 路径（项目根目录）")
    ap.add_argument("--args-out", required=True, help="doc_set_table_cells 参数 JSON 输出路径")
    ap.add_argument("--summary-out", help="额外输出审查统计 JSON")
    ap.add_argument("--file-id", default="", help="open_file 返回的 file_id")
    ap.add_argument("--table-id", default="", help="doc_list_tables 返回的 table_id")
    ap.add_argument("--project", help="覆盖 opinions.json 中的项目名")
    ap.add_argument("--design-no", help="覆盖设计号")
    ap.add_argument("--reviewer", help="覆盖审核人")
    ap.add_argument("--date", help="覆盖日期，如 2026年11月9日")
    ap.add_argument("--sign-blank", action="store_true", help="签署行设计人/验证人列留空（建筑最终版口径）")
    ap.add_argument("--overwrite", action="store_true", help="允许覆盖已存在成品")
    ap.add_argument("--no-copy", action="store_true",
                    help="不重新复制模板，只重新生成参数文件；用于 open_file 后绑定 file_id/table_id（此时成品被编辑器占用，不能覆盖）")
    args = ap.parse_args()

    tpl = Path(args.template).resolve()
    out = Path(args.out).resolve()
    layout = json.loads(Path(args.layout).read_text(encoding="utf-8"))
    meta, ops = load_opinions(args.opinions)
    c = layout["columns"]
    first, last = layout["opinion_first_row"], layout["opinion_last_row"]
    capacity = layout["opinion_capacity"]

    if not tpl.is_file():
        print(f"[ERROR] 模板不存在：{tpl}", file=sys.stderr)
        sys.exit(2)
    if out.parent == tpl.parent:
        print("[ERROR] 成品不能输出到参考模板目录（会覆盖旧项目归档件）", file=sys.stderr)
        sys.exit(2)
    if len(ops) > capacity:
        print(f"[ERROR] 意见 {len(ops)} 条 > 模板容量 {capacity} 条（意见行 {first}~{last}）；请分页或精简", file=sys.stderr)
        sys.exit(2)
    if out.exists() and not (args.overwrite or args.no_copy):
        print(f"[ERROR] 成品已存在：{out}；确认覆盖请加 --overwrite，仅重生成参数请加 --no-copy", file=sys.stderr)
        sys.exit(2)
    if args.no_copy and not out.exists():
        print(f"[ERROR] --no-copy 要求成品已存在：{out}", file=sys.stderr)
        sys.exit(2)

    project = args.project or meta.get("project", "")
    design_no = args.design_no or meta.get("design_no", "")
    reviewer = args.reviewer or meta.get("reviewer", "")
    date = args.date or meta.get("date", "")

    cells = []

    def put(row, col, text):
        cells.append({"row": row, "col": col, "text": text})

    # 表头：项目名 / 设计号；清空旧项目子项名称
    put(1, 3, project)
    put(1, 7, design_no)
    put(2, 3, "")

    counts = {"强条": 0, "法规": 0, "图面": 0}
    warnings = []
    for i, o in enumerate(ops):
        r = first + i
        cat = str(o.get("category", "")).strip()
        text = str(o.get("text", "")).strip()
        no = str(o.get("drawing_no", "")).strip()
        if not text:
            warnings.append(f"第 {i + 1} 条意见文字为空")
        if cat in CATS:
            counts[cat] += 1
        else:
            warnings.append(f"第 {i + 1} 条分类「{cat}」无效，将不勾选任何分类")
        put(r, c["drawing_no"], no)
        put(r, c["opinion"], text)
        for label, key in CATS.items():
            put(r, c[key], "✓" if cat == label else "")
        put(r, c["handling"], "")
        put(r, c["verification"], "")

    # 未用到的意见行逐格清空（模板里有旧意见、旧「已修改 / ✓」）
    clear_cols = [c["drawing_no"], c["opinion"], c["mandatory"], c["regulation"],
                  c["drawing"], c["handling"], c["verification"]]
    for r in range(first + len(ops), last + 1):
        for col in clear_cols:
            put(r, col, "")

    # 小计：必须随条数重算
    sr = layout["subtotal_row"]
    put(sr, c["mandatory"], str(counts["强条"]))
    put(sr, c["regulation"], str(counts["法规"]))
    put(sr, c["drawing"], str(counts["图面"]))
    put(sr, c["handling"], "")
    put(sr, c["verification"], "")

    # 签署：只填审核人+日期，设计人/验证人留待回复
    gr = layout["sign_row"]
    put(gr, 2, f"{reviewer}            {date}".rstrip())
    blank_sign = "" if args.sign_blank else "            年 月  日"
    put(gr, 5, blank_sign)
    put(gr, 8, blank_sign)

    out.parent.mkdir(parents=True, exist_ok=True)
    if args.no_copy:
        print("复用已打开的成品（未重新复制模板）")
    else:
        shutil.copy2(tpl, out)
    args_doc = {"file_id": args.file_id, "table_id": args.table_id, "cells": cells}
    ao = Path(args.args_out).resolve()
    ao.parent.mkdir(parents=True, exist_ok=True)
    ao.write_text(json.dumps(args_doc, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "project": project, "design_no": design_no, "reviewer": reviewer, "date": date,
        "opinion_count": len(ops), "subtotal": counts,
        "opinion_rows": f"{first}~{first + len(ops) - 1}" if ops else "-",
        "template": str(tpl), "output": str(out), "args": str(ao),
        "warnings": warnings,
    }
    if args.summary_out:
        so = Path(args.summary_out).resolve()
        so.parent.mkdir(parents=True, exist_ok=True)
        so.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"模板 → 成品：{out}")
    print(f"意见 {len(ops)} 条（容量 {capacity}）  小计 强条 {counts['强条']} / 法规 {counts['法规']} / 图面 {counts['图面']}")
    print(f"单元格操作数：{len(cells)}  参数文件：{ao}")
    if not args.file_id or not args.table_id:
        print("⚠ 尚未绑定 file_id / table_id：请先 open_file + doc_list_tables，再用 --file-id / --table-id 重跑生成参数文件")
    for w in warnings:
        print("⚠ " + w)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
