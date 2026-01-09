#!/usr/bin/env python3
"""
Генератор страниц маршрутов для ТК Динамика
Создаёт /routes/{город1-город2}/index.html для всех маршрутов

Использование:
  python3 generate_route_pages.py              # Все маршруты (1264 страницы)
  python3 generate_route_pages.py --test       # Тестовый режим (первые 5 маршрутов)
  python3 generate_route_pages.py --route moskva-kazan  # Только один маршрут
"""

import json
import os
import sys
import math
import re

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')
ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')
PHONES_FILE = os.path.join(BASE_DIR, 'data', 'city-phones.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'route-template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'routes')
META_MAPPING_FILE = os.path.join(BASE_DIR, 'data', 'routes-meta-mapping.json')

# 17 крупных городов (областные центры и крупные города РФ)
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

# Крупные города без Москвы (для маршрутов с Подмосковьем)
MAJOR_CITIES_NO_MOSCOW = [c for c in MAJOR_CITIES if c != 'moskva']

# Алиасы для URL (spb вместо saint-petersburg в URL маршрутов)
CITY_URL_ALIASES = {
    'saint-petersburg': 'spb'
}

# FAQ для всех маршрутов (общие вопросы)
ROUTE_FAQ = [
    {
        'question': 'Сколько стоит перевозка {FROM} — {TO}?',
        'answer': 'Стоимость зависит от тоннажа и типа кузова. Газель (1-3 тонны) — от {PRICE_1T} ₽, пятитонник — от {PRICE_5T} ₽, еврофура (20 тонн) — от {PRICE_20T} ₽. Точную цену рассчитаем за 5 минут после заявки.'
    },
    {
        'question': 'Сколько времени занимает доставка?',
        'answer': 'Расстояние {FROM} — {TO} составляет {DISTANCE} км. Стандартный срок доставки — {DELIVERY_TIME}. Точное время зависит от загрузки, дорожной ситуации и типа транспорта.'
    },
    {
        'question': 'Как рассчитывается ваша комиссия?',
        'answer': '<p><strong>Без НДС:</strong> 5 000 ₽ + 1% от стоимости перевозки.</p><p><strong>С НДС:</strong> 6 000 ₽ + 1,5% от стоимости перевозки.</p><p class="mb-0">Мы показываем закупочную цену и комиссию отдельно — всё прозрачно.</p>'
    },
    {
        'question': 'Можно ли отследить груз в пути?',
        'answer': 'Да, мы контролируем перевозку на всех этапах и информируем вас о местоположении груза. По запросу предоставляем фото при погрузке и выгрузке.'
    },
    {
        'question': 'Что если груз повредят в дороге?',
        'answer': 'Мы несём полную ответственность за груз согласно ГК РФ и Уставу автомобильного транспорта. За 7 лет работы — ни одного случая полной утери груза, все повреждения компенсированы.'
    }
]


def load_json(filepath):
    """Загружает JSON файл"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_meta_mapping():
    """Загружает маппинг мета-тегов (если существует)"""
    if os.path.exists(META_MAPPING_FILE):
        with open(META_MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_meta_mapping(mapping):
    """Сохраняет маппинг мета-тегов"""
    with open(META_MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def extract_meta_from_html(html_content):
    """Извлекает мета-теги из существующего HTML"""
    meta = {}

    # Title
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    if title_match:
        meta['title'] = title_match.group(1)

    # Description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    if desc_match:
        meta['description'] = desc_match.group(1)

    # Canonical
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', html_content)
    if canonical_match:
        meta['canonical'] = canonical_match.group(1)

    return meta


def get_existing_meta(route_slug, meta_mapping):
    """Получает сохранённые мета-теги для маршрута"""
    # Сначала проверяем маппинг
    if route_slug in meta_mapping:
        return meta_mapping[route_slug]

    # Если нет в маппинге, пробуем извлечь из существующего файла
    existing_file = os.path.join(OUTPUT_DIR, route_slug, 'index.html')
    if os.path.exists(existing_file):
        with open(existing_file, 'r', encoding='utf-8') as f:
            html = f.read()
        return extract_meta_from_html(html)

    return None


def load_template():
    """Загружает HTML шаблон"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def calculate_distance(lat1, lon1, lat2, lon2):
    """Расчёт расстояния между двумя точками (формула Хаверсайна)"""
    R = 6371  # Радиус Земли в км

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Умножаем на 1.3 для учёта реального расстояния по дорогам
    return int(R * c * 1.3)


