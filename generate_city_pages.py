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

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')
ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')
PHONES_FILE = os.path.join(BASE_DIR, 'data', 'city-phones.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'city-index-template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')

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

def generate_city_page(city_slug, city_data, addresses, phones, template):
    """Генерирует HTML страницу для города"""
    html = template

    # Замена плейсхолдеров города
    html = html.replace('{{CITY_SLUG}}', city_slug)
    html = html.replace('{{CITY_NAME}}', city_data['name'])
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

    return html

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

    print(f"Загружено городов: {len(cities)}")
    print(f"Загружено адресов БЦ: {len(addresses)}")
    print(f"Загружено телефонов: {len(phones)}")
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

        # Генерируем HTML
        html = generate_city_page(city_slug, city_data, addresses, phones, template)

        # Сохраняем файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ {city_data['name']} → /regions/{city_slug}/index.html")
        created += 1

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Пропущено: {skipped}")

if __name__ == '__main__':
    main()
