#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""计算「收表」时需要删除的空白意见行，贴近用户最终版的排版习惯。

用户最终版会把模板预留的空白意见行删掉（臻玺宣府建筑 36→29、给排水 18→17、电气 23→22），
只留 1~2 行余量。本脚本只计算行号并打印命令，实际删除在填表保存之后执行。

用法：
  python trim_rows.py --layout "<tmp>/layout_建筑.json" --count 21 --keep-blank 1 \
      --out "<tmp>/trim_建筑.json"
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", required=True)
    ap.add_argument("--count", type=int, required=True, help="实际意见条数")
    ap.add_argument("--keep-blank", type=int, default=1, help="保留的空白意见行数（默认 1）")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    layout = json.loads(Path(args.layout).read_text(encoding="utf-8"))
    first, last = layout["opinion_first_row"], layout["opinion_last_row"]
    capacity = layout["opinion_capacity"]
    if args.count > capacity:
        print(f"[ERROR] 意见 {args.count} 条 > 容量 {capacity} 条", file=sys.stderr)
        sys.exit(2)

    start = first + args.count + max(0, args.keep_blank)
    rows = list(range(last, start - 1, -1))  # 从大到小，避免删除时行号漂移

    data = {
        "delete_rows": rows,
        "count": args.count,
        "keep_blank": args.keep_blank,
        "opinion_rows": f"{first}~{first + args.count - 1}" if args.count else "-",
        "rows_after_trim": last - len(rows),
        "note": ("在 doc_set_table_cells + save_file 之后执行；按 delete_rows 顺序（从大到小）逐行删除；"
                 "删除后小计/签署行号上移，需重新 doc_list_tables 核对。"),
    }
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if not rows:
        print(f"无需收表：意见 {args.count} 条 + 余量 {args.keep_blank} 行已占满模板")
    else:
        print(f"意见 {args.count} 条，保留 {args.keep_blank} 行空行，删除 {len(rows)} 行：{rows}")
        print("执行命令（填表保存后，按顺序）：")
        for r in rows:
            print(f'python "$EDSDK" call doc_delete_table_row file_id="<file_id>" '
                  f'table_id="<table_id>" row={r}')
    print(f"结果文件：{out}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
