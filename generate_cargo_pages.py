#!/usr/bin/env python3
"""
Генератор страниц для грузовых кластеров (по типу груза)
Создаёт /regions/{город}/{кластер}/index.html с галереей фото

Особенности:
- 4 случайных фото на страницу (не повторяются внутри страницы)
- Маппинг картинок сохраняется для стабильности SEO
- Маппинг мета-тегов сохраняется (не перезаписываются при регенерации)
- Schema.org разметка с родительской организацией
"""

import os
import re
import random
import json
import math

# Базовые пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'cluster-cargo-template.html')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images', 'clusters')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Файлы маппинга
CARGO_IMAGES_MAPPING_FILE = os.path.join(DATA_DIR, 'cargo-images-mapping.json')
CARGO_META_MAPPING_FILE = os.path.join(DATA_DIR, 'cargo-meta-mapping.json')
CITY_PHONES_FILE = os.path.join(DATA_DIR, 'city-phones.json')
CITY_ADDRESSES_FILE = os.path.join(DATA_DIR, 'city-addresses.json')
CITIES_FILE = os.path.join(DATA_DIR, 'cities.json')
CARGO_CLUSTERS_FILE = os.path.join(DATA_DIR, 'cargo-clusters.json')

# Словарь городов: url-slug → (именительный, родительный, предложный)
CITIES = {
    "balashikha": ("Балашиха", "Балашихи", "Балашихе"),
    "chekhov": ("Чехов", "Чехова", "Чехове"),
    "chelyabinsk": ("Челябинск", "Челябинска", "Челябинске"),
    "dmitrov": ("Дмитров", "Дмитрова", "Дмитрове"),
    "dolgoprudny": ("Долгопрудный", "Долгопрудного", "Долгопрудном"),
    "domodedovo": ("Домодедово", "Домодедова", "Домодедове"),
    "dubna": ("Дубна", "Дубны", "Дубне"),
    "dzerzhinsky": ("Дзержинский", "Дзержинского", "Дзержинском"),
    "egoryevsk": ("Егорьевск", "Егорьевска", "Егорьевске"),
    "ekaterinburg": ("Екатеринбург", "Екатеринбурга", "Екатеринбурге"),
    "elektrostal": ("Электросталь", "Электростали", "Электростали"),
    "fryazino": ("Фрязино", "Фрязино", "Фрязино"),
    "ivanteyevka": ("Ивантеевка", "Ивантеевки", "Ивантеевке"),
    "izhevsk": ("Ижевск", "Ижевска", "Ижевске"),
    "kaluga": ("Калуга", "Калуги", "Калуге"),
    "kazan": ("Казань", "Казани", "Казани"),
    "khimki": ("Химки", "Химок", "Химках"),
    "klin": ("Клин", "Клина", "Клину"),
    "kolomna": ("Коломна", "Коломны", "Коломне"),
    "korolev": ("Королёв", "Королёва", "Королёве"),
    "krasnogorsk": ("Красногорск", "Красногорска", "Красногорске"),
    "lobnya": ("Лобня", "Лобни", "Лобне"),
    "lyubertsy": ("Люберцы", "Люберец", "Люберцах"),
    "moskva": ("Москва", "Москвы", "Москве"),
    "mytishchi": ("Мытищи", "Мытищ", "Мытищах"),
    "naberezhnye-chelny": ("Набережные Челны", "Набережных Челнов", "Набережных Челнах"),
    "nizhnekamsk": ("Нижнекамск", "Нижнекамска", "Нижнекамске"),
    "nizhny-novgorod": ("Нижний Новгород", "Нижнего Новгорода", "Нижнем Новгороде"),
    "noginsk": ("Ногинск", "Ногинска", "Ногинске"),
    "obninsk": ("Обнинск", "Обнинска", "Обнинске"),
    "odintsovo": ("Одинцово", "Одинцова", "Одинцове"),
    "orekhovo-zuevo": ("Орехово-Зуево", "Орехово-Зуева", "Орехово-Зуеве"),
    "perm": ("Пермь", "Перми", "Перми"),
    "podolsk": ("Подольск", "Подольска", "Подольске"),
    "pushkino": ("Пушкино", "Пушкино", "Пушкино"),
    "ramenskoe": ("Раменское", "Раменского", "Раменском"),
    "reutov": ("Реутов", "Реутова", "Реутове"),
    "saint-petersburg": ("Санкт-Петербург", "Санкт-Петербурга", "Санкт-Петербурге"),
    "samara": ("Самара", "Самары", "Самаре"),
    "sergiev-posad": ("Сергиев Посад", "Сергиева Посада", "Сергиевом Посаде"),
    "serpukhov": ("Серпухов", "Серпухова", "Серпухове"),
    "shchelkovo": ("Щелково", "Щелкова", "Щелково"),
    "tula": ("Тула", "Тулы", "Туле"),
    "tver": ("Тверь", "Твери", "Твери"),
    "ufa": ("Уфа", "Уфы", "Уфе"),
    "voskresensk": ("Воскресенск", "Воскресенска", "Воскресенске"),
    "yaroslavl": ("Ярославль", "Ярославля", "Ярославле"),
    "zhukovsky": ("Жуковский", "Жуковского", "Жуковском"),
}

