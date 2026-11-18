"""Generate assets/brand/index.html: a downloadable logo kit page. Run after brand_build.py."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent; B = ROOT / 'assets' / 'brand'
NIGHT, DEEP, TEAL, MINT, PEARL = '#061a19', '#0b2b29', '#11a392', '#8fe3d5', '#f7f4ee'

def tile(svg, bg, label, pngs):
    links = ' · '.join(f'<a href="png/{p}" download>{p.split("-")[-1].replace(".png", "").upper()} PNG</a>' for p in pngs)
    return (f'<figure class="t" style="background:{bg}"><img src="svg/{svg}" alt="{label}"></figure>'
            f'<figcaption><b>{label}</b><span><a href="svg/{svg}" download>SVG</a> · {links}</span></figcaption>')

def group(title, desc, items):
    cells = ''.join(f'<div class="c">{tile(*i)}</div>' for i in items)
    return f'<section><h2>{title}</h2><p>{desc}</p><div class="grid">{cells}</div></section>'

W, D = '#ffffff', NIGHT
def pngs(stem, kind):
    return [f'{stem}-{s}.png' for s in (('2400w', '1200w', '600w') if kind == 'wide' else ('1024', '512', '256', '128', '64'))]

sections = [
 group('Primary logo · horizontal', 'Use this first: website header, documents, email signatures, presentations. Keep clear space equal to the height of the crescent around it.', [
   ('luno-logo-horizontal.svg', W, 'On light', pngs('luno-logo-horizontal', 'wide')),
   ('luno-logo-horizontal-white.svg', D, 'On dark', pngs('luno-logo-horizontal-white', 'wide')),
   ('luno-logo-horizontal-mono-dark.svg', W, 'One colour, dark', pngs('luno-logo-horizontal-mono-dark', 'wide')),
   ('luno-logo-horizontal-mono-white.svg', D, 'One colour, white', pngs('luno-logo-horizontal-mono-white', 'wide'))]),
 group('Stacked logo', 'For square or centred layouts: signage, posters, the first slide of a deck.', [
   ('luno-logo-stacked.svg', W, 'On light', pngs('luno-logo-stacked', 'wide')),
   ('luno-logo-stacked-white.svg', D, 'On dark', pngs('luno-logo-stacked-white', 'wide')),
   ('luno-logo-stacked-mono-dark.svg', W, 'One colour, dark', pngs('luno-logo-stacked-mono-dark', 'wide')),
   ('luno-logo-stacked-mono-white.svg', D, 'One colour, white', pngs('luno-logo-stacked-mono-white', 'wide'))]),
 group('Mark (short logo)', 'The Lumen moon on its own: favicons, stamps, watermarks, small spaces.', [
   ('luno-mark.svg', W, 'On light', pngs('luno-mark', 'sq')),
   ('luno-mark-white.svg', D, 'On dark', pngs('luno-mark-white', 'sq')),
   ('luno-mark-mono-dark.svg', W, 'One colour, dark', pngs('luno-mark-mono-dark', 'sq')),
   ('luno-mark-mono-white.svg', D, 'One colour, white', pngs('luno-mark-mono-white', 'sq'))]),
 group('Wordmark', 'The name alone, for places where the mark already appears nearby.', [
   ('luno-wordmark.svg', W, 'On light', pngs('luno-wordmark', 'wide')),
   ('luno-wordmark-white.svg', D, 'On dark', pngs('luno-wordmark-white', 'wide')),
   ('luno-wordmark-mono-dark.svg', W, 'One colour, dark', pngs('luno-wordmark-mono-dark', 'wide')),
   ('luno-wordmark-mono-white.svg', D, 'One colour, white', pngs('luno-wordmark-mono-white', 'wide'))]),
 group('App icon & profile picture', 'Profile picture for Instagram, WhatsApp Business, Facebook and Telegram (square, safe inside a circle crop).', [
   ('luno-avatar.svg', '#eeebe5', 'Profile picture', ['luno-avatar-1080.png', 'luno-avatar-1024.png']),
   ('luno-app-icon.svg', '#eeebe5', 'App icon, dark', ['luno-app-icon-1024.png']),
   ('luno-app-icon-light.svg', '#eeebe5', 'App icon, light', ['luno-app-icon-light-1024.png'])]),
]
pal = ''.join(f'<div class="sw" style="background:{c}"><span>{n}<br>{c}</span></div>' for n, c in
              [('Night', NIGHT), ('Deep Green', DEEP), ('Luno Teal', TEAL), ('Mint Light', MINT), ('Pearl', PEARL)])

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brand assets | Luno Health</title><meta name="robots" content="noindex">
<link rel="icon" href="favicon/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#eeebe5;color:#101615;font:15px/1.6 Manrope,"Segoe UI",sans-serif}}
.wrap{{max-width:1200px;margin:0 auto;padding:40px 24px 80px}}
header{{background:radial-gradient(120% 140% at 70% 10%,#123e3a 0%,{NIGHT} 60%);color:#fff;border-radius:24px;padding:72px 40px;text-align:center}}
header img{{height:150px;max-width:100%}} header p{{color:#9fb8b4;margin:24px auto 0}}
h1{{font-size:36px;letter-spacing:-.03em;margin:48px 0 4px}} h2{{font-size:22px;letter-spacing:-.02em;margin:48px 0 2px}} p{{margin:0;color:#4b5755;max-width:46rem}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:18px}} .c{{background:#fff;border-radius:16px;padding:10px;border:1px solid #e4e1da}}
.t{{margin:0;border-radius:10px;height:170px;display:grid;place-items:center;padding:24px;border:1px solid rgba(0,0,0,.05)}} .t img{{width:100%;height:100%;object-fit:contain}}
figcaption{{padding:10px 4px 2px;font-size:12.5px;display:flex;flex-direction:column}} figcaption a{{color:{TEAL};font-weight:600;text-decoration:none}}
.palette{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:18px}} .sw{{height:110px;border-radius:14px;display:flex;align-items:flex-end;padding:12px;font-size:12px;color:#fff;border:1px solid rgba(0,0,0,.06)}}
.sw:nth-child(4),.sw:nth-child(5){{color:#101615}}
.rules{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px}} .rules div{{background:#fff;border-radius:16px;padding:20px;border:1px solid #e4e1da}} .rules ul{{margin:8px 0 0;padding-left:18px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}.palette{{grid-template-columns:repeat(3,1fr)}}.rules{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<header><img src="svg/luno-logo-stacked-white.svg" alt="Luno Health"><p>Brand assets · Lumen identity</p></header>
<h1>Luno Health logo kit</h1>
<p>The Lumen mark is a night-green moon with a crescent of light on its edge: light arriving in the dark. Download any file below. SVG scales to any size; use PNG where SVG is not accepted.</p>
{''.join(sections)}
<section><h2>Colours</h2><p>Deep Green and Pearl carry the brand; Luno Teal and Mint form the light; Night is for dark backgrounds.</p><div class="palette">{pal}</div></section>
<section><h2>Type</h2><p>Wordmark and headings: <b>Manrope</b> (Google Fonts, open licence). Website headings: Instrument Serif; Russian pages: Lora; body text: Source Sans 3.</p></section>
<section><h2>Use it well</h2><div class="rules">
<div><b>Do</b><ul><li>Use the colour logo on white or Pearl, the white logo on Night or Deep Green.</li><li>Use one-colour versions for stamps, embroidery, engraving and fax.</li><li>Keep clear space around the logo at least the width of the crescent.</li></ul></div>
<div><b>Don't</b><ul><li>Stretch, rotate, recolour or add shadows.</li><li>Put the colour logo on busy photos; use the white version on a dark overlay.</li><li>Recreate the wordmark in another font.</li></ul></div>
</div></section>
<p style="margin-top:48px;font-size:12.5px">© Utkarashish Ecom Private Limited. Luno Health and the Lumen mark are brands of Utkarashish Ecom Private Limited.</p>
</div></body></html>
'''
(B / 'index.html').write_text(html, encoding='utf-8')
print('brand page written')
