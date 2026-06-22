#!/usr/bin/env python3
"""Generates assets/nebula.svg: a painterly nebula built from hundreds of
soft overlapping circles at varying scale (the actual technique used for
digital nebula art), not flat vector blobs."""
import random
import math

random.seed(7)

W, H = 1600, 1000

def cluster(cx, cy, base_r, color, n, op_lo, op_hi, spread_x, spread_y, r_lo=0.15, r_hi=1.0):
    parts = []
    for _ in range(n):
        angle = random.uniform(0, math.tau)
        # bias toward center using sqrt falloff for denser core
        t = random.random() ** 1.6
        x = cx + spread_x * t * math.cos(angle)
        y = cy + spread_y * t * math.sin(angle)
        r = base_r * random.uniform(r_lo, r_hi)
        op = random.uniform(op_lo, op_hi)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}" opacity="{op:.3f}"/>')
    return parts

svg_parts = []
svg_parts.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">')
svg_parts.append('<defs>')
svg_parts.append('''
  <radialGradient id="vignette" cx="50%" cy="42%" r="75%">
    <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="62%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#05040a" stop-opacity="0.82"/>
  </radialGradient>
  <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#fdf0d8" stop-opacity="0.95"/>
    <stop offset="18%" stop-color="#f0caa0" stop-opacity="0.55"/>
    <stop offset="45%" stop-color="#caa06f" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#caa06f" stop-opacity="0"/>
  </radialGradient>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" result="noise" seed="3"/>
    <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.04 0"/>
  </filter>
  <filter id="blurXXL" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="80"/>
  </filter>
  <filter id="blurXL" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="55"/>
  </filter>
  <filter id="blurL" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="38"/>
  </filter>
  <filter id="blurM" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="22"/>
  </filter>
  <filter id="blurS" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="10"/>
  </filter>''')
svg_parts.append('</defs>')

# base sky
svg_parts.append(f'<rect width="{W}" height="{H}" fill="#0a0814"/>')

def wrap(parts, blur_id):
    return f'<g filter="url(#{blur_id})">' + ''.join(parts) + '</g>'

# Deep background wash — large, very soft, sets the overall color mood
bg_parts = []
bg_parts.extend(cluster(880, 420, 380, '#241a42', 110, 0.035, 0.075, 600, 400, 0.55, 1.0))
bg_parts.extend(cluster(500, 600, 340, '#3a1f3e', 90, 0.035, 0.07, 520, 370, 0.55, 1.0))
bg_parts.extend(cluster(1240, 560, 320, '#1f2a52', 90, 0.035, 0.07, 500, 350, 0.55, 1.0))
bg_parts.extend(cluster(800, 500, 420, '#160f2c', 60, 0.03, 0.06, 650, 430, 0.6, 1.0))
svg_parts.append(wrap(bg_parts, 'blurXXL'))

# Mid dust structure — indigo/violet drifting mass, asymmetric, off-center like real nebula photos
mid_parts = []
mid_parts.extend(cluster(760, 380, 150, '#6a3f9e', 90, 0.06, 0.14, 420, 260, 0.3, 0.9))
mid_parts.extend(cluster(880, 470, 130, '#8a4a7e', 80, 0.06, 0.13, 360, 230, 0.3, 0.85))
mid_parts.extend(cluster(620, 480, 120, '#4a3a8a', 70, 0.06, 0.12, 320, 220, 0.3, 0.85))
mid_parts.extend(cluster(1020, 360, 110, '#a8567a', 60, 0.05, 0.11, 300, 200, 0.3, 0.8))
svg_parts.append(wrap(mid_parts, 'blurL'))

# Warm core bleed — gold/amber threading through the violet, your accent color living IN the art
warm_parts = []
warm_parts.extend(cluster(820, 420, 110, '#caa06f', 110, 0.06, 0.15, 240, 160, 0.35, 0.85))
warm_parts.extend(cluster(880, 460, 90, '#e8c9a0', 90, 0.06, 0.16, 190, 125, 0.3, 0.7))
svg_parts.append(wrap(warm_parts, 'blurM'))

# Fine texture pass — soft inner highlight, heavily blurred to avoid visible bubbles
fine_parts = []
fine_parts.extend(cluster(800, 410, 60, '#f0d9b8', 50, 0.05, 0.11, 260, 170, 0.4, 0.9))
fine_parts.extend(cluster(700, 500, 50, '#9a6fb0', 40, 0.04, 0.09, 220, 150, 0.4, 0.85))
fine_parts.extend(cluster(950, 350, 50, '#7a8fc0', 35, 0.04, 0.09, 210, 145, 0.4, 0.85))
svg_parts.append(wrap(fine_parts, 'blurL'))

# Bright core point — the "star" the nebula is born around
svg_parts.append('<ellipse cx="810" cy="415" rx="260" ry="190" fill="url(#coreGlow)"/>')
svg_parts.append('<circle cx="810" cy="415" r="5" fill="#fffaf0"/>')
svg_parts.append('<circle cx="810" cy="415" r="16" fill="#fdf0d8" opacity="0.5"/>')
svg_parts.append('<circle cx="810" cy="415" r="42" fill="#f0caa0" opacity="0.22"/>')

# Secondary smaller bright points scattered (distant star-forming regions)
for (x, y, r, c) in [(1280, 230, 2, '#e8d8c0'), (340, 250, 1.8, '#d8c8e8'), (1180, 700, 2, '#e8c9a0'), (260, 720, 1.6, '#c8d8f0')]:
    svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{r*3.5}" fill="{c}" opacity="0.10"/>')
    svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="0.8"/>')

# vignette + subtle grain to kill any banding/flatness
svg_parts.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
svg_parts.append(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.5"/>')

svg_parts.append('</svg>')

with open('assets/nebula.svg', 'w') as f:
    f.write('\n'.join(svg_parts))

print(f"Generated nebula.svg with {len(svg_parts)} elements")