# Базовые кластеры для перелинковки
BASE_CLUSTERS = {
    'mezhgorod': {
        'title': 'Междугородние грузоперевозки',
        'description': 'Доставка по всей России: 1-20 тонн',
        'icon': 'bi-signpost-2'
    },
    'dlinnomer': {
        'title': 'Длинномеры и шаланды',
        'description': 'Перевозка негабаритных грузов',
        'icon': 'bi-arrows-expand'
    },
    'po-rossii': {
        'title': 'Грузоперевозки по России',
        'description': 'Маршруты во все регионы РФ',
        'icon': 'bi-map'
    },
    'fura': {
        'title': 'Перевозка фурой',
        'description': 'Полные загрузки фур 5-20 тонн',
        'icon': 'bi-truck-front'
    }
}

# Папка с контентом для грузовых кластеров
CARGO_CONTENT_DIR = os.path.join(BASE_DIR, 'seo-texts', 'cargo')

# CARGO_CLUSTERS загружается из JSON в main()


# ==========================================
# ФУНКЦИИ РАБОТЫ С ДАННЫМИ
# ==========================================

def load_json(filepath):
    """Загружает JSON файл, возвращает {} если не существует"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_json(filepath, data):
    """Сохраняет данные в JSON файл"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_template():
    """Загружает HTML шаблон"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def load_content_file(cluster, cargo_clusters):
    """Загружает HTML контент для кластера из файла"""
    cluster_config = cargo_clusters.get(cluster, {})
    content_file = cluster_config.get('content_file')

    if not content_file:
        return ''

    filepath = os.path.join(CARGO_CONTENT_DIR, content_file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Убираем HTML комментарии в начале файла
            import re
            content = re.sub(r'<!--.*?-->\s*', '', content, flags=re.DOTALL)
            return content.strip()

    print(f"  ⚠ Файл контента не найден: {filepath}")
    return ''


def get_cluster_images(cluster):
    """Получает список изображений для кластера"""
    cluster_dir = os.path.join(IMAGES_DIR, cluster)
    if not os.path.exists(cluster_dir):
        return []

    images = []
    for f in os.listdir(cluster_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            images.append(f'/assets/images/clusters/{cluster}/{f}')

    return sorted(images)  # Сортируем для детерминированности


def get_images_for_page(city_slug, cluster, all_images, images_mapping):
    """
    Получает 4 изображения для страницы.
    Если уже есть в маппинге — возвращает их.
    Если нет — выбирает случайные 4 и сохраняет в маппинг.
    """
    key = f"{city_slug}/{cluster}"

    # Проверяем маппинг
    if key in images_mapping:
        saved_images = images_mapping[key]
        # Проверяем что все файлы существуют
        all_exist = True
        for img in saved_images:
            img_path = os.path.join(BASE_DIR, img.lstrip('/'))
            if not os.path.exists(img_path):
                all_exist = False
                break
        if all_exist and len(saved_images) == 4:
            return saved_images

    # Нет маппинга или файлы удалены — выбираем случайные 4
    if len(all_images) < 4:
        # Если мало фото — дублируем
        selected = (all_images * 4)[:4]
    else:
        # Используем seed для детерминированности по городу
        # Но при этом для разных городов — разные фото
        random.seed(hash(city_slug + cluster))
        selected = random.sample(all_images, 4)
        random.seed()  # Сбрасываем seed

    # Сохраняем в маппинг
    images_mapping[key] = selected

    return selected


def generate_faq_html(faq_items):
    """Генерирует HTML для FAQ аккордеона"""
    html_parts = []
    for idx, item in enumerate(faq_items, 1):
        html_parts.append(f'''                <div class="accordion-item mb-3">
                    <h3 class="accordion-header">
                        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq{idx}">
                            {item['question']}
                        </button>
                    </h3>
                    <div id="faq{idx}" class="accordion-collapse collapse">
                        <div class="accordion-body">
                            {item['answer']}
                        </div>
                    </div>
                </div>''')
    return '\n'.join(html_parts)


def generate_faq_schema(faq_items):
    """Генерирует Schema.org разметку для FAQ"""
    schema_parts = []
    for item in faq_items:
        schema_parts.append(f'''            {{
                "@type": "Question",
                "name": "{item['question']}",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{item['answer']}"
                }}
            }}''')
    return ',\n'.join(schema_parts)


def generate_other_clusters_html(current_cluster):
    """Генерирует HTML блок с другими услугами для перелинковки"""
    html_parts = []
    for cluster, info in BASE_CLUSTERS.items():
        html_parts.append(f'''                <div class="col-md-6 col-lg-3">
                    <a href="../{cluster}/" class="service-card">
                        <i class="bi {info['icon']}"></i>
                        <h3>{info['title']}</h3>
                        <p>{info['description']}</p>
                    </a>
                </div>''')
    return '\n'.join(html_parts)


def generate_other_cargo_clusters_html(current_cluster, cargo_clusters):
    """Генерирует HTML блок с другими грузовыми кластерами для перелинковки"""
    html_parts = []
    for cluster, config in cargo_clusters.items():
        if cluster == current_cluster:
            continue  # Пропускаем текущий кластер
        icon = config.get('icon', 'bi-box')
        html_parts.append(f'''                <div class="col-md-6 col-lg-3">
                    <a href="../{cluster}/" class="service-card">
                        <i class="bi {icon}"></i>
                        <h3>{config['title']}</h3>
                    </a>
                </div>''')

    # Если нет других cargo-кластеров — возвращаем заглушку
    if not html_parts:
        return '''                <div class="col-12">
                    <p class="text-muted">Скоро здесь появятся другие типы грузов</p>
                </div>'''

    return '\n'.join(html_parts)


def generate_cargo_page(city_slug, cluster, template, cluster_config, images_mapping, meta_mapping, city_phones, city_addresses, cities_data, cargo_clusters):
    """
    Генерирует HTML страницу для грузового кластера.

    Возвращает (html, meta) или None если ошибка.
    """
    # Получаем падежи города
    if city_slug not in CITIES:
        return None

    city_name, city_genitive, city_prepositional = CITIES[city_slug]

    # Получаем данные города
    city_data = cities_data.get(city_slug, {})
    region_name = city_data.get('region', 'Московская область')

    # Телефон и адрес
    local_phone = city_phones.get(city_slug, "+7-495-000-00-00")
    address_data = city_addresses.get(city_slug, {
        "name": "Бизнес-центр",
        "street": "ул. Центральная, 1",
        "office": "101",
        "postalCode": "",
        "latitude": 55.75,
        "longitude": 37.62
    })

    bc_name = address_data.get("name", "Бизнес-центр")
    bc_street = address_data.get("street", "")
    bc_office = address_data.get("office", "")
    bc_postal = address_data.get("postalCode", "")
    bc_latitude = address_data.get("latitude", 55.75)
    bc_longitude = address_data.get("longitude", 37.62)
    full_address = f"{bc_street}, офис {bc_office}"

    # Получаем изображения
    all_images = get_cluster_images(cluster)
    if not all_images:
        print(f"  ⚠ Нет изображений для кластера {cluster}")
        return None

    page_images = get_images_for_page(city_slug, cluster, all_images, images_mapping)

    # Генерируем H1 и intro с подстановкой города
    h1 = cluster_config['h1_template'].replace('{{CITY_PREPOSITIONAL}}', city_prepositional)
    intro = cluster_config['intro_template'].replace('{{CITY_PREPOSITIONAL}}', city_prepositional)

    # Мета-теги: используем сохранённые или генерируем новые
    meta_key = f"{city_slug}/{cluster}"
    existing_meta = meta_mapping.get(meta_key, {})

    if 'title' in existing_meta:
        meta_title = existing_meta['title']
    else:
        meta_title = f"{cluster_config['title']} {city_name}"

    if 'description' in existing_meta:
        meta_description = existing_meta['description']
    else:
        # Генерируем описание на основе ключевых слов
        meta_description = f"{cluster_config['title']} {city_name}. Доставка по городу и межгород. Прозрачные цены, страхование груза. ☎ 8-800-707-29-36"

    meta_canonical = f"https://dinamika-cargo.ru/regions/{city_slug}/{cluster}/"

    # Генерируем FAQ
    faq_html = generate_faq_html(cluster_config['faq'])
    faq_schema = generate_faq_schema(cluster_config['faq'])

    # Генерируем перелинковку
    other_clusters_html = generate_other_clusters_html(cluster)

    # Подставляем все плейсхолдеры
    html = template

    # Мета-теги
    html = html.replace('{{TITLE}}', meta_title)
    html = html.replace('{{META_DESCRIPTION}}', meta_description)

    # Город
    html = html.replace('{{CITY_NAME}}', city_name)
    html = html.replace('{{CITY_NAME_GENITIVE}}', city_genitive)
    html = html.replace('{{CITY_NAME_PREPOSITIONAL}}', city_prepositional)
    html = html.replace('{{CITY_SLUG}}', city_slug)

    # Кластер
    html = html.replace('{{CLUSTER_SLUG}}', cluster)
    html = html.replace('{{CLUSTER_TITLE}}', cluster_config['title'])
    html = html.replace('{{H1}}', h1)
    html = html.replace('{{INTRO}}', intro)

    # Контент — загружаем из файла
    content_sections = load_content_file(cluster, cargo_clusters)
    html = html.replace('{{CONTENT_SECTIONS}}', content_sections)

    # Изображения (4 штуки)
    for i, img in enumerate(page_images, 1):
        html = html.replace(f'{{{{IMAGE_{i}}}}}', img)
        alt_text = cluster_config['image_alts'][i-1] if i <= len(cluster_config['image_alts']) else cluster_config['title']
        html = html.replace(f'{{{{IMAGE_ALT_{i}}}}}', f"{alt_text} {city_name}")

    # FAQ
    html = html.replace('{{FAQ_ITEMS}}', faq_html)
    html = html.replace('{{FAQ_SCHEMA}}', faq_schema)

    # Перелинковка на основные услуги
    html = html.replace('{{OTHER_CLUSTERS}}', other_clusters_html)

    # Перелинковка на другие cargo-кластеры
    other_cargo_html = generate_other_cargo_clusters_html(cluster, cargo_clusters)
    html = html.replace('{{OTHER_CARGO_CLUSTERS}}', other_cargo_html)

    # Контакты и адрес
    html = html.replace('{{LOCAL_PHONE}}', local_phone)
    html = html.replace('{{BC_NAME}}', bc_name)
    html = html.replace('{{BC_STREET}}', bc_street)
    html = html.replace('{{FULL_ADDRESS}}', full_address)
    html = html.replace('{{REGION_NAME}}', region_name)
    html = html.replace('{{POSTAL_CODE}}', bc_postal)
    html = html.replace('{{LATITUDE}}', str(bc_latitude))
    html = html.replace('{{LONGITUDE}}', str(bc_longitude))

    # Сохраняем мета-теги
    generated_meta = {
        'title': meta_title,
        'description': meta_description,
        'canonical': meta_canonical
    }

    return html, generated_meta


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Генератор страниц грузовых кластеров')
    parser.add_argument('--test', action='store_true', help='Тестовый режим (1 город)')
    parser.add_argument('--city', type=str, help='Генерировать только для города')
    parser.add_argument('--cluster', type=str, help='Генерировать только кластер')
    args = parser.parse_args()

    print("=== Генератор грузовых кластеров ===\n")

    # Загружаем конфиг cargo-кластеров из JSON
    cargo_clusters = load_json(CARGO_CLUSTERS_FILE)
    if not cargo_clusters:
        print("❌ Файл cargo-clusters.json не найден или пуст")
        return

    # Загружаем данные
    images_mapping = load_json(CARGO_IMAGES_MAPPING_FILE)
    meta_mapping = load_json(CARGO_META_MAPPING_FILE)
    city_phones = load_json(CITY_PHONES_FILE)
    city_addresses = load_json(CITY_ADDRESSES_FILE)
    cities_data = load_json(CITIES_FILE)

    print(f"Cargo-кластеров в JSON: {len(cargo_clusters)}")
    print(f"Маппинг картинок: {len(images_mapping)} записей")
    print(f"Маппинг мета-тегов: {len(meta_mapping)} записей")
    print(f"Телефоны городов: {len(city_phones)}")
    print(f"Адреса городов: {len(city_addresses)}")
    print(f"Данные городов: {len(cities_data)}\n")

    # Загружаем шаблон
    template = load_template()
    print(f"Шаблон: {TEMPLATE_FILE}\n")

    # Определяем города и кластеры
    cities = [args.city] if args.city else list(CITIES.keys())
    if args.test:
        cities = cities[:1]

    clusters = [args.cluster] if args.cluster else list(cargo_clusters.keys())

    # Фильтруем несуществующие кластеры
    clusters = [c for c in clusters if c in cargo_clusters]

    if not clusters:
        print("⚠ Нет кластеров для генерации")
        return

    print(f"Города: {len(cities)}")
    print(f"Кластеры: {clusters}\n")

    created = 0
    skipped = 0

    for cluster in clusters:
        cluster_config = cargo_clusters[cluster]
        print(f"\n--- Кластер: {cluster} ({cluster_config['title']}) ---")

        # Проверяем наличие фото
        images = get_cluster_images(cluster)
        if not images:
            print(f"⚠ Нет фото в /assets/images/clusters/{cluster}/")
            continue
        print(f"Найдено фото: {len(images)}")

        for city_slug in cities:
            if city_slug not in CITIES:
                print(f"  ⚠ Город {city_slug} не найден")
                skipped += 1
                continue

            city_name = CITIES[city_slug][0]

            result = generate_cargo_page(
                city_slug, cluster, template, cluster_config,
                images_mapping, meta_mapping, city_phones, city_addresses, cities_data, cargo_clusters
            )

            if not result:
                skipped += 1
                continue

            html, generated_meta = result

            # Сохраняем мета-теги
            meta_key = f"{city_slug}/{cluster}"
            if meta_key not in meta_mapping:
                meta_mapping[meta_key] = generated_meta

            # Создаём папку и сохраняем HTML
            output_dir = os.path.join(OUTPUT_DIR, city_slug, cluster)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, 'index.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"  ✓ {city_name} → /regions/{city_slug}/{cluster}/")
            created += 1

    # Сохраняем маппинги
    save_json(CARGO_IMAGES_MAPPING_FILE, images_mapping)
    save_json(CARGO_META_MAPPING_FILE, meta_mapping)

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Пропущено: {skipped}")
    print(f"\n💾 Маппинг картинок: {CARGO_IMAGES_MAPPING_FILE}")
    print(f"💾 Маппинг мета-тегов: {CARGO_META_MAPPING_FILE}")


if __name__ == '__main__':
    main()
