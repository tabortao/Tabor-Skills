#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 docx 导出为纯文本（含表格），并导出 word/media 内嵌图片。

用法：
  python extract_docx.py "<设计建议 V3.1.docx>" --out "<tmp>/给排水设计建议.txt"
  python extract_docx.py "<参考模板.docx>" --out "<tmp>/给排水_参考模板.txt" --tables-json "<tmp>/tpl_tables.json"
"""
import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def para_text(p):
    parts = []
    for node in p.iter():
        if node.tag == W + "t":
            parts.append(node.text or "")
        elif node.tag == W + "tab":
            parts.append("\t")
        elif node.tag in (W + "br", W + "cr"):
            parts.append(" ")
    return "".join(parts).strip()


def parse_tables(xml_bytes):
    root = ET.fromstring(xml_bytes)
    body = root.find(W + "body")
    tables = []
    lines = []
    if body is None:
        return tables, lines
    ti = 0
    for child in body:
        if child.tag == W + "p":
            t = para_text(child)
            if t:
                lines.append("[P] " + t)
        elif child.tag == W + "tbl":
            ti += 1
            rows = []
            grid_cursor = 0
            for tr in child.findall(W + "tr"):
                col = 1
                cells = []
                for tc in tr.findall(W + "tc"):
                    tcpr = tc.find(W + "tcPr")
                    span = 1
                    vmerge = None
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
                rows.append({"index": len(rows) + 1, "cells": cells})
                grid_cursor = max(grid_cursor, col - 1)
                lines.append(f"[T{ti} R{len(rows)}] " + " | ".join(
                    f"c{c['col']}:{c['text']}" for c in cells if c["text"]))
            tables.append({"index": ti, "grid_cols": grid_cursor, "rows": rows})
    return tables, lines


def extract_media(docx: Path, media_dir: Path):
    media_dir.mkdir(parents=True, exist_ok=True)
    names = []
    with zipfile.ZipFile(docx) as z:
        for n in z.namelist():
            if n.startswith("word/media/") and not n.endswith("/"):
                target = media_dir / Path(n).name
                target.write_bytes(z.read(n))
                names.append(str(target))
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--out", required=True)
    ap.add_argument("--media-dir", help="内嵌图片输出目录；默认 <out>.media/")
    ap.add_argument("--tables-json", help="额外输出表格结构 JSON")
    ap.add_argument("--no-media", action="store_true")
    args = ap.parse_args()

    docx = Path(args.docx).resolve()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(docx) as z:
        xml = z.read("word/document.xml")
    tables, lines = parse_tables(xml)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    media = []
    if not args.no_media:
        mdir = Path(args.media_dir).resolve() if args.media_dir else out.with_suffix(".media")
        media = extract_media(docx, mdir)
    if args.tables_json:
        tj = Path(args.tables_json).resolve()
        tj.parent.mkdir(parents=True, exist_ok=True)
        tj.write_text(json.dumps(tables, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"表格结构：{tj}")

    print(f"源文件：{docx.name}")
    print(f"文本行数：{len(lines)}  表格数：{len(tables)}  "
          f"最大网格列数：{max((t['grid_cols'] for t in tables), default=0)}")
    print(f"内嵌图片：{len(media)} 张" + (f" → {Path(media[0]).parent}" if media else ""))
    for m in media:
        print("   " + Path(m).name)
    print(f"文本输出：{out}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
