"""Build the Luno Health logo kit (Lumen direction).

Usage (from repo root):  pip install fonttools pillow
                         python tools/brand_build.py
Outputs SVG + PNG to assets/brand/, favicons to the site root and assets/brand/favicon/.
PNG rendering uses headless Chrome (path below) for exact SVG fidelity.
"""
import math, pathlib, subprocess, tempfile, json, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'brand'; SVG = OUT / 'svg'; PNG = OUT / 'png'; FAV = OUT / 'favicon'
for d in (SVG, PNG, FAV): d.mkdir(parents=True, exist_ok=True)
CHROME = os.environ.get('CHROME', r'C:\Program Files\Google\Chrome\Application\chrome.exe')

# ---- Palette ----
NIGHT, DEEP, TEAL, MINT, PEARL = '#061a19', '#0b2b29', '#11a392', '#8fe3d5', '#f7f4ee'
SUB_ON_LIGHT, SUB_ON_DARK = '#5d7a77', '#9fb8b4'

# ---- Type ----
_mr = ROOT / 'tools' / 'fonts' / 'Manrope.ttf'
def _inst(w): return instantiateVariableFont(TTFont(_mr), {'wght': w})
WM, WM_L = _inst(650), _inst(400)

def text(fnt, s, size, tracking=0.0):
    gs = fnt.getGlyphSet(); cmap = fnt.getBestCmap(); k = size / fnt['head'].unitsPerEm
    pen = SVGPathPen(gs); x = 0; hm = fnt['hmtx']
    for i, ch in enumerate(s):
        g = cmap[ord(ch)]; gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        x += hm[g][0] * k + (tracking * size if i < len(s) - 1 else 0)
    return pen.getCommands(), x
XH = WM['OS/2'].sxHeight / WM['head'].unitsPerEm
ASC = 0.73  # cap/ascender height of "l" relative to size (Manrope)

# ---- Mark geometry (100 x 100) ----
def _flags(c, p0, p1, q):
    a = lambda p: math.atan2(p[1] - c[1], p[0] - c[0]) % (2 * math.pi)
    a0, a1, aq = a(p0), a(p1), a(q); dp = (a1 - a0) % (2 * math.pi); dq = (aq - a0) % (2 * math.pi)
    sweep, span = (1, dp) if dq < dp else (0, 2 * math.pi - dp)
    return (1 if span > math.pi else 0), sweep

def crescent(cx, cy, R, dx, dy, r):
    d = math.hypot(dx, dy); a = (R*R - r*r + d*d) / (2*d); h = math.sqrt(R*R - a*a); ux, uy = dx/d, dy/d
    mx, my = cx + a*ux, cy + a*uy; p1 = (mx - h*uy, my + h*ux); p2 = (mx + h*uy, my - h*ux)
    la, s1 = _flags((cx, cy), p1, p2, (cx - R*ux, cy - R*uy))
    lb, s2 = _flags((cx+dx, cy+dy), p2, p1, (cx+dx - r*ux, cy+dy - r*uy))
    return f'M{p1[0]:.3f} {p1[1]:.3f}A{R} {R} 0 {la} {s1} {p2[0]:.3f} {p2[1]:.3f}A{r} {r} 0 {lb} {s2} {p1[0]:.3f} {p1[1]:.3f}Z'

CRES = crescent(50, 50, 46, -22, 0, 44)
_n = [0]
def mark(variant):
    """variant: color | color-dark (for dark backgrounds) | mono-<hex>"""
    _n[0] += 1; gid = f'lh{_n[0]}'
    if variant.startswith('mono'):
        col = variant.split('-', 1)[1]
        return (f'<defs><mask id="{gid}"><circle cx="50" cy="50" r="46" fill="#fff"/>'
                f'<circle cx="28" cy="50" r="44" fill="none" stroke="#000" stroke-width="4.5"/></mask></defs>'
                f'<circle cx="50" cy="50" r="46" fill="{col}" mask="url(#{gid})"/>')
    disc = DEEP if variant == 'color' else PEARL
    return (f'<defs><linearGradient id="{gid}" x1="96" y1="70" x2="62" y2="18" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{MINT}"/></linearGradient></defs>'
            f'<circle cx="50" cy="50" r="46" fill="{disc}"/><path d="{CRES}" fill="url(#{gid})"/>')

