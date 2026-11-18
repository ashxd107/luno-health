import json, re, pathlib, html

ROOT = pathlib.Path('.')
BASE = 'https://lunohealth.in/'
OG = BASE + 'assets/img/og-image.jpg'

PAGES = {
  'index.html': ('', 'Luno Health | Medical Treatment in India at Top Hospitals',
    'Heart surgery, cancer care, joint replacement, transplant and IVF at accredited hospitals in India. Free written opinion and fixed quote in 48 hours.', 'Home', 1.0, 'weekly'),
  'treatments.html': ('treatments.html', 'Treatment Costs in India: Heart, Knee, IVF | Luno Health',
    'Costs in India for heart bypass, knee and hip replacement, kidney transplant, neurosurgery, cancer care and IVF. Get a free, fixed written quote.', 'Treatments', 0.9, 'monthly'),
  'how-it-works.html': ('how-it-works.html', 'How Medical Travel to India Works | Luno Health',
    'Specialist opinion and quote in 48 hours, medical visa invitation, airport pickup, accommodation, interpreter and follow-up after you return home.', 'How it works', 0.8, 'monthly'),
  'about.html': ('about.html', 'About Luno Health | Medical Travel Facilitator in India',
    'Luno Health connects international patients with accredited hospitals in India. A brand of Utkarashish Ecom Private Limited. Free for patients.', 'About', 0.7, 'monthly'),
  'contact.html': ('contact.html', 'Get a Free Treatment Plan in India | Contact Luno Health',
    'Send your medical reports on WhatsApp or email. Same-day reply in Russian or English. Free written opinion and fixed hospital quote in 48 hours.', 'Contact', 0.8, 'monthly'),
  'privacy.html': ('privacy.html', 'Privacy Policy | Luno Health', 'How Luno Health collects, uses and protects your personal and medical information.', 'Privacy policy', 0.3, 'yearly'),
  'terms.html': ('terms.html', 'Terms of Service | Luno Health', 'Terms of service for Luno Health, a brand of Utkarashish Ecom Private Limited.', 'Terms', 0.3, 'yearly'),
  'patient-data.html': ('patient-data.html', 'Patient Data and Consent | Luno Health', 'How Luno Health shares your medical reports with hospitals, with your consent, and how to ask us to delete them.', 'Patient data', 0.3, 'yearly'),
  'cookies.html': ('cookies.html', 'Cookie Policy | Luno Health', 'Luno Health uses only essential cookies. No medical data is stored in cookies.', 'Cookies', 0.2, 'yearly'),
}

ORG = {
  "@type": "Organization", "@id": BASE + "#organization",
  "name": "Luno Health", "alternateName": ["LunoHealth", "Luno Health India", "lunohealth.in"], "legalName": "Utkarashish Ecom Private Limited",
  "url": BASE, "logo": BASE + "assets/img/logo.png", "image": OG,
  "description": "Medical travel facilitator connecting international patients with accredited hospitals in India.",
  "email": "lunohealthpe@gmail.com", "telephone": "+91-8431336991",
  "identifier": {"@type": "PropertyValue", "propertyID": "CIN", "value": "U47912CT2024PTC016818"},
  "foundingDate": "2024-09-04",
  "address": {"@type": "PostalAddress", "streetAddress": "G-19, 5th Floor, CHPL Dream Homes, Motilal Nehru Nagar", "addressLocality": "Bhilai", "addressRegion": "Chhattisgarh", "postalCode": "490020", "addressCountry": "IN"},
  "contactPoint": {"@type": "ContactPoint", "telephone": "+91-8431336991", "contactType": "customer service", "availableLanguage": ["English", "Russian"], "areaServed": "Worldwide"},
  "areaServed": "Worldwide",
  "knowsAbout": ["Medical tourism in India", "Cardiac surgery", "Oncology", "Joint replacement", "Kidney transplant", "Neurosurgery", "IVF"],
}
SITE = {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Luno Health", "alternateName": ["LunoHealth", "lunohealth.in"], "publisher": {"@id": BASE + "#organization"}, "inLanguage": "en"}

def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def faq_schema(s):
    qs = re.findall(r'<div class="buybox_faq-q"><h3[^>]*>(.*?)</h3></div>\s*<div class="buybox_faq-body"><p[^>]*>(.*?)</p>', s, re.S)
    if not qs: return None
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}} for q, a in qs]}

