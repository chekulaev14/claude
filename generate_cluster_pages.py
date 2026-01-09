#!/usr/bin/env python3
"""
Генератор кластерных страниц для ТК Динамика
Создаёт /regions/{город}/{кластер}/index.html из MD файлов и шаблона
"""

import os
import re
import random
import json
import math

# Базовые пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'cluster-template.html')
SEO_TEXTS_DIR = os.path.join(BASE_DIR, 'seo-texts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images', 'clusters')
MAPPING_FILE = os.path.join(BASE_DIR, 'data', 'images-mapping.json')
META_MAPPING_FILE = os.path.join(BASE_DIR, 'data', 'clusters-meta-mapping.json')
CITY_PHONES_FILE = os.path.join(BASE_DIR, 'data', 'city-phones.json')
CITY_ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')
IMAGE_ALTS_FILE = os.path.join(BASE_DIR, 'data', 'image-alts.json')
CITIES_FILE = os.path.join(BASE_DIR, 'data', 'cities.json')

# Словарь городов: url-slug → (именительный, родительный, предложный)
# 48 городов с SEO-текстами
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

# Кластеры
CLUSTERS = ['mezhgorod', 'transportnaya', 'dlinnomer', 'po-rossii', 'fura']

# 17 крупных городов (из generate_route_pages.py)
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

# Алиасы для URL маршрутов
CITY_URL_ALIASES = {
    'saint-petersburg': 'spb'
}

# Информация о кластерах для перелинковки
CLUSTER_INFO = {
    'mezhgorod': {
        'title': 'Междугородние грузоперевозки',
        'description': 'Доставка по всей России: 1-20 тонн, любые маршруты',
        'icon': 'bi-signpost-2'
    },
    'transportnaya': {
        'title': 'Услуги транспортной компании',
        'description': 'Полный комплекс услуг: от экспедирования до страхования груза',
        'icon': 'bi-building'
    },
    'dlinnomer': {
        'title': 'Длинномеры и шаланды',
        'description': 'Перевозка любых грузов на открытых машинах до 24 метров',
        'icon': 'bi-arrows-expand'
    },
    'po-rossii': {
        'title': 'Грузоперевозки по России',
        'description': 'Маршруты во все регионы РФ с отслеживанием',
        'icon': 'bi-map'
    },
    'fura': {
        'title': 'Перевозка фурой',
        'description': 'Полные загрузки фур 5-20 тонн',
        'icon': 'bi-truck-front'
    }
}