def g(x, y, s, inner): return f'<g transform="translate({x:.3f} {y:.3f}) scale({s/100:.5f})">{inner}</g>'
def svg(w, h, body, title='Luno Health'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')

# Wordmark "luno health": Manrope 650 tightened + Manrope 400
def wordmark_paths(size, ink, sub):
    d1, w1 = text(WM, 'luno', size, -0.045); d2, w2 = text(WM_L, 'health', size, -0.03); gap = size * 0.26
    return f'<path d="{d1}" fill="{ink}"/><g transform="translate({w1 + gap:.3f} 0)"><path d="{d2}" fill="{sub}"/></g>', w1 + gap + w2

def colours(theme):
    if theme == 'color': return 'color', DEEP, SUB_ON_LIGHT
    if theme == 'white': return 'color-dark', PEARL, SUB_ON_DARK
    col = theme.split('-', 1)[1]; return f'mono-{col}', col, col

# The mark is 92 units tall per 64 units of type: optical balance from round 3
def horizontal(theme, M=100):
    mv, ink, sub = colours(theme); size = M * 64 / 92; gap = M * 26 / 92
    wp, W = wordmark_paths(size, ink, sub); base = M / 2 + XH * size / 2
    return svg(M + gap + W, M, g(0, 0, M, mark(mv)) + f'<g transform="translate({M + gap:.3f} {base:.3f})">{wp}</g>')

def stacked(theme, M=100):
    mv, ink, sub = colours(theme); size = M * 0.45
    wp, W = wordmark_paths(size, ink, sub); Wt = max(W, M); gap = M * 0.28
    H = M + gap + ASC * size + 0.22 * size
    return svg(Wt, H, g((Wt - M) / 2, 0, M, mark(mv)) + f'<g transform="translate({(Wt - W)/2:.3f} {M + gap + ASC*size:.3f})">{wp}</g>')

def wordmark_only(theme, size=100):
    mv, ink, sub = colours(theme); wp, W = wordmark_paths(size, ink, sub)
    top = ASC * size; return svg(W, top + 0.22 * size, f'<g transform="translate(0 {top:.3f})">{wp}</g>')

def mark_only(theme): return svg(100, 100, mark(colours(theme)[0]))

def app_icon(bg=NIGHT, inner='color-dark', pad=0.2, radius=0.225, n=1024):
    r = f'<rect width="{n}" height="{n}" rx="{n*radius:.1f}" fill="{bg}"/>' if radius is not None else f'<rect width="{n}" height="{n}" fill="{bg}"/>'
    return svg(n, n, r + g(n*pad, n*pad, n*(1-2*pad), mark(inner)))

FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><style>'
               '.d{fill:' + DEEP + '}@media (prefers-color-scheme:dark){.d{fill:' + PEARL + '}}</style>'
               '<defs><linearGradient id="g" x1="96" y1="70" x2="62" y2="18" gradientUnits="userSpaceOnUse">'
               f'<stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{MINT}"/></linearGradient></defs>'
               f'<circle class="d" cx="50" cy="50" r="46"/><path d="{CRES}" fill="url(#g)"/></svg>\n')

# ---- Write SVGs ----
files = {}
def put(name, content): (SVG / name).write_text(content, encoding='utf-8'); files[name] = content; return SVG / name
for theme, suf in [('color', ''), ('white', '-white'), (f'mono-{DEEP}', '-mono-dark'), ('mono-#ffffff', '-mono-white')]:
    put(f'luno-logo-horizontal{suf}.svg', horizontal(theme))
    put(f'luno-logo-stacked{suf}.svg', stacked(theme))
    put(f'luno-mark{suf}.svg', mark_only(theme))
    put(f'luno-wordmark{suf}.svg', wordmark_only(theme))
put('luno-app-icon.svg', app_icon())
put('luno-app-icon-light.svg', app_icon(bg=PEARL, inner='color'))
put('luno-avatar.svg', app_icon(radius=None, pad=0.24))           # square, circle-safe for Instagram/WhatsApp
(FAV / 'favicon.svg').write_text(FAVICON_SVG, encoding='utf-8')

# ---- Render PNGs with headless Chrome ----
def render(svg_path, out_png, long_side):
    s = svg_path.read_text(encoding='utf-8')
    import re
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    k = long_side / max(w, h); W, H = max(1, round(w * k)), max(1, round(h * k))
    with tempfile.TemporaryDirectory() as td:
        page = pathlib.Path(td) / 'p.html'
        page.write_text(f'<html><body style="margin:0;background:transparent"><img src="{svg_path.as_uri()}" '
                        f'style="display:block;width:{W}px;height:{H}px"></body></html>', encoding='utf-8')
        shot = pathlib.Path(td) / 's.png'
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                        '--default-background-color=00000000', f'--window-size={W},{H}', '--virtual-time-budget=2000',
                        f'--user-data-dir={td}/prof', f'--screenshot={shot}', page.as_uri()],
                       check=True, capture_output=True)
        Image.open(shot).convert('RGBA').crop((0, 0, W, H)).save(out_png, optimize=True)
    return out_png

big = {}
for name in files:
    stem = name[:-4]
    if 'app-icon' in name or 'avatar' in name:
        big[stem] = render(SVG / name, PNG / f'{stem}-1024.png', 1024)
    elif 'mark' in name:
        big[stem] = render(SVG / name, PNG / f'{stem}-1024.png', 1024)
        for s in (512, 256, 128, 64):
            Image.open(big[stem]).resize((s, s), Image.LANCZOS).save(PNG / f'{stem}-{s}.png', optimize=True)
    else:
        big[stem] = render(SVG / name, PNG / f'{stem}-2400w.png', 2400)
        im = Image.open(big[stem])
        for wdt in (1200, 600):
            im.resize((wdt, round(im.height * wdt / im.width)), Image.LANCZOS).save(PNG / f'{stem}-{wdt}w.png', optimize=True)
# Instagram / WhatsApp profile picture
Image.open(big['luno-avatar']).resize((1080, 1080), Image.LANCZOS).save(PNG / 'luno-avatar-1080.png', optimize=True)

# ---- Favicons ----
icon = Image.open(big['luno-app-icon'])
mk = Image.open(big['luno-mark'])
icon.resize((180, 180), Image.LANCZOS).save(FAV / 'apple-touch-icon.png', optimize=True)
for s in (192, 512): icon.resize((s, s), Image.LANCZOS).save(FAV / f'icon-{s}.png', optimize=True)
for s in (16, 32, 48): mk.resize((s, s), Image.LANCZOS).save(FAV / f'favicon-{s}.png', optimize=True)
mk.resize((256, 256), Image.LANCZOS).save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
(FAV / 'site.webmanifest').write_text(json.dumps({
    'name': 'Luno Health', 'short_name': 'Luno', 'start_url': '/', 'display': 'standalone',
    'background_color': NIGHT, 'theme_color': DEEP,
    'icons': [{'src': '/assets/brand/favicon/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
              {'src': '/assets/brand/favicon/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=2), encoding='utf-8')
print('SVGs:', len(files), '| PNGs:', len(list(PNG.glob('*.png'))), '| favicons:', len(list(FAV.iterdir())) + 1)
