# -*- coding: utf-8 -*-
"""探测 A1 图框.dwg 的图签格位：打印图签区 MTEXT / 横竖线坐标，并给出图名、图号格建议值。

新项目换了图框时，先跑这个脚本确认 `--name-cell` / `--no-cell`，再跑 draw_cad.py。
图框必须是**参数不一致时的唯一真值**：不同院的图签格位差别很大，不要照抄默认值。

用法：
    python probe_frame.py --frame "P2607/A1图框.dwg"
    python probe_frame.py --frame "P2607/A1图框.dwg" --bbox 700,0,841,230
"""
import argparse
import os
import sys
import time

import win32com.client as win32


def norm(p):
    return os.path.normcase(os.path.abspath(str(p)))


def get_doc(app, path, must_open=False):
    for i in range(app.Documents.Count):
        d = app.Documents.Item(i)
        if norm(d.FullName) == norm(path):
            return d
    if must_open:
        app.Documents.Open(os.path.abspath(path))
        time.sleep(3.0)
        app = win32.GetActiveObject("AutoCAD.Application")
        return get_doc(app, path)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True)
    ap.add_argument("--bbox", default="700,0,841,230",
                    help="只关心这个区域的图签，x0,y0,x1,y1")
    a = ap.parse_args()
    bx0, by0, bx1, by1 = [float(v) for v in a.bbox.split(",")]

    app = win32.GetActiveObject("AutoCAD.Application")
    doc = get_doc(app, a.frame, must_open=True)
    if doc is None:
        sys.exit("打不开图框：%s" % a.frame)
    ms = doc.ModelSpace
    print("图框:", doc.Name, "| 实体数:", ms.Count)

    from collections import Counter
    kinds = Counter()
    mts, vs, hs = [], set(), set()
    for i in range(ms.Count):
        try:
            e = ms.Item(i)
            kinds[e.EntityName] += 1
            if e.EntityName == "AcDbMText":
                bb = e.GetBoundingBox()
                x0, y0, x1, y1 = bb[0][0], bb[0][1], bb[1][0], bb[1][1]
                if x1 > bx0 and y1 > by0:
                    mts.append((x0, y0, x1, y1, float(e.Height),
                                str(e.StyleName), str(e.TextString)[:40]))
            elif e.EntityName == "AcDbLine":
                sp, ep = e.StartPoint, e.EndPoint
                if abs(sp[0] - ep[0]) < 0.05 and sp[0] > bx0:
                    vs.add((round(sp[0], 1), round(min(sp[1], ep[1]), 1),
                            round(max(sp[1], ep[1]), 1)))
                elif abs(sp[1] - ep[1]) < 0.05 and max(sp[0], ep[0]) > bx0:
                    hs.add((round(sp[1], 1), round(min(sp[0], ep[0]), 1),
                            round(max(sp[0], ep[0]), 1)))
        except Exception:
            pass

    print("实体类型:", dict(kinds))
    print("\n=== 图签区 MTEXT（按 y 降序）===")
    for r in sorted(mts, key=lambda r: -r[1]):
        print("  x=%7.2f~%7.2f  y=%6.2f~%6.2f  h=%.1f  %-8s  %r"
              % (r[0], r[2], r[1], r[3], r[4], r[5], r[6]))

    print("\n=== 竖线（图签区）===")
    for v in sorted(vs):
        if by0 <= v[1] <= by1 or by0 <= v[2] <= by1:
            print("  x=%.1f   y %.1f~%.1f" % v)

    print("\n=== 横线（图签区，y<=%.0f）===" % by1)
    for h in sorted(hs, key=lambda h: -h[0]):
        if h[0] <= by1:
            print("  y=%.1f   x %.1f~%.1f" % h)

    print("""
怎么用这些数字：
  * 「图纸名称」格 = 找到标签「图纸名称」那一行下方的空白格，
    --name-cell 取该格**正文区**（去掉标签与格线的内缩量，通常左右各留 2mm、上下各留 2mm）。
  * 「图号」格同理，--no-cell。
  * 字高：图名一般 h=4.5，图号一般 h=3.5（跟图框里其他小字一致）。
""")


if __name__ == "__main__":
    main()