# FAQ для каждого кластера (по 5 вопросов, распределены равномерно)
CLUSTER_FAQ = {
    'mezhgorod': [
        {'question': 'Как быстро вы находите машину?', 'answer': 'Скорость поиска зависит от маршрута (областные центры быстрее), дня недели (конец недели быстрее) и времени суток (утро до 9:00 — быстрее). Мы сразу информируем клиента о сроках и стоимости.'},
        {'question': 'Как рассчитывается комиссия?', 'answer': '<p><strong>Без НДС:</strong> комиссия 5 000 ₽ + 1% от стоимости перевозки.</p><p><strong>С НДС:</strong> комиссия 6 000 ₽ + 1,5% от стоимости перевозки.</p><p class="mb-0">Мы показываем закупочную цену и нашу комиссию отдельно — всё прозрачно.</p>'},
        {'question': 'Какие машины есть?', 'answer': 'Работаем с любым тоннажем: от газелей (1-1,5 тонны) до фур (20 тонн). Подбираем машину с нужным типом кузова: закрытый фургон, тент, платформа, рефрижератор.'},
        {'question': 'Как отслеживать груз в пути?', 'answer': 'Мы контролируем перевозку на всех этапах и информируем вас о местоположении груза. По запросу предоставляем фото при погрузке и выгрузке.'},
        {'question': 'Что если груз повредят в дороге?', 'answer': 'Мы несём полную ответственность за груз согласно ГК РФ и Уставу автомобильного транспорта. За 7 лет работы — ни одного случая полной утери груза, все повреждения компенсированы.'},
    ],
    'transportnaya': [
        {'question': 'Чем вы отличаетесь от других компаний?', 'answer': 'Мы не зарабатываем на разнице ставок — у нас фиксированная комиссия. Вы видите закупочную цену и нашу наценку отдельно.'},
        {'question': 'Какие документы вы оформляете?', 'answer': 'Договор-заявку, транспортную накладную и все необходимые документы. При работе с НДС предоставляем полный пакет закрывающих документов (УПД).'},
        {'question': 'Как вы проверяете перевозчиков?', 'answer': 'Тщательно проверяем на ATI.su: активность аккаунта, изменения в руководстве, задаём проверочные вопросы. За 7 лет работы у нас не украли ни одного груза.'},
        {'question': 'С кем вы уже работали?', 'answer': 'У нас есть страница клиентов — выгрузка из 1С за 7 лет. Там указаны все организации, которые пользовались нашими услугами.'},
        {'question': 'Что происходит при срыве погрузки?', 'answer': 'Отмена за день и более — без штрафа. В день погрузки: если водитель далеко — в ~50% случаев договариваемся без штрафа.'},
    ],
    'dlinnomer': [
        {'question': 'Что если я не знаю точный вес груза?', 'answer': 'Не проблема — просто опишите груз, и мы подберём подходящую машину. В 99% случаев мы понимаем, какой транспорт нужен.'},
        {'question': 'Предоставляете ли фото груза?', 'answer': 'Да, по запросу предоставляем фото при погрузке и выгрузке. Это помогает контролировать состояние груза.'},
        {'question': 'Можно ли организовать несколько машин?', 'answer': 'Да, организуем любое количество машин: переезды складов, перевозка башенных кранов, крупные партии стройматериалов.'},
        {'question': 'Как происходит оплата?', 'answer': 'Оплата на погрузке, когда машина прибыла. Возможны варианты: 50/50 или 100% перед выгрузкой. Машина выгружается после поступления средств.'},
        {'question': 'Сколько времени занимает доставка?', 'answer': 'Зависит от расстояния: Москва — СПб за 1 день, Москва — Екатеринбург за 2-3 дня, до Владивостока — 10-14 дней.'},
    ],
    'po-rossii': [
        {'question': 'В какие города России вы доставляете?', 'answer': 'Доставляем в любой город РФ — от областных центров до небольших населённых пунктов. Работаем со всеми регионами.'},
        {'question': 'Сколько времени занимает доставка?', 'answer': 'Зависит от расстояния: Москва — СПб за 1 день, Москва — Екатеринбург за 2-3 дня, до Владивостока — 10-14 дней.'},
        {'question': 'Как быстро вы находите машину?', 'answer': 'Скорость поиска зависит от маршрута (областные центры быстрее), дня недели (конец недели быстрее) и времени суток (утро до 9:00 — быстрее). Мы сразу информируем клиента о сроках и стоимости.'},
        {'question': 'Как происходит оплата?', 'answer': 'Оплата на погрузке, когда машина прибыла. Возможны варианты: 50/50 или 100% перед выгрузкой. Машина выгружается после поступления средств.'},
        {'question': 'Что если груз повредят в дороге?', 'answer': 'Мы несём полную ответственность за груз согласно ГК РФ и Уставу автомобильного транспорта. За 7 лет работы — ни одного случая полной утери груза, все повреждения компенсированы.'},
    ],
    'fura': [
        {'question': 'Какой максимальный вес для фуры?', 'answer': 'Стандартная еврофура: до 20 тонн при объёме 82-96 м³. Подбираем машину под ваш груз — важны и вес, и объём.'},
        {'question': 'Можно ли загрузить фуру частично?', 'answer': 'Да, работаем с догрузом, если груз занимает до 3-4 метров по полу. Для более крупных грузов выгоднее полная загрузка.'},
        {'question': 'Какие машины есть?', 'answer': 'Работаем с любым тоннажем: от газелей (1-1,5 тонны) до фур (20 тонн). Подбираем машину с нужным типом кузова: закрытый фургон, тент, платформа, рефрижератор.'},
        {'question': 'Как рассчитывается комиссия?', 'answer': '<p><strong>Без НДС:</strong> комиссия 5 000 ₽ + 1% от стоимости перевозки.</p><p><strong>С НДС:</strong> комиссия 6 000 ₽ + 1,5% от стоимости перевозки.</p><p class="mb-0">Мы показываем закупочную цену и нашу комиссию отдельно — всё прозрачно.</p>'},
        {'question': 'Как вы проверяете перевозчиков?', 'answer': 'Тщательно проверяем на ATI.su: активность аккаунта, изменения в руководстве, задаём проверочные вопросы. За 7 лет работы у нас не украли ни одного груза.'},
    ],
}