def treatments_schema(s):
    items = []
    for m in re.finditer(r'<article class="tx" id="([a-z]+)">.*?<h2[^>]*>(.*?)</h2>.*?<p[^>]*>(.*?)</p>', s, re.S):
        items.append({"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Treatment coordination in India: " + text(m.group(2)), "description": text(m.group(3)), "url": BASE + "treatments.html#" + m.group(1)}})
    return {"@type": "Service", "name": "Medical treatment coordination in India", "provider": {"@id": BASE + "#organization"}, "areaServed": "Worldwide", "serviceType": "Medical tourism facilitation",
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Treatments", "itemListElement": items}}


RU = {
  'index.html': ('Luno Health | Лечение в Индии в лучших клиниках', 'Кардиохирургия, онкология, эндопротезирование, трансплантация и ЭКО в аккредитованных клиниках Индии. Бесплатное заключение и фиксированная цена за 48 часов.', 'Главная'),
  'treatments.html': ('Стоимость лечения в Индии: сердце, суставы, ЭКО | Luno Health', 'Цены в Индии на шунтирование, эндопротезирование колена и бедра, трансплантацию почки, нейрохирургию, онкологию и ЭКО. Бесплатный расчёт.', 'Лечение'),
  'how-it-works.html': ('Как организовать лечение в Индии | Luno Health', 'Заключение и цена за 48 часов, приглашение на медицинскую визу, встреча в аэропорту, проживание, переводчик и наблюдение после возвращения.', 'Как это работает'),
  'about.html': ('О Luno Health | Организация лечения в Индии', 'Luno Health помогает иностранным пациентам лечиться в аккредитованных клиниках Индии. Бренд Utkarashish Ecom Private Limited. Бесплатно для пациентов.', 'О нас'),
  'contact.html': ('Бесплатный план лечения в Индии | Luno Health', 'Отправьте медицинские документы в WhatsApp или на почту. Ответ на русском в тот же день. Бесплатное заключение и цена от клиники за 48 часов.', 'Контакты'),
  'privacy.html': ('Политика конфиденциальности | Luno Health', 'Как Luno Health собирает, использует и защищает ваши персональные и медицинские данные.', 'Конфиденциальность'),
  'terms.html': ('Условия использования | Luno Health', 'Условия использования Luno Health, бренда Utkarashish Ecom Private Limited.', 'Условия'),
  'patient-data.html': ('Данные пациента и согласие | Luno Health', 'Как Luno Health передаёт ваши медицинские документы клиникам с вашего согласия и как запросить их удаление.', 'Данные пациента'),
  'cookies.html': ('Политика cookie | Luno Health', 'Luno Health использует только необходимые cookie. Медицинские данные в cookie не хранятся.', 'Cookie'),
}

def url_for(lang, name):
    return BASE + ('ru/' if lang == 'ru' else '') + PAGES[name][0]

urls = []
for lang in ('en', 'ru'):
    for name, (path, title, desc, crumb, prio, freq) in PAGES.items():
        if lang == 'ru':
            title, desc, crumb = RU[name]
            f = ROOT / 'ru' / name; home_name = 'Главная'; prefix = '../'
        else:
            f = ROOT / name; home_name = 'Home'; prefix = ''
        s = f.read_text(encoding='utf-8')
        url = url_for(lang, name); home = url_for(lang, 'index.html')
        en_url, ru_url = url_for('en', name), url_for('ru', name)
        s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title, quote=False) + '</title>', s, count=1)
        s = re.sub(r'\s*<meta name="description"[^>]*>', '', s)
        s = re.sub(r'\s*<!-- seo -->.*?<!-- /seo -->', '', s, flags=re.S)
        graph = [ORG, SITE, {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
                 "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": BASE + "#organization"}, "inLanguage": lang}]
        if path:
            graph.append({"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": home_name, "item": home},
                {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]})
        fq = faq_schema(s)
        if fq: graph.append(fq)
        if name == 'treatments.html' and lang == 'en': graph.append(treatments_schema(s))
        robots = 'index, follow, max-image-preview:large' if prio >= 0.5 else 'index, follow'
        loc, alt_loc = ('ru_RU', 'en_IN') if lang == 'ru' else ('en_IN', 'ru_RU')
        ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
        block = '\n'.join([
            '', '  <!-- seo -->',
            f'  <meta name="description" content="{html.escape(desc)}">',
            f'  <meta name="robots" content="{robots}">',
            f'  <link rel="canonical" href="{url}">',
            f'  <link rel="alternate" hreflang="en" href="{en_url}">',
            f'  <link rel="alternate" hreflang="ru" href="{ru_url}">',
            f'  <link rel="alternate" hreflang="x-default" href="{en_url}">',
            '  <meta name="theme-color" content="#0b2b29">',
            '  <meta property="og:type" content="website">',
            '  <meta property="og:site_name" content="Luno Health">',
            f'  <meta property="og:locale" content="{loc}">',
            f'  <meta property="og:locale:alternate" content="{alt_loc}">',
            f'  <meta property="og:title" content="{html.escape(title)}">',
            f'  <meta property="og:description" content="{html.escape(desc)}">',
            f'  <meta property="og:url" content="{url}">',
            f'  <meta property="og:image" content="{OG}">',
            '  <meta property="og:image:width" content="1200">',
            '  <meta property="og:image:height" content="630">',
            '  <meta property="og:image:alt" content="Luno Health">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:title" content="{html.escape(title)}">',
            f'  <meta name="twitter:description" content="{html.escape(desc)}">',
            f'  <meta name="twitter:image" content="{OG}">',
            f'  <link rel="apple-touch-icon" href="{prefix}assets/img/favicon.png">',
            f'  <script type="application/ld+json">{ld}</script>',
            '  <!-- /seo -->'])
        s = s.replace('</title>', '</title>' + block, 1)
        s = re.sub(r'<img (?![^>]*loading=)(?![^>]*navbar_logo-mark)(?![^>]*hero)', '<img loading="lazy" decoding="async" ', s)
        s = s.replace('<div class="hero_bg"><img src=', '<div class="hero_bg"><img fetchpriority="high" src=')
        f.write_text(s, encoding='utf-8')
        urls.append((url, en_url, ru_url, prio, freq))

sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for u, e, r, pr, fr in urls:
    sm.append(f'  <url><loc>{u}</loc><lastmod>2026-11-18</lastmod><changefreq>{fr}</changefreq><priority>{pr:.1f}</priority>'
              f'<xhtml:link rel="alternate" hreflang="en" href="{e}"/><xhtml:link rel="alternate" hreflang="ru" href="{r}"/>'
              f'<xhtml:link rel="alternate" hreflang="x-default" href="{e}"/></url>')
sm.append('</urlset>')
(ROOT / 'sitemap.xml').write_text('\n'.join(sm) + '\n', encoding='utf-8')
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://lunohealth.in/sitemap.xml\n', encoding='utf-8')
print('done', len(urls))