def calculate_prices(distance_km):
    """
    Расчёт цен по формуле:
    - 1-3т: км × 30, минимум 20 000 ₽
    - 5т: км × 40, минимум 25 000 ₽
    - 10т: км × 50, минимум 30 000 ₽
    - 20т: км × 80, минимум 40 000 ₽
    """
    prices = {
        '1t': max(distance_km * 30, 20000),
        '5t': max(distance_km * 40, 25000),
        '10t': max(distance_km * 50, 30000),
        '20t': max(distance_km * 80, 40000)
    }
    return prices


def calculate_delivery_time(distance_km):
    """Расчёт времени доставки"""
    if distance_km <= 500:
        return '1 день'
    elif distance_km <= 1000:
        return '1-2 дня'
    elif distance_km <= 1500:
        return '2-3 дня'
    elif distance_km <= 2000:
        return '3-4 дня'
    else:
        days = int(distance_km / 500)
        return f'{days}-{days+2} дней'


def format_price(price):
    """Форматирование цены с разделителями тысяч"""
    return f"{price:,}".replace(',', ' ')


def get_route_slug(city_from, city_to):
    """Генерирует slug для маршрута"""
    from_slug = CITY_URL_ALIASES.get(city_from, city_from)
    to_slug = CITY_URL_ALIASES.get(city_to, city_to)
    return f"{from_slug}-{to_slug}"


def get_reverse_route_slug(city_from, city_to):
    """Генерирует slug для обратного маршрута"""
    return get_route_slug(city_to, city_from)


def generate_faq_html(city_from_name, city_to_name, distance, delivery_time, prices):
    """Генерирует HTML блок FAQ для маршрута"""
    html_parts = []

    for idx, item in enumerate(ROUTE_FAQ, 1):
        question = item['question'].replace('{FROM}', city_from_name).replace('{TO}', city_to_name)
        answer = item['answer']
        answer = answer.replace('{FROM}', city_from_name)
        answer = answer.replace('{TO}', city_to_name)
        answer = answer.replace('{DISTANCE}', str(distance))
        answer = answer.replace('{DELIVERY_TIME}', delivery_time)
        answer = answer.replace('{PRICE_1T}', format_price(prices['1t']))
        answer = answer.replace('{PRICE_5T}', format_price(prices['5t']))
        answer = answer.replace('{PRICE_20T}', format_price(prices['20t']))

        html_parts.append(f'''                <div class="accordion-item">
                    <h3 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq{idx}">
                            {question}
                        </button>
                    </h3>
                    <div id="faq{idx}" class="accordion-collapse collapse">
                        <div class="accordion-body">
                            {answer}
                        </div>
                    </div>
                </div>''')

    return '\n'.join(html_parts)


