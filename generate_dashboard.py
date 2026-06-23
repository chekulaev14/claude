#!/usr/bin/env python3
"""
SEO Dashboard Generator
Генерирует статический HTML с данными из Google Search Console и Яндекс.Вебмастер
Запуск: python3 generate_dashboard.py
Результат: /seo-dashboard/index.html
"""

import json
import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

# ─── Настройки ────────────────────────────────────────────────────────────────
GSC_CREDENTIALS_FILE = 'gsc-credentials.json'
GSC_SITE_URL = 'https://dinamika-cargo.ru/'

YANDEX_CREDENTIALS_FILE = 'yandex-credentials.json'
YANDEX_API_BASE = 'https://api.webmaster.yandex.net/v4'

OUTPUT_DIR = 'seo-dashboard'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'index.html')


# ─── GSC ──────────────────────────────────────────────────────────────────────

def get_gsc_service():
    credentials = service_account.Credentials.from_service_account_file(
        GSC_CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    return build('searchconsole', 'v1', credentials=credentials)


def gsc_query(service, start_date, end_date, dimensions, row_limit=500):
    resp = service.searchanalytics().query(
        siteUrl=GSC_SITE_URL,
        body={
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': row_limit,
        }
    ).execute()
    return resp.get('rows', [])


def get_gsc_data():
    print("  GSC: подключение...")
    service = get_gsc_service()

    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    start_date_90 = (datetime.now() - timedelta(days=93)).strftime('%Y-%m-%d')
    start_date_28 = (datetime.now() - timedelta(days=31)).strftime('%Y-%m-%d')

    print("  GSC: данные по дням (90 дней)...")
    daily_rows = gsc_query(service, start_date_90, end_date, ['date'], 500)
    daily = []
    for row in daily_rows:
        daily.append({
            'date': row['keys'][0],
            'clicks': int(row.get('clicks', 0)),
            'impressions': int(row.get('impressions', 0)),
            'ctr': round(row.get('ctr', 0) * 100, 2),
            'position': round(row.get('position', 0), 1),
        })
    daily.sort(key=lambda x: x['date'])

    start_date_7 = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

    queries = {}
    pages = {}
    for label, start in [('7', start_date_7), ('28', start_date_28), ('90', start_date_90)]:
        print(f"  GSC: топ запросов ({label} дней)...")
        q_rows = gsc_query(service, start, end_date, ['query'], 50)
        queries[label] = [{
            'query': r['keys'][0],
            'clicks': int(r.get('clicks', 0)),
            'impressions': int(r.get('impressions', 0)),
            'ctr': round(r.get('ctr', 0) * 100, 2),
            'position': round(r.get('position', 0), 1),
        } for r in q_rows]

        print(f"  GSC: топ страниц ({label} дней)...")
        p_rows = gsc_query(service, start, end_date, ['page'], 30)
        pages[label] = [{
            'page': r['keys'][0].replace('https://dinamika-cargo.ru', '') or '/',
            'clicks': int(r.get('clicks', 0)),
            'impressions': int(r.get('impressions', 0)),
            'ctr': round(r.get('ctr', 0) * 100, 2),
            'position': round(r.get('position', 0), 1),
        } for r in p_rows]

    return {'daily': daily, 'queries': queries, 'pages': pages}


# ─── Яндекс ───────────────────────────────────────────────────────────────────

def yandex_token():
    with open(YANDEX_CREDENTIALS_FILE, 'r') as f:
        return json.load(f)['access_token']


def yandex_api(endpoint, token, params=None):
    headers = {'Authorization': f'OAuth {token}', 'Content-Type': 'application/json'}
    url = f'{YANDEX_API_BASE}{endpoint}'
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print(f'  Яндекс ошибка {resp.status_code}: {resp.text[:200]}')
        return None
    return resp.json()


def yandex_post(endpoint, token, body):
    headers = {'Authorization': f'OAuth {token}', 'Content-Type': 'application/json; charset=UTF-8'}
    url = f'{YANDEX_API_BASE}{endpoint}'
    resp = requests.post(url, headers=headers, json=body)
    if resp.status_code != 200:
        print(f'  Яндекс ошибка {resp.status_code}: {resp.text[:200]}')
        return None
    return resp.json()


def get_yandex_data():
    print("  Яндекс: подключение...")
    token = yandex_token()

    user_data = yandex_api('/user/', token)
    if not user_data:
        return None
    user_id = user_data['user_id']

    hosts_data = yandex_api(f'/user/{user_id}/hosts/', token)
    if not hosts_data:
        return None

    host = None
    for h in hosts_data.get('hosts', []):
        if h.get('verified'):
            host = h
            break

    if not host:
        print("  Яндекс: нет верифицированного сайта")
        return None

    host_id = host['host_id']
    print(f"  Яндекс: сайт {host.get('unicode_host_url')}")

    print("  Яндекс: сводка (ИКС)...")
    summary = yandex_api(f'/user/{user_id}/hosts/{host_id}/summary/', token)

    iks = None
    searchable_pages = 0
    if summary:
        iks = summary.get('sqi')
        searchable_pages = summary.get('searchable_pages_count', 0)

    q_endpoint = f'/user/{user_id}/hosts/{host_id}/search-queries/popular/'
    date_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    def parse_yandex_queries(q_data, limit=50):
        result = []
        if q_data and q_data.get('queries'):
            for q in q_data['queries'][:limit]:
                ind = q.get('indicators', {})
                shows = ind.get('TOTAL_SHOWS', 0)
                clicks = ind.get('TOTAL_CLICKS', 0)
                position = ind.get('AVG_SHOW_POSITION', 0)
                result.append({
                    'query': q.get('query_text', ''),
                    'clicks': int(clicks),
                    'impressions': int(shows),
                    'ctr': round(clicks / shows * 100, 2) if shows > 0 else 0,
                    'position': round(float(position), 1),
                })
        return result

    # Данные за несколько периодов + топ запросов
    print("  Яндекс: суммарные данные и запросы за периоды...")
    periods = {}
    queries = {}
    for days in [7, 28, 90]:
        d_from = (datetime.now() - timedelta(days=days + 2)).strftime('%Y-%m-%d')
        p_params = f'order_by=TOTAL_SHOWS&date_from={d_from}&date_to={date_to}&query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&query_indicator=AVG_SHOW_POSITION'
        p_data = yandex_api(f'{q_endpoint}?{p_params}', token)
        total_shows = 0
        total_clicks = 0
        if p_data and p_data.get('queries'):
            for q in p_data['queries']:
                ind = q.get('indicators', {})
                total_shows += ind.get('TOTAL_SHOWS', 0)
                total_clicks += ind.get('TOTAL_CLICKS', 0)
        periods[str(days)] = {'impressions': int(total_shows), 'clicks': int(total_clicks)}
        queries[str(days)] = parse_yandex_queries(p_data)

    # Дневные данные через search-queries/all/history (полная история)
    print("  Яндекс: данные по дням...")
    d_to = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    d_from = (datetime.now() - timedelta(days=92)).strftime('%Y-%m-%d')
    hist_params = (f'query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS'
                   f'&device_type_indicator=ALL&date_from={d_from}&date_to={d_to}')
    hist_data = yandex_api(f'/user/{user_id}/hosts/{host_id}/search-queries/all/history?{hist_params}', token)
    daily_by_date = {}
    if hist_data and hist_data.get('indicators'):
        for point in hist_data['indicators'].get('TOTAL_CLICKS', []):
            date = point['date'][:10]
            if date not in daily_by_date:
                daily_by_date[date] = {'clicks': 0, 'impressions': 0}
            daily_by_date[date]['clicks'] = int(point.get('value', 0))
        for point in hist_data['indicators'].get('TOTAL_SHOWS', []):
            date = point['date'][:10]
            if date not in daily_by_date:
                daily_by_date[date] = {'clicks': 0, 'impressions': 0}
            daily_by_date[date]['impressions'] = int(point.get('value', 0))
    daily = [{'date': d, 'clicks': v['clicks'], 'impressions': v['impressions']}
             for d, v in sorted(daily_by_date.items())]
    print(f"  Яндекс: дней с данными: {len(daily)}")

    return {
        'iks': iks,
        'searchable_pages': searchable_pages,
        'queries': queries,
        'periods': periods,
        'daily': daily,
    }


# ─── HTML генератор ───────────────────────────────────────────────────────────

def generate_html(gsc, yandex, generated_at):
    gsc_json = json.dumps(gsc, ensure_ascii=False)
    yandex_json = json.dumps(yandex, ensure_ascii=False)
    generated_str = generated_at.strftime('%d.%m.%Y %H:%M')

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Dashboard — dinamika-cargo.ru</title>
<meta name="robots" content="noindex, nofollow">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #f5f6fa;
    --card: #ffffff;
    --border: #e2e5ec;
    --text: #1a1d27;
    --muted: #6b7280;
    --google: #4285F4;
    --yandex: #fc3f1d;
    --green: #16a34a;
    --accent: #6366f1;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 14px; }}

  .header {{ padding: 16px 24px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }}
  .header h1 {{ font-size: 18px; font-weight: 600; }}
  .header-right {{ display: flex; align-items: center; gap: 12px; }}
  .updated {{ font-size: 12px; color: var(--muted); }}
  .btn-refresh {{ padding: 7px 18px; border-radius: 7px; border: none; background: var(--accent); color: #fff; font-size: 13px; font-weight: 500; cursor: pointer; transition: opacity .15s; }}
  .btn-refresh:hover {{ opacity: .85; }}
  .btn-refresh:disabled {{ opacity: .4; cursor: not-allowed; }}
  .status {{ padding: 7px 24px; font-size: 12px; background: rgba(255,255,255,.02); border-bottom: 1px solid var(--border); min-height: 32px; display: flex; align-items: center; gap: 8px; color: var(--muted); }}
  .spinner {{ display:none; width:13px; height:13px; border:2px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin .6s linear infinite; flex-shrink:0; }}
  @keyframes spin {{ to {{ transform:rotate(360deg); }} }}

  .period-nav {{ padding: 16px 24px 0; display: flex; gap: 8px; }}
  .period-btn {{ padding: 6px 16px; border-radius: 6px; border: 1px solid var(--border); background: transparent; color: var(--muted); cursor: pointer; font-size: 13px; transition: all .15s; }}
  .period-btn.active {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
  .period-btn:hover:not(.active) {{ border-color: var(--text); color: var(--text); }}

  .container {{ padding: 20px 24px; max-width: 1400px; }}

  .section-title {{ font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }}

  .cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-bottom: 24px; }}
  .cards-split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }}
  .cards-col {{ display: flex; flex-direction: column; gap: 12px; }}
  .col-title {{ font-size: 13px; font-weight: 600; padding: 4px 2px; }}
  .col-title.yandex {{ color: #fc3f1d; }}
  .col-title.google {{ color: #4285F4; }}
  @media (max-width: 640px) {{ .cards-split {{ grid-template-columns: 1fr; }} }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }}
  .card .label {{ font-size: 11px; color: var(--muted); margin-bottom: 6px; }}
  .card .value {{ font-size: 26px; font-weight: 700; line-height: 1; }}
  .card .sub {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
  .card.google {{ border-top: 2px solid var(--google); }}
  .card.yandex {{ border-top: 2px solid var(--yandex); }}
  .card.neutral {{ border-top: 2px solid var(--accent); }}

  .chart-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin-bottom: 24px; }}
  .chart-top {{ display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }}
  .chart-top h3 {{ font-size: 13px; font-weight: 500; color: var(--muted); }}
  .metric-btns {{ display: flex; gap: 6px; flex-wrap: wrap; }}
  .metric-btn {{ padding: 4px 12px; border-radius: 5px; border: 1px solid var(--border); background: transparent; color: var(--muted); cursor: pointer; font-size: 12px; transition: all .15s; }}
  .metric-btn.active {{ color: #fff; border-color: transparent; }}
  .metric-btn[data-metric="clicks"].active {{ background: #4285F4; }}
  .metric-btn[data-metric="impressions"].active {{ background: #a78bfa; }}
  .metric-btn[data-metric="position"].active {{ background: #16a34a; }}
  .chart-note {{ font-size: 11px; color: var(--muted); }}
  .chart-card canvas {{ max-height: 300px; }}

  .tables {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }}
  @media (max-width: 900px) {{ .tables {{ grid-template-columns: 1fr; }} }}
  .table-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }}
  .table-card .table-header {{ padding: 14px 16px; border-bottom: 1px solid var(--border); font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }}
  .badge {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; }}
  .badge.google {{ background: var(--google); }}
  .badge.yandex {{ background: var(--yandex); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  th {{ padding: 8px 12px; text-align: left; color: var(--muted); font-weight: 500; border-bottom: 1px solid var(--border); white-space: nowrap; }}
  td {{ padding: 7px 12px; border-bottom: 1px solid var(--border); }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(255,255,255,.03); }}
  .query-text {{ max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .num {{ text-align: right; color: var(--muted); font-variant-numeric: tabular-nums; }}
  .pos {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .pos.good {{ color: var(--green); }}
  .pos.mid {{ color: #f59e0b; }}
  .pos.low {{ color: #ef4444; }}

  .pages-section {{ margin-bottom: 24px; }}
  .pages-section .table-card {{ max-height: 400px; overflow-y: auto; }}
  .page-url {{ max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--muted); font-size: 11px; }}
</style>
</head>
<body>

<div class="header">
  <h1>SEO Dashboard — dinamika-cargo.ru</h1>
  <div class="header-right">
    <span class="updated" id="updated-at">Данные от: {generated_str}</span>
    <button class="btn-refresh" onclick="refreshData()">Обновить данные</button>
  </div>
</div>
<div class="status"><div class="spinner" id="spinner"></div><span id="status-msg">Для обновления нажми кнопку (нужен запущенный dashboard_server.py)</span></div>

<div class="period-nav">
  <button class="period-btn" data-days="7">7 дней</button>
  <button class="period-btn" data-days="28">28 дней</button>
  <button class="period-btn active" data-days="90">90 дней</button>
</div>

<div class="container">

  <!-- Сводные карточки -->
  <div class="section-title">Сводка</div>
  <div class="cards" style="grid-template-columns: repeat(5, 1fr); margin-bottom: 16px;">
    <div class="card neutral"><div class="label">Клики всего</div><div class="value" id="t-clicks">—</div><div class="sub">Яндекс + Google</div></div>
    <div class="card neutral"><div class="label">Показы всего</div><div class="value" id="t-impr">—</div><div class="sub">Яндекс + Google</div></div>
    <div class="card neutral"><div class="label">Средний CTR</div><div class="value" id="t-ctr">—</div><div class="sub">клики / показы</div></div>
    <div class="card neutral">
      <div class="label">Лиды за период</div>
      <input type="number" id="leads-input" min="0" placeholder="0" style="font-size:1.6rem;font-weight:700;width:100%;border:none;background:transparent;text-align:center;color:var(--text);outline:none;margin:8px 0;">
      <div class="sub">введите вручную</div>
    </div>
    <div class="card neutral"><div class="label">Конверсия</div><div class="value" id="conversion">—</div><div class="sub">лиды / (G+Я клики)</div></div>
  </div>
  <div class="cards-split" id="cards-section">
    <div class="cards-col">
      <div class="col-title yandex">Яндекс</div>
      <div class="card yandex"><div class="label">Клики</div><div class="value" id="y-clicks">—</div><div class="sub">из поиска</div></div>
      <div class="card yandex"><div class="label">Показы</div><div class="value" id="y-impr">—</div><div class="sub">в результатах</div></div>
      <div class="card yandex"><div class="label">CTR</div><div class="value" id="y-ctr">—</div><div class="sub">кликабельность</div></div>
      <div class="card neutral"><div class="label">ИКС</div><div class="value" id="y-iks">—</div><div class="sub">индекс качества</div></div>
      <div class="card neutral"><div class="label">Страниц в поиске</div><div class="value" id="y-pages">—</div><div class="sub">Яндекс</div></div>
    </div>
    <div class="cards-col">
      <div class="col-title google">Google</div>
      <div class="card google"><div class="label">Клики</div><div class="value" id="g-clicks">—</div><div class="sub">из поиска</div></div>
      <div class="card google"><div class="label">Показы</div><div class="value" id="g-impr">—</div><div class="sub">в результатах</div></div>
      <div class="card google"><div class="label">CTR</div><div class="value" id="g-ctr">—</div><div class="sub">кликабельность</div></div>
      <div class="card google"><div class="label">Позиция</div><div class="value" id="g-pos">—</div><div class="sub">средняя</div></div>
    </div>
  </div>

  <!-- График -->
  <div class="section-title">Динамика по дням</div>
  <div class="chart-card">
    <div class="chart-top">
      <h3 id="chart-title">Клики</h3>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <div class="period-nav" style="margin:0;">
          <button class="period-btn active" data-chart-days="7">7 дней</button>
          <button class="period-btn" data-chart-days="28">28 дней</button>
          <button class="period-btn" data-chart-days="90">90 дней</button>
        </div>
        <div class="metric-btns">
          <button class="metric-btn active" data-metric="clicks">Клики</button>
          <button class="metric-btn" data-metric="impressions">Показы</button>
          <button class="metric-btn" data-metric="position">Позиция (Google)</button>
        </div>
      </div>
    </div>
    <canvas id="mainChart"></canvas>
  </div>

  <!-- Топ запросов -->
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid var(--border);">
    <div class="section-title" id="queries-title" style="margin-bottom:0;padding-bottom:0;border-bottom:none;">Топ запросов</div>
    <div class="period-nav" style="margin:0;">
      <button class="period-btn" data-table-days="7">7 дней</button>
      <button class="period-btn" data-table-days="28">28 дней</button>
      <button class="period-btn active" data-table-days="90">90 дней</button>
    </div>
  </div>
  <div class="tables">
    <div class="table-card">
      <div class="table-header"><span class="badge google"></span> Google</div>
      <table>
        <thead><tr><th>#</th><th>Запрос</th><th>Клики</th><th>Показы</th><th>Позиция</th></tr></thead>
        <tbody id="gsc-queries"></tbody>
      </table>
    </div>
    <div class="table-card">
      <div class="table-header"><span class="badge yandex"></span> Яндекс</div>
      <table>
        <thead><tr><th>#</th><th>Запрос</th><th>Клики</th><th>Показы</th><th>Позиция</th></tr></thead>
        <tbody id="ya-queries"></tbody>
      </table>
    </div>
  </div>

  <!-- Топ страниц Google -->
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid var(--border);">
    <div class="section-title" id="pages-title" style="margin-bottom:0;padding-bottom:0;border-bottom:none;">Топ страниц Google</div>
    <div class="period-nav" style="margin:0;">
      <button class="period-btn" data-pages-days="7">7 дней</button>
      <button class="period-btn" data-pages-days="28">28 дней</button>
      <button class="period-btn active" data-pages-days="90">90 дней</button>
    </div>
  </div>
  <div class="pages-section">
    <div class="table-card">
      <table>
        <thead><tr><th>#</th><th>Страница</th><th>Клики</th><th>Показы</th><th>CTR</th><th>Позиция</th></tr></thead>
        <tbody id="gsc-pages"></tbody>
      </table>
    </div>
  </div>

</div>

<script>
// ─── Встроенные данные ─────────────────────────────────────────────────
const GSC = {gsc_json};
const YANDEX = {yandex_json};

// ─── Утилиты ──────────────────────────────────────────────────────────
function fmt(n) {{
  if (n >= 1000000) return (n/1000000).toFixed(1) + 'M';
  if (n >= 1000) return (n/1000).toFixed(1) + 'K';
  return String(n);
}}

function posClass(p) {{
  if (p <= 10) return 'good';
  if (p <= 30) return 'mid';
  return 'low';
}}

function filterDailyByDays(days) {{
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days - 3);
  return GSC.daily.filter(r => new Date(r.date) >= cutoff);
}}

// ─── Карточки ─────────────────────────────────────────────────────────
function updateCards(days) {{
  const rows = filterDailyByDays(days);
  const clicks = rows.reduce((s, r) => s + r.clicks, 0);
  const impr = rows.reduce((s, r) => s + r.impressions, 0);
  const avgPos = rows.length > 0 ? (rows.reduce((s, r) => s + r.position, 0) / rows.length) : 0;
  const ctr = impr > 0 ? (clicks / impr * 100) : 0;

  document.getElementById('g-clicks').textContent = fmt(clicks);
  document.getElementById('g-impr').textContent = fmt(impr);
  document.getElementById('g-pos').textContent = avgPos.toFixed(1);
  document.getElementById('g-ctr').textContent = ctr.toFixed(1) + '%';

  // Яндекс — берём ближайший период
  const key = String(days);
  const yp = YANDEX && YANDEX.periods && YANDEX.periods[key];
  let yClicks = 0;
  if (yp) {{
    yClicks = yp.clicks || 0;
    document.getElementById('y-clicks').textContent = fmt(yClicks);
    document.getElementById('y-impr').textContent = fmt(yp.impressions);
    const yCtr = yp.impressions > 0 ? (yClicks / yp.impressions * 100) : 0;
    document.getElementById('y-ctr').textContent = yCtr.toFixed(1) + '%';
  }}
  if (YANDEX) {{
    document.getElementById('y-iks').textContent = YANDEX.iks !== null ? YANDEX.iks : '—';
    document.getElementById('y-pages').textContent = fmt(YANDEX.searchable_pages || 0);
  }}

  // Итого (Яндекс + Google)
  const yImpr = yp ? (yp.impressions || 0) : 0;
  const totalClicks = clicks + yClicks;
  const totalImpr = impr + yImpr;
  const totalCtr = totalImpr > 0 ? (totalClicks / totalImpr * 100) : 0;
  document.getElementById('t-clicks').textContent = fmt(totalClicks);
  document.getElementById('t-impr').textContent = fmt(totalImpr);
  document.getElementById('t-ctr').textContent = totalImpr > 0 ? totalCtr.toFixed(1) + '%' : '—';

  // Конверсия
  const leads = parseInt(document.getElementById('leads-input').value) || 0;
  const conv = totalClicks > 0 && leads > 0 ? (leads / totalClicks * 100) : 0;
  document.getElementById('conversion').textContent = conv > 0 ? conv.toFixed(2) + '%' : '—';
}}

// ─── График ───────────────────────────────────────────────────────────
let mainChart = null;
let activeMetric = 'clicks';

function filterYandexDailyByDays(days) {{
  if (!YANDEX || !YANDEX.daily) return [];
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days - 2);
  return YANDEX.daily.filter(r => new Date(r.date) >= cutoff);
}}

// Создаём объединённые labels из обоих источников
function buildLabels(days) {{
  const gRows = filterDailyByDays(days);
  const yRows = filterYandexDailyByDays(days);
  const all = new Set([...gRows.map(r => r.date), ...yRows.map(r => r.date)]);
  return [...all].sort();
}}

function updateCharts(days) {{
  const gc = 'rgba(0,0,0,0.06)', tc = '#6b7280';
  const labels = buildLabels(days);
  const shortLabels = labels.map(d => {{ const [,m,day] = d.split('-'); return `${{day}}.${{m}}`; }});

  const gRows = filterDailyByDays(days);
  const yRows = filterYandexDailyByDays(days);
  const gMap = Object.fromEntries(gRows.map(r => [r.date, r]));
  const yMap = Object.fromEntries(yRows.map(r => [r.date, r]));

  const datasets = [];

  if (activeMetric === 'clicks') {{
    datasets.push({{
      label: 'Клики Google',
      data: labels.map(d => gMap[d]?.clicks ?? null),
      borderColor: '#4285F4', backgroundColor: 'rgba(66,133,244,0.08)',
      borderWidth: 2, pointRadius: 0, tension: 0.3, fill: true, spanGaps: true,
    }});
    if (yRows.length > 0) datasets.push({{
      label: 'Клики Яндекс',
      data: labels.map(d => yMap[d]?.clicks ?? null),
      borderColor: '#fc3f1d', backgroundColor: 'rgba(252,63,29,0.07)',
      borderWidth: 2, pointRadius: 0, tension: 0.3, fill: true, spanGaps: true,
    }});
  }} else if (activeMetric === 'impressions') {{
    datasets.push({{
      label: 'Показы Google',
      data: labels.map(d => gMap[d]?.impressions ?? null),
      borderColor: '#a78bfa', backgroundColor: 'rgba(167,139,250,0.08)',
      borderWidth: 2, pointRadius: 0, tension: 0.3, fill: true, spanGaps: true,
    }});
    if (yRows.length > 0) datasets.push({{
      label: 'Показы Яндекс',
      data: labels.map(d => yMap[d]?.impressions ?? null),
      borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.07)',
      borderWidth: 2, pointRadius: 0, tension: 0.3, fill: true, spanGaps: true,
    }});
  }} else {{
    // position — только Google
    datasets.push({{
      label: 'Позиция Google',
      data: labels.map(d => gMap[d]?.position ?? null),
      borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.06)',
      borderWidth: 2, pointRadius: 0, tension: 0.3, fill: true, spanGaps: true,
    }});
  }}

  const reverseY = activeMetric === 'position';

  if (mainChart) mainChart.destroy();
  mainChart = new Chart(document.getElementById('mainChart'), {{
    type: 'line',
    data: {{ labels: shortLabels, datasets }},
    options: {{
      responsive: true,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{ legend: {{ labels: {{ color: tc, boxWidth: 12, font: {{ size: 11 }} }} }} }},
      scales: {{
        x: {{ ticks: {{ color: tc, maxTicksLimit: 14, font: {{ size: 11 }} }}, grid: {{ color: gc }} }},
        y: {{ reverse: reverseY, ticks: {{ color: tc, font: {{ size: 11 }} }}, grid: {{ color: gc }} }},
      }}
    }}
  }});
}}

document.querySelectorAll('.metric-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.metric-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeMetric = btn.dataset.metric;
    document.getElementById('chart-title').textContent = btn.textContent;
    updateCharts(activeDays);
  }});
}});

// ─── Таблицы ──────────────────────────────────────────────────────────
function renderQueryTable(tbodyId, queries) {{
  const tbody = document.getElementById(tbodyId);
  tbody.innerHTML = '';
  queries.slice(0, 30).forEach((q, i) => {{
    const pc = posClass(q.position);
    tbody.innerHTML += `<tr>
      <td class="num">${{i+1}}</td>
      <td><div class="query-text" title="${{q.query}}">${{q.query}}</div></td>
      <td class="num">${{fmt(q.clicks)}}</td>
      <td class="num">${{fmt(q.impressions)}}</td>
      <td class="pos ${{pc}}">${{q.position.toFixed(1)}}</td>
    </tr>`;
  }});
}}

function renderPagesTable(days) {{
  const key = String(days);
  const tbody = document.getElementById('gsc-pages');
  tbody.innerHTML = '';
  const list = (GSC.pages && GSC.pages[key]) ? GSC.pages[key] : [];
  list.slice(0, 30).forEach((p, i) => {{
    const pc = posClass(p.position);
    tbody.innerHTML += `<tr>
      <td class="num">${{i+1}}</td>
      <td><div class="page-url" title="${{p.page}}">${{p.page}}</div></td>
      <td class="num">${{fmt(p.clicks)}}</td>
      <td class="num">${{fmt(p.impressions)}}</td>
      <td class="num">${{p.ctr}}%</td>
      <td class="pos ${{pc}}">${{p.position.toFixed(1)}}</td>
    </tr>`;
  }});
}}


function renderQueriesByDays(days) {{
  const key = String(days);
  document.getElementById('queries-title').textContent = 'Топ запросов — ' + days + ' дней';
  const gQueries = (GSC.queries && GSC.queries[key]) ? GSC.queries[key] : [];
  const yQueries = (YANDEX && YANDEX.queries && YANDEX.queries[key]) ? YANDEX.queries[key] : [];
  renderQueryTable('gsc-queries', gQueries);
  renderQueryTable('ya-queries', yQueries);
}}

function renderPagesByDays(days) {{
  document.getElementById('pages-title').textContent = 'Топ страниц Google — ' + days + ' дней';
  renderPagesTable(days);
}}

// ─── Переключатель периода (карточки + график) ────────────────────────
let activeDays = 90;
let activeTableDays = 90;
let activePagesDays = 90;

document.querySelectorAll('[data-days]').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('[data-days]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeDays = parseInt(btn.dataset.days);
    updateCards(activeDays);
    updateCharts(activeDays);
  }});
}});

