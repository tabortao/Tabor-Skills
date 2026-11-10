# -*- coding: utf-8 -*-
"""在 AutoCAD（天正包装版）里把 blocks.json 画成多页 A1 绿色专篇 DWG。

用法（必须已有 AutoCAD 在运行，且当前文档数 >= 1）：
    python draw_cad.py --frame "P2607/A1图框.dwg" --blocks blocks.json \
        --out "P2607/项目_绿色专篇_CAD版.dwg" \
        --no-prefix AW- --no-start 10 \
        --title "深圳市设计阶段绿色专篇" \
        --subitem 通用图

设计要点（都是踩坑换来的，改动前先看 references/experience.md）：
1) 文字统一国标 SHX 样式 `GB-标准` = gbenor.shx + gbcbig.shx，字高 3.5（天正 3.5 号字）；
2) 排版是「建一块、量一块」：AddMText 后 GetBoundingBox 取真实高度，放不下换栏/换页；
3) 合并块放不下时按「段落」二分切分填充，避免整块跳栏在栏底留大片空白；
4) 表格按行画：行高 = 行内最高单元格实测高度 + 2.4mm；行线/竖线用 LINE 逐段画；
5) 图签：改「子项名称」「专业」，再逐页写图号/图名（bbox 实测居中，不用 AttachmentPoint=5）。
"""
import argparse
import json
import os
import shutil
import sys
import time

import pythoncom
import pywintypes
import win32com.client as win32
from win32com.client import VARIANT

CN = "一二三四五六七八九十"


def log(*a):
    print(*a, flush=True)


def P(x, y, z=0.0):
    """AutoCAD COM 的点参数必须是 SAFEARRAY(VT_R8)，普通 tuple 会被拒绝。"""
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,
                   [float(x), float(y), float(z)])


def retry_call(fn, *a, tries=90, delay=1.0):
    """天正包装的 AutoCAD 在打开/重生成图形时会短暂拒绝 COM 调用。"""
    last = None
    for _ in range(tries):
        try:
            return fn(*a)
        except pywintypes.com_error as ex:
            last = ex
            time.sleep(delay)
    raise last


def get_app():
    """文档增删后旧 Application 句柄会失效，必须重新绑定。"""
    last = None
    for _ in range(30):
        try:
            a = win32.GetActiveObject("AutoCAD.Application")
            _ = a.Documents.Count
            return a
        except Exception as ex:
            last = ex
            time.sleep(1)
    raise RuntimeError("无法绑定 AutoCAD：%s" % last)


def norm(p):
    return os.path.normcase(os.path.abspath(str(p)))


def find_doc(app, full):
    for i in range(app.Documents.Count):
        try:
            d = app.Documents.Item(i)
            if norm(d.FullName) == norm(full):
                return d
        except Exception:
            pass
    return None