def generate_route_page(city_from, city_to, cities, addresses, phones, template, existing_meta=None):
    """Генерирует HTML страницу для маршрута. Если existing_meta передан, использует сохранённые мета-теги."""

    # Данные города отправления
    from_data = cities.get(city_from, {})
    from_address = addresses.get(city_from, {})
    from_phone = phones.get(city_from, '+7-800-707-29-36')

    # Данные города назначения
    to_data = cities.get(city_to, {})
    to_address = addresses.get(city_to, {})

    # Названия городов
    city_from_name = from_data.get('name', city_from)
    city_to_name = to_data.get('name', city_to)
    city_from_genitive = from_data.get('genitive', city_from_name)
    city_to_genitive = to_data.get('genitive', city_to_name)
    city_from_prepositional = from_data.get('prepositional', city_from_name)

    # Регион города отправления
    region_name = from_data.get('region', '')

    # Координаты
    lat_from = from_address.get('latitude', 55.75)
    lon_from = from_address.get('longitude', 37.62)
    lat_to = to_address.get('latitude', 55.75)
    lon_to = to_address.get('longitude', 37.62)

    # Расстояние и время
    distance = calculate_distance(lat_from, lon_from, lat_to, lon_to)
    delivery_time = calculate_delivery_time(distance)

    # Цены
    prices = calculate_prices(distance)

    # Slugs
    route_slug = get_route_slug(city_from, city_to)
    reverse_slug = get_reverse_route_slug(city_from, city_to)

    # Адрес офиса (город отправления)
    bc_name = from_address.get('name', 'Офис')
    bc_street = from_address.get('street', '')
    bc_office = from_address.get('office', '')
    postal_code = from_address.get('postalCode', '')

    # Центр карты (между двумя городами)
    lat_center = (lat_from + lat_to) / 2
    lon_center = (lon_from + lon_to) / 2

    # Уровень зума на основе расстояния
    if distance <= 300:
        zoom_level = 7
    elif distance <= 600:
        zoom_level = 6
    elif distance <= 1000:
        zoom_level = 5
    elif distance <= 1500:
        zoom_level = 4
    else:
        zoom_level = 3

    # Генерируем FAQ
    faq_html = generate_faq_html(city_from_name, city_to_name, distance, delivery_time, prices)

    # Мета-теги: используем сохранённые или генерируем новые
    if existing_meta and 'title' in existing_meta:
        meta_title = existing_meta['title']
    else:
        meta_title = f"Грузоперевозки {city_from_name} — {city_to_name} | Цены, сроки - ТК Динамика"

    if existing_meta and 'description' in existing_meta:
        meta_description = existing_meta['description']
    else:
        meta_description = f"Грузоперевозки {city_from_name} — {city_to_name}. Расстояние {distance} км. Доставка от 1 до 20 тонн. Прозрачные цены, расчёт за 5 минут. ☎ 8-800-707-29-36"

    # Canonical всегда одинаковый
    meta_canonical = f"https://dinamika-cargo.ru/routes/{route_slug}/"

    # Заменяем плейсхолдеры
    html = template

    # Мета-теги (заменяем сгенерированные шаблоном на сохранённые/новые)
    html = re.sub(r'<title>[^<]+</title>', f'<title>{meta_title}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{meta_description}"', html)

    # Города
    html = html.replace('{{CITY_FROM}}', city_from_name)
    html = html.replace('{{CITY_TO}}', city_to_name)
    html = html.replace('{{CITY_FROM_GENITIVE}}', city_from_genitive)
    html = html.replace('{{CITY_TO_GENITIVE}}', city_to_genitive)
    html = html.replace('{{CITY_FROM_PREPOSITIONAL}}', city_from_prepositional)

    # Маршрут
    html = html.replace('{{ROUTE_SLUG}}', route_slug)
    html = html.replace('{{REVERSE_ROUTE_SLUG}}', reverse_slug)
    html = html.replace('{{DISTANCE}}', str(distance))
    html = html.replace('{{DELIVERY_TIME}}', delivery_time)

    # Цены
    html = html.replace('{{PRICE_1T}}', format_price(prices['1t']))
    html = html.replace('{{PRICE_5T}}', format_price(prices['5t']))
    html = html.replace('{{PRICE_10T}}', format_price(prices['10t']))
    html = html.replace('{{PRICE_20T}}', format_price(prices['20t']))
    html = html.replace('{{MIN_PRICE}}', format_price(prices['1t']))

    # Координаты
    html = html.replace('{{LAT_FROM}}', str(lat_from))
    html = html.replace('{{LON_FROM}}', str(lon_from))
    html = html.replace('{{LAT_TO}}', str(lat_to))
    html = html.replace('{{LON_TO}}', str(lon_to))
    html = html.replace('{{LAT_CENTER}}', str(lat_center))
    html = html.replace('{{LON_CENTER}}', str(lon_center))
    html = html.replace('{{ZOOM_LEVEL}}', str(zoom_level))

    # Офис (город отправления)
    html = html.replace('{{BC_NAME}}', bc_name)
    html = html.replace('{{BC_STREET}}', bc_street)
    html = html.replace('{{BC_ADDRESS}}', bc_street)
    html = html.replace('{{BC_OFFICE}}', f'офис {bc_office}')
    html = html.replace('{{POSTAL_CODE}}', postal_code)
    html = html.replace('{{PHONE_CITY}}', from_phone)
    html = html.replace('{{REGION_NAME}}', region_name)

    # FAQ
    html = html.replace('{{FAQ_ITEMS}}', faq_html)

    # Возвращаем HTML и мета-теги для сохранения в маппинг
    generated_meta = {
        'title': meta_title,
        'description': meta_description,
        'canonical': meta_canonical
    }

    return html, generated_meta


