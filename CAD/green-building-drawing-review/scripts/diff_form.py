#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对比「AI 生成版」与「用户审核最终版」审图记录单，输出差异报告。

用于经验回流：每次用户返回审核后的最终版，先跑本脚本，再据此更新
references/lessons-learned.md 与 references/case-<项目>.md。

用法：
  python diff_form.py --ai "<项目根>/20261109 ...提给排水.docx" \
      --final "<项目>/内审意见最终版/20261109 ...提给排水.docx" \
      --layout "<tmp>/layout_给排水.json" --out "<tmp>/diff_给排水.md"
"""
import argparse
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_form import read_tables, cell_at, infer_layout  # noqa: E402

CAT_KEYS = (("强条", "mandatory"), ("法规", "regulation"), ("图面", "drawing"))


def pick_table(docx: Path):
    tables = read_tables(docx)
    if not tables:
        return None
    cand = [t for t in tables if any("小计" in " ".join(c["text"] for c in r["cells"]) for r in t["rows"])]
    return max(cand or tables, key=lambda t: len(t["rows"]))


def read_opinions(docx: Path, layout: dict):
    table = pick_table(docx)
    if table is None:
        raise SystemExit(f"[ERROR] 未找到表格：{docx}")
    rows = {r["row"]: r for r in table["rows"]}
    c = layout["columns"]
    first, last = layout["opinion_first_row"], layout["opinion_last_row"]
    items = []
    for r in range(first, last + 1):
        if r not in rows:
            continue
        text = cell_at(rows[r], c["opinion"]).strip()
        if not text:
            continue
        cat = ""
        for label, key in CAT_KEYS:
            if cell_at(rows[r], c[key]).strip():
                cat = label
                break
        items.append({
            "row": r,
            "no": cell_at(rows[r], c["drawing_no"]).strip(),
            "text": text,
            "cat": cat,
        })
    subtotal = {}
    sr = layout["subtotal_row"]
    if sr in rows:
        for label, key in CAT_KEYS:
            subtotal[label] = cell_at(rows[sr], c[key]).strip()
    return items, subtotal


def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def align(ai_items, final_items, threshold=0.45):
    """贪心对齐，容忍用户插行/删行造成的位移。"""
    pairs, used = [], set()
    for a in ai_items:
        best, best_i = 0.0, None
        for i, f in enumerate(final_items):
            if i in used:
                continue
            s = sim(a["text"], f["text"])
            if s > best:
                best, best_i = s, i
        if best_i is not None and best >= threshold:
            used.add(best_i)
            pairs.append((a, final_items[best_i], best))
        else:
            pairs.append((a, None, 0.0))
    added = [f for i, f in enumerate(final_items) if i not in used]
    return pairs, added


def brief(text, n=120):
    text = " ".join(text.split())
    return text if len(text) <= n else text[:n] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ai", required=True)
    ap.add_argument("--final", required=True)
    ap.add_argument("--layout", help="可选：AI 版 layout JSON；默认自动解析。用户最终版常删掉空白意见行，行号会变，两边必须各自推断")
    ap.add_argument("--out", required=True, help="差异报告 markdown 输出路径")
    ap.add_argument("--threshold", type=float, default=0.45, help="判定为同一条意见的相似度阈值")
    args = ap.parse_args()

    import json
    ai_layout = (json.loads(Path(args.layout).read_text(encoding="utf-8"))
                 if args.layout else infer_layout(Path(args.ai)))
    fi_layout = infer_layout(Path(args.final))
    ai_items, ai_sub = read_opinions(Path(args.ai), ai_layout)
    fi_items, fi_sub = read_opinions(Path(args.final), fi_layout)
    pairs, added = align(ai_items, fi_items, args.threshold)

    kept = [(a, f, s) for a, f, s in pairs if f and s >= 0.995]
    modified = [(a, f, s) for a, f, s in pairs if f and s < 0.995]
    deleted = [a for a, f, s in pairs if f is None]

    lines = [f"# 审图记录单差异报告", "",
             f"- AI 版：`{Path(args.ai).name}`，{len(ai_items)} 条",
             f"- 最终版：`{Path(args.final).name}`，{len(fi_items)} 条",
             f"- 结果：原样保留 {len(kept)} 条，改写 {len(modified)} 条，删除 {len(deleted)} 条，新增 {len(added)} 条",
             f"- 小计：AI {ai_sub} → 最终 {fi_sub}",
             f"- 表格：AI {ai_layout['row_count']} 行（意见行 {ai_layout['opinion_first_row']}~{ai_layout['opinion_last_row']}）"
             f" → 最终 {fi_layout['row_count']} 行（{fi_layout['opinion_first_row']}~{fi_layout['opinion_last_row']}）", ""]
    if fi_layout["row_count"] < ai_layout["row_count"]:
        lines += [f"> 用户删除了 {ai_layout['row_count'] - fi_layout['row_count']} 个空白意见行："
                  "最终交付版按实际条数收表，不保留模板预留空行。", ""]

    lines += ["## 一、删除的意见（AI 有、最终版无）", ""]
    for a in deleted:
        lines += [f"**AI R{a['row']} · {a['no']} · {a['cat']}**", "", f"> {brief(a['text'], 300)}", ""]
    if not deleted:
        lines.append("无。")

    lines += ["", "## 二、新增的意见（最终版有、AI 无）", ""]
    for f in added:
        lines += [f"**最终 R{f['row']} · {f['no']} · {f['cat']}**", "", f"> {brief(f['text'], 300)}", ""]
    if not added:
        lines.append("无。")

    lines += ["", "## 三、改写的意见（相似度 < 1）", ""]
    for a, f, s in modified:
        cat_change = f"（分类 {a['cat']} → {f['cat']}）" if a["cat"] != f["cat"] else ""
        no_change = f"（图号 {a['no']} → {f['no']}）" if a["no"] != f["no"] else ""
        lines += [f"### R{a['row']} → R{f['row']}  相似度 {s:.2f}{cat_change}{no_change}", "",
                  f"- 原：{brief(a['text'], 400)}",
                  f"- 改：{brief(f['text'], 400)}", ""]
    if not modified:
        lines.append("无。")

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"AI {len(ai_items)} 条 → 最终 {len(fi_items)} 条：保留 {len(kept)}，改写 {len(modified)}，删除 {len(deleted)}，新增 {len(added)}")
    print(f"小计：AI {ai_sub} → 最终 {fi_sub}")
    print(f"报告：{out}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