def generate_faq_html(cluster):
    """Генерирует HTML блок FAQ для кластера"""
    faq_items = CLUSTER_FAQ.get(cluster, [])
    if not faq_items:
        return ''

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


def calculate_distance(lat1, lon1, lat2, lon2):
    """Расчёт расстояния между двумя точками (формула Хаверсайна × 1.3)"""
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c * 1.3)


def calculate_prices(distance_km):
    """Расчёт цен: 1-3т: км×30 (мин 20к), 5т: км×40 (мин 25к), 10т: км×50 (мин 30к), 20т: км×80 (мин 40к)"""
    return {
        '1t': max(distance_km * 30, 20000),
        '5t': max(distance_km * 40, 25000),
        '10t': max(distance_km * 50, 30000),
        '20t': max(distance_km * 80, 40000)
    }


def format_price(price):
    """Форматирование цены с разделителями тысяч"""
    return f"{price:,}".replace(',', ' ')


def get_route_slug(city_from, city_to):
    """Генерирует slug для маршрута"""
    from_slug = CITY_URL_ALIASES.get(city_from, city_from)
    to_slug = CITY_URL_ALIASES.get(city_to, city_to)
    return f"{from_slug}-{to_slug}"


def get_destinations_for_city(city_slug):
    """Получает список городов назначения для города"""
    if city_slug == 'moskva':
        # Москва → все крупные кроме себя
        return [c for c in MAJOR_CITIES if c != 'moskva']
    elif city_slug in MOSCOW_REGION_CITIES:
        # Подмосковье → крупные без Москвы
        return MAJOR_CITIES_NO_MOSCOW
    elif city_slug in MAJOR_CITIES:
        # Крупный город → все крупные кроме себя
        return [c for c in MAJOR_CITIES if c != city_slug]
    else:
        return []


def get_routes_for_cluster(city_slug, cluster, city_addresses):
    """
    Возвращает 3 маршрута для кластера (детерминированно).
    5 кластеров × 3 маршрута = 15, у нас 16 доступных → без повторов.
    """
    destinations = get_destinations_for_city(city_slug)
    if not destinations:
        return []

    # Сортируем для детерминированности
    destinations = sorted(destinations)

    # Индекс кластера определяет какие 3 маршрута взять
    cluster_idx = CLUSTERS.index(cluster)
    start_idx = cluster_idx * 3

    # Берём 3 маршрута (циклически если выходим за границы)
    routes = []
    for i in range(3):
        idx = (start_idx + i) % len(destinations)
        dest = destinations[idx]
        routes.append(dest)

    return routes


