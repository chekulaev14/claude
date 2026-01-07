#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для поиска реальных бизнес-центров в городах через Яндекс.Карты API
"""

import json
import os
import random
from time import sleep

# Список городов
CITIES = [
    "balashikha", "chekhov", "chelyabinsk", "dmitrov", "dolgoprudny",
    "domodedovo", "dubna", "dzerzhinsky", "egoryevsk", "ekaterinburg",
    "elektrostal", "fryazino", "ivanteyevka", "izhevsk", "kaluga",
    "kazan", "khimki", "klin", "kolomna", "korolev",
    "krasnogorsk", "lobnya", "lyubertsy", "moskva", "mytishchi",
    "naberezhnye-chelny", "nizhnekamsk", "nizhny-novgorod", "noginsk", "obninsk",
    "odintsovo", "orekhovo-zuevo", "perm", "podolsk", "pushkino",
    "ramenskoe", "reutov", "saint-petersburg", "samara", "sergiev-posad",
    "serpukhov", "shchelkovo", "tula", "tver", "ufa",
    "voskresensk", "yaroslavl", "zhukovsky"
]

# Названия городов для поиска
CITY_NAMES = {
    "balashikha": "Балашиха",
    "chekhov": "Чехов",
    "chelyabinsk": "Челябинск",
    "dmitrov": "Дмитров",
    "dolgoprudny": "Долгопрудный",
    "domodedovo": "Домодедово",
    "dubna": "Дубна",
    "dzerzhinsky": "Дзержинский",
    "egoryevsk": "Егорьевск",
    "ekaterinburg": "Екатеринбург",
    "elektrostal": "Электросталь",
    "fryazino": "Фрязино",
    "ivanteyevka": "Ивантеевка",
    "izhevsk": "Ижевск",
    "kaluga": "Калуга",
    "kazan": "Казань",
    "khimki": "Химки",
    "klin": "Клин",
    "kolomna": "Коломна",
    "korolev": "Королёв",
    "krasnogorsk": "Красногорск",
    "lobnya": "Лобня",
    "lyubertsy": "Люберцы",
    "moskva": "Москва",
    "mytishchi": "Мытищи",
    "naberezhnye-chelny": "Набережные Челны",
    "nizhnekamsk": "Нижнекамск",
    "nizhny-novgorod": "Нижний Новгород",
    "noginsk": "Ногинск",
    "obninsk": "Обнинск",
    "odintsovo": "Одинцово",
    "orekhovo-zuevo": "Орехово-Зуево",
    "perm": "Пермь",
    "podolsk": "Подольск",
    "pushkino": "Пушкино",
    "ramenskoe": "Раменское",
    "reutov": "Реутов",
    "saint-petersburg": "Санкт-Петербург",
    "samara": "Самара",
    "sergiev-posad": "Сергиев Посад",
    "serpukhov": "Серпухов",
    "shchelkovo": "Щёлково",
    "tula": "Тула",
    "tver": "Тверь",
    "ufa": "Уфа",
    "voskresensk": "Воскресенск",
    "yaroslavl": "Ярославль",
    "zhukovsky": "Жуковский"
}

def search_business_center(city_slug):
    """
    Ищет бизнес-центр для города
    ВАЖНО: Эта функция требует ручного ввода данных
    """
    city_name = CITY_NAMES.get(city_slug, city_slug)

    print(f"\n{'='*60}")
    print(f"🔍 Поиск бизнес-центра для города: {city_name}")
    print(f"{'='*60}")
    print(f"\nПоисковой запрос для Яндекс/Google:")
    print(f"  'бизнес центр {city_name} адрес'")
    print(f"\nИли откройте Яндекс.Карты:")
    print(f"  https://yandex.ru/maps/?text=бизнес%20центр%20{city_name.replace(' ', '%20')}")

    print(f"\nВведите данные для города {city_name}:")
    print(f"  (Введите 'нет' если не нашли бизнес-центр)")

    # Название бизнес-центра
    bc_name = input("  Название БЦ: ").strip()

    # Проверка на "не найдено"
    if bc_name.lower() in ['нет', 'не найдено', 'не нашел', 'не нашёл', 'n', 'no']:
        print(f"\n⚠️  БЦ не найден для города {city_name}")
        return None

    if not bc_name:
        print(f"\n⚠️  Пустое название - город пропущен")
        return None

    # Адрес (улица и дом)
    street = input("  Улица и дом (например: ул. Ленина, д. 25): ").strip()
    if not street:
        print(f"\n⚠️  Пустой адрес - город пропущен")
        return None

    # Индекс (опционально)
    postal_code = input("  Индекс (Enter = пропустить): ").strip()

    # Генерация номера офиса (случайный)
    office_number = random.randint(101, 505)

    result = {
        "name": bc_name,
        "street": street,
        "office": str(office_number),
        "postalCode": postal_code if postal_code else ""
    }

    print(f"\n✅ Сохранено:")
    print(f"   {bc_name}")
    print(f"   {street}, офис {office_number}")
    if postal_code:
        print(f"   Индекс: {postal_code}")

    return result


def main():
    """Основная функция"""
    output_file = "data/city-addresses.json"

    # Загружаем существующие данные, если файл есть
    addresses = {}
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            addresses = json.load(f)
        print(f"📂 Загружено {len(addresses)} существующих адресов")

    print(f"\n🏢 ПОИСК БИЗНЕС-ЦЕНТРОВ")
    print(f"Всего городов: {len(CITIES)}")
    print(f"Уже заполнено: {len(addresses)}")
    print(f"Осталось: {len(CITIES) - len(addresses)}")

    # Спрашиваем, с какого города начать
    print(f"\nВарианты:")
    print(f"  1. Начать сначала (с первого города)")
    print(f"  2. Продолжить с незаполненных городов")
    print(f"  3. Заполнить конкретный город")

    choice = input("\nВыберите вариант (1/2/3): ").strip()

    if choice == "1":
        # Начать сначала
        cities_to_process = CITIES
    elif choice == "3":
        # Конкретный город
        city_slug = input("Введите slug города (например: moskva): ").strip()
        if city_slug in CITIES:
            cities_to_process = [city_slug]
        else:
            print(f"❌ Город '{city_slug}' не найден")
            return
    else:
        # Продолжить с незаполненных
        cities_to_process = [c for c in CITIES if c not in addresses]

    if not cities_to_process:
        print("\n✅ Все города уже заполнены!")
        return

    print(f"\nБудет обработано городов: {len(cities_to_process)}")
    input("Нажмите Enter для начала...")

    # Обрабатываем города
    for i, city_slug in enumerate(cities_to_process, 1):
        print(f"\n[{i}/{len(cities_to_process)}]")

        try:
            address_data = search_business_center(city_slug)

            # Если не найдено - пропускаем, не сохраняем
            if address_data is None:
                print(f"⏭️  Город {CITY_NAMES[city_slug]} пропущен (БЦ не найден)")
            else:
                addresses[city_slug] = address_data

                # Сохраняем после каждого успешного города
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(addresses, f, ensure_ascii=False, indent=2)

                print(f"💾 Прогресс сохранён ({len(addresses)}/{len(CITIES)})")

            # Спрашиваем, продолжать ли
            if i < len(cities_to_process):
                cont = input("\nПродолжить? (Enter = да, n = стоп): ").strip().lower()
                if cont == 'n':
                    print("\n⏸️  Остановлено пользователем")
                    break

        except KeyboardInterrupt:
            print("\n\n⏸️  Прервано пользователем")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"✅ ГОТОВО!")
    print(f"Заполнено городов: {len(addresses)}/{len(CITIES)}")
    print(f"Файл сохранён: {output_file}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
