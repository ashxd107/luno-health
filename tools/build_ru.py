import json, re, sys, pathlib, html

ROOT = pathlib.Path('.')
T = json.load(open(sys.argv[1], encoding='utf-8'))
PAGES = ['index.html', 'treatments.html', 'how-it-works.html', 'about.html', 'contact.html',
         'privacy.html', 'terms.html', 'patient-data.html', 'cookies.html']
(ROOT / 'ru').mkdir(exist_ok=True)
missing = set()

def tr_text(m):
    raw = m.group(1)
    key = html.unescape(raw.strip())
    if key in T:
        lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
        return '>' + lead + html.escape(T[key], quote=False) + trail + '<'
    if re.search(r'[A-Za-z]{3}', key) and not key.startswith(('$', 'CIN', '+91')):
        missing.add(key)
    return m.group(0)

def tr_attr(m):
    key = html.unescape(m.group(2))
    return m.group(1) + '="' + html.escape(T.get(key, key)) + '"'

def switcher(page, to_ru):
    target = ('ru/' + page) if to_ru else ('../' + page)
    label, lang = ('RU', 'ru') if to_ru else ('EN', 'en')
    full = 'Русский' if to_ru else 'English'
    return target, label, lang, full

for page in PAGES:
    s = (ROOT / page).read_text(encoding='utf-8')
    # language switchers on the EN page (idempotent)
    if 'navbar_lang' not in s:
        tgt, label, lang, full = switcher(page, True)
        s = s.replace('<div class="navbar_right">', f'<div class="navbar_right"><a class="navbar_link navbar_lang" href="{tgt}" hreflang="{lang}" lang="{lang}" aria-label="{full}">{label}</a>', 1)
        s = s.replace('</aside>', f'  <a class="navbar_menu-lang" href="{tgt}" hreflang="{lang}" lang="{lang}">{full}</a>\n  </aside>', 1)
        (ROOT / page).write_text(s, encoding='utf-8')

    r = s
    r = r.replace('<html lang="en">', '<html lang="ru">', 1)
    r = re.sub(r'\s*<!-- seo -->.*?<!-- /seo -->', '', r, flags=re.S)
    # swap the switcher to point back to English
    tgt, label, lang, full = switcher(page, True)
    btgt, blabel, blang, bfull = switcher(page, False)
    r = r.replace(f'href="{tgt}" hreflang="{lang}" lang="{lang}" aria-label="{full}">{label}</a>', f'href="{btgt}" hreflang="{blang}" lang="{blang}" aria-label="{bfull}">{blabel}</a>')
    r = r.replace(f'<a class="navbar_menu-lang" href="{tgt}" hreflang="{lang}" lang="{lang}">{full}</a>', f'<a class="navbar_menu-lang" href="{btgt}" hreflang="{blang}" lang="{blang}">{bfull}</a>')
    # mobile "Languages" block on home: make it a real switcher
    # Cyrillic display font
    r = r.replace('family=Instrument+Serif:ital@0;1&family=Source+Sans+3', 'family=Instrument+Serif:ital@0;1&family=Lora:wght@400;500&family=Source+Sans+3')
    # asset paths
    r = r.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    # translate attributes, then text nodes (skip <script>/<style>)
    r = re.sub(r'(alt|placeholder|aria-label)="([^"]+)"', tr_attr, r)
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<title>.*?</title>)', r, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'>([^<>]*\S[^<>]*)<', tr_text, parts[i])
    r = ''.join(parts)
    r = re.sub(r'</a>\s+, ', '</a>, ', r).replace('</a> .', '</a>.')
    (ROOT / 'ru' / page).write_text(r, encoding='utf-8')

print('built', len(PAGES), 'ru pages')
if missing: print('UNTRANSLATED:', *sorted(missing), sep='\n  ')