def generate_routes_table_html(city_slug, cluster, city_addresses):
    """Генерирует HTML таблицы маршрутов для кластера (3 прямых + 3 обратных = 6 строк)"""
    routes = get_routes_for_cluster(city_slug, cluster, city_addresses)
    if not routes:
        return ''

    city_name = CITIES.get(city_slug, (city_slug,))[0]
    city_addr = city_addresses.get(city_slug, {})
    lat_from = city_addr.get('latitude', 55.75)
    lon_from = city_addr.get('longitude', 37.62)

    rows = []

    for dest_slug in routes:
        dest_name = CITIES.get(dest_slug, (dest_slug,))[0]
        dest_addr = city_addresses.get(dest_slug, {})
        lat_to = dest_addr.get('latitude', 55.75)
        lon_to = dest_addr.get('longitude', 37.62)

        distance = calculate_distance(lat_from, lon_from, lat_to, lon_to)
        prices = calculate_prices(distance)

        # Прямой маршрут
        route_slug = get_route_slug(city_slug, dest_slug)
        rows.append(f'''                        <tr>
                            <td><a href="/routes/{route_slug}/">{city_name} — {dest_name}</a></td>
                            <td>{distance} км</td>
                            <td>от {format_price(prices["1t"])} ₽</td>
                            <td>от {format_price(prices["5t"])} ₽</td>
                            <td>от {format_price(prices["10t"])} ₽</td>
                            <td>от {format_price(prices["20t"])} ₽</td>
                        </tr>''')

        # Обратный маршрут
        reverse_slug = get_route_slug(dest_slug, city_slug)
        rows.append(f'''                        <tr>
                            <td><a href="/routes/{reverse_slug}/">{dest_name} — {city_name}</a></td>
                            <td>{distance} км</td>
                            <td>от {format_price(prices["1t"])} ₽</td>
                            <td>от {format_price(prices["5t"])} ₽</td>
                            <td>от {format_price(prices["10t"])} ₽</td>
                            <td>от {format_price(prices["20t"])} ₽</td>
                        </tr>''')

    return '\n'.join(rows)


def generate_other_clusters_html(current_cluster):
    """Генерирует HTML блок с другими кластерами для перелинковки"""
    html_parts = []
    for cluster in CLUSTERS:
        if cluster == current_cluster:
            continue
        info = CLUSTER_INFO[cluster]
        html_parts.append(f'''                <div class="col-md-6 col-lg-3">
                    <a href="../{cluster}/" class="service-card">
                        <i class="bi {info['icon']}"></i>
                        <h3>{info['title']}</h3>
                        <p>{info['description']}</p>
                    </a>
                </div>''')
    return '\n'.join(html_parts)


