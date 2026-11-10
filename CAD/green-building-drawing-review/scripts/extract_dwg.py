#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 AutoCAD COM 提取 DWG 全部文字（TEXT / MTEXT / 块属性 / 块定义内文字）。

用法：
  "F:/Program Files/Python312/python.exe" extract_dwg.py \
      --file "<项目>/CAD/给排水设计说明.dwg" --out "<tmp>/给排水图纸文字.txt" --columns
  # 多张说明图平铺时按 x 区间映射图号：
  ... --drawing-map "<tmp>/drawing_map.json"

注意：
  - 必须连接已启动的 AutoCAD（含天正插件）会话，脚本用 GetActiveObject。
  - 默认 python 常缺 pywin32，脚本会自动改用本机装有 pywin32 的解释器重跑。
  - ModelSpace 必须用 Count + Item(i) 索引遍历，直接 for 会报「不支持枚举」。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---- 自动切换到带 pywin32 的解释器 -----------------------------------------
try:
    import win32com.client  # noqa: F401
except ImportError:
    if not os.environ.get("_GBDR_REEXEC"):
        candidates = [
            r"F:\Program Files\Python312\python.exe",
            r"C:\Python312\python.exe",
            r"C:\Python311\python.exe",
        ]
        for c in candidates:
            if Path(c).is_file():
                env = dict(os.environ, _GBDR_REEXEC="1")
                rc = subprocess.call([c, os.path.abspath(__file__)] + sys.argv[1:], env=env)
                sys.exit(rc)
        print("[ERROR] 未找到装有 pywin32 的 Python；请用 --python 指定解释器", file=sys.stderr)
        sys.exit(2)
    else:
        raise


def clean_mtext(s: str) -> str:
    s = s.replace("\\P", "\n").replace("\\~", " ")
    s = re.sub(r"\\[A-Za-z][^;]{0,40};", "", s)
    s = re.sub(r"\{\\[^;]{0,40};", "", s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"[ \t]+", " ", s)
    return s


def iter_items(container):
    try:
        n = int(container.Count)
    except Exception:
        return
    for i in range(n):
        try:
            yield container.Item(i)
        except Exception:
            continue


def xy(entity):
    try:
        p = entity.InsertionPoint
        return float(p[0]), float(p[1])
    except Exception:
        return 0.0, 0.0


def get_app():
    import win32com.client
    try:
        return win32com.client.GetActiveObject("AutoCAD.Application")
    except Exception:
        return win32com.client.Dispatch("AutoCAD.Application")


def open_or_active(app, path: Path):
    target = os.path.normcase(str(path))
    try:
        for d in iter_items(app.Documents):
            try:
                if os.path.normcase(os.path.abspath(d.FullName)) == os.path.normcase(os.path.abspath(target)):
                    print(f"复用已打开文档：{d.Name}")
                    return d
            except Exception:
                continue
    except Exception:
        pass
    try:
        d = app.Documents.Open(str(path))
        if hasattr(d, "FullName"):
            return d
    except Exception as e:
        # 天正环境常见：抛 AttributeError: Open.Name，但文档实际已打开
        print(f"[WARN] Documents.Open 异常（文档可能已打开）：{type(e).__name__}: {e}")
    try:
        d = app.ActiveDocument
        print(f"改用 ActiveDocument：{d.Name}")
        return d
    except Exception as e:
        print(f"[ERROR] 无法取得文档：{e}", file=sys.stderr)
        sys.exit(3)


