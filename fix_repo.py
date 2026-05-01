#!/usr/bin/env python3
"""
Fix all non-ASCII / emoji issues across the repo.
Rules:
  - In .py files:  replace emoji in print/comment strings with plain ASCII
  - In .md files:  strip emoji from headings; replace check/cross marks;
                   keep box-drawing chars (they render fine everywhere)
  - × -> x   (multiplication sign used in dimension strings)
  - → ->  ->
  - ≥ ->  >=
  - ≤ ->  <=
"""

import re, pathlib, sys

ROOT = pathlib.Path(r"C:\Users\GunjanMehta\Desktop\patent\-Video_Forgery_Detection_Using_Machine_Learning")

# ── emoji → plain-text map ────────────────────────────────────────────────────
EMOJI_MAP = {
    # status marks
    "✅": "[OK]",        # ✅
    "❌": "[ERROR]",     # ❌
    "✔": "[OK]",        # ✔
    "✖": "[X]",         # ✖
    "⚠": "[WARNING]",   # ⚠
    "️": "",            # variation selector (invisible, strip it)
    "⭐": "",            # ⭐  (strip from markdown prose)

    # category emoji used in MD headings / body
    "\U0001f3ac": "",   # 🎬
    "\U0001f4cb": "",   # 📋
    "\U0001f680": "",   # 🚀
    "\U0001f3af": "",   # 🎯
    "\U0001f3d7": "",   # 🏗
    "\U0001f52c": "",   # 🔬
    "\U0001f4ca": "",   # 📊
    "\U0001f4c1": "",   # 📁
    "\U0001f527": "",   # 🔧
    "\U0001f4d6": "",   # 📖
    "\U0001f4de": "",   # 📞
    "\U0001f4da": "",   # 📚
    "\U0001f393": "",   # 🎓
    "\U0001f3c6": "",   # 🏆
    "\U0001f4c4": "",   # 📄
    "\U0001f64f": "",   # 🙏
    "\U0001f4e7": "",   # 📧
    "\U0001f4cc": "",   # 📌
    "\U0001f31f": "",   # 🌟
    "\U0001f4dd": "",   # 📝
    "\U0001f52e": "",   # 🔮
    "❤": "",        # ❤
    "\U0001f4d0": "",   # 📐
    "\U0001f4f9": "",   # 📹
    "\U0001f501": "",   # 🔄
    "\U0001f4e2": "",   # 📢
    "\U0001f389": "",   # 🎉
    "\U0001f41b": "",   # 🐛
    "\U0001f4a1": "",   # 💡
    "\U0001f91d": "",   # 🤝

    # math / special
    "×": "x",      # × (multiplication / dimensions)
    "→": "->",     # →
    "←": "<-",     # ←
    "≥": ">=",     # ≥
    "≤": "<=",     # ≤
    "≠": "!=",     # ≠
}

# Characters to KEEP (box-drawing, used in architecture diagrams):
# ─ │ ├ └ ↓ ┐ ┘  etc.  We deliberately do NOT add these to EMOJI_MAP.


def clean(text: str) -> str:
    for char, replacement in EMOJI_MAP.items():
        text = text.replace(char, replacement)
    return text


def fix_md_heading(line: str) -> str:
    """Remove stray emoji from markdown headings and tidy double-spaces."""
    if line.startswith("#"):
        line = clean(line)
        # Collapse multiple spaces after the # markers
        line = re.sub(r"(#+)\s{2,}", r"\1 ", line)
        line = line.rstrip()
    else:
        line = clean(line)
    return line


def process_file(path: pathlib.Path) -> int:
    """Return number of lines changed."""
    original = path.read_text(encoding="utf-8", errors="replace")
    lines    = original.splitlines(keepends=True)
    changed  = 0
    out      = []

    for line in lines:
        if path.suffix == ".md":
            new = fix_md_heading(line.rstrip("\n")) + ("\n" if line.endswith("\n") else "")
        else:
            new = clean(line)
        if new != line:
            changed += 1
        out.append(new)

    if changed:
        path.write_text("".join(out), encoding="utf-8")
    return changed


# ── Run ───────────────────────────────────────────────────────────────────────
total_files  = 0
total_lines  = 0

for ext in ("*.py", "*.md", "*.txt"):
    for path in ROOT.rglob(ext):
        n = process_file(path)
        if n:
            print(f"  fixed {n:3d} line(s)  {path.relative_to(ROOT)}")
            total_files += 1
            total_lines += n

print(f"\n[DONE]  {total_files} file(s) cleaned,  {total_lines} line(s) changed.")
