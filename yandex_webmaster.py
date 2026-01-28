#!/usr/bin/env python3
"""
Яндекс.Вебмастер API
Получение данных для dinamika-cargo.ru
"""

import json
import requests
from datetime import datetime, timedelta

# Настройки
CREDENTIALS_FILE = 'yandex-credentials.json'
API_BASE = 'https://api.webmaster.yandex.net/v4'
SITE_URL = 'https:dinamika-cargo.ru:443'  # Формат Яндекса

def get_token():
    """Получение токена из файла"""
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
    return creds['access_token']

def api_request(endpoint, method='GET', params=None):
    """Запрос к API Яндекс.Вебмастера"""
    token = get_token()
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }

    url = f'{API_BASE}{endpoint}'

    if method == 'GET':
        response = requests.get(url, headers=headers, params=params)
    else:
        response = requests.post(url, headers=headers, json=params)

    if response.status_code != 200:
        print(f'Error {response.status_code}: {response.text}')
        return None

    return response.json()

def get_user_id():
    """Получение user_id"""
    data = api_request('/user/')
    if data:
        return data.get('user_id')
    return None

def get_hosts(user_id):
    """Список сайтов пользователя"""
    data = api_request(f'/user/{user_id}/hosts/')
    return data.get('hosts', []) if data else []

def get_host_info(user_id, host_id):
    """Информация о сайте"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/')

def get_summary(user_id, host_id):
    """Сводка по сайту (индексация, проблемы)"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/summary/')

def get_indexing_stats(user_id, host_id):
    """Статистика индексирования"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/indexing/samples/')

def get_search_queries(user_id, host_id, date_from=None, date_to=None):
    """Поисковые запросы"""
    if not date_to:
        date_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    if not date_from:
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    endpoint = f'/user/{user_id}/hosts/{host_id}/search-queries/popular/'
    params = f'order_by=TOTAL_SHOWS&date_from={date_from}&date_to={date_to}&query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&query_indicator=AVG_SHOW_POSITION'

    return api_request(f'{endpoint}?{params}')

def get_external_links(user_id, host_id):
    """Внешние ссылки на сайт"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/links/external/samples/')

def get_diagnostics(user_id, host_id):
    """Диагностика сайта (ошибки, проблемы)"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/diagnostics/')

def get_indexing_history(user_id, host_id):
    """История индексирования"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/indexing/history/')

def get_important_urls(user_id, host_id):
    """Важные URL (с проблемами)"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/important-urls/')

def get_sitemaps(user_id, host_id):
    """Список сайтмапов"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/sitemaps/')

def get_crawling_status(user_id, host_id):
    """Статус обхода робота"""
    return api_request(f'/user/{user_id}/hosts/{host_id}/crawling/state/')