def collect_text(doc, tag, include_blocks=True, include_paper=False):
    """返回 [(x, y, text), ...]"""
    out = []

    def handle(e, prefix):
        try:
            name = str(e.ObjectName)
        except Exception:
            name = ""
        x, y = xy(e)
        try:
            if name == "AcDbMText":
                for line in clean_mtext(str(e.TextString)).split("\n"):
                    if line.strip():
                        out.append((x, y, line.strip()))
                return
            if name == "AcDbText":
                t = str(e.TextString).strip()
                if t:
                    out.append((x, y, t))
                return
        except Exception:
            pass
        if name == "AcDbBlockReference":
            try:
                if e.HasAttributes:
                    for a in e.GetAttributes():
                        t = str(a.TextString).strip()
                        if t:
                            ax, ay = xy(a)
                            out.append((ax or x, ay or y, t))
            except Exception:
                pass

    ms = doc.ModelSpace
    total = int(ms.Count)
    print(f"[{tag}] ModelSpace 实体数：{total}")
    for i, e in enumerate(iter_items(ms)):
        handle(e, "MS")
        if (i + 1) % 2000 == 0:
            print(f"  ... {i + 1}/{total}")
    if include_paper:
        try:
            for e in iter_items(doc.PaperSpace):
                handle(e, "PS")
        except Exception:
            pass
    if include_blocks:
        nb = 0
        for b in iter_items(doc.Blocks):
            for e in iter_items(b):
                handle(e, "BLK")
                nb += 1
        print(f"[{tag}] 块定义内实体数：{nb}")
    print(f"[{tag}] 提取文字条目：{len(out)}")
    return out


def drawing_no(x, rules):
    for r in rules:
        if "max_x" not in r or x < float(r["max_x"]):
            return r.get("no", "")
    return rules[-1].get("no", "") if rules else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", action="append", required=True, help="DWG 路径，可多次指定")
    ap.add_argument("--out", required=True, help="输出 txt")
    ap.add_argument("--columns", action="store_true", help="额外输出按 x 分栏展开的文本")
    ap.add_argument("--column-tolerance", type=float, default=5000.0,
                    help="分栏时 x 归桶宽度（图纸单位），默认 5000")
    ap.add_argument("--drawing-map", help="图号映射规则 JSON 文件路径")
    ap.add_argument("--no-blocks", action="store_true", help="不读取块定义内文字（一般不要用）")
    ap.add_argument("--paper", action="store_true", help="同时读取 PaperSpace")
    args = ap.parse_args()

    rules = []
    if args.drawing_map:
        raw = json.loads(Path(args.drawing_map).read_text(encoding="utf-8"))
        rules = raw.get("rules", raw) if isinstance(raw, dict) else raw

    app = get_app()
    all_items = []
    for f in args.file:
        p = Path(f).resolve()
        if not p.is_file():
            print(f"[ERROR] 文件不存在：{p}", file=sys.stderr)
            sys.exit(2)
        doc = open_or_active(app, p)
        all_items.extend(collect_text(doc, p.stem, not args.no_blocks, args.paper))

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    # 阅读顺序：y 降序、x 升序
    ordered = sorted(all_items, key=lambda t: (-t[1], t[0]))
    lines = []
    for x, y, t in ordered:
        no = drawing_no(x, rules) if rules else ""
        prefix = f"[{no}] " if no else ""
        lines.append(f"[y={y:.1f} x={x:.1f}] {prefix}{t}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"文字输出：{out}（{len(lines)} 行）")

    if args.columns:
        tol = args.column_tolerance
        buckets = {}
        for x, y, t in all_items:
            buckets.setdefault(int(x // tol), []).append((x, y, t))
        exp = []
        for key in sorted(buckets):
            exp.append(f"\n===== 栏 x≈{key * tol:.0f} =====")
            for x, y, t in sorted(buckets[key], key=lambda t: (-t[1], t[0])):
                no = drawing_no(x, rules) if rules else ""
                prefix = f"[{no}] " if no else ""
                exp.append(f"[y={y:.1f}] {prefix}{t}")
        expanded = out.with_name(out.stem + "_展开.txt")
        expanded.write_text("\n".join(exp) + "\n", encoding="utf-8")
        print(f"分栏展开：{expanded}（{len(buckets)} 栏）")
        print("提示：按 x 区间映射图号时，用 --drawing-map 传规则，例如 "
              '[{"max_x":109000,"no":"0-EW-0001"},{"max_x":181000,"no":"0-EW-0002"},{"no":"0-EW-0003"}]')


if __name__ == "__main__":
    main()
