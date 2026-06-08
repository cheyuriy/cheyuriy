#!/usr/bin/env python3
"""Generate assets/skills.svg — a static scatter graph of skills.

Domain is -100..100 on both axes, crossing at the center (0,0):
  X = relevance  (-100 = "sometimes in past"  ->  +100 = "everyday practice")
  Y = knowledge  (-100 = "barely know"        ->  +100 = "expertise")

Skills are entered on a 0-20 scale as (knowledge, relevance) and mapped to
the domain with  d = v*10 - 100  (so 0 -> -100, 10 -> 0, 20 -> +100).
A seeded jitter breaks up stacked dots; a greedy pass de-collides labels
and draws a thin connector when a label is nudged away from its dot.

NOTE: GitHub serves SVGs through its Camo proxy as <img>, so hover/tooltips
do NOT work. Labels are baked in.

Edit GROUPS below and run:  python3 assets/gen_skills.py
"""
import random

# group name -> (color, [ (skill, knowledge 0-20, relevance 0-20[, "L"|"R"]), ... ])
# optional 4th item forces the label to the Left or Right of the dot.
GROUPS = {
    "Programming": ("#4C8DFF", [
        ("Python", 17, 20), ("C++", 2, 2), ("Rust", 12, 20), ("JS", 10, 12, "R"),
        ("Haskell", 5, 5), ("Go", 2, 3), ("R", 3, 3), ("SQL", 17, 20),
        ("Java", 3, 3), ("Functional programming", 5, 7, "R"),
    ]),
    "Platforms": ("#F5A623", [
        ("GCP", 17, 19, "L"), ("AWS", 8, 10), ("Self-hosting", 15, 16),
    ]),
    "Infra tools": ("#2BD9D9", [
        ("Docker", 13, 14), ("Git", 12, 17, "L"), ("CI/CD", 5, 6),
    ]),
    "OS": ("#5BD75B", [
        ("Linux", 10, 12, "R"), ("Shell", 10, 14, "R"), ("Android", 7, 5),
    ]),
    "Databases": ("#B36BFF", [
        ("Postgres", 11, 10), ("ClickHouse", 12, 17), ("Neo4j", 9, 15),
        ("Redis", 9, 15, "L"), ("BigQuery", 18, 20), ("Redshift", 4, 4),
    ]),
    "Frameworks": ("#E255C9", [
        ("Vue", 10, 12), ("React", 8, 10), ("Flask", 9, 13),
        ("Ruby on Rails", 4, 3), ("Warp", 6, 9),
    ]),
    "Data": ("#F2545B", [
        ("Stats", 12, 14), ("Math", 10, 11), ("ML", 12, 12),
        ("Neural Networks", 11, 12), ("LLM-tools", 13, 20), ("MCP", 13, 19),
        ("Agents", 12, 19), ("Data Analysis", 14, 16),
        ("Data Engineering", 16, 19, "L"), ("System Analysis", 13, 8),
        ("MLOps", 13, 18),
    ]),
    "Other": ("#E8D44D", [
        ("Requirements", 13, 5), ("Testing", 14, 14), ("API-design", 13, 17, "L"),
    ]),
}

# ---- canvas / layout ----
W, H = 1500, 902
L, R, T, B = 70, 70, 110, 70            # margins (T leaves room for legend)
PW, PH = W - L - R, H - T - B           # plot area
random.seed(42)

VR = 120                                             # view range: data is +-100,
                                                     # the +-100..+-VR band is padding for labels
def clampd(v, lo=-99, hi=99):  return max(lo, min(hi, v))
def px(d):  return L + (d + VR) / (2 * VR) * PW       # domain -VR..VR -> x
def py(d):  return T + (VR - d) / (2 * VR) * PH       # domain -VR..VR -> y
CX, CY = px(0), py(0)
PB = py(-VR)                                          # plot bottom y

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def lighten(hexc, t=0.5):                 # blend a color toward white by t (0..1)
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * t) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"

def halo(x, y, txt, size, fill, anchor="start", weight="600", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{fill}" '
            f'font-size="{size}" font-weight="{weight}" style="paint-order:stroke" '
            f'stroke="#0d1117" stroke-width="3.5" stroke-linejoin="round" {extra}>{esc(txt)}</text>')

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'width="{W}" height="{H}" font-family="\'Segoe UI\',Verdana,sans-serif">')
parts.append('<rect x="0" y="0" width="100%" height="100%" rx="16" fill="#0d1117"/>')

# quadrant tints (sweet spot = top-right, green)
for x, y, c in [(L, T, "#1f6feb"), (CX, T, "#238636"), (L, CY, "#6e40c9"), (CX, CY, "#9e6a03")]:
    parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{PW/2:.0f}" height="{PH/2:.0f}" fill="{c}" fill-opacity="0.06"/>')

# grid
for d in (-80, -60, -40, -20, 20, 40, 60, 80):
    parts.append(f'<line x1="{px(d):.0f}" y1="{py(VR):.0f}" x2="{px(d):.0f}" y2="{PB:.0f}" stroke="#21262d" stroke-width="1"/>')
    parts.append(f'<line x1="{px(-VR):.0f}" y1="{py(d):.0f}" x2="{px(VR):.0f}" y2="{py(d):.0f}" stroke="#21262d" stroke-width="1"/>')

