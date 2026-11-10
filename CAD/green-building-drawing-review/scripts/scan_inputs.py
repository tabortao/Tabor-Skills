#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描项目目录，建立「专业 → 设计建议 docx / CAD dwg / 参考模板 docx」映射。

用法：
  python scan_inputs.py --cad-dir "<项目>/CAD" --advice-dir "<项目>/01 绿建设计建议" \
      --template-dir "<工作区>/参考审图意见" --out "<工作区>/.workbuddy/tmp/inputs.json"
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 长别名优先，避免「给排水」被「排水」、「绿色建筑」被「建筑」误吞
ALIASES = [
    ("给排水", ["给排水", "给水排水", "plumbing", "pw"]),
    ("智能化", ["智能化", "弱电", "智能建筑"]),
    ("暖通", ["暖通", "采暖通风", "空调", "通风", "hvac", "mw"]),
    ("电气", ["电气", "强电", "electrical", "ew"]),
    ("结构", ["结构", "结施", "structural"]),
    ("景观", ["景观", "园林", "landscape"]),
    ("幕墙", ["幕墙", "curtainwall"]),
    ("室内", ["室内", "精装", "装修"]),
    ("建筑", ["建筑", "建施", "arch", "aw"]),
    ("标识", ["标识", "signage"]),
    ("泛光", ["泛光", "照明", "lighting"]),
    ("燃气", ["燃气", "gas"]),
]

# 只认「XX绿色建筑设计建议」这种命名；「绿色建筑采购建议书」「施工单位绿色建筑建议」
# 不是专业设计建议，一律跳过，避免误归到「建筑」专业。
ADVICE_RE = re.compile(r"(.{1,14}?)绿色建筑设计建议")
TEMPLATE_RE = re.compile(r"绿建提([^\s.、]+?)(?=\.docx|$)")


def normalize(raw: str):
    raw = raw.strip().lower()
    for std, keys in ALIASES:
        for k in keys:
            if k in raw:
                return std
    return None


def advice_discipline(name: str):
    m = ADVICE_RE.search(name)
    if not m:
        return None
    prefix = m.group(1).lstrip("0123456789、.．_- ")
    return normalize(prefix) or normalize(m.group(1))


def template_discipline(name: str):
    m = TEMPLATE_RE.search(name)
    if m:
        return normalize(m.group(1)) or m.group(1)
    return normalize(name)


def cad_discipline(name: str):
    stem = Path(name).stem
    low = stem.lower()
    # 设计说明类文件名常见「XX绿色建筑设计建议」不会出现在 CAD 目录，仍加保险
    low = low.replace("绿色建筑", "")
    for std, keys in ALIASES:
        for k in keys:
            if k in low:
                return std
    return None


def guess_project(root: Path, explicit: str) -> str:
    if explicit:
        return explicit
    n = root.name
    for suffix in ("项目绿建审查", "绿建审查", "项目资料", "施工图审查"):
        if n.endswith(suffix):
            n = n[: -len(suffix)]
    return n.strip() or root.name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cad-dir", required=True, help="项目 CAD 图纸目录")
    ap.add_argument("--advice-dir", required=True, help="项目绿建设计建议目录")
    ap.add_argument("--template-dir", required=True, help="参考审图意见模板目录")
    ap.add_argument("--project-root", help="成品输出根目录；默认取 CAD 目录的父目录")
    ap.add_argument("--project", help="项目名称；默认从目录名推断")
    ap.add_argument("--out", required=True, help="输出 inputs.json 路径")
    args = ap.parse_args()

    cad_dir = Path(args.cad_dir).resolve()
    advice_dir = Path(args.advice_dir).resolve()
    tpl_dir = Path(args.template_dir).resolve()
    root = Path(args.project_root).resolve() if args.project_root else cad_dir.parent

    for p, label in ((cad_dir, "CAD"), (advice_dir, "设计建议"), (tpl_dir, "模板")):
        if not p.is_dir():
            print(f"[ERROR] {label}目录不存在: {p}", file=sys.stderr)
            sys.exit(2)

    def in_real_folder(p: Path, base: Path) -> bool:
        # 跳过 _学习示例 / _json输出 / .workbuddy 等临时目录
        return not any(seg.startswith("_") or seg.startswith(".")
                       for seg in p.relative_to(base).parts[:-1])

    cads = sorted([p for p in cad_dir.rglob("*")
                   if p.suffix.lower() in (".dwg", ".dxf") and in_real_folder(p, cad_dir)])
    advices = sorted([p for p in advice_dir.rglob("*.docx")
                      if not p.name.startswith("~$") and in_real_folder(p, advice_dir)])
    templates = sorted([p for p in tpl_dir.rglob("*.docx")
                        if not p.name.startswith("~$") and in_real_folder(p, tpl_dir)])

    buckets = {}

    def bucket(name):
        return buckets.setdefault(name, {"name": name, "advice": None, "cads": [], "template": None})

    for p in advices:
        d = advice_discipline(p.name)
        if d:
            b = bucket(d)
            if b["advice"] is None or "V3" in p.name.upper():
                b["advice"] = str(p)
    for p in cads:
        d = cad_discipline(p.name)
        if d:
            bucket(d)["cads"].append(str(p))
    for p in templates:
        d = template_discipline(p.name)
        if d:
            b = bucket(d)
            b.setdefault("template_candidates", []).append(str(p))
            # 模板目录里可能混有旧项目归档件（已填处理/验证栏），排序靠前的通常是标准参考模板
            if b["template"] is None:
                b["template"] = str(p)

    order = [std for std, _ in ALIASES]
    disciplines = []
    for d in sorted(buckets, key=lambda x: order.index(x) if x in order else 99):
        b = buckets[d]
        missing = []
        if not b["advice"]:
            missing.append("设计建议")
        if not b["cads"]:
            missing.append("CAD 图纸")
        if not b["template"]:
            missing.append("参考模板")
        b["status"] = "ready" if not missing else "缺：" + "、".join(missing)
        disciplines.append(b)

    unmatched = {
        "cad": [str(p) for p in cads if not cad_discipline(p.name)],
        "advice": [str(p) for p in advices if not advice_discipline(p.name)],
        "template": [str(p) for p in templates if not template_discipline(p.name)],
    }

    result = {
        "project": guess_project(root, args.project),
        "project_root": str(root),
        "cad_dir": str(cad_dir),
        "advice_dir": str(advice_dir),
        "template_dir": str(tpl_dir),
        "disciplines": disciplines,
        "unmatched": unmatched,
        "notes": [
            "模板目录内与成品同名的文件是旧项目归档件，禁止覆盖；成品统一输出到 project_root。",
            "status != ready 的专业需用户补齐资料后再审。",
            "设计号、审核人、日期需从设计建议/图纸/用户指令中确认，填入 opinions.json。",
        ],
    }
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"项目：{result['project']}    项目根目录：{root}")
    for d in disciplines:
        print(f"  {d['name']:<6} 建议:{int(bool(d['advice']))} CAD:{len(d['cads'])} 模板:{int(bool(d['template']))}  {d['status']}")
        if len(d.get("template_candidates", [])) > 1:
            print("          ⚠ 多个模板候选，人工确认（含旧项目归档件不可用）：")
            for t in d["template_candidates"]:
                print(f"            {Path(t).name}")
    for k, v in unmatched.items():
        if v:
            print(f"  [未匹配 {k}] {len(v)} 个：")
            for p in v[:5]:
                print(f"      {p}")
    print(f"\n映射文件：{out}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
