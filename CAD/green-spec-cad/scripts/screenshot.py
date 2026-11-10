# -*- coding: utf-8 -*-
"""把 CAD 当前图放大到指定窗口并截图，用于视觉复核（文字是否压线、图签是否对格）。

踩过的坑：
- 天正 AutoCAD 的主窗口类名是 `AfxMDIFrame140u`；窗口最小化时
  `GetWindowRect` 返回 `(-32000,-32000,...)`，必须先 `ShowWindow(SW_RESTORE)`
  再 `SetForegroundWindow`，否则截到的是别的程序。
- `ZOOM _W` 传的是模型空间坐标；截完记得 `ZOOM _E` 还原，免得用户看到乱放大。

用法：
    python screenshot.py out.png --win 0,0,841,594
    python screenshot.py out.png --win 745,5,835,215 --keep-zoom   # 只截图签
"""
import sys
import time

import win32com.client as win32
import win32con
import win32gui
from PIL import ImageGrab


def cad_window():
    hits = []

    def cb(h, _):
        if win32gui.IsWindowVisible(h) and "AfxMDIFrame" in win32gui.GetClassName(h):
            hits.append(h)

    win32gui.EnumWindows(cb, None)
    return hits[0] if hits else 0


def grab(win, out, wait=3.0, keep_zoom=False):
    app = win32.GetActiveObject("AutoCAD.Application")
    doc = app.ActiveDocument
    doc.Activate()

    hwnd = cad_window()
    if hwnd:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        time.sleep(1.2)

    x1, y1, x2, y2 = win
    doc.SendCommand("_.ZOOM\n_W\n%.3f,%.3f\n%.3f,%.3f\n" % (x1, y1, x2, y2))
    time.sleep(wait)

    l, t, r, b = win32gui.GetWindowRect(hwnd)
    if l < -10000:                      # 仍在最小化，退回全屏抓
        img = ImageGrab.grab(all_screens=True)
    else:
        img = ImageGrab.grab(bbox=(l, t, r, b), all_screens=True)
    img.save(out)
    print("saved", out, img.size)

    if not keep_zoom:
        doc.SendCommand("_.ZOOM\n_E\n")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "shot.png"
    win = (0, 0, 841, 594)
    if "--win" in sys.argv:
        win = tuple(float(v) for v in sys.argv[sys.argv.index("--win") + 1].split(","))
    grab(win, out, keep_zoom="--keep-zoom" in sys.argv)