# data boundary (+-100) — points live inside this box; the band out to the edge is label padding
parts.append(f'<rect x="{px(-100):.0f}" y="{py(100):.0f}" width="{px(100)-px(-100):.0f}" height="{py(-100)-py(100):.0f}" '
             f'fill="none" stroke="#2d333b" stroke-width="1.2" stroke-dasharray="5 5"/>')

# centered axes with arrowheads
parts.append('<defs><marker id="arr" markerWidth="11" markerHeight="11" refX="6" refY="3" orient="auto">'
             '<path d="M0,0 L6,3 L0,6 Z" fill="#9aa4b2"/></marker></defs>')
parts.append(f'<line x1="{px(-VR):.0f}" y1="{CY:.0f}" x2="{px(VR):.0f}" y2="{CY:.0f}" stroke="#9aa4b2" stroke-width="2.2" marker-end="url(#arr)"/>')
parts.append(f'<line x1="{CX:.0f}" y1="{PB:.0f}" x2="{CX:.0f}" y2="{py(VR):.0f}" stroke="#9aa4b2" stroke-width="2.2" marker-end="url(#arr)"/>')

# legend (two rows of four, above the plot)
for i, (gname, (color, _)) in enumerate(GROUPS.items()):
    col, row = i % 4, i // 4
    lx, ly = 110 + col * 340, 34 + row * 30
    parts.append(f'<circle cx="{lx}" cy="{ly-4:.0f}" r="7" fill="{color}"/>')
    parts.append(halo(lx + 14, ly, gname, 15, "#c9d1d9"))

# ---- points + greedy label de-collision ----
CHARW, LH, GAP = 7.3, 16.0, 2.0         # est. char width, label height, min gap
labels = []
for color, skills in GROUPS.values():
    for entry in skills:
        name, kno, rel = entry[0], entry[1], entry[2]
        forced = entry[3] if len(entry) > 3 else None    # "L"/"R" forces label side
        dx_dom = clampd(rel * 10 - 100 + random.uniform(-5, 5))
        dy_dom = clampd(kno * 10 - 100 + random.uniform(-5, 5))
        x, y = px(dx_dom), py(dy_dom)
        w = len(name) * CHARW + 6
        # Forced side wins; else near an edge -> label outward into the padding,
        # interior -> inward toward the central axis.
        if forced in ("L", "R"):
            to_right = forced == "R"
        elif dx_dom >= 45:
            to_right = True
        elif dx_dom <= -45:
            to_right = False
        else:
            to_right = dx_dom < 0
        if to_right:
            anchor, ax = "start", x + 11
            x0, x1 = ax, ax + w
        else:
            anchor, ax = "end", x - 11
            x0, x1 = ax - w, ax
        labels.append({"name": name, "color": color, "dotx": x, "doty": y,
                       "ly": y, "ax": ax, "x0": x0, "x1": x1, "anchor": anchor})

# relax label y to remove overlaps among boxes whose x-ranges intersect
for _ in range(400):
    moved = False
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            a, b = labels[i], labels[j]
            if a["x1"] <= b["x0"] or b["x1"] <= a["x0"]:
                continue
            dv = a["ly"] - b["ly"]
            need = LH + GAP
            if abs(dv) < need:
                push = (need - abs(dv)) / 2 + 0.1
                s = 1 if dv >= 0 else -1
                a["ly"] += s * push
                b["ly"] -= s * push
                moved = True
    if not moved:
        break
for a in labels:                         # keep labels inside the plot band
    a["ly"] = max(T + 8, min(PB - 8, a["ly"]))

# draw: connectors (under), dots, then label text (on top)
for a in labels:
    if abs(a["ly"] - a["doty"]) > 9:
        parts.append(f'<line x1="{a["dotx"]:.1f}" y1="{a["doty"]:.1f}" x2="{a["ax"]:.1f}" y2="{a["ly"]:.1f}" '
                     f'stroke="{a["color"]}" stroke-width="1" stroke-opacity="0.5"/>')
for a in labels:
    parts.append(f'<circle cx="{a["dotx"]:.1f}" cy="{a["doty"]:.1f}" r="6.5" fill="{a["color"]}" stroke="#0d1117" stroke-width="2"/>')
for a in labels:
    parts.append(halo(a["ax"] + (-2 if a["anchor"] == "end" else 2), a["ly"] + 4,
                      a["name"], 13.5, lighten(a["color"], 0.55), anchor=a["anchor"]))

# ---- end-of-axis descriptors only (no axis names), placed in the padding ----
parts.append(halo(px(-VR) + 6, CY - 9, "◀ long time ago", 15, "#aeb6c2", anchor="start"))
parts.append(halo(px(VR) - 4, CY - 9, "everyday usage ▶", 15, "#aeb6c2", anchor="end"))

parts.append(halo(CX + 16, py(-110), "◀ touched a bit", 15, "#aeb6c2", anchor="start",
                  extra=f'transform="rotate(-90 {CX+16:.0f} {py(-110):.0f})"'))
parts.append(halo(CX + 16, py(110), "expertise ▶", 15, "#aeb6c2", anchor="end",
                  extra=f'transform="rotate(-90 {CX+16:.0f} {py(110):.0f})"'))

parts.append('</svg>')

with open("assets/skills.svg", "w") as f:
    f.write("\n".join(parts))
n = sum(len(s) for _, s in GROUPS.values())
print(f"wrote assets/skills.svg with {n} skills across {len(GROUPS)} groups")
