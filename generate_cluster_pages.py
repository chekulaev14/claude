#!/usr/bin/env python3
"""
Генератор кластерных страниц для ТК Динамика
Создаёт /regions/{город}/{кластер}/index.html из MD файлов и шаблона
"""

import os
import re
import random
import json

# Базовые пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'cluster-template.html')
SEO_TEXTS_DIR = os.path.join(BASE_DIR, 'seo-texts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images', 'clusters')
MAPPING_FILE = os.path.join(BASE_DIR, 'data', 'images-mapping.json')
CITY_PHONES_FILE = os.path.join(BASE_DIR, 'data', 'city-phones.json')
CITY_ADDRESSES_FILE = os.path.join(BASE_DIR, 'data', 'city-addresses.json')

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
    "shchelkovo": ("Щёлково", "Щёлкова", "Щёлкове"),
    "tula": ("Тула", "Тулы", "Туле"),
    "tver": ("Тверь", "Твери", "Твери"),
    "ufa": ("Уфа", "Уфы", "Уфе"),
    "voskresensk": ("Воскресенск", "Воскресенска", "Воскресенске"),
    "yaroslavl": ("Ярославль", "Ярославля", "Ярославле"),
    "zhukovsky": ("Жуковский", "Жуковского", "Жуковском"),
}

# Кластеры
CLUSTERS = ['mezhgorod', 'transportnaya', 'dlinnomer', 'po-rossii', 'fura']

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


def generate_sections_html(sections, cluster, city, mapping):
    """Генерирует HTML для секций с изображениями (с использованием маппинга)"""
    html_parts = []
    images = get_cluster_images(cluster)

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
            # Генерируем HTML для изображений
            if len(section_images) == 1:
                images_html = f'<img src="{section_images[0]}" alt="{section["title"]}" loading="lazy">'
            else:
                # Несколько фото — в ряд
                img_items = ''.join([f'<div class="col"><img src="{img}" alt="{section["title"]}" loading="lazy" class="img-fluid rounded"></div>' for img in section_images])
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


def generate_cluster_page(city_slug, cluster, template, mapping, city_phones, city_addresses):
    """Генерирует HTML страницу для города и кластера"""

    # Получаем падежи города
    city_name, city_genitive, city_prepositional = CITIES.get(city_slug, (city_slug, city_slug, city_slug))

    # Получаем локальный номер телефона
    local_phone = city_phones.get(city_slug, "+7-495-000-00-00")

    # Получаем адрес бизнес-центра
    address_data = city_addresses.get(city_slug, {
        "name": "Бизнес-центр",
        "street": "ул. Центральная, 1",
        "office": "101",
        "postalCode": ""
    })

    bc_name = address_data.get("name", "Бизнес-центр")
    bc_street = address_data.get("street", "")
    bc_office = address_data.get("office", "")
    bc_postal = address_data.get("postalCode", "")

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

    # Генерируем секции с использованием маппинга
    sections_html = generate_sections_html(parsed['sections'], cluster, city_slug, mapping)

    # Заменяем плейсхолдеры
    html = template
    html = html.replace('{{TITLE}}', h1)
    html = html.replace('{{META_DESCRIPTION}}', f"{h1}. Быстрый расчёт, прозрачные цены, страхование груза. ☎ 8-800-707-29-36")
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

    # Генерируем блок других кластеров
    other_clusters_html = generate_other_clusters_html(cluster)
    html = html.replace('{{OTHER_CLUSTERS}}', other_clusters_html)

    # Генерируем FAQ для кластера
    faq_html = generate_faq_html(cluster)
    html = html.replace('{{FAQ_ITEMS}}', faq_html)

    return html


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
            # Генерируем HTML с использованием маппинга
            html = generate_cluster_page(city_slug, cluster, template, mapping, city_phones, city_addresses)

            if not html:
                skipped += 1
                continue

            # Создаём папку и сохраняем
            output_dir = os.path.join(OUTPUT_DIR, city_slug, cluster)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, 'index.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"✓ {city_name} / {cluster} → /regions/{city_slug}/{cluster}/index.html")
            created += 1

    # Сохраняем обновлённый маппинг
    save_images_mapping(mapping)
    print(f"\n💾 Маппинг картинок сохранён в {MAPPING_FILE}")

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Пропущено: {skipped}")


if __name__ == '__main__':
    main()
