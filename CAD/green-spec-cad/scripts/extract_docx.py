# -*- coding: utf-8 -*-
"""把 Word 版绿色专篇（.docx）按 **文档顺序** 抽成 JSON，供 make_layout.py 排版。

只依赖 Python 标准库（zipfile + xml.etree），不需要 python-docx。

输出结构：
[
  {"t": "p",   "v": "项目概况"},
  {"t": "tbl", "rows": [["楼栋名称", "评分", "标准"], ["1栋", "76%", "深标"]]},
  ...
]

用法：
    python extract_docx.py 绿色专篇.docx content.json
    python extract_docx.py 绿色专篇.docx content.json --keep-empty

说明 / 取舍：
- 只取 body 的直接子节点 w:p / w:tbl，文本框、页眉页脚、批注一律忽略
  （绿色专篇正文里的文字都在 body 里，页眉页脚是“第 x 页 共 y 页”之类，不要）。
- 表格：一行一 w:tr，一格一 w:tc；横向合并（w:gridSpan）按一个格处理，
  纵向合并（w:vMerge 续行）输出空格，与原表视觉一致。
- 单元格内多段文字用「空格」拼（CAD 单元格里换行会把行高撑爆）。
- 空段落默认丢弃（--keep-empty 保留）；纯空格、纯制表符也丢弃。
"""
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def para_text(p):
    """取段落里所有 w:t 的文字；w:tab -> 空格，w:br -> 空格。"""
    buf = []
    for node in p.iter():
        tag = node.tag
        if tag == W + "t":
            buf.append(node.text or "")
        elif tag in (W + "tab", W + "br"):
            buf.append(" ")
    return re.sub(r"\s+", " ", "".join(buf)).strip()


def cell_text(tc):
    """单元格：内部所有段落用空格串起来。"""
    parts = [para_text(p) for p in tc.findall(W + "p")]
    return re.sub(r"\s+", " ", " ".join(x for x in parts if x)).strip()


def grid_span(tc):
    pr = tc.find(W + "tcPr")
    if pr is None:
        return 1
    gs = pr.find(W + "gridSpan")
    if gs is None:
        return 1
    try:
        return max(1, int(gs.get(W + "val")))
    except (TypeError, ValueError):
        return 1


def is_vmerge_continue(tc):
    pr = tc.find(W + "tcPr")
    if pr is None:
        return False
    vm = pr.find(W + "vMerge")
    if vm is None:
        return False
    return vm.get(W + "val") in (None, "continue")


def table_rows(tbl):
    rows = []
    for tr in tbl.findall(W + "tr"):
        row = []
        for tc in tr.findall(W + "tc"):
            txt = "" if is_vmerge_continue(tc) else cell_text(tc)
            span = grid_span(tc)
            row.append(txt)
            for _ in range(span - 1):     # 横向合并占位，保持列对齐
                row.append("")
        while row and row[-1] == "":      # 去掉行尾空占位
            row.pop()
        rows.append(row)
    while rows and all(c == "" for c in rows[-1]):
        rows.pop()
    return rows


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]
    keep_empty = "--keep-empty" in sys.argv

    with zipfile.ZipFile(src) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find(W + "body")
    if body is None:
        sys.exit("文档里找不到 w:body")

    items, n_p, n_t = [], 0, 0
    for child in list(body):
        if child.tag == W + "p":
            txt = para_text(child)
            if not txt and not keep_empty:
                continue
            items.append({"t": "p", "v": txt})
            n_p += 1
        elif child.tag == W + "tbl":
            rows = table_rows(child)
            if not rows:
                continue
            items.append({"t": "tbl", "rows": rows})
            n_t += 1

    with open(out, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
    chars = sum(len(x.get("v", "")) for x in items if x["t"] == "p")
    chars += sum(len(c) for x in items if x["t"] == "tbl" for r in x["rows"] for c in r)
    print("paragraphs =", n_p, "| tables =", n_t, "| chars =", chars)
    print("saved", out)


if __name__ == "__main__":
    main()