document.querySelectorAll('[data-chart-days]').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('[data-chart-days]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    updateCharts(parseInt(btn.dataset.chartDays));
  }});
}});

document.querySelectorAll('[data-table-days]').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('[data-table-days]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeTableDays = parseInt(btn.dataset.tableDays);
    renderQueriesByDays(activeTableDays);
  }});
}});

document.querySelectorAll('[data-pages-days]').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('[data-pages-days]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activePagesDays = parseInt(btn.dataset.pagesDays);
    renderPagesByDays(activePagesDays);
  }});
}});

// ─── Обновление данных ────────────────────────────────────────────────
async function refreshData() {{
  const btn = document.querySelector('.btn-refresh');
  btn.disabled = true;
  document.getElementById('spinner').style.display = 'block';
  document.getElementById('status-msg').textContent = 'Загружаю данные из GSC и Яндекс...';

  try {{
    const resp = await fetch('/api/refresh', {{ method: 'POST' }});
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json();

    // Обновляем глобальные данные
    Object.assign(GSC, data.gsc);
    Object.assign(YANDEX, data.yandex);

    // Перерисовываем всё
    updateCards(activeDays);
    updateCharts(activeDays);
    renderTables(activeDays);

    document.getElementById('updated-at').textContent = 'Данные от: ' + data.updated_at;
    document.getElementById('status-msg').textContent = '✓ Данные обновлены: ' + data.updated_at;
  }} catch (e) {{
    document.getElementById('status-msg').textContent = '✗ Ошибка: запусти python3 dashboard_server.py в терминале';
  }}

  document.getElementById('spinner').style.display = 'none';
  btn.disabled = false;
}}

