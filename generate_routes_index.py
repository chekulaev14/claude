#!/usr/bin/env python3
"""
Генератор страницы /routes/index.html со всеми маршрутами
"""

import json
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')
ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'routes', 'index.html')

# 17 крупных городов
MAJOR_CITIES = [
    'moskva', 'kazan', 'samara', 'kaluga', 'obninsk', 'tula', 'tver',
    'yaroslavl', 'saint-petersburg', 'nizhny-novgorod', 'nizhnekamsk',
    'naberezhnye-chelny', 'izhevsk', 'ufa', 'chelyabinsk', 'ekaterinburg', 'perm'
]

# 31 город Московской области
MOSCOW_REGION_CITIES = [
    'balashikha', 'podolsk', 'khimki', 'korolev', 'mytishchi', 'lyubertsy',
    'krasnogorsk', 'elektrostal', 'kolomna', 'odintsovo', 'domodedovo',
    'serpukhov', 'shchelkovo', 'orekhovo-zuevo', 'ramenskoe', 'dolgoprudny',
    'zhukovsky', 'pushkino', 'reutov', 'sergiev-posad', 'voskresensk',
    'lobnya', 'klin', 'ivanteyevka', 'dubna', 'egoryevsk', 'chekhov',
    'dmitrov', 'noginsk', 'fryazino', 'dzerzhinsky'
]

MAJOR_CITIES_NO_MOSCOW = [c for c in MAJOR_CITIES if c != 'moskva']

CITY_URL_ALIASES = {
    'saint-petersburg': 'spb'
}


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c * 1.3)


def calculate_prices(distance_km):
    return {
        '1t': max(distance_km * 30, 20000),
        '5t': max(distance_km * 40, 25000),
        '10t': max(distance_km * 50, 30000),
        '20t': max(distance_km * 80, 40000)
    }


def format_price(price):
    return f"{price:,}".replace(',', ' ')


def get_route_slug(city_from, city_to):
    from_slug = CITY_URL_ALIASES.get(city_from, city_from)
    to_slug = CITY_URL_ALIASES.get(city_to, city_to)
    return f"{from_slug}-{to_slug}"


def get_all_routes(cities, addresses):
    """
    Генерирует все маршруты (1264 штуки):
    - 272: между крупными городами (17 × 16)
    - 992: Подмосковье ↔ крупные города без Москвы (31 × 16 × 2)
    """
    route_pairs = []

    # 1. Маршруты между крупными городами (17 × 16 = 272)
    for city_from in MAJOR_CITIES:
        for city_to in MAJOR_CITIES:
            if city_from != city_to:
                route_pairs.append((city_from, city_to))

    # 2. Маршруты Подмосковье ↔ крупные города (без Москвы!)
    for mo_city in MOSCOW_REGION_CITIES:
        for major_city in MAJOR_CITIES_NO_MOSCOW:
            route_pairs.append((mo_city, major_city))  # из Подмосковья
            route_pairs.append((major_city, mo_city))  # в Подмосковье

    routes = []
    for city_from, city_to in route_pairs:
        city_from_data = cities.get(city_from)
        city_to_data = cities.get(city_to)
        if not city_from_data or not city_to_data:
            continue

        city_from_name = city_from_data.get('name', city_from)
        city_to_name = city_to_data.get('name', city_to)

        addr_from = addresses.get(city_from, {})
        addr_to = addresses.get(city_to, {})
        lat_from = addr_from.get('latitude', 55.75)
        lon_from = addr_from.get('longitude', 37.62)
        lat_to = addr_to.get('latitude', 55.75)
        lon_to = addr_to.get('longitude', 37.62)

        distance = calculate_distance(lat_from, lon_from, lat_to, lon_to)
        prices = calculate_prices(distance)
        slug = get_route_slug(city_from, city_to)

        route_name = f"{city_from_name} — {city_to_name}"

        routes.append({
            'name': route_name,
            'slug': slug,
            'distance': distance,
            'prices': prices
        })

    # Сортируем по алфавиту
    routes.sort(key=lambda x: x['name'])
    return routes


def generate_table_rows(routes):
    """Генерирует строки таблицы"""
    rows = []
    for route in routes:
        rows.append(f'''                        <tr>
                            <td><a href="/routes/{route['slug']}/" class="route-table-link">{route['name']}</a></td>
                            <td>{route['distance']} км</td>
                            <td>от {format_price(route['prices']['1t'])} ₽</td>
                            <td>от {format_price(route['prices']['5t'])} ₽</td>
                            <td>от {format_price(route['prices']['10t'])} ₽</td>
                            <td>от {format_price(route['prices']['20t'])} ₽</td>
                        </tr>''')
    return '\n'.join(rows)


