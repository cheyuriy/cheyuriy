#!/usr/bin/env python3
"""Generate assets/interests.svg — interest pills with custom icons.

8 pills, two centered rows of four, each with a hand-drawn icon + label.
Edit INTERESTS (label, accent color, icon key) and run:
    python3 assets/gen_interests.py
"""
import math

# label, accent color, icon key
INTERESTS = [
    ("Programming",  "#4C8DFF", "terminal"),
    ("Data",         "#F2545B", "database"),
    ("IT Products",  "#3FB950", "globe"),
    ("Open Source",  "#C9D1D9", "github"),
    ("Pragmatic AI", "#B36BFF", "neural"),
    ("Technologies", "#F5A623", "gear"),
    ("Music",        "#E255C9", "guitar"),
    ("Games",        "#66C0F4", "steam"),
]

BG = "#161b22"          # opaque pill fill (consistent in light/dark themes)
TXT = "#e6edf3"
FS = 19                 # label font size
CHARW = 10.2            # est. char width for layout
PADL, ICON, GAPI, PADR = 18, 28, 12, 22
BH, BGAP, ROWGAP, TOP = 56, 20, 18, 12

# ---- icons: each returns markup drawn in a 24x24 box using color `c` ----
GITHUB = ("M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 "
          "0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 "
          "17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 "
          "1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.305-5.467-1.334-5.467-5.931 "
          "0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 "
          "1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 "
          "3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 "
          "5.624-5.479 5.921.43.372.823 1.102.823 2.222 0 1.606-.014 2.898-.014 3.293 0 .322.216.694."
          "825.576C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12")
STEAM = ("M11.979 0C5.678 0 .511 4.86.022 11.037l6.432 2.658c.545-.371 1.203-.59 1.912-.59.063 0 "
         ".125.004.188.006l2.861-4.142V8.91c0-2.495 2.028-4.524 4.524-4.524 2.494 0 4.524 2.031 "
         "4.524 4.527s-2.03 4.525-4.524 4.525h-.105l-4.076 2.911c0 .052.004.105.004.159 0 1.875-1.515 "
         "3.396-3.39 3.396-1.635 0-3.016-1.173-3.331-2.727L.436 15.27C1.862 20.307 6.486 24 11.979 "
         "24c6.627 0 11.999-5.373 11.999-12S18.605 0 11.979 0zM7.54 18.21l-1.473-.61c.262.543.714.999 "
         "1.314 1.25 1.297.539 2.793-.076 3.332-1.375.263-.63.264-1.319.005-1.949s-.75-1.121-1.377-1.383"
         "c-.624-.26-1.29-.249-1.878-.03l1.523.63c.956.4 1.409 1.5 1.009 2.455-.397.957-1.497 1.41-2.454 "
         "1.011H7.54zm11.415-9.303c0-1.662-1.353-3.015-3.015-3.015-1.665 0-3.015 1.353-3.015 3.015 0 "
         "1.665 1.35 3.015 3.015 3.015 1.663 0 3.015-1.35 3.015-3.015zm-5.273-.005c0-1.252 1.013-2.266 "
         "2.265-2.266 1.249 0 2.266 1.014 2.266 2.266 0 1.251-1.017 2.265-2.266 2.265-1.253 0-2.265-1.014"
         "-2.265-2.265z")


def gear_path():
    teeth, ro, ri, cx, cy = 8, 11.2, 8.6, 12, 12
    p = []
    for i in range(teeth):
        a0 = 2 * math.pi * i / teeth
        for frac, r in ((0.0, ri), (0.12, ro), (0.38, ro), (0.5, ri)):
            a = a0 + 2 * math.pi / teeth * frac
            p.append(f"{cx + r*math.cos(a):.2f},{cy + r*math.sin(a):.2f}")
    return "M" + " L".join(p) + " Z"