// ─── Лиды localStorage ────────────────────────────────────────────────
const leadsInput = document.getElementById('leads-input');
leadsInput.value = localStorage.getItem('seo_leads') || '';
leadsInput.addEventListener('input', () => {{
  localStorage.setItem('seo_leads', leadsInput.value);
  updateCards(activeDays);
}});

// ─── Инициализация ────────────────────────────────────────────────────
updateCards(90);
updateCharts(7);
renderQueriesByDays(90);
renderPagesByDays(90);
</script>
</body>
</html>"""
    return html


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=== SEO Dashboard Generator ===")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n[1/2] Google Search Console...")
    gsc_data = None
    try:
        gsc_data = get_gsc_data()
        print(f"  Дней: {len(gsc_data['daily'])}, запросов: {len(gsc_data['queries'].get('28',[]))}, страниц: {len(gsc_data['pages'].get('28',[]))}")
    except Exception as e:
        print(f"  ОШИБКА: {e}")
        gsc_data = {'daily': [], 'queries': [], 'pages': []}

    print("\n[2/2] Яндекс.Вебмастер...")
    yandex_data = None
    try:
        yandex_data = get_yandex_data()
        if yandex_data:
            print(f"  ИКС: {yandex_data['iks']}, запросов: {len(yandex_data['queries'].get('28',[]))}")
    except Exception as e:
        print(f"  ОШИБКА: {e}")
        yandex_data = {'iks': None, 'searchable_pages': 0, 'queries': [], 'periods': {}}

    print("\nГенерирую HTML...")
    generated_at = datetime.now()
    html = generate_html(gsc_data, yandex_data, generated_at)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✅ Готово! Файл: {OUTPUT_FILE}")
    print(f"   URL после деплоя: https://dinamika-cargo.ru/seo-dashboard/")
    print(f"\nЧтобы задеплоить: git add . && git commit -m 'Dashboard: обновление данных' && git push origin main-secure")


if __name__ == '__main__':
    main()
