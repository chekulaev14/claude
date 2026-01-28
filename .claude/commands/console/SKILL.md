---
name: console
description: SEO-аналитика сайта dinamika-cargo.ru через Google Search Console API. Показывает индексацию, клики, показы, позиции, запросы с потенциалом, динамику роста. Используй когда нужен отчёт по SEO, проверка GSC, анализ поисковых запросов.
---

# Google Search Console — SEO отчёт

Полный отчёт по SEO для dinamika-cargo.ru.

## Инструкции

Выполни все проверки последовательно и выведи результаты в компактном виде.

### 1. Статус индексации (sitemap)

```bash
python3 -c "
from gsc_analytics import get_service

service = get_service()
SITE_URL = 'https://dinamika-cargo.ru/'

sitemaps = service.sitemaps().list(siteUrl=SITE_URL).execute()
for sm in sitemaps.get('sitemap', []):
    contents = sm.get('contents', [])
    for c in contents:
        print(f\"Sitemap: {c.get('submitted', 0)} URL | Indexed: {c.get('indexed', 'N/A')}\")
    print(f\"Errors: {sm.get('errors', 0)} | Warnings: {sm.get('warnings', 0)}\")
    print(f\"Last download: {sm.get('lastDownloaded', 'N/A')[:10]}\")
"
```

### 2. Динамика (последние 14 дней vs предыдущие 14)

```bash
python3 -c "
from gsc_analytics import get_service
from datetime import datetime, timedelta

service = get_service()
SITE_URL = 'https://dinamika-cargo.ru/'

end = datetime.now() - timedelta(days=3)
mid = end - timedelta(days=14)
start = mid - timedelta(days=14)

print('Период           | Клики | Показы | CTR   | Позиция')
print('-' * 55)

for name, s, e in [('Пред. 14 дней', start, mid), ('Посл. 14 дней', mid, end)]:
    req = {'startDate': s.strftime('%Y-%m-%d'), 'endDate': e.strftime('%Y-%m-%d'), 'dimensions': [], 'rowLimit': 1}
    resp = service.searchanalytics().query(siteUrl=SITE_URL, body=req).execute()
    row = resp.get('rows', [{}])[0] if resp.get('rows') else {}
    print(f\"{name:16} | {row.get('clicks', 0):5} | {row.get('impressions', 0):6} | {row.get('ctr', 0)*100:4.1f}% | {row.get('position', 0):5.1f}\")
"
```

### 3. Топ-10 страниц по кликам

```bash
python3 gsc_analytics.py pages 10
```

### 4. Топ-10 запросов

```bash
python3 gsc_analytics.py queries 10
```

### 5. Запросы с потенциалом (позиция < 15, но 0 кликов)

```bash
python3 -c "
from gsc_analytics import get_service
from datetime import datetime, timedelta

service = get_service()
SITE_URL = 'https://dinamika-cargo.ru/'

end = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
start = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')

req = {'startDate': start, 'endDate': end, 'dimensions': ['query'], 'rowLimit': 500}
resp = service.searchanalytics().query(siteUrl=SITE_URL, body=req).execute()
rows = resp.get('rows', [])

potential = [r for r in rows if r.get('position', 100) < 15 and r.get('clicks', 0) == 0]
potential.sort(key=lambda x: x.get('impressions', 0), reverse=True)

print('Запросы с потенциалом (позиция < 15, 0 кликов):')
for r in potential[:10]:
    print(f\"  Поз {r['position']:.0f} | {r['impressions']} показов | {r['keys'][0]}\")
"
```

### 6. Проверка ключевых страниц (URL Inspection)

```bash
python3 -c "
from gsc_analytics import get_service

service = get_service()
SITE_URL = 'https://dinamika-cargo.ru/'

urls = [
    'https://dinamika-cargo.ru/',
    'https://dinamika-cargo.ru/regions/',
    'https://dinamika-cargo.ru/routes/',
]

print('URL Inspection:')
for url in urls:
    try:
        result = service.urlInspection().index().inspect(body={'inspectionUrl': url, 'siteUrl': SITE_URL}).execute()
        status = result.get('inspectionResult', {}).get('indexStatusResult', {})
        verdict = status.get('verdict', 'N/A')
        coverage = status.get('coverageState', 'N/A')
        print(f\"  {verdict:6} | {url.replace('https://dinamika-cargo.ru', '')}\")
    except Exception as e:
        print(f\"  ERROR | {url} | {str(e)[:50]}\")
"
```

## Формат вывода

Выводи результаты в виде таблиц. После всех проверок дай краткий вывод:
- Что хорошо
- Что требует внимания
- Рекомендации (1-3 пункта)

## Зависимости

- Python 3
- gsc_analytics.py в корне проекта
- gsc-credentials.json (Service Account)
