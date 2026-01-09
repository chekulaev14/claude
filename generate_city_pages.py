#!/usr/bin/env python3
"""
Генератор страниц городов для ТК Динамика
Создаёт /regions/{город}/index.html для всех городов из cities.json

Использование:
  python3 generate_city_pages.py              # Все города
  python3 generate_city_pages.py --city balashikha  # Только Балашиха
"""

import json
import os
import sys
import re

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')
ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')
PHONES_FILE = os.path.join(BASE_DIR, 'data', 'city-phones.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'city-index-template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')
META_MAPPING_FILE = os.path.join(BASE_DIR, 'data', 'cities-meta-mapping.json')
CARGO_CLUSTERS_FILE = os.path.join(BASE_DIR, 'data', 'cargo-clusters.json')

def load_cities():
    """Загружает данные городов из JSON"""
    with open(CITIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_addresses():
    """Загружает адреса БЦ из JSON"""
    with open(ADDRESSES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_phones():
    """Загружает телефоны городов из JSON"""
    with open(PHONES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template():
    """Загружает HTML шаблон"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def load_cargo_clusters():
    """Загружает конфигурацию cargo-кластеров из JSON"""
    if os.path.exists(CARGO_CLUSTERS_FILE):
        with open(CARGO_CLUSTERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def generate_cargo_clusters_html(cargo_clusters):
    """Генерирует HTML блок с cargo-кластерами (перевозка по типам грузов)"""
    if not cargo_clusters:
        return ''

    html_parts = []
    for cluster_slug, config in cargo_clusters.items():
        icon = config.get('icon', 'bi-box')
        title = config.get('title', cluster_slug)
        description = config.get('description', '')
        html_parts.append(f'''                <div class="col-md-6 col-lg-3">
                    <a href="{cluster_slug}/" class="service-card">
                        <i class="bi {icon}"></i>
                        <h3>{title}</h3>
                        <p>{description}</p>
                    </a>
                </div>''')
    return '\n'.join(html_parts)


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

    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    if title_match:
        meta['title'] = title_match.group(1)

    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    if desc_match:
        meta['description'] = desc_match.group(1)

    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', html_content)
    if canonical_match:
        meta['canonical'] = canonical_match.group(1)

    return meta


def get_existing_meta(city_slug, meta_mapping):
    """Получает сохранённые мета-теги для города"""
    if city_slug in meta_mapping:
        return meta_mapping[city_slug]

    existing_file = os.path.join(OUTPUT_DIR, city_slug, 'index.html')
    if os.path.exists(existing_file):
        with open(existing_file, 'r', encoding='utf-8') as f:
            html = f.read()
        return extract_meta_from_html(html)

    return None


def generate_city_page(city_slug, city_data, addresses, phones, template, cargo_clusters, existing_meta=None):
    """Генерирует HTML страницу для города. Если existing_meta передан, использует сохранённые мета-теги."""
    city_name = city_data['name']

    # Мета-теги: используем сохранённые или генерируем новые
    if existing_meta and 'title' in existing_meta:
        meta_title = existing_meta['title']
    else:
        meta_title = f"Грузоперевозки {city_name} — ТК Динамика | Доставка грузов по России"

    if existing_meta and 'description' in existing_meta:
        meta_description = existing_meta['description']
    else:
        meta_description = f"Грузоперевозки в {city_data['prepositional']}. Междугородние перевозки, транспортные услуги, длинномеры, фуры. Доставка по России от 1 до 20 тонн. ☎ 8-800-707-29-36"

    meta_canonical = f"https://dinamika-cargo.ru/regions/{city_slug}/"

    html = template

    # Мета-теги (заменяем сгенерированные шаблоном на сохранённые/новые)
    html = re.sub(r'<title>[^<]+</title>', f'<title>{meta_title}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]+"', f'<meta name="description" content="{meta_description}"', html)

    # Замена плейсхолдеров города
    html = html.replace('{{CITY_SLUG}}', city_slug)
    html = html.replace('{{CITY_NAME}}', city_name)
    html = html.replace('{{CITY_GENITIVE}}', city_data['genitive'])
    html = html.replace('{{CITY_PREPOSITIONAL}}', city_data['prepositional'])
    html = html.replace('{{REGION_DATIVE}}', city_data['region_dative'])

    # Замена плейсхолдеров региона
    html = html.replace('{{REGION_NAME}}', city_data.get('region', ''))

    # Замена плейсхолдеров БЦ и контактов
    address_data = addresses.get(city_slug, {})
    html = html.replace('{{BC_NAME}}', address_data.get('name', ''))
    html = html.replace('{{BC_ADDRESS}}', address_data.get('street', ''))
    html = html.replace('{{BC_OFFICE}}', address_data.get('office', ''))

    # Координаты и индекс для Schema.org LocalBusiness
    html = html.replace('{{POSTAL_CODE}}', address_data.get('postalCode', ''))
    html = html.replace('{{LATITUDE}}', str(address_data.get('latitude', 0)))
    html = html.replace('{{LONGITUDE}}', str(address_data.get('longitude', 0)))

    # Замена телефона
    phone = phones.get(city_slug, '')
    html = html.replace('{{PHONE_CITY}}', phone)

    # Генерируем блок cargo-кластеров (перевозка по типам грузов)
    cargo_clusters_html = generate_cargo_clusters_html(cargo_clusters)
    html = html.replace('{{CARGO_CLUSTERS}}', cargo_clusters_html)

    # Возвращаем HTML и мета-теги для сохранения
    generated_meta = {
        'title': meta_title,
        'description': meta_description,
        'canonical': meta_canonical
    }

    return html, generated_meta

def main():
    print("=== Генератор страниц городов ===\n")

    # Парсинг аргументов
    target_city = None
    if '--city' in sys.argv:
        idx = sys.argv.index('--city')
        if idx + 1 < len(sys.argv):
            target_city = sys.argv[idx + 1]
            print(f"🎯 Режим: генерация только города '{target_city}'\n")

    # Загрузка данных
    cities = load_cities()
    addresses = load_addresses()
    phones = load_phones()
    template = load_template()
    meta_mapping = load_meta_mapping()
    cargo_clusters = load_cargo_clusters()

    print(f"Загружено городов: {len(cities)}")
    print(f"Загружено адресов БЦ: {len(addresses)}")
    print(f"Загружено телефонов: {len(phones)}")
    print(f"Загружено мета-тегов: {len(meta_mapping)}")
    print(f"Загружено cargo-кластеров: {len(cargo_clusters)}")
    print(f"Шаблон: {TEMPLATE_FILE}\n")

    # Фильтруем города если указан --city
    if target_city:
        if target_city not in cities:
            print(f"❌ Ошибка: город '{target_city}' не найден в cities.json")
            return
        cities = {target_city: cities[target_city]}

    # Создание директории regions если нет
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    created = 0
    skipped = 0

    for city_slug, city_data in cities.items():
        # Путь к папке города
        city_dir = os.path.join(OUTPUT_DIR, city_slug)
        output_file = os.path.join(city_dir, 'index.html')

        # Создаём папку города
        os.makedirs(city_dir, exist_ok=True)

        # Получаем сохранённые мета-теги (если есть)
        existing_meta = get_existing_meta(city_slug, meta_mapping)

        # Генерируем HTML
        html, generated_meta = generate_city_page(city_slug, city_data, addresses, phones, template, cargo_clusters, existing_meta)

        # Сохраняем мета-теги в маппинг
        meta_mapping[city_slug] = generated_meta

        # Сохраняем файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ {city_data['name']} → /regions/{city_slug}/index.html")
        created += 1

    # Сохраняем маппинг мета-тегов
    save_meta_mapping(meta_mapping)
    print(f"\n💾 Маппинг мета-тегов сохранён в {META_MAPPING_FILE}")

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Сохранено мета-тегов: {len(meta_mapping)}")
    print(f"Пропущено: {skipped}")

if __name__ == '__main__':
    main()
