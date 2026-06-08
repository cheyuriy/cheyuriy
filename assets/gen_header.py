#!/usr/bin/env python3
"""Generate assets/header.svg — animated retro-wave / cyberpunk skyline banner.

- small flat "cheyuriy's github" title in the upper-left corner
- a city silhouette that grows taller toward the right
- edges fade to GitHub-dark (#0d1117) so the banner blends into the page
- subtle auto-animations only (twinkling stars, pulsing sun, flickering windows)
  — no hover/JS, since GitHub serves SVGs through Camo as <img>.

Run:  python3 assets/gen_header.py
"""
import random

W, H = 1200, 320
GH = "#0d1117"            # GitHub dark-theme background
Y0 = H                    # skyline baseline
random.seed(7)

WIN_COLORS = ["#ffd479", "#ffd479", "#ffc04d", "#79e6ff", "#ff7bd5"]
NEON = ["#36e0ff", "#ff5fbf"]

parts = []


def building(bx, bw, bh, fill, lit=0.0, idx=0, neon=None, antenna=False):
    """Return svg for one building with optional windows / neon rim / antenna."""
    by = Y0 - bh
    out = [f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh+2:.0f}" fill="{fill}"/>']
    if neon:
        out.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="3" fill="{neon}" opacity="0.85"/>')
        out.append(f'<rect x="{bx:.0f}" y="{by-2:.0f}" width="{bw:.0f}" height="6" fill="{neon}" opacity="0.18"/>')
    if antenna:
        tx = bx + bw / 2
        out.append(f'<line x1="{tx:.0f}" y1="{by:.0f}" x2="{tx:.0f}" y2="{by-20:.0f}" stroke="#3a4252" stroke-width="2"/>')
        out.append(f'<circle class="blink" cx="{tx:.0f}" cy="{by-22:.0f}" r="2.6" fill="#ff4d5e" '
                   f'style="animation-delay:{(idx%5)*0.4:.1f}s"/>')
    if lit:
        cell, m = 10, 6
        cols = int((bw - 2 * m) // cell)
        rows = int((bh - 2 * m) // cell)
        for r in range(rows):
            for c in range(cols):
                if random.random() > lit:
                    continue
                wx = bx + m + c * cell
                wy = by + m + r * cell
                col = random.choice(WIN_COLORS)
                if random.random() < 0.16:        # some windows flicker
                    out.append(f'<rect class="flk" x="{wx:.0f}" y="{wy:.0f}" width="3.4" height="4.2" '
                               f'fill="{col}" style="animation-delay:{(idx*7+r*3+c)%40*0.11:.2f}s"/>')
                else:
                    out.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="3.4" height="4.2" fill="{col}" opacity="0.9"/>')
    return "".join(out)


# ---- skyline: two depth layers, heights ramp up toward the right ----
def layer(fill, base, growth, rand, wmin, wmax, lit, neon_thresh=None, gap=0):
    segs = []
    x = -20
    i = 0
    while x < W + 20:
        bw = random.randint(wmin, wmax)
        ramp = base + growth * (x / W) + random.randint(0, rand)
        bh = max(24, int(ramp))
        neon = (random.choice(NEON) if neon_thresh and bh > neon_thresh else None)
        antenna = bh > 175 and x > 820 and random.random() < 0.7
        segs.append(building(x, bw, bh, fill, lit=lit, idx=i, neon=neon, antenna=antenna))
        x += bw + gap
        i += 1
    return "".join(segs)


# stars
stars = []
for _ in range(26):
    sx, sy, sr = random.randint(20, W - 20), random.randint(10, 150), random.uniform(0.7, 1.7)
    stars.append(f'<circle class="star" cx="{sx}" cy="{sy}" r="{sr:.1f}" '
                 f'style="animation-delay:{random.uniform(0,3):.1f}s"/>')

defs = f'''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{GH}"/>
    <stop offset="32%" stop-color="#1b1030"/>
    <stop offset="56%" stop-color="#3a1457"/>
    <stop offset="76%" stop-color="#7a1f63"/>
    <stop offset="92%" stop-color="#b83271"/>
    <stop offset="100%" stop-color="#ff7a44"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffe27a"/><stop offset="55%" stop-color="#ff9d54"/>
    <stop offset="100%" stop-color="#ff5f86"/>
  </linearGradient>
  <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#ff9d54" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#ff9d54" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{GH}"/><stop offset="100%" stop-color="{GH}" stop-opacity="0"/></linearGradient>
  <linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{GH}" stop-opacity="0"/><stop offset="100%" stop-color="{GH}"/></linearGradient>
  <linearGradient id="fadeT" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{GH}"/><stop offset="100%" stop-color="{GH}" stop-opacity="0"/></linearGradient>
  <linearGradient id="fadeB" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{GH}" stop-opacity="0"/><stop offset="100%" stop-color="{GH}"/></linearGradient>
  <mask id="sunStripes">
    <rect x="0" y="0" width="{W}" height="{H}" fill="white"/>
    <g fill="black">
      <rect x="190" y="206" width="220" height="4"/><rect x="190" y="214" width="220" height="5"/>
      <rect x="190" y="224" width="220" height="6"/><rect x="190" y="236" width="220" height="8"/>
    </g>
  </mask>
  <style>
    .star{{animation:tw 3s ease-in-out infinite}}
    @keyframes tw{{0%,100%{{opacity:.2}}50%{{opacity:1}}}}
    #sun{{animation:pulse 5s ease-in-out infinite;transform-origin:300px 230px}}
    @keyframes pulse{{0%,100%{{opacity:.92}}50%{{opacity:1;transform:scale(1.02)}}}}
    .flk{{animation:flk 4s steps(1,end) infinite}}
    @keyframes flk{{0%,100%{{opacity:1}}45%{{opacity:.12}}50%{{opacity:1}}72%{{opacity:.45}}}}
    .blink{{animation:bl 1.8s ease-in-out infinite}}
    @keyframes bl{{0%,100%{{opacity:1}}50%{{opacity:.15}}}}
  </style>
</defs>'''

parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
             f'font-family="\'Trebuchet MS\',\'Segoe UI\',Verdana,sans-serif">')
parts.append(defs)
parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{GH}"/>')
parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#sky)"/>')
parts.append('<g>' + "".join(stars) + '</g>')
# retro sun, low and behind the skyline
parts.append('<g id="sun"><circle cx="300" cy="230" r="150" fill="url(#sunGlow)"/>'
             '<circle cx="300" cy="230" r="86" fill="url(#sun)" mask="url(#sunStripes)"/></g>')
# back layer (purple, lit by sky) then front layer (dark, blends into base)
parts.append('<g>' + layer("#241a3d", base=34, growth=120, rand=28, wmin=46, wmax=92, lit=0.0) + '</g>')
parts.append('<g>' + layer("#0c0f17", base=52, growth=150, rand=40, wmin=30, wmax=78, lit=0.42,
                           neon_thresh=120, gap=2) + '</g>')
# edge fades -> blend into GitHub dark
parts.append(f'<rect x="0" y="0" width="150" height="{H}" fill="url(#fadeL)"/>')
parts.append(f'<rect x="{W-150}" y="0" width="150" height="{H}" fill="url(#fadeR)"/>')
parts.append(f'<rect x="0" y="0" width="{W}" height="70" fill="url(#fadeT)"/>')
parts.append(f'<rect x="0" y="{H-50}" width="{W}" height="50" fill="url(#fadeB)"/>')
# flat title, upper-left
parts.append('<text x="30" y="44" fill="#e6edf3" font-size="24" font-weight="600" letter-spacing="1.2" '
             'style="paint-order:stroke" stroke="#0d1117" stroke-width="3" stroke-linejoin="round">'
             '<tspan fill="#ff5fbf">&gt;</tspan> cheyuriy\'s github</text>')
parts.append('</svg>')

with open("assets/header.svg", "w") as f:
    f.write("\n".join(parts))
print("wrote assets/header.svg")
