#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验生成的审图记录单：条数 / 分类勾选 / 小计 / 空列 / 旧项目残留 / 内嵌图片。

用法：
  python verify_form.py --form "<成品.docx>" --layout "<tmp>/layout_给排水.json" \
      --template "<参考模板.docx>" --old-project "平湖街道凤凰工业园" --strict
"""
import argparse
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_form import read_tables, cell_at, row_text  # noqa: E402


def media_count(p: Path):
    try:
        with zipfile.ZipFile(p) as z:
            return len([n for n in z.namelist() if n.startswith("word/media/") and not n.endswith("/")])
    except Exception:
        return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--form", required=True)
    ap.add_argument("--layout", required=True)
    ap.add_argument("--template", help="参考模板，用于对比内嵌图片数")
    ap.add_argument("--old-project", action="append", default=[], help="旧项目关键词，可多次指定")
    ap.add_argument("--strict", action="store_true", help="存在问题时返回非零退出码")
    args = ap.parse_args()

    form = Path(args.form).resolve()
    layout = json.loads(Path(args.layout).read_text(encoding="utf-8"))
    c = layout["columns"]
    tables = read_tables(form)
    if not tables:
        print("[ERROR] 成品中未找到表格", file=sys.stderr)
        sys.exit(2)
    table = max(tables, key=lambda t: len(t["rows"]))
    rows = {r["row"]: r for r in table["rows"]}
    first, last = layout["opinion_first_row"], layout["opinion_last_row"]
    sr, gr = layout["subtotal_row"], layout["sign_row"]

    problems = []
    notes = []
    actual = {"强条": 0, "法规": 0, "图面": 0}
    count = 0
    for r in range(first, last + 1):
        if r not in rows:
            continue
        text = cell_at(rows[r], c["opinion"])
        if not text.strip():
            continue
        count += 1
        marks = {"强条": cell_at(rows[r], c["mandatory"]),
                 "法规": cell_at(rows[r], c["regulation"]),
                 "图面": cell_at(rows[r], c["drawing"])}
        checked = [k for k, v in marks.items() if v.strip()]
        if len(checked) != 1:
            problems.append(f"R{r} 分类勾选 {len(checked)} 个（应为 1）：{checked}")
        else:
            actual[checked[0]] += 1
        if "（第" not in text and "(第" not in text:
            # 设计依据、标准版本更新类意见本来就不写条文号，只提示不阻断
            notes.append(f"R{r} 未见条文号（设计依据/标准版本类可不写）：{text[:40]}…")
        for label, col in (("处理", c["handling"]), ("验证", c["verification"])):
            v = cell_at(rows[r], col).strip()
            if v:
                problems.append(f"R{r} {label}列应为空，实为「{v}」")

    if sr in rows:
        for label, key in (("强条", "mandatory"), ("法规", "regulation"), ("图面", "drawing")):
            v = cell_at(rows[sr], c[key]).strip()
            if v != str(actual[label]):
                problems.append(f"小计 {label} = {v}，实际应为 {actual[label]}")

    full_text = "\n".join(row_text(r) for r in table["rows"])
    for kw in args.old_project:
        if kw and kw in full_text:
            problems.append(f"仍残留旧项目信息「{kw}」")
    head_project = cell_at(rows[1], 3) if 1 in rows else ""
    head_no = cell_at(rows[1], 7) if 1 in rows else ""

    if args.template:
        a, b = media_count(form), media_count(Path(args.template))
        if b >= 0 and a < b:
            notes.append(f"内嵌图片 {a} 张，模板 {b} 张：doc_set_table_cells 会清空单元格内嵌图片"
                         "（属已知行为）。按精简口径只留标准表号即可；若要保图需另行插图并在交付说明中提示。")

    print(f"成品：{form.name}")
    print(f"项目名：{head_project}    设计号：{head_no}")
    print(f"意见条数：{count}    实际分类：强条 {actual['强条']} / 法规 {actual['法规']} / 图面 {actual['图面']}")
    print(f"小计行：强条 {cell_at(rows[sr], c['mandatory']) if sr in rows else '?'} / "
          f"法规 {cell_at(rows[sr], c['regulation']) if sr in rows else '?'} / "
          f"图面 {cell_at(rows[sr], c['drawing']) if sr in rows else '?'}")
    print(f"签署行：{row_text(rows[gr])[:80] if gr in rows else '?'}")
    print(f"内嵌图片：{media_count(form)} 张")
    if notes:
        print("\n提示：")
        for n in notes:
            print("  ! " + n)
    if problems:
        print(f"\n发现 {len(problems)} 个问题：")
        for p in problems:
            print("  ✗ " + p)
    else:
        print("\n✓ 校验通过")
    if problems and args.strict:
        sys.exit(1)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