def cn_num(n):
    if n <= 10:
        return CN[n - 1]
    if n < 20:
        return "十" + CN[n - 11]
    return CN[n // 10 - 1] + "十" + (CN[n % 10 - 1] if n % 10 else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True, help="A1 图框 dwg（1:1，841x594）")
    ap.add_argument("--blocks", required=True, help="make_layout.py 产出的 blocks.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--style", default="GB-标准")
    ap.add_argument("--font", default="gbenor.shx", help="西文字体")
    ap.add_argument("--bigfont", default="gbcbig.shx", help="中文大字体")
    ap.add_argument("--subitem", default="通用图",
                    help="图签「子项名称」要写的文字")
    ap.add_argument("--subitem-from", default="海绵城市",
                    help="图框里原有的「子项名称」文字（用来定位替换）")
    ap.add_argument("--trade-from", default="海绵城市(HM)",
                    help="图框里原有的「专业」文字")
    ap.add_argument("--trade-to", default="绿色建筑(LJ)")
    ap.add_argument("--no-prefix", default="AW-", help="图号前缀，如 AW-")
    ap.add_argument("--no-start", type=int, default=10, help="首页图号数字")
    ap.add_argument("--title", default="深圳市设计阶段绿色专篇",
                    help="图名主体；每页自动加（一）（二）…；传空串则只写图号")
    ap.add_argument("--name-cell", default="751,42,829,78",
                    help="图签「图纸名称」正文区 x0,y0,x1,y1")
    ap.add_argument("--no-cell", default="767,12,795.5,24",
                    help="图签「图号」格 x0,y0,x1,y1")
    ap.add_argument("--name-h", type=float, default=4.5)
    ap.add_argument("--no-h", type=float, default=3.5)
    ap.add_argument("--tb-style", default="宋体", help="图签用的文字样式（跟随图框）")
    ap.add_argument("--header", action="store_true",
                    help="每页顶部加页眉标题+页码（默认不加，图名图号由图签承担）")
    a = ap.parse_args()

    FRAME, TARGET = os.path.abspath(a.frame), os.path.abspath(a.out)
    cfg = json.load(open(a.blocks, encoding="utf-8"))
    H = float(cfg["h"])
    X0, X1, GUT, CW, TW = (cfg["x0"], cfg["x1"], cfg["gut"], cfg["cw"], cfg["tw"])
    Y_TOP, Y_BOT, STEP, NCOL = cfg["y_top"], cfg["y_bot"], cfg["step"], cfg["ncol"]
    LS = cfg["ls_factor"]
    BLOCKS = cfg["blocks"]

    app = get_app()
    log("AutoCAD:", app.Name, app.Version, "| docs:", app.Documents.Count)

    # ---------- 1) 干净底图 ----------
    # 天正包装的 AutoCAD 一旦用 COM Close() 关闭文档就整体断连，
    # 所以这里不关任何文档，只对同名旧图用 CLOSE 命令关掉。
    if app.Documents.Count == 0:
        retry_call(app.Documents.Open, FRAME, tries=30)
        app = get_app()

    old = find_doc(app, TARGET)
    if old is not None:
        try:
            old.SendCommand("_.CLOSE\n")
            time.sleep(3.0)
            log("已关闭同名旧图")
        except Exception as ex:
            log("WARN 关闭旧图:", str(ex)[:100])
        app = get_app()

    if os.path.exists(TARGET):
        try:
            os.remove(TARGET)          # 沙箱里可能转为回收站，删不掉也不致命
        except Exception as ex:
            log("WARN 删除旧文件:", str(ex)[:100])
    shutil.copy2(FRAME, TARGET)
    log("已复制干净图框 ->", TARGET)

    retry_call(app.Documents.Open, TARGET, tries=30)
    time.sleep(3.0)
    app = get_app()
    doc = retry_call(find_doc, app, TARGET, tries=30)
    if doc is None:
        raise RuntimeError("在 %d 个文档里找不到目标图：%s"
                           % (app.Documents.Count, TARGET))
    retry_call(doc.Activate, tries=20)
    ms = retry_call(lambda: doc.ModelSpace)
    log("当前图:", doc.Name, "| 实体数:", ms.Count)
    if "绿色专篇" not in os.path.basename(TARGET):
        log("WARN 文件名里没有「绿色专篇」，请确认 --out 指的确实是本篇")

    frame_src = [ms.Item(i) for i in range(ms.Count)]
    if not (8 <= len(frame_src) <= 200):
        raise RuntimeError("图框实体数异常：%d，可能打开的不是 A1 图框" % len(frame_src))

    # ---------- 2) 图签：子项名称 / 专业 ----------
    for e in frame_src:
        if e.EntityName != "AcDbMText":
            continue
        s = str(e.TextString)
        if s.strip() == a.subitem_from:
            e.TextString = a.subitem
        elif a.trade_from in s:
            e.TextString = s.replace(a.trade_from, a.trade_to)

    # ---------- 3) 图层与文字样式 ----------
    for name, color in (("GB-TEXT", 7), ("GB-HEAD", 5), ("GB-TABLE", 8)):
        try:
            lay = retry_call(doc.Layers.Add, name, tries=20)
        except Exception:
            lay = doc.Layers.Item(name)
        lay.Color = color

    try:
        style = doc.TextStyles.Item(a.style)
    except Exception:
        style = retry_call(doc.TextStyles.Add, a.style, tries=20)
    style.FontFile = a.font
    style.BigFontFile = a.bigfont
    style.Height = 0.0
    retry_call(lambda: setattr(doc, "ActiveTextStyle", style), tries=20)
    chk = doc.TextStyles.Item(a.style)
    log("文字样式:", chk.Name, "|", chk.FontFile, "|", chk.BigFontFile)

    _last = [None]

    def set_layer(name):
        if _last[0] == name:
            return
        try:
            lay = doc.Layers.Item(name)
        except Exception:
            lay = None                     # 图框里没有这个图层就留在当前层，不报错
        if lay is not None:
            retry_call(lambda: setattr(doc, "ActiveLayer", lay), tries=30)
        _last[0] = name

    counts = {"mtext": 0, "line": 0}
    splits = [0]
    records = []
    warnings = []
    SEP = "\\P"

    def add_mtext(x, y, w, s, layer, attach=1, height=None):
        set_layer(layer)
        m = retry_call(ms.AddMText, P(x, y), float(w), s)
        target = H if height is None else float(height)
        # 坑：AddMText 新建的 MTEXT 继承系统 TEXTSIZE（常见 350），必须显式设字高
        for attr, val in (("Height", target), ("AttachmentPoint", attach),
                          ("LineSpacingStyle", 2), ("LineSpacingFactor", LS)):
            try:
                setattr(m, attr, val)
            except Exception:
                pass
        try:
            m.StyleName = a.style
        except Exception:
            pass
        try:
            if abs(float(m.Height) - target) > 1e-6:
                m.Height = target
        except Exception:
            pass
        try:
            bb = retry_call(m.GetBoundingBox, tries=20)
            hh = float(bb[1][1] - bb[0][1])
        except Exception:
            hh = 4.67
        counts["mtext"] += 1
        return m, max(hh, 1.0)

    def add_line(x1, y1, x2, y2, layer):
        set_layer(layer)
        retry_call(ms.AddLine, P(x1, y1), P(x2, y2))
        counts["line"] += 1

    # ---------- 4) 流式分栏排版 ----------
    state = {"page": 0, "col": 0, "y": Y_TOP}

    def col_x(page=None, col=None):
        p = state["page"] if page is None else page
        c = state["col"] if col is None else col
        return p * STEP + X0 + c * (CW + GUT)

    def fit(hh, span=False):
        if state["y"] - hh >= Y_BOT:
            return None
        oldx, oldy = col_x(), state["y"]
        if span:
            state["page"] += 1
            state["col"] = 0
        else:
            state["col"] += 1
            if state["col"] >= NCOL:
                state["page"] += 1
                state["col"] = 0
        state["y"] = Y_TOP
        nx, ny = col_x(), state["y"]
        if ny - hh < Y_BOT:
            warnings.append("块太高 %.1fmm（第 %d 页）" % (hh, state["page"] + 1))
        return (nx - oldx, ny - oldy, nx, ny)

    def move(obj, dx, dy):
        if dx or dy:
            retry_call(obj.Move, P(0, 0), P(dx, dy), tries=20)

    def measure(m):
        bb = retry_call(m.GetBoundingBox, tries=20)
        return float(bb[1][1] - bb[0][1])

    t0 = time.time()
    for bi, b in enumerate(BLOCKS):
        if b["k"] == "para":
            role = b["role"]
            gap = 3.0 if role == "head" else 1.6
            layer = "GB-HEAD" if role in ("head", "clause") else "GB-TEXT"
            segs = b["s"].split(SEP) if b.get("n", 1) > 1 else [b["s"]]
            i, made = 0, 0
            while i < len(segs):
                made += 1
                rest = segs[i:]
                x, y = col_x(), state["y"]
                m, hh = add_mtext(x + 1.0, y, CW - 2.0, SEP.join(rest), layer)
                take = len(rest)
                if len(rest) > 1 and y - hh - gap < Y_BOT:
                    # 二分找「放得下的段落前缀」，只把放得下的留在本栏
                    lo, hi, best, bh = 1, len(rest) - 1, 0, 0.0
                    while lo <= hi:
                        mid = (lo + hi) // 2
                        m.TextString = SEP.join(rest[:mid])
                        h2 = measure(m)
                        if y - h2 - gap >= Y_BOT:
                            best, bh = mid, h2
                            lo = mid + 1
                        else:
                            hi = mid - 1
                    if best:
                        m.TextString = SEP.join(rest[:best])
                        hh, take = bh, best
                    else:
                        m.TextString = SEP.join(rest)
                        hh = measure(m)
                if y - hh - gap < Y_BOT:
                    f = fit(hh + gap)
                    if f:
                        move(m, f[0], f[1])
                        x, y = f[2], f[3]
                records.append((state["page"], state["col"], x + 1.0, CW - 2.0, "para"))
                if i == 0 and role == "head":
                    add_line(x, y + 1.2, x + CW, y + 1.2, "GB-HEAD")
                state["y"] = y - hh - gap
                i += take
            if made > 1:
                splits[0] += 1
        else:
            span = bool(b.get("span"))
            if span and b.get("head") and (state["col"] > 0 or state["y"] < Y_TOP - 0.5):
                state["page"] += 1
                state["col"] = 0
                state["y"] = Y_TOP
            widths = b["w"]
            bounds = [0.0]
            for w in widths:
                bounds.append(bounds[-1] + w)
            x, y = col_x(), state["y"]
            layer = "GB-HEAD" if b["head"] else "GB-TEXT"
            objs, maxh = [], 0.0
            for j, cell in enumerate(b["cells"]):
                if not cell:
                    continue
                w = max(widths[j] - 2.0, 6.0)
                cx = x + bounds[j] + 1.0
                m, hh = add_mtext(cx, y - 1.2, w, cell, layer)
                objs.append(m)
                maxh = max(maxh, hh)
                records.append((state["page"], state["col"], cx, w,
                                "cell-span" if span else "cell"))
            rowh = maxh + 2.4
            f = fit(rowh, span=span)
            if f:
                for m in objs:
                    move(m, f[0], f[1])
                x, y = f[2], f[3]
            add_line(x, y - rowh, x + bounds[-1], y - rowh, "GB-TABLE")
            if b["head"]:
                add_line(x, y, x + bounds[-1], y, "GB-TABLE")
            for j in range(len(widths) + 1):
                add_line(x + bounds[j], y, x + bounds[j], y - rowh, "GB-TABLE")
            state["y"] = y - rowh
        if (bi + 1) % 300 == 0:
            log("  块 %d/%d  页=%d 栏=%d y=%.1f  %.0fs"
                % (bi + 1, len(BLOCKS), state["page"] + 1, state["col"] + 1,
                   state["y"], time.time() - t0))

    pages = state["page"] + 1
    log("排版完成: 页数=%d  MTEXT=%d  LINE=%d  被切分块=%d  %.0fs"
        % (pages, counts["mtext"], counts["line"], splits[0], time.time() - t0))

    # ---------- 5) 页眉（默认不加） ----------
    if a.header:
        for p in range(pages):
            ox = p * STEP
            add_mtext(ox + X0, Y_TOP + 12.0, 420.0, a.title, "GB-HEAD")
            add_mtext(ox + X1 - 92.0, Y_TOP + 12.0, 88.0,
                      "第 %d 页 / 共 %d 页" % (p + 1, pages), "GB-HEAD")
            add_line(ox + X0, Y_TOP + 4.5, ox + X1, Y_TOP + 4.5, "GB-HEAD")

    # ---------- 6) 复制图框到其余各页 ----------
    for p in range(1, pages):
        n0 = ms.Count
        retry_call(doc.CopyObjects,
                   VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, frame_src),
                   ms, tries=30)
        added = ms.Count - n0
        if added != len(frame_src):
            log("WARN 复制实体数不符：第 %d 页 %d/%d" % (p + 1, added, len(frame_src)))
        for i in range(n0, ms.Count):
            retry_call(ms.Item(i).Move, P(0, 0), P(p * STEP, 0), tries=20)
    log("图框已复制到 %d 页" % pages)

    # ---------- 7) 逐页写图号 / 图名 ----------
    nx0, ny0, nx1, ny1 = [float(v) for v in a.name_cell.split(",")]
    ux0, uy0, ux1, uy1 = [float(v) for v in a.no_cell.split(",")]

    def put(cx, cy, s, height):
        set_layer("图框")
        m = retry_call(ms.AddMText, P(cx, cy), 0.0, s)
        # 坑：AttachmentPoint=5（正中）在 COM 里不可靠，插入点会被当左上角，
        # 文字整体右移半宽 -> 改成建完后按 bbox 实测居中
        for attr, val in (("Height", height), ("AttachmentPoint", 1)):
            try:
                setattr(m, attr, val)
            except Exception:
                pass
        try:
            m.StyleName = a.tb_style
        except Exception:
            pass
        bb = retry_call(m.GetBoundingBox, tries=20)
        move(m, cx - (bb[0][0] + bb[1][0]) / 2.0, cy - (bb[0][1] + bb[1][1]) / 2.0)
        counts["mtext"] += 1
        return m

    for p in range(pages):
        ox = p * STEP
        no = "%s%04d" % (a.no_prefix, a.no_start + p)
        put(ox + (ux0 + ux1) / 2.0, (uy0 + uy1) / 2.0, no, a.no_h)
        if a.title:
            name = "%s（%s）" % (a.title, cn_num(p + 1))
            put(ox + (nx0 + nx1) / 2.0, (ny0 + ny1) / 2.0, name, a.name_h)
        log("图签 第%d页: %s | %s" % (p + 1, no, a.title or "-"))

    # ---------- 8) 溢出校验 ----------
    overflow = 0
    for page, col, x, w, kind in records:
        right = page * STEP + (X0 + TW if kind == "cell-span"
                               else X0 + col * (CW + GUT) + CW)
        if x + w > right + 0.05:
            overflow += 1
    log("越界 MTEXT = %d / %d" % (overflow, len(records)))
    log("warnings =", warnings[:10], "total", len(warnings))

    retry_call(doc.Save, tries=60)
    try:
        doc.SendCommand("_.ZOOM\n_E\n")
    except Exception:
        pass
    log("SAVED", doc.FullName)
    log("最终实体数:", ms.Count, counts)
    if overflow:
        sys.exit(2)


if __name__ == "__main__":
    main()
