#!/usr/bin/env python3
"""
Google Search Console Analytics
Получение данных о поисковых запросах для dinamika-cargo.ru
"""

import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Настройки
CREDENTIALS_FILE = 'gsc-credentials.json'
SITE_URL = 'https://dinamika-cargo.ru/'  # формат URL-ресурса

def get_service():
    """Создание сервиса GSC API"""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    return build('searchconsole', 'v1', credentials=credentials)

def get_search_analytics(service, start_date, end_date, dimensions=['query'], row_limit=100):
    """Получение данных поисковой аналитики"""
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': dimensions,
        'rowLimit': row_limit
    }

    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request
    ).execute()

    return response.get('rows', [])

def get_top_queries(days=28, limit=50):
    """Топ поисковых запросов за последние N дней"""
    service = get_service()

    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+3)).strftime('%Y-%m-%d')

    rows = get_search_analytics(service, start_date, end_date, ['query'], limit)

    print(f"\n{'='*60}")
    print(f"ТОП-{limit} ЗАПРОСОВ за {days} дней ({start_date} — {end_date})")
    print(f"{'='*60}\n")

    for i, row in enumerate(rows, 1):
        query = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0) * 100
        position = row.get('position', 0)

        print(f"{i:3}. {query[:50]:<50}")
        print(f"     Клики: {clicks:<6} | Показы: {impressions:<8} | CTR: {ctr:.1f}% | Позиция: {position:.1f}")
        print()

def get_top_pages(days=28, limit=30):
    """Топ страниц по кликам"""
    service = get_service()

    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+3)).strftime('%Y-%m-%d')

    rows = get_search_analytics(service, start_date, end_date, ['page'], limit)

    print(f"\n{'='*60}")
    print(f"ТОП-{limit} СТРАНИЦ за {days} дней")
    print(f"{'='*60}\n")

    for i, row in enumerate(rows, 1):
        page = row['keys'][0].replace('https://dinamika-cargo.ru', '')
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0) * 100
        position = row.get('position', 0)

        print(f"{i:3}. {page[:60]}")
        print(f"     Клики: {clicks:<6} | Показы: {impressions:<8} | CTR: {ctr:.1f}% | Позиция: {position:.1f}")
        print()

def get_queries_by_page(page_filter, days=28, limit=20):
    """Запросы для конкретной страницы"""
    service = get_service()

    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+3)).strftime('%Y-%m-%d')

    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query'],
        'dimensionFilterGroups': [{
            'filters': [{
                'dimension': 'page',
                'operator': 'contains',
                'expression': page_filter
            }]
        }],
        'rowLimit': limit
    }

    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request
    ).execute()

    rows = response.get('rows', [])

    print(f"\n{'='*60}")
    print(f"ЗАПРОСЫ для страниц содержащих: {page_filter}")
    print(f"{'='*60}\n")

    for i, row in enumerate(rows, 1):
        query = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        position = row.get('position', 0)

        print(f"{i:3}. {query[:50]:<50} | Клики: {clicks} | Показы: {impressions} | Поз: {position:.1f}")

def export_to_json(filename='gsc_data.json', days=28):
    """Экспорт всех данных в JSON"""
    service = get_service()

    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+3)).strftime('%Y-%m-%d')

    data = {
        'period': {'start': start_date, 'end': end_date},
        'queries': get_search_analytics(service, start_date, end_date, ['query'], 500),
        'pages': get_search_analytics(service, start_date, end_date, ['page'], 500),
        'countries': get_search_analytics(service, start_date, end_date, ['country'], 50),
        'devices': get_search_analytics(service, start_date, end_date, ['device'], 10),
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Данные экспортированы в {filename}")

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'queries':
            get_top_queries(limit=int(sys.argv[2]) if len(sys.argv) > 2 else 50)
        elif cmd == 'pages':
            get_top_pages(limit=int(sys.argv[2]) if len(sys.argv) > 2 else 30)
        elif cmd == 'page':
            get_queries_by_page(sys.argv[2] if len(sys.argv) > 2 else '/regions/')
        elif cmd == 'export':
            export_to_json()
        else:
            print("Использование:")
            print("  python gsc_analytics.py queries [limit]  - топ запросов")
            print("  python gsc_analytics.py pages [limit]    - топ страниц")
            print("  python gsc_analytics.py page /path/      - запросы для страницы")
            print("  python gsc_analytics.py export           - экспорт в JSON")
    else:
        get_top_queries(limit=30)
