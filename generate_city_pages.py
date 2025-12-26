#!/usr/bin/env python3
"""
Генератор страниц городов для ТК Динамика
Создаёт /regions/{город}/index.html для всех городов из cities.json
"""

import json
import os

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'city-index-template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')

def load_cities():
    """Загружает данные городов из JSON"""
    with open(CITIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template():
    """Загружает HTML шаблон"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def generate_city_page(city_slug, city_data, template):
    """Генерирует HTML страницу для города"""
    html = template

    # Замена плейсхолдеров
    html = html.replace('{{CITY_NAME}}', city_data['name'])
    html = html.replace('{{CITY_GENITIVE}}', city_data['genitive'])
    html = html.replace('{{CITY_PREPOSITIONAL}}', city_data['prepositional'])
    html = html.replace('{{REGION_DATIVE}}', city_data['region_dative'])

    return html

def main():
    print("=== Генератор страниц городов ===\n")

    # Загрузка данных
    cities = load_cities()
    template = load_template()

    print(f"Загружено городов: {len(cities)}")
    print(f"Шаблон: {TEMPLATE_FILE}\n")

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
        html = generate_city_page(city_slug, city_data, template)

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