def generate_all_routes():
    """
    Генерирует список всех маршрутов (1264 штуки):
    - 272: между крупными городами (17 × 16)
    - 992: Подмосковье ↔ крупные города без Москвы (31 × 16 × 2)

    Исключены:
    - Москва ↔ Подмосковье (не делаем)
    - Подмосковье ↔ Подмосковье (не делаем)
    """
    routes = []

    # 1. Маршруты между крупными городами (17 × 16 = 272)
    for city_from in MAJOR_CITIES:
        for city_to in MAJOR_CITIES:
            if city_from != city_to:
                routes.append((city_from, city_to))

    # 2. Маршруты Подмосковье ↔ крупные города (без Москвы!)
    for mo_city in MOSCOW_REGION_CITIES:
        for major_city in MAJOR_CITIES_NO_MOSCOW:
            routes.append((mo_city, major_city))  # из Подмосковья
            routes.append((major_city, mo_city))  # в Подмосковье

    return routes


def main():
    print("=== Генератор страниц маршрутов ===\n")

    # Парсинг аргументов
    test_mode = '--test' in sys.argv
    target_route = None

    if '--route' in sys.argv:
        idx = sys.argv.index('--route')
        if idx + 1 < len(sys.argv):
            target_route = sys.argv[idx + 1]
            print(f"Режим: генерация только маршрута '{target_route}'\n")

    if test_mode:
        print("Тестовый режим: первые 5 маршрутов\n")

    # Загрузка данных
    cities = load_json(CITIES_FILE)
    addresses = load_json(ADDRESSES_FILE)
    phones = load_json(PHONES_FILE)
    template = load_template()
    meta_mapping = load_meta_mapping()

    print(f"Загружено городов: {len(cities)}")
    print(f"Загружено адресов: {len(addresses)}")
    print(f"Загружено телефонов: {len(phones)}")
    print(f"Загружено мета-тегов: {len(meta_mapping)}")
    print(f"Шаблон: {TEMPLATE_FILE}\n")

    # Генерируем список маршрутов
    routes = generate_all_routes()
    print(f"Всего маршрутов: {len(routes)}\n")

    # Фильтруем если указан конкретный маршрут
    if target_route:
        # Ищем маршрут по slug
        found = False
        for city_from, city_to in routes:
            if get_route_slug(city_from, city_to) == target_route:
                routes = [(city_from, city_to)]
                found = True
                break
        if not found:
            print(f"Ошибка: маршрут '{target_route}' не найден")
            return

    # Тестовый режим
    if test_mode:
        routes = routes[:5]

    # Создаём директорию routes
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    created = 0
    errors = 0

    for city_from, city_to in routes:
        route_slug = get_route_slug(city_from, city_to)

        try:
            # Получаем сохранённые мета-теги (если есть)
            existing_meta = get_existing_meta(route_slug, meta_mapping)

            # Генерируем HTML
            html, generated_meta = generate_route_page(city_from, city_to, cities, addresses, phones, template, existing_meta)

            # Сохраняем мета-теги в маппинг
            meta_mapping[route_slug] = generated_meta

            # Создаём папку маршрута
            route_dir = os.path.join(OUTPUT_DIR, route_slug)
            os.makedirs(route_dir, exist_ok=True)

            # Сохраняем файл
            output_file = os.path.join(route_dir, 'index.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            city_from_name = cities.get(city_from, {}).get('name', city_from)
            city_to_name = cities.get(city_to, {}).get('name', city_to)
            print(f"✓ {city_from_name} → {city_to_name} → /routes/{route_slug}/")
            created += 1

        except Exception as e:
            print(f"✗ Ошибка {route_slug}: {e}")
            errors += 1

    # Сохраняем маппинг мета-тегов
    save_meta_mapping(meta_mapping)
    print(f"\n💾 Маппинг мета-тегов сохранён в {META_MAPPING_FILE}")

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Сохранено мета-тегов: {len(meta_mapping)}")
    print(f"Ошибок: {errors}")


if __name__ == '__main__':
    main()