def load_template():
    """Загружает HTML шаблон"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def parse_markdown(md_content):
    """Парсит MD файл и возвращает структуру"""
    lines = md_content.strip().split('\n')

    result = {
        'h1': '',
        'intro': '',
        'sections': []
    }

    current_section = None
    current_content = []

    for line in lines:
        # H1
        if line.startswith('# ') and not result['h1']:
            result['h1'] = line[2:].strip()
        # H2
        elif line.startswith('## '):
            # Сохраняем предыдущую секцию
            if current_section:
                result['sections'].append({
                    'title': current_section,
                    'content': '\n'.join(current_content).strip()
                })
            current_section = line[3:].strip()
            current_content = []
        # Контент
        elif current_section:
            current_content.append(line)
        elif result['h1'] and not current_section:
            # Это intro после H1
            if line.strip():
                result['intro'] += line.strip() + ' '

    # Последняя секция
    if current_section:
        result['sections'].append({
            'title': current_section,
            'content': '\n'.join(current_content).strip()
        })

    result['intro'] = result['intro'].strip()

    return result


def load_images_mapping():
    """Загружает маппинг картинок из JSON файла"""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_images_mapping(mapping):
    """Сохраняет маппинг картинок в JSON файл"""
    os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def load_meta_mapping():
    """Загружает маппинг мета-тегов из JSON файла"""
    if os.path.exists(META_MAPPING_FILE):
        with open(META_MAPPING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_meta_mapping(mapping):
    """Сохраняет маппинг мета-тегов в JSON файл"""
    os.makedirs(os.path.dirname(META_MAPPING_FILE), exist_ok=True)
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


def get_existing_meta(city_slug, cluster, meta_mapping):
    """Получает сохранённые мета-теги для кластера города"""
    key = f"{city_slug}/{cluster}"
    if key in meta_mapping:
        return meta_mapping[key]

    existing_file = os.path.join(OUTPUT_DIR, city_slug, cluster, 'index.html')
    if os.path.exists(existing_file):
        with open(existing_file, 'r', encoding='utf-8') as f:
            html = f.read()
        return extract_meta_from_html(html)

    return None


def load_city_phones():
    """Загружает готовые номера телефонов из JSON файла"""
    if os.path.exists(CITY_PHONES_FILE):
        with open(CITY_PHONES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_city_addresses():
    """Загружает адреса бизнес-центров из JSON файла"""
    if os.path.exists(CITY_ADDRESSES_FILE):
        with open(CITY_ADDRESSES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_image_alts():
    """Загружает SEO alt-тексты для изображений из JSON файла"""
    if os.path.exists(IMAGE_ALTS_FILE):
        with open(IMAGE_ALTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_cities_data():
    """Загружает данные городов (регион и т.д.) из JSON файла"""
    if os.path.exists(CITIES_FILE):
        with open(CITIES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_cluster_images(cluster):
    """Получает список изображений для кластера"""
    cluster_dir = os.path.join(IMAGES_DIR, cluster)
    if not os.path.exists(cluster_dir):
        return []

    images = []
    for f in os.listdir(cluster_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            images.append(f'/assets/images/clusters/{cluster}/{f}')

    return images


def get_image_for_section(city, cluster, section_title, images, mapping):
    """
    Получает картинку для секции:
    - Если уже есть в маппинге → возвращает её
    - Если нет → выбирает случайную и сохраняет в маппинг
    """
    # Проверяем, есть ли уже маппинг
    if city in mapping and cluster in mapping[city]:
        if section_title in mapping[city][cluster]:
            saved_image = mapping[city][cluster][section_title]
            # Проверяем, что файл существует
            image_path = saved_image.replace('/assets/images/', os.path.join(BASE_DIR, 'assets', 'images') + '/')
            if os.path.exists(image_path):
                return saved_image

    # Нет маппинга → выбираем случайную картинку
    if not images:
        return None

    # Исключаем уже использованные в других секциях этого кластера/города
    used_in_cluster = []
    if city in mapping and cluster in mapping[city]:
        used_in_cluster = list(mapping[city][cluster].values())

    available = [img for img in images if img not in used_in_cluster]
    if not available:
        available = images  # Если все использованы, берём любую

    selected = random.choice(available)

    # Сохраняем в маппинг
    if city not in mapping:
        mapping[city] = {}
    if cluster not in mapping[city]:
        mapping[city][cluster] = {}
    mapping[city][cluster][section_title] = selected

    return selected


def generate_sections_html(sections, cluster, city, mapping, image_alts, city_name):
    """Генерирует HTML для секций с изображениями (с использованием маппинга)"""
    html_parts = []
    images = get_cluster_images(cluster)

    # Получаем alt-тексты для кластера
    cluster_alts = image_alts.get(cluster, [])
    alt_counter = 0  # Счётчик для циклического выбора alt

    for idx, section in enumerate(sections):
        # Преобразуем markdown в HTML
        content_html = section['content']
        # Жирный текст (включая многострочный)
        content_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content_html, flags=re.DOTALL)

        # Обработка списков (- item и 1. item)
        lines = content_html.split('\n')
        processed_lines = []
        in_ul = False  # маркированный список
        in_ol = False  # нумерованный список
        for line in lines:
            stripped = line.strip()
            # Нумерованный список (1. 2. 3. и т.д.)
            ol_match = re.match(r'^(\d+)\.\s+(.+)$', stripped)
            if ol_match:
                if in_ul:
                    processed_lines.append('</ul>')
                    in_ul = False
                if not in_ol:
                    processed_lines.append('<ol>')
                    in_ol = True
                processed_lines.append(f'<li>{ol_match.group(2)}</li>')
            elif stripped.startswith('- '):
                if in_ol:
                    processed_lines.append('</ol>')
                    in_ol = False
                if not in_ul:
                    processed_lines.append('<ul>')
                    in_ul = True
                processed_lines.append(f'<li>{stripped[2:]}</li>')
            else:
                if in_ul:
                    processed_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    processed_lines.append('</ol>')
                    in_ol = False
                processed_lines.append(line)
        if in_ul:
            processed_lines.append('</ul>')
        if in_ol:
            processed_lines.append('</ol>')
        content_html = '\n'.join(processed_lines)

        # Абзацы (только для текста вне списков)
        paragraphs = content_html.split('\n\n')
        result_parts = []
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if p.startswith('<ul>') or p.startswith('<ol>') or p.startswith('<li>'):
                result_parts.append(p)
            else:
                result_parts.append(f'<p>{p}</p>')
        content_html = ''.join(result_parts)

        # Количество фото зависит от длины секции
        section_length = len(section['content'])
        if section_length > 5000:
            num_images = 3
        elif section_length > 2500:
            num_images = 2
        else:
            num_images = 1

        # Получаем фото для этой секции из маппинга
        section_images = []
        for img_idx in range(num_images):
            # Создаём уникальный ключ для каждой картинки в секции
            section_key = f"{section['title']}_img{img_idx}" if num_images > 1 else section['title']
            img = get_image_for_section(city, cluster, section_key, images, mapping)
            if img:
                section_images.append(img)

        image_left = idx % 2 == 0

        if section_images:
            # Генерируем HTML для изображений с SEO alt-текстами
            def get_next_alt():
                nonlocal alt_counter
                if cluster_alts:
                    alt_text = cluster_alts[alt_counter % len(cluster_alts)]
                    alt_counter += 1
                    return f"{alt_text} {city_name}"
                return section["title"]

            if len(section_images) == 1:
                alt = get_next_alt()
                images_html = f'<img src="{section_images[0]}" alt="{alt}" loading="lazy">'
            else:
                # Несколько фото — в ряд
                img_items = ''.join([f'<div class="col"><img src="{img}" alt="{get_next_alt()}" loading="lazy" class="img-fluid rounded"></div>' for img in section_images])
                images_html = f'<div class="row g-2">{img_items}</div>'

            if image_left:
                html_parts.append(f'''
    <section class="content-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-5">
                    {images_html}
                </div>
                <div class="col-lg-7 section-text">
                    <h2>{section['title']}</h2>
                    {content_html}
                </div>
            </div>
        </div>
    </section>''')
            else:
                html_parts.append(f'''
    <section class="content-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-7 section-text">
                    <h2>{section['title']}</h2>
                    {content_html}
                </div>
                <div class="col-lg-5">
                    {images_html}
                </div>
            </div>
        </div>
    </section>''')
        else:
            html_parts.append(f'''
    <section class="content-section">
        <div class="container">
            <h2>{section['title']}</h2>
            {content_html}
        </div>
    </section>''')

    return '\n'.join(html_parts)


def generate_cluster_page(city_slug, cluster, template, mapping, city_phones, city_addresses, image_alts, cities_data, existing_meta=None):
    """Генерирует HTML страницу для города и кластера. Если existing_meta передан, использует сохранённые мета-теги."""

    # Получаем падежи города
    city_name, city_genitive, city_prepositional = CITIES.get(city_slug, (city_slug, city_slug, city_slug))

    # Получаем данные города (регион и т.д.)
    city_data = cities_data.get(city_slug, {})
    region_name = city_data.get('region', 'Московская область')

    # Получаем локальный номер телефона
    local_phone = city_phones.get(city_slug, "+7-495-000-00-00")

    # Получаем адрес бизнес-центра
    address_data = city_addresses.get(city_slug, {
        "name": "Бизнес-центр",
        "street": "ул. Центральная, 1",
        "office": "101",
        "postalCode": "",
        "latitude": 0,
        "longitude": 0
    })

    bc_name = address_data.get("name", "Бизнес-центр")
    bc_street = address_data.get("street", "")
    bc_office = address_data.get("office", "")
    bc_postal = address_data.get("postalCode", "")
    bc_latitude = address_data.get("latitude", 0)
    bc_longitude = address_data.get("longitude", 0)

    # Полный адрес для отображения
    full_address = f"{bc_street}, офис {bc_office}"

    # Путь к MD файлу
    md_file = os.path.join(SEO_TEXTS_DIR, cluster, f'{cluster}-{city_slug}.md')
    if not os.path.exists(md_file):
        return None

    # Читаем и парсим MD
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    parsed = parse_markdown(md_content)

    if not parsed['h1']:
        return None

    # Преобразуем H1 в именительный падеж для SEO
    h1 = parsed['h1']
    # Заменяем "в {предложный}" на именительный без "в"
    h1 = h1.replace(f" в {city_prepositional}", f" {city_name}")
    h1 = h1.replace(f" в {city_genitive}", f" {city_name}")
    # Если города нет вообще - добавляем
    if city_name not in h1 and city_genitive not in h1 and city_prepositional not in h1:
        h1 = f"{h1} {city_name}"

    # Генерируем секции с использованием маппинга и alt-текстов
    sections_html = generate_sections_html(parsed['sections'], cluster, city_slug, mapping, image_alts, city_name)

    # Мета-теги: используем сохранённые или генерируем новые
    if existing_meta and 'title' in existing_meta:
        meta_title = existing_meta['title']
    else:
        meta_title = h1

    if existing_meta and 'description' in existing_meta:
        meta_description = existing_meta['description']
    else:
        meta_description = f"{h1}. Быстрый расчёт, прозрачные цены, страхование груза. ☎ 8-800-707-29-36"

    meta_canonical = f"https://dinamika-cargo.ru/regions/{city_slug}/{cluster}/"

    # Заменяем плейсхолдеры
    html = template
    html = html.replace('{{TITLE}}', meta_title)
    html = html.replace('{{META_DESCRIPTION}}', meta_description)
    html = html.replace('{{H1}}', h1)
    # Обрабатываем intro
    if parsed['intro']:
        intro_text = parsed['intro']
        intro_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', intro_text, flags=re.DOTALL)
    else:
        # Берём первый абзац первой секции целиком (без обрезки)
        content = parsed['sections'][0]['content'] if parsed['sections'] else ''
        first_paragraph = content.split('\n\n')[0] if content else ''
        # Убираем markdown разметку
        intro_text = re.sub(r'\*\*(.+?)\*\*', r'\1', first_paragraph, flags=re.DOTALL)
    html = html.replace('{{INTRO}}', intro_text)
    html = html.replace('{{SECTIONS}}', sections_html)
    html = html.replace('{{CITY_NAME_RU}}', city_name)
    html = html.replace('{{CITY_NAME}}', city_name)
    html = html.replace('{{CITY_NAME_GENITIVE}}', city_genitive)
    html = html.replace('{{CITY_NAME_PREPOSITIONAL}}', city_prepositional)
    html = html.replace('{{CITY_SLUG}}', city_slug)
    html = html.replace('{{CLUSTER_SLUG}}', cluster)
    html = html.replace('{{CLUSTER_TITLE}}', CLUSTER_INFO[cluster]['title'])
    html = html.replace('{{LOCAL_PHONE}}', local_phone)
    html = html.replace('{{BC_NAME}}', bc_name)
    html = html.replace('{{BC_STREET}}', bc_street)
    html = html.replace('{{FULL_ADDRESS}}', full_address)

    # Плейсхолдеры для Schema.org LocalBusiness
    html = html.replace('{{REGION_NAME}}', region_name)
    html = html.replace('{{POSTAL_CODE}}', bc_postal)
    html = html.replace('{{LATITUDE}}', str(bc_latitude))
    html = html.replace('{{LONGITUDE}}', str(bc_longitude))

    # Генерируем блок других кластеров
    other_clusters_html = generate_other_clusters_html(cluster)
    html = html.replace('{{OTHER_CLUSTERS}}', other_clusters_html)

    # Генерируем FAQ для кластера
    faq_html = generate_faq_html(cluster)
    html = html.replace('{{FAQ_ITEMS}}', faq_html)

    # Генерируем таблицу маршрутов
    routes_table_html = generate_routes_table_html(city_slug, cluster, city_addresses)
    html = html.replace('{{ROUTES_TABLE}}', routes_table_html)

    # Возвращаем HTML и мета-теги для сохранения
    generated_meta = {
        'title': meta_title,
        'description': meta_description,
        'canonical': meta_canonical
    }

    return html, generated_meta


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Генератор кластерных страниц')
    parser.add_argument('--test', action='store_true', help='Тестовый режим (1 город)')
    parser.add_argument('--city', type=str, help='Генерировать только для города')
    parser.add_argument('--cluster', type=str, help='Генерировать только кластер')
    args = parser.parse_args()

    print("=== Генератор кластерных страниц ===\n")

    # Загрузка маппинга картинок
    mapping = load_images_mapping()
    print(f"Загружен маппинг картинок: {len(mapping)} городов\n")

    # Загрузка номеров телефонов
    city_phones = load_city_phones()
    print(f"Загружено номеров телефонов: {len(city_phones)}\n")

    # Загрузка адресов бизнес-центров
    city_addresses = load_city_addresses()
    print(f"Загружено адресов БЦ: {len(city_addresses)}\n")

    # Загрузка alt-текстов для изображений
    image_alts = load_image_alts()
    print(f"Загружено alt-текстов: {sum(len(v) for v in image_alts.values())} (кластеров: {len(image_alts)})\n")

    # Загрузка данных городов (регион)
    cities_data = load_cities_data()
    print(f"Загружено данных городов: {len(cities_data)}\n")

    # Загрузка маппинга мета-тегов
    meta_mapping = load_meta_mapping()
    print(f"Загружен маппинг мета-тегов: {len(meta_mapping)}\n")

    # Загрузка шаблона
    template = load_template()
    print(f"Шаблон: {TEMPLATE_FILE}\n")

    # Определяем города
    cities = [args.city] if args.city else list(CITIES.keys())
    if args.test:
        cities = cities[:1]

    # Определяем кластеры
    clusters = [args.cluster] if args.cluster else CLUSTERS

    created = 0
    skipped = 0

    for city_slug in cities:
        if city_slug not in CITIES:
            print(f"⚠ Город {city_slug} не найден в словаре")
            continue

        city_name = CITIES[city_slug][0]

        for cluster in clusters:
            # Получаем сохранённые мета-теги (если есть)
            existing_meta = get_existing_meta(city_slug, cluster, meta_mapping)

            # Генерируем HTML с использованием маппинга и alt-текстов
            result = generate_cluster_page(city_slug, cluster, template, mapping, city_phones, city_addresses, image_alts, cities_data, existing_meta)

            if not result:
                skipped += 1
                continue

            html, generated_meta = result

            # Сохраняем мета-теги в маппинг
            meta_key = f"{city_slug}/{cluster}"
            meta_mapping[meta_key] = generated_meta

            # Создаём папку и сохраняем
            output_dir = os.path.join(OUTPUT_DIR, city_slug, cluster)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, 'index.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"✓ {city_name} / {cluster} → /regions/{city_slug}/{cluster}/index.html")
            created += 1

    # Сохраняем обновлённый маппинг картинок
    save_images_mapping(mapping)
    print(f"\n💾 Маппинг картинок сохранён в {MAPPING_FILE}")

    # Сохраняем маппинг мета-тегов
    save_meta_mapping(meta_mapping)
    print(f"💾 Маппинг мета-тегов сохранён в {META_MAPPING_FILE}")

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Сохранено мета-тегов: {len(meta_mapping)}")
    print(f"Пропущено: {skipped}")


if __name__ == '__main__':
    main()
