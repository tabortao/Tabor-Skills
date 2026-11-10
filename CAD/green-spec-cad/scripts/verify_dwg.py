# -*- coding: utf-8 -*-
"""出图后自检：页数、字高、越界、纵向重叠、图签文字、页眉残留。

判定标准（都是用户验收过的）：
- 越界 MTEXT 必须是 0（按 bbox 判栏位，不能按插入点判，否则表格单元格会假报警）
- 同栏内 MTEXT 不得纵向重叠
- 正文字高必须是目标字高（天正 3.5）

用法：
    python verify_dwg.py --dwg "P2607/项目_绿色专篇_CAD版.dwg" --step 861 --cols 3
"""
import argparse
import os
import sys

import win32com.client as win32


def norm(p):
    return os.path.normcase(os.path.abspath(str(p)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dwg", required=True)
    ap.add_argument("--step", type=float, default=861.0)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--x0", type=float, default=30.0)
    ap.add_argument("--x1", type=float, default=740.0)
    ap.add_argument("--gut", type=float, default=8.0)
    ap.add_argument("--height", type=float, default=3.5)
    a = ap.parse_args()

    app = win32.GetActiveObject("AutoCAD.Application")
    doc = None
    for i in range(app.Documents.Count):
        d = app.Documents.Item(i)
        if norm(d.FullName) == norm(a.dwg):
            doc = d
            break
    if doc is None:
        sys.exit("图纸未在 CAD 中打开：%s" % a.dwg)
    app.ActiveDocument = doc
    ms = doc.ModelSpace
    print("图纸:", doc.Name, "| 实体数:", ms.Count)

    CW = (a.x1 - a.x0 - a.gut * (a.cols - 1)) / float(a.cols)
    frames, mts, heads = 0, [], []
    for i in range(ms.Count):
        try:
            e = ms.Item(i)
            if e.EntityName == "AcDbBlockReference":
                if "图框" in str(e.Name):
                    frames += 1
                continue
            if e.EntityName != "AcDbMText":
                continue
            bb = e.GetBoundingBox()
            x0, y0, x1, y1 = bb[0][0], bb[0][1], bb[1][0], bb[1][1]
            page = int(x0 // a.step)
            rx0, rx1 = x0 - page * a.step, x1 - page * a.step
            mts.append({"i": i, "page": page, "x0": rx0, "x1": rx1, "y0": y0,
                        "y1": y1, "h": float(e.Height), "s": str(e.TextString),
                        "style": str(e.StyleName),
                        "col": max(0, int((rx0 - a.x0) // (CW + a.gut)))
                        if rx0 >= a.x0 else 0})
            if y1 > 568:
                heads.append((i, round(rx0, 1), round(y1, 1), str(e.TextString)[:30]))
        except Exception:
            pass

    print("图框块引用:", frames, "| MTEXT:", len(mts))

    body = [m for m in mts if m["x0"] < a.x1 - 1]
    hs = {}
    for m in body:
        hs[round(m["h"], 2)] = hs.get(round(m["h"], 2), 0) + 1
    print("字高分布(正文区):", dict(sorted(hs.items())))
    bad_h = [m for m in body if abs(m["h"] - a.height) > 0.01 and m["y1"] < 560]
    print("字高不符目标 %.1f 的正文字块: %d" % (a.height, len(bad_h)))
    for m in bad_h[:5]:
        print("   h=%.2f y=%.1f %r" % (m["h"], m["y1"], m["s"][:30]))

    # 越界：右边界按所属栏算
    overflow = []
    for m in body:
        right = a.x0 + (m["col"] + 1) * CW + m["col"] * a.gut
        if m["x1"] > right + 0.5 and m["x1"] - m["x0"] > 2.0:
            overflow.append((m["page"] + 1, round(m["x1"], 1), round(right, 1),
                             m["s"][:20]))
    print("越界 MTEXT: %d" % len(overflow))
    for o in overflow[:8]:
        print("   第%d页 x1=%.1f > 栏右 %.1f  %r" % o)

    # 纵向重叠：同页同栏按 y 排序，检查相邻块
    overlaps = 0
    by = {}
    for m in body:
        by.setdefault((m["page"], m["col"]), []).append(m)
    for k, arr in by.items():
        arr.sort(key=lambda m: -m["y1"])
        for u, v in zip(arr, arr[1:]):
            if v["y1"] > u["y0"] + 0.3 and abs(v["x0"] - u["x0"]) < 1.0:
                overlaps += 1
    print("纵向重叠: %d" % overlaps)

    print("页眉残留(y>568):", heads if heads else "无")

    print("\n=== 图签关键格 ===")
    for m in mts:
        if m["x0"] > 745 and (m["y0"] > 80):
            print("   第%d页 y=%.1f x=%.1f  %r" % (m["page"] + 1, m["y0"], m["x0"], m["s"]))
    print("\n=== 图号 / 图名 ===")
    for m in mts:
        if m["x0"] > 745 and m["y0"] < 70:
            print("   第%d页 y=%.1f x=%.1f  %r" % (m["page"] + 1, m["y0"], m["x0"], m["s"]))

    ok = (not overflow) and (not overlaps) and (not bad_h) and (not heads) \
        and frames >= 1
    print("\n结论:", "通过" if ok else "需要处理")


if __name__ == "__main__":
    main()
