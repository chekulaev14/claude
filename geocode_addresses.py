#!/usr/bin/env python3
"""
Скрипт геокодирования адресов через Яндекс.Геокодер
Добавляет в city-addresses.json: postalCode, latitude, longitude

Использование:
  python3 geocode_addresses.py              # Все города
  python3 geocode_addresses.py --city moscow  # Только Москва
  python3 geocode_addresses.py --dry-run    # Показать что будет сделано
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')

# API ключ
API_KEY = os.getenv('YANDEX_GEOCODER_API_KEY', '4a699c0f-112d-4cf0-a1ee-fa70c817500a')

def load_json(filepath):
    """Загружает JSON файл"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    """Сохраняет JSON файл"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def geocode_address(city_name, street):
    """
    Получает координаты и индекс через Яндекс.Геокодер
    Возвращает: (latitude, longitude, postal_code) или (None, None, None)
    """
    address = f"{city_name}, {street}"
    encoded_address = urllib.parse.quote(address)
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&format=json&geocode={encoded_address}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

        # Парсим ответ
        feature_member = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
        if not feature_member:
            return None, None, None

        geo_object = feature_member[0].get('GeoObject', {})

        # Координаты (lon lat)
        pos = geo_object.get('Point', {}).get('pos', '')
        if pos:
            lon, lat = pos.split(' ')
            latitude = float(lat)
            longitude = float(lon)
        else:
            latitude, longitude = None, None

        # Почтовый индекс (находится в поле postal_code объекта Address)
        postal_code = None
        address_details = geo_object.get('metaDataProperty', {}).get('GeocoderMetaData', {}).get('Address', {})
        postal_code = address_details.get('postal_code')

        return latitude, longitude, postal_code

    except Exception as e:
        print(f"  ❌ Ошибка геокодирования: {e}")
        return None, None, None

def main():
    print("=== Геокодирование адресов через Яндекс ===\n")

    # Парсинг аргументов
    dry_run = '--dry-run' in sys.argv
    target_city = None
    if '--city' in sys.argv:
        idx = sys.argv.index('--city')
        if idx + 1 < len(sys.argv):
            target_city = sys.argv[idx + 1]

    if dry_run:
        print("🔍 Режим dry-run: изменения не будут сохранены\n")

    # Загрузка данных
    addresses = load_json(ADDRESSES_FILE)
    cities = load_json(CITIES_FILE)

    print(f"Загружено адресов: {len(addresses)}")
    print(f"API ключ: {API_KEY[:8]}...{API_KEY[-4:]}\n")

    # Фильтруем города
    city_slugs = [target_city] if target_city else list(addresses.keys())

    updated = 0
    skipped = 0
    errors = 0

    for city_slug in city_slugs:
        if city_slug not in addresses:
            print(f"⚠ {city_slug}: не найден в addresses")
            skipped += 1
            continue

        addr_data = addresses[city_slug]
        city_info = cities.get(city_slug, {})
        city_name = city_info.get('name', city_slug)
        street = addr_data.get('street', '')

        # Пропускаем если уже есть ВСЕ данные (координаты И индекс)
        has_coords = addr_data.get('latitude') and addr_data.get('longitude')
        has_postal = addr_data.get('postalCode') and addr_data.get('postalCode') != ""
        if has_coords and has_postal:
            print(f"⏭ {city_name}: уже есть данные")
            skipped += 1
            continue

        print(f"📍 {city_name}: {street}...", end=" ")

        # Геокодируем
        lat, lon, postal = geocode_address(city_name, street)

        if lat and lon:
            addresses[city_slug]['latitude'] = lat
            addresses[city_slug]['longitude'] = lon
            if postal:
                addresses[city_slug]['postalCode'] = postal
            print(f"✓ ({lat:.6f}, {lon:.6f}) индекс: {postal or 'не найден'}")
            updated += 1
        else:
            print("❌ не удалось")
            errors += 1

        # Пауза между запросами (чтобы не превысить лимит)
        time.sleep(0.2)

    print(f"\n=== Результат ===")
    print(f"Обновлено: {updated}")
    print(f"Пропущено: {skipped}")
    print(f"Ошибок: {errors}")

    # Сохраняем
    if not dry_run and updated > 0:
        save_json(ADDRESSES_FILE, addresses)
        print(f"\n💾 Сохранено в {ADDRESSES_FILE}")
    elif dry_run:
        print("\n⚠ Dry-run: изменения НЕ сохранены")

if __name__ == '__main__':
    main()
