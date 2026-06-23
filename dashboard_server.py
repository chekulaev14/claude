#!/usr/bin/env python3
"""
SEO Dashboard API сервер
Запуск: python3 dashboard_server.py  (держать открытым в терминале)
Слушает на localhost:8087 — принимает запросы от seo-dashboard/index.html
"""

import json
import os
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests as req_lib

os.chdir(os.path.dirname(os.path.abspath(__file__)))

GSC_CREDENTIALS_FILE = 'gsc-credentials.json'
GSC_SITE_URL = 'https://dinamika-cargo.ru/'
YANDEX_CREDENTIALS_FILE = 'yandex-credentials.json'
YANDEX_API_BASE = 'https://api.webmaster.yandex.net/v4'
PORT = 8087


# ─── GSC ──────────────────────────────────────────────────────────────────────

def fetch_gsc():
    creds = service_account.Credentials.from_service_account_file(
        GSC_CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    service = build('searchconsole', 'v1', credentials=creds)

    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    start_90 = (datetime.now() - timedelta(days=93)).strftime('%Y-%m-%d')
    start_28 = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')

    def query(start, dims, limit=500):
        return service.searchanalytics().query(
            siteUrl=GSC_SITE_URL,
            body={'startDate': start, 'endDate': end_date, 'dimensions': dims, 'rowLimit': limit}
        ).execute().get('rows', [])

    daily = sorted([{
        'date': r['keys'][0],
        'clicks': int(r.get('clicks', 0)),
        'impressions': int(r.get('impressions', 0)),
        'ctr': round(r.get('ctr', 0) * 100, 2),
        'position': round(r.get('position', 0), 1),
    } for r in query(start_90, ['date'])], key=lambda x: x['date'])

    queries = [{
        'query': r['keys'][0],
        'clicks': int(r.get('clicks', 0)),
        'impressions': int(r.get('impressions', 0)),
        'ctr': round(r.get('ctr', 0) * 100, 2),
        'position': round(r.get('position', 0), 1),
    } for r in query(start_28, ['query'], 50)]

    pages = [{
        'page': r['keys'][0].replace('https://dinamika-cargo.ru', '') or '/',
        'clicks': int(r.get('clicks', 0)),
        'impressions': int(r.get('impressions', 0)),
        'ctr': round(r.get('ctr', 0) * 100, 2),
        'position': round(r.get('position', 0), 1),
    } for r in query(start_28, ['page'], 30)]

    return {'daily': daily, 'queries': queries, 'pages': pages}


# ─── Яндекс ───────────────────────────────────────────────────────────────────

def fetch_yandex():
    with open(YANDEX_CREDENTIALS_FILE) as f:
        token = json.load(f)['access_token']

    headers = {'Authorization': f'OAuth {token}', 'Content-Type': 'application/json'}

    def get(ep):
        r = req_lib.get(f'{YANDEX_API_BASE}{ep}', headers=headers)
        return r.json() if r.status_code == 200 else None

    user_id = get('/user/')['user_id']
    hosts = get(f'/user/{user_id}/hosts/')['hosts']
    host = next((h for h in hosts if h.get('verified')), None)
    if not host:
        return None

    host_id = host['host_id']
    summary = get(f'/user/{user_id}/hosts/{host_id}/summary/')
    iks = summary.get('sqi') if summary else None
    searchable = summary.get('searchable_pages_count', 0) if summary else 0

    date_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    def get_q(days):
        d_from = (datetime.now() - timedelta(days=days + 2)).strftime('%Y-%m-%d')
        ep = (f'/user/{user_id}/hosts/{host_id}/search-queries/popular/'
              f'?order_by=TOTAL_SHOWS&date_from={d_from}&date_to={date_to}'
              f'&query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&query_indicator=AVG_SHOW_POSITION')
        return get(ep)

    q_data = get_q(30)
    queries = []
    if q_data and q_data.get('queries'):
        for q in q_data['queries'][:50]:
            ind = q.get('indicators', {})
            shows = ind.get('TOTAL_SHOWS', 0)
            clicks = ind.get('TOTAL_CLICKS', 0)
            pos = ind.get('AVG_SHOW_POSITION', 0)
            queries.append({
                'query': q.get('query_text', ''),
                'clicks': int(clicks),
                'impressions': int(shows),
                'ctr': round(clicks / shows * 100, 2) if shows > 0 else 0,
                'position': round(float(pos), 1),
            })

    periods = {}
    for days in [7, 28, 90]:
        d_from = (datetime.now() - timedelta(days=days + 2)).strftime('%Y-%m-%d')
        ep = (f'/user/{user_id}/hosts/{host_id}/search-queries/popular/'
              f'?order_by=TOTAL_SHOWS&date_from={d_from}&date_to={date_to}'
              f'&query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS')
        pd = get(ep)
        ts, tc = 0, 0
        if pd and pd.get('queries'):
            for q in pd['queries']:
                ind = q.get('indicators', {})
                ts += ind.get('TOTAL_SHOWS', 0)
                tc += ind.get('TOTAL_CLICKS', 0)
        periods[str(days)] = {'impressions': int(ts), 'clicks': int(tc)}

    # Дневные данные через search-queries/all/history (полная история)
    d_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    d_from = (datetime.now() - timedelta(days=92)).strftime('%Y-%m-%d')
    hist_url = (f'{YANDEX_API_BASE}/user/{user_id}/hosts/{host_id}/search-queries/all/history'
                f'?query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS'
                f'&device_type_indicator=ALL&date_from={d_from}&date_to={d_to}')
    hist_resp = req_lib.get(hist_url, headers=headers)
    daily_by_date = {}
    if hist_resp.status_code == 200:
        hist_data = hist_resp.json()
        for point in hist_data.get('indicators', {}).get('TOTAL_CLICKS', []):
            date = point['date'][:10]
            if date not in daily_by_date:
                daily_by_date[date] = {'clicks': 0, 'impressions': 0}
            daily_by_date[date]['clicks'] = int(point.get('value', 0))
        for point in hist_data.get('indicators', {}).get('TOTAL_SHOWS', []):
            date = point['date'][:10]
            if date not in daily_by_date:
                daily_by_date[date] = {'clicks': 0, 'impressions': 0}
            daily_by_date[date]['impressions'] = int(point.get('value', 0))
    daily = [{'date': d, 'clicks': v['clicks'], 'impressions': v['impressions']}
             for d, v in sorted(daily_by_date.items())]

    return {'iks': iks, 'searchable_pages': searchable, 'queries': queries, 'periods': periods, 'daily': daily}


# ─── HTTP Handler ──────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  {args[0]} {args[1]}")

    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self.cors()
        self.end_headers()

    def do_GET(self):
        html_path = os.path.join(os.path.dirname(__file__), 'seo-dashboard', 'index.html')
        try:
            with open(html_path, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != '/api/refresh':
            self.send_response(404)
            self.end_headers()
            return

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Обновляю данные...")

        result = {}
        try:
            print("  GSC...", end=' ', flush=True)
            result['gsc'] = fetch_gsc()
            print("OK")
        except Exception as e:
            print(f"ОШИБКА: {e}")
            result['gsc'] = {'daily': [], 'queries': [], 'pages': []}

        try:
            print("  Яндекс...", end=' ', flush=True)
            result['yandex'] = fetch_yandex()
            print("OK")
        except Exception as e:
            print(f"ОШИБКА: {e}")
            result['yandex'] = {'iks': None, 'searchable_pages': 0, 'queries': [], 'periods': {}}

        result['updated_at'] = datetime.now().strftime('%d.%m.%Y %H:%M')
        result['ok'] = True

        body = json.dumps(result, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print("  Готово!")


if __name__ == '__main__':
    server = HTTPServer(('localhost', PORT), Handler)
    print(f"SEO Dashboard API запущен на localhost:{PORT}")
    print(f"Открой seo-dashboard/index.html в браузере и нажми «Обновить данные»")
    print(f"Ctrl+C для остановки\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
