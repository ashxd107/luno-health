# Build tools

Run from the repo root after editing any English page:

```
python tools/build_ru.py tools/ru.json   # regenerate /ru/ pages from English
python tools/seo.py                      # titles, meta, hreflang, schema, sitemap
```

New English text must get a Russian entry in `tools/ru.json`; the build lists anything untranslated.