def neural():
    cols = {5: (7, 17), 12: (5, 12, 19), 19: (8, 16)}
    layers = list(cols.items())
    lines = []
    for (x1, ys1), (x2, ys2) in zip(layers, layers[1:]):
        for a in ys1:
            for b in ys2:
                lines.append(f'<line x1="{x1}" y1="{a}" x2="{x2}" y2="{b}"/>')
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.9"/>' for x, ys in cols.items() for y in ys)
    return ('<g stroke="{c}" stroke-width="1.2" stroke-opacity="0.55">' + "".join(lines) + "</g>"
            + '<g fill="{c}">' + dots + "</g>")


def icon(key, c):
    if key == "terminal":
        return (f'<rect x="1.5" y="3" width="21" height="18" rx="3.2" fill="none" stroke="{c}" stroke-width="2"/>'
                f'<polyline points="6,9 9.6,12.5 6,16" fill="none" stroke="{c}" stroke-width="2" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<line x1="12.5" y1="16" x2="17" y2="16" stroke="{c}" stroke-width="2" stroke-linecap="round"/>')
    if key == "database":
        return (f'<g fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round">'
                f'<ellipse cx="12" cy="5" rx="8" ry="3"/>'
                f'<path d="M4 5 V19 a8 3 0 0 0 16 0 V5"/>'
                f'<path d="M4 12 a8 3 0 0 0 16 0"/></g>')
    if key == "globe":
        return (f'<g fill="none" stroke="{c}" stroke-width="2">'
                f'<circle cx="12" cy="12" r="9.3"/>'
                f'<ellipse cx="12" cy="12" rx="3.8" ry="9.3"/>'
                f'<line x1="2.7" y1="12" x2="21.3" y2="12"/>'
                f'<path d="M4.4 7 H19.6 M4.4 17 H19.6"/></g>')
    if key == "github":
        return f'<path fill="{c}" d="{GITHUB}"/>'
    if key == "neural":
        return neural().replace("{c}", c)
    if key == "gear":
        return (f'<path fill="{c}" d="{gear_path()}"/>'
                f'<circle cx="12" cy="12" r="3.4" fill="{BG}"/>')
    if key == "guitar":
        return (f'<g fill="{c}"><circle cx="8.5" cy="16.2" r="6.1"/>'
                f'<circle cx="11" cy="9.8" r="4.4"/></g>'
                f'<circle cx="8.5" cy="15.6" r="2.2" fill="{BG}"/>'
                f'<line x1="13.2" y1="7.6" x2="19.8" y2="2.6" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>'
                f'<line x1="18.6" y1="1.4" x2="21.2" y2="3.4" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>')
    if key == "steam":
        return f'<path fill="{c}" fill-rule="evenodd" d="{STEAM}"/>'
    return ""


def badge_w(label):
    return PADL + ICON + GAPI + len(label) * CHARW + PADR


rows = [INTERESTS[:4], INTERESTS[4:]]
row_w = [sum(badge_w(l) for l, _, _ in r) + BGAP * (len(r) - 1) for r in rows]
W = int(max(row_w)) + 40
H = TOP + BH + ROWGAP + BH + TOP

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="\'Segoe UI\',Verdana,sans-serif">']

for ri, row in enumerate(rows):
    y = TOP + ri * (BH + ROWGAP)
    x = (W - row_w[ri]) / 2
    for label, color, key in row:
        bw = badge_w(label)
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{BH}" rx="14" '
                     f'fill="{BG}" stroke="{color}" stroke-width="1.8"/>')
        s = ICON / 24
        parts.append(f'<g transform="translate({x+PADL:.1f},{y+(BH-ICON)/2:.1f}) scale({s:.3f})">{icon(key, color)}</g>')
        parts.append(f'<text x="{x+PADL+ICON+GAPI:.1f}" y="{y+BH/2+6.5:.1f}" fill="{TXT}" '
                     f'font-size="{FS}" font-weight="600">{label}</text>')
        x += bw + BGAP

parts.append("</svg>")
with open("assets/interests.svg", "w") as f:
    f.write("\n".join(parts))
print(f"wrote assets/interests.svg ({W}x{H})")