def main():
    print("Загружаем данные...")
    cities = load_json(CITIES_FILE)
    addresses = load_json(ADDRESSES_FILE)

    print("Генерируем маршруты...")
    routes = get_all_routes(cities, addresses)
    print(f"Всего маршрутов: {len(routes)}")

    table_rows = generate_table_rows(routes)

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Все маршруты грузоперевозок по России | ТК Динамика</title>
    <meta name="description" content="Полный каталог маршрутов грузоперевозок ТК Динамика. {len(routes)} направлений по России с ценами. Москва, Санкт-Петербург, Казань, Екатеринбург и другие города.">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/assets/images/favicon-new.png?v=4">
    <link rel="apple-touch-icon" href="/assets/images/favicon-new.png?v=4">

    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link href="/assets/css/styles.css" rel="stylesheet">

    <!-- Yandex.Metrika counter -->
    <script type="text/javascript">
        (function(m,e,t,r,i,k,a){{
            m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
            m[i].l=1*new Date();
            for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
            k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
        }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=103783702', 'ym');

        ym(103783702, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true}});
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/103783702" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
    <!-- /Yandex.Metrika counter -->

    <style>
        .routes-page {{
            padding-top: 80px;
            min-height: 100vh;
        }}
        .hero-section h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3436;
        }}
        .stat-card {{
            transition: transform 0.2s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: #2563eb;
        }}
        .stat-label {{
            color: #636e72;
            font-size: 0.9rem;
        }}
        .routes-table {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .routes-table th {{
            font-weight: 600;
            color: #2d3436;
            border-bottom: 2px solid #dee2e6;
            padding: 1rem;
            white-space: nowrap;
            position: sticky;
            top: 0;
            background: #f8f9fa;
            z-index: 10;
        }}
        .routes-table td {{
            padding: 0.75rem 1rem;
            vertical-align: middle;
        }}
        .routes-table tbody tr:hover {{
            background-color: #f8f9fa;
        }}
        .route-table-link {{
            color: #2563eb;
            text-decoration: none;
            font-weight: 500;
        }}
        .route-table-link:hover {{
            text-decoration: underline;
        }}
        .table-container {{
            max-height: 800px;
            overflow-y: auto;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .cta-section {{
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        }}
        .service-card {{
            transition: all 0.2s;
            border: 1px solid transparent;
        }}
        .service-card:hover {{
            background: #e2e8f0 !important;
            border-color: #2563eb;
            transform: translateY(-3px);
        }}
        .service-card i {{
            display: block;
        }}
        @media (max-width: 768px) {{
            .routes-table th,
            .routes-table td {{
                padding: 0.5rem;
                font-size: 0.85rem;
            }}
            .table-container {{
                max-height: 600px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header Placeholder -->
    <div id="header-placeholder"></div>

    <main class="routes-page">
        <div class="container">
            <!-- Breadcrumbs -->
            <nav aria-label="breadcrumb" class="pt-4">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="/">Главная</a></li>
                    <li class="breadcrumb-item active">Маршруты</li>
                </ol>
            </nav>

            <!-- Hero Section -->
            <section class="hero-section mt-2 mb-5">
                <h1>Все маршруты грузоперевозок</h1>
                <p class="lead mt-4">Транспортная компания «Динамика» осуществляет грузоперевозки по <strong>{len(routes)} маршрутам</strong> между городами России. Выберите нужный маршрут для расчёта стоимости и сроков доставки.</p>
                <p class="mt-3">Работаем с 2018 года, перевозим грузы от 100 кг до 24 тонн. Прозрачное ценообразование: вы видите закупочную цену и нашу комиссию отдельно. Страхование каждого груза, отслеживание в пути, документальное сопровождение.</p>
            </section>

            <!-- Stats -->
            <section class="stats-section mb-5">
                <div class="row text-center g-4">
                    <div class="col-6 col-md-3">
                        <div class="stat-card p-4 rounded bg-light h-100">
                            <i class="bi bi-signpost-2 text-primary fs-1 mb-3"></i>
                            <div class="stat-number">{len(routes)}</div>
                            <div class="stat-label">маршрутов</div>
                        </div>
                    </div>
                    <div class="col-6 col-md-3">
                        <div class="stat-card p-4 rounded bg-light h-100">
                            <i class="bi bi-geo-alt text-primary fs-1 mb-3"></i>
                            <div class="stat-number">48</div>
                            <div class="stat-label">городов</div>
                        </div>
                    </div>
                    <div class="col-6 col-md-3">
                        <div class="stat-card p-4 rounded bg-light h-100">
                            <i class="bi bi-truck text-primary fs-1 mb-3"></i>
                            <div class="stat-number">24т</div>
                            <div class="stat-label">макс. вес</div>
                        </div>
                    </div>
                    <div class="col-6 col-md-3">
                        <div class="stat-card p-4 rounded bg-light h-100">
                            <i class="bi bi-shield-check text-primary fs-1 mb-3"></i>
                            <div class="stat-number">100%</div>
                            <div class="stat-label">страхование</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- All Routes Table -->
            <section class="all-routes mb-5">
                <h2 class="mb-4">Все маршруты (по алфавиту)</h2>
                <p class="text-muted mb-4">Цены указаны ориентировочно и зависят от типа груза и условий перевозки.</p>
                <div class="table-container">
                    <table class="table table-hover routes-table mb-0">
                        <thead>
                            <tr>
                                <th>Маршрут</th>
                                <th>Расстояние</th>
                                <th>1-3 т</th>
                                <th>5 т</th>
                                <th>10 т</th>
                                <th>20 т</th>
                            </tr>
                        </thead>
                        <tbody>
{table_rows}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Услуги и перелинковка -->
            <section class="services-links mb-5">
                <h2 class="mb-4">Наши услуги</h2>
                <div class="row g-4">
                    <div class="col-md-6 col-lg-3">
                        <a href="/regions/moskva/mezhgorod/" class="service-card text-decoration-none d-block p-4 bg-light rounded h-100">
                            <i class="bi bi-signpost-2 text-primary fs-2 mb-3"></i>
                            <h3 class="h6 mb-2">Междугородние перевозки</h3>
                            <p class="text-muted small mb-0">Доставка грузов между городами России</p>
                        </a>
                    </div>
                    <div class="col-md-6 col-lg-3">
                        <a href="/regions/moskva/fura/" class="service-card text-decoration-none d-block p-4 bg-light rounded h-100">
                            <i class="bi bi-truck-front text-primary fs-2 mb-3"></i>
                            <h3 class="h6 mb-2">Перевозка фурами</h3>
                            <p class="text-muted small mb-0">Полная загрузка 5-20 тонн</p>
                        </a>
                    </div>
                    <div class="col-md-6 col-lg-3">
                        <a href="/regions/moskva/dlinnomer/" class="service-card text-decoration-none d-block p-4 bg-light rounded h-100">
                            <i class="bi bi-arrows-expand text-primary fs-2 mb-3"></i>
                            <h3 class="h6 mb-2">Длинномеры</h3>
                            <p class="text-muted small mb-0">Негабаритные грузы до 24 метров</p>
                        </a>
                    </div>
                    <div class="col-md-6 col-lg-3">
                        <a href="/regions/" class="service-card text-decoration-none d-block p-4 bg-light rounded h-100">
                            <i class="bi bi-geo-alt text-primary fs-2 mb-3"></i>
                            <h3 class="h6 mb-2">Все регионы</h3>
                            <p class="text-muted small mb-0">48 городов России</p>
                        </a>
                    </div>
                </div>
            </section>

        </div>
    </main>

    <!-- Callback Section -->
    <section id="callback-section" class="py-5 bg-primary text-white">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto text-center">
                    <h2 class="mb-4">Любой груз, любой транспорт, любой маршрут</h2>
                    <p class="lead mb-4">Оставляйте заявку, сделаем расчёт!</p>
                    <div style="max-width: 400px; margin: 0 auto;">
                        <form id="callbackForm" class="callback-form">
                            <div class="mb-3">
                                <input type="tel" id="phone" name="phone" class="form-control form-control-lg" placeholder="+7 (___) ___-__-__" value="+7 " required>
                            </div>
                            <button type="submit" class="btn btn-light btn-lg w-100">
                                <i class="bi bi-telephone-fill me-2"></i>Позвоните мне
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer Placeholder -->
    <div id="footer-placeholder"></div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Template Loader -->
    <script src="/assets/js/template-loader.js"></script>
    <script src="/assets/js/script.js"></script>
    <script src="/assets/js/forms-handler.js"></script>
</body>
</html>'''

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\nГотово! Создан файл: {OUTPUT_FILE}")
    print(f"Маршрутов в таблице: {len(routes)}")


if __name__ == '__main__':
    main()