def get_top_pages(user_id, host_id, limit=50, date_from=None, date_to=None):
    """Топ страниц по показам/кликам через query-analytics API"""
    if not date_to:
        date_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    if not date_from:
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    token = get_token()
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    url = f'{API_BASE}/user/{user_id}/hosts/{host_id}/query-analytics/list'

    body = {
        'offset': 0,
        'limit': limit,
        'device_type_indicator': 'ALL',
        'text_indicator': 'URL',
        'date_from': date_from,
        'date_to': date_to
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        print(f'Error {response.status_code}: {response.text}')
        return None

    return response.json()

def get_queries_for_url(user_id, host_id, url_filter, limit=20):
    """Запросы для конкретной страницы"""
    date_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    token = get_token()
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    url = f'{API_BASE}/user/{user_id}/hosts/{host_id}/query-analytics/list'

    body = {
        'offset': 0,
        'limit': limit,
        'device_type_indicator': 'ALL',
        'text_indicator': 'QUERY',
        'date_from': date_from,
        'date_to': date_to,
        'filters': {
            'text_filters': [{
                'text_indicator': 'URL',
                'operation': 'TEXT_CONTAINS',
                'value': url_filter
            }]
        }
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        print(f'Error {response.status_code}: {response.text}')
        return None

    return response.json()

def print_summary():
    """Вывод сводки по сайту"""
    user_id = get_user_id()
    if not user_id:
        print('Ошибка: не удалось получить user_id')
        return

    print(f'User ID: {user_id}')
    print('=' * 60)

    # Получаем список сайтов
    hosts = get_hosts(user_id)

    if not hosts:
        print('Сайты не найдены')
        return

    print(f'\nНайдено сайтов: {len(hosts)}')

    for host in hosts:
        host_id = host.get('host_id')
        host_url = host.get('unicode_host_url', host.get('ascii_host_url', 'Unknown'))
        verified = host.get('verified', False)

        print(f'\n{"=" * 60}')
        print(f'Сайт: {host_url}')
        print(f'Host ID: {host_id}')
        print(f'Верифицирован: {"Да" if verified else "Нет"}')

        if not verified:
            print('⚠️  Сайт не верифицирован, данные ограничены')
            continue

        # Сводка
        summary = get_summary(user_id, host_id)
        if summary:
            print(f'\n--- Индексация ---')
            indexing = summary.get('indexing', {})
            searchable = indexing.get('searchable_pages_count', 0)
            excluded = indexing.get('excluded_pages_count', 0)
            total = searchable + excluded
            print(f'В поиске: {searchable} страниц')
            print(f'Исключено: {excluded} страниц')
            print(f'Всего обработано: {total} страниц')

            sqi = summary.get('sqi')
            if sqi is not None:
                print(f'ИКС (индекс качества): {sqi}')

            # Проблемы из summary
            problems = summary.get('problems', {})
            fatal = problems.get('FATAL', 0)
            critical = problems.get('CRITICAL', 0)
            warning = problems.get('WARNING', 0)
            if fatal or critical or warning:
                print(f'\n--- Проблемы ---')
                if fatal: print(f'🔴 Фатальные: {fatal}')
                if critical: print(f'🟠 Критические: {critical}')
                if warning: print(f'🟡 Предупреждения: {warning}')

        # Диагностика (ошибки)
        diagnostics = get_diagnostics(user_id, host_id)
        if diagnostics and diagnostics.get('problems'):
            problems_list = []
            for problem_type, problem_data in diagnostics['problems'].items():
                if problem_data.get('state') == 'PRESENT':
                    problems_list.append({
                        'type': problem_type,
                        'severity': problem_data.get('severity', 'N/A')
                    })

            if problems_list:
                print(f'\n--- Диагностика (активные проблемы) ---')
                # Сортируем по важности
                severity_order = {'FATAL': 0, 'CRITICAL': 1, 'POSSIBLE_PROBLEM': 2, 'RECOMMENDATION': 3}
                problems_list.sort(key=lambda x: severity_order.get(x['severity'], 99))

                for p in problems_list[:10]:
                    severity = p['severity']
                    icon = '🔴' if severity == 'FATAL' else '🟠' if severity == 'CRITICAL' else '🟡'
                    print(f'{icon} [{severity}] {p["type"]}')

        # Сайтмапы
        sitemaps = get_sitemaps(user_id, host_id)
        if sitemaps and sitemaps.get('sitemaps'):
            print(f'\n--- Сайтмапы ---')
            for sm in sitemaps.get('sitemaps', [])[:5]:
                sm_url = sm.get('sitemap_url', 'N/A')
                urls_count = sm.get('urls_count', 0)
                errors_count = sm.get('errors_count', 0)
                last_access = sm.get('last_access_date', 'N/A')
                if last_access and last_access != 'N/A':
                    last_access = last_access[:10]  # только дата
                status = '✅' if errors_count == 0 else f'⚠️ {errors_count} ошибок'
                print(f'{sm_url[-50:]}: {urls_count} URL | {status} | {last_access}')

        # Поисковые запросы
        queries = get_search_queries(user_id, host_id)
        if queries and queries.get('queries'):
            print(f'\n--- Топ-10 запросов ---')
            for i, q in enumerate(queries['queries'][:10], 1):
                query_text = q.get('query_text', 'N/A')
                indicators = q.get('indicators', {})
                shows = indicators.get('TOTAL_SHOWS', 0)
                clicks = indicators.get('TOTAL_CLICKS', 0)
                position = indicators.get('AVG_SHOW_POSITION', 0)
                ctr = (clicks / shows * 100) if shows > 0 else 0
                print(f'{i:2}. {query_text[:35]:<35} | Показы: {shows:>5} | Клики: {clicks:>3} | CTR: {ctr:>4.1f}% | Поз: {position:.1f}')

def print_queries(limit=50):
    """Топ запросов с лимитом"""
    user_id = get_user_id()
    if not user_id:
        print('Ошибка: не удалось получить user_id')
        return

    hosts = get_hosts(user_id)
    for host in hosts:
        if not host.get('verified'):
            continue

        host_url = host.get('unicode_host_url', 'Unknown')
        print(f'\n{"=" * 70}')
        print(f'ТОП-{limit} ЗАПРОСОВ для {host_url}')
        print(f'{"=" * 70}\n')

        queries = get_search_queries(user_id, host['host_id'])
        if queries and queries.get('queries'):
            for i, q in enumerate(queries['queries'][:limit], 1):
                query_text = q.get('query_text', 'N/A')
                indicators = q.get('indicators', {})
                shows = indicators.get('TOTAL_SHOWS', 0)
                clicks = indicators.get('TOTAL_CLICKS', 0)
                position = indicators.get('AVG_SHOW_POSITION', 0)
                ctr = (clicks / shows * 100) if shows > 0 else 0
                print(f'{i:3}. {query_text[:45]:<45}')
                print(f'     Показы: {shows:<6} | Клики: {clicks:<4} | CTR: {ctr:.1f}% | Позиция: {position:.1f}')
                print()

def print_pages(limit=30):
    """Топ страниц по показам"""
    user_id = get_user_id()
    if not user_id:
        print('Ошибка: не удалось получить user_id')
        return

    hosts = get_hosts(user_id)
    for host in hosts:
        if not host.get('verified'):
            continue

        host_url = host.get('unicode_host_url', 'Unknown')
        print(f'\n{"=" * 70}')
        print(f'ТОП-{limit} СТРАНИЦ для {host_url}')
        print(f'{"=" * 70}\n')

        pages_data = get_top_pages(user_id, host['host_id'], limit)
        if pages_data and pages_data.get('text_indicator_to_statistics'):
            for i, item in enumerate(pages_data['text_indicator_to_statistics'][:limit], 1):
                page_url = item.get('text_indicator', {}).get('value', 'N/A')
                # Убираем домен для компактности
                page_url = page_url.replace('https://dinamika-cargo.ru', '').replace('http://dinamika-cargo.ru', '')

                stats_list = item.get('statistics', [])
                # Суммируем данные по дням
                shows = sum(s['value'] for s in stats_list if s.get('field') == 'IMPRESSIONS')
                clicks = sum(s['value'] for s in stats_list if s.get('field') == 'CLICKS')
                positions = [s['value'] for s in stats_list if s.get('field') == 'POSITION' and s.get('value', 0) > 0]
                position = sum(positions) / len(positions) if positions else 0
                ctr = (clicks / shows * 100) if shows > 0 else 0

                print(f'{i:3}. {page_url[:55]}')
                print(f'     Показы: {shows:<6} | Клики: {clicks:<4} | CTR: {ctr:.1f}% | Позиция: {position:.1f}')
                print()

def print_queries_for_page(url_filter, limit=20):
    """Запросы для конкретной страницы"""
    user_id = get_user_id()
    if not user_id:
        print('Ошибка: не удалось получить user_id')
        return

    hosts = get_hosts(user_id)
    for host in hosts:
        if not host.get('verified'):
            continue

        print(f'\n{"=" * 60}')
        print(f'ЗАПРОСЫ для страниц содержащих: {url_filter}')
        print(f'{"=" * 60}\n')

        queries_data = get_queries_for_url(user_id, host['host_id'], url_filter, limit)
        if queries_data and queries_data.get('text_indicator_to_statistics'):
            for i, item in enumerate(queries_data['text_indicator_to_statistics'][:limit], 1):
                query = item.get('text_indicator', {}).get('value', 'N/A')
                stats = item.get('statistics', {})
                shows = stats.get('impressions', 0)
                clicks = stats.get('clicks', 0)
                position = stats.get('position', 0)
                print(f'{i:3}. {query[:50]:<50} | Клики: {clicks} | Показы: {shows} | Поз: {position:.1f}')

def print_diagnostics():
    """Вывод диагностики отдельно"""
    user_id = get_user_id()
    if not user_id:
        print('Ошибка: не удалось получить user_id')
        return

    hosts = get_hosts(user_id)
    for host in hosts:
        if not host.get('verified'):
            continue

        host_url = host.get('unicode_host_url', 'Unknown')
        host_id = host['host_id']
        print(f'\n{"=" * 60}')
        print(f'ДИАГНОСТИКА: {host_url}')
        print(f'{"=" * 60}')

        diagnostics = get_diagnostics(user_id, host_id)
        if diagnostics and diagnostics.get('problems'):
            for problem_type, problem_data in diagnostics['problems'].items():
                state = problem_data.get('state', 'UNDEFINED')
                severity = problem_data.get('severity', 'N/A')
                last_update = problem_data.get('last_state_update', 'N/A')
                if last_update and last_update != 'N/A':
                    last_update = last_update[:10]

                if state == 'PRESENT':
                    icon = '🔴' if severity == 'FATAL' else '🟠' if severity == 'CRITICAL' else '🟡'
                else:
                    icon = '✅'
                print(f'{icon} {problem_type}: {state} [{severity}] | {last_update}')

def export_to_json(filename='yandex_data.json'):
    """Экспорт всех данных в JSON"""
    user_id = get_user_id()
    if not user_id:
        print('Ошибка: не удалось получить user_id')
        return

    hosts = get_hosts(user_id)
    data = {'hosts': []}

    for host in hosts:
        if not host.get('verified'):
            continue

        host_id = host['host_id']
        host_data = {
            'url': host.get('unicode_host_url'),
            'host_id': host_id,
            'summary': get_summary(user_id, host_id),
            'queries': get_search_queries(user_id, host_id),
            'diagnostics': get_diagnostics(user_id, host_id),
            'sitemaps': get_sitemaps(user_id, host_id),
            'external_links': get_external_links(user_id, host_id),
        }
        data['hosts'].append(host_data)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Данные экспортированы в {filename}')

def main():
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'hosts':
            user_id = get_user_id()
            hosts = get_hosts(user_id)
            for h in hosts:
                print(f"{h.get('unicode_host_url')} | ID: {h.get('host_id')} | Verified: {h.get('verified')}")

        elif cmd == 'summary':
            print_summary()

        elif cmd == 'queries':
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            print_queries(limit)

        elif cmd == 'pages':
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            print_pages(limit)

        elif cmd == 'page':
            url_filter = sys.argv[2] if len(sys.argv) > 2 else '/regions/'
            print_queries_for_page(url_filter)

        elif cmd == 'diagnostics':
            print_diagnostics()

        elif cmd == 'export':
            filename = sys.argv[2] if len(sys.argv) > 2 else 'yandex_data.json'
            export_to_json(filename)

        else:
            print('Использование:')
            print('  python yandex_webmaster.py summary         - сводка (по умолчанию)')
            print('  python yandex_webmaster.py queries [limit] - топ запросов')
            print('  python yandex_webmaster.py pages [limit]   - топ страниц')
            print('  python yandex_webmaster.py page /path/     - запросы для страницы')
            print('  python yandex_webmaster.py diagnostics     - диагностика/ошибки')
            print('  python yandex_webmaster.py hosts           - список сайтов')
            print('  python yandex_webmaster.py export [file]   - экспорт в JSON')
    else:
        print_summary()

if __name__ == '__main__':
    main()
