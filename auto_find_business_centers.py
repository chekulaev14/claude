#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматический поиск бизнес-центров через веб-поиск
"""

import json
import os
import random
from time import sleep

# Список городов
CITIES = {
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

def main():
    """Основная функция - выводит команду для Claude"""

    print("=" * 70)
    print("АВТОМАТИЧЕСКИЙ ПОИСК БИЗНЕС-ЦЕНТРОВ")
    print("=" * 70)
    print()
    print("Этот скрипт создаёт запрос для Claude, чтобы он автоматически")
    print("нашёл бизнес-центры для всех 48 городов через WebSearch.")
    print()
    print("=" * 70)
    print()

    # Формируем список городов для поиска
    cities_list = list(CITIES.items())

    print("📋 ЗАДАЧА ДЛЯ CLAUDE:")
    print()
    print("Найди реальные бизнес-центры для следующих городов:")
    print()

    for i, (slug, name) in enumerate(cities_list, 1):
        print(f"  {i}. {name} ({slug})")

    print()
    print("Для КАЖДОГО города:")
    print("  1. Используй WebSearch с запросом 'бизнес центр [город] адрес'")
    print("  2. Найди РЕАЛЬНЫЙ бизнес-центр с полным адресом")
    print("  3. Сгенерируй случайный номер офиса (101-505)")
    print("  4. Если не нашёл - пропусти город")
    print()
    print("Формат результата (JSON):")
    print('''{
  "город-slug": {
    "name": "Название БЦ",
    "street": "ул. Улица, д. 123",
    "office": "305",
    "postalCode": "123456"
  }
}''')
    print()
    print("Сохрани результат в: data/city-addresses.json")
    print()
    print("=" * 70)
    print()
    print("⚠️  ВАЖНО: Поиск займёт время, так как нужно найти 48 городов.")
    print("    Лучше делать партиями по 5-10 городов.")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
