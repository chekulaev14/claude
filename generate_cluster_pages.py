#!/usr/bin/env python3
"""
Генератор кластерных страниц для ТК Динамика
Создаёт /regions/{город}/{кластер}/index.html из MD файлов и шаблона
"""

import os
import re
import random

# Базовые пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates', 'cluster-template.html')
SEO_TEXTS_DIR = os.path.join(BASE_DIR, 'seo-texts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'regions')
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images', 'clusters')

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
    "irkutsk": ("Иркутск", "Иркутска", "Иркутске"),
    "ivanteyevka": ("Ивантеевка", "Ивантеевки", "Ивантеевке"),
    "izhevsk": ("Ижевск", "Ижевска", "Ижевске"),
    "kaluga": ("Калуга", "Калуги", "Калуге"),
    "kazan": ("Казань", "Казани", "Казани"),
    "khabarovsk": ("Хабаровск", "Хабаровска", "Хабаровске"),
    "khimki": ("Химки", "Химок", "Химках"),
    "klin": ("Клин", "Клина", "Клину"),
    "kolomna": ("Коломна", "Коломны", "Коломне"),
    "korolev": ("Королёв", "Королёва", "Королёве"),
    "krasnodar": ("Краснодар", "Краснодара", "Краснодаре"),
    "krasnogorsk": ("Красногорск", "Красногорска", "Красногорске"),
    "krasnoyarsk": ("Красноярск", "Красноярска", "Красноярске"),
    "lobnya": ("Лобня", "Лобни", "Лобне"),
    "lyubertsy": ("Люберцы", "Люберец", "Люберцах"),
    "moscow": ("Москва", "Москвы", "Москве"),
    "mytishchi": ("Мытищи", "Мытищ", "Мытищах"),
    "naberezhnye-chelny": ("Набережные Челны", "Набережных Челнов", "Набережных Челнах"),
    "nizhnekamsk": ("Нижнекамск", "Нижнекамска", "Нижнекамске"),
    "nizhny-novgorod": ("Нижний Новгород", "Нижнего Новгорода", "Нижнем Новгороде"),
    "noginsk": ("Ногинск", "Ногинска", "Ногинске"),
    "novosibirsk": ("Новосибирск", "Новосибирска", "Новосибирске"),
    "obninsk": ("Обнинск", "Обнинска", "Обнинске"),
    "odintsovo": ("Одинцово", "Одинцова", "Одинцове"),
    "omsk": ("Омск", "Омска", "Омске"),
    "orekhovo-zuevo": ("Орехово-Зуево", "Орехово-Зуева", "Орехово-Зуеве"),
    "perm": ("Пермь", "Перми", "Перми"),
    "podolsk": ("Подольск", "Подольска", "Подольске"),
    "pushkino": ("Пушкино", "Пушкино", "Пушкино"),
    "ramenskoe": ("Раменское", "Раменского", "Раменском"),
    "reutov": ("Реутов", "Реутова", "Реутове"),
    "rostov-on-don": ("Ростов-на-Дону", "Ростова-на-Дону", "Ростове-на-Дону"),
    "saint-petersburg": ("Санкт-Петербург", "Санкт-Петербурга", "Санкт-Петербурге"),
    "samara": ("Самара", "Самары", "Самаре"),
    "sergiev-posad": ("Сергиев Посад", "Сергиева Посада", "Сергиевом Посаде"),
    "serpukhov": ("Серпухов", "Серпухова", "Серпухове"),
    "shchelkovo": ("Щёлково", "Щёлкова", "Щёлкове"),
    "stupino": ("Ступино", "Ступино", "Ступино"),
    "tula": ("Тула", "Тулы", "Туле"),
    "tver": ("Тверь", "Твери", "Твери"),
    "tyumen": ("Тюмень", "Тюмени", "Тюмени"),
    "ufa": ("Уфа", "Уфы", "Уфе"),
    "vidnoye": ("Видное", "Видного", "Видном"),
    "vladivostok": ("Владивосток", "Владивостока", "Владивостоке"),
    "volgograd": ("Волгоград", "Волгограда", "Волгограде"),
    "voronezh": ("Воронеж", "Воронежа", "Воронеже"),
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


def generate_sections_html(sections, cluster, used_images):
    """Генерирует HTML для секций с изображениями"""
    html_parts = []
    images = get_cluster_images(cluster)
    available_images = [img for img in images if img not in used_images]

    # Количество изображений зависит от длины текста
    total_text = ' '.join([s['content'] for s in sections])
    if len(total_text) > 5000:
        num_images = 3
    elif len(total_text) > 2500:
        num_images = 2
    else:
        num_images = 1

    # Выбираем секции для изображений
    image_positions = []
    if len(sections) >= num_images:
        step = len(sections) // (num_images + 1)
        for i in range(num_images):
            image_positions.append((i + 1) * step)

    for idx, section in enumerate(sections):
        # Преобразуем markdown в HTML
        content_html = section['content']
        # Жирный текст
        content_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content_html)
        # Абзацы
        paragraphs = content_html.split('\n\n')
        content_html = ''.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])

        # Определяем, нужно ли изображение
        has_image = idx in image_positions and available_images
        image_left = idx % 2 == 0

        if has_image:
            # Выбираем случайное изображение
            img = random.choice(available_images)
            available_images.remove(img)
            used_images.add(img)

            if image_left:
                html_parts.append(f'''
    <section class="content-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-5">
                    <img src="{img}" alt="{section['title']}" loading="lazy">
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
                    <img src="{img}" alt="{section['title']}" loading="lazy">
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


def generate_cluster_page(city_slug, cluster, template):
    """Генерирует HTML страницу для города и кластера"""

    # Получаем падежи города
    city_name, city_genitive, city_prepositional = CITIES.get(city_slug, (city_slug, city_slug, city_slug))

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

    # Генерируем секции
    used_images = set()
    sections_html = generate_sections_html(parsed['sections'], cluster, used_images)

    # Заменяем плейсхолдеры
    html = template
    html = html.replace('{{TITLE}}', h1)
    html = html.replace('{{META_DESCRIPTION}}', f"{h1}. Быстрый расчёт, прозрачные цены, страхование груза. ☎ 8-800-707-29-36")
    html = html.replace('{{H1}}', h1)
    html = html.replace('{{INTRO}}', parsed['intro'] if parsed['intro'] else parsed['sections'][0]['content'][:200] + '...' if parsed['sections'] else '')
    html = html.replace('{{SECTIONS}}', sections_html)
    html = html.replace('{{CITY_NAME_RU}}', city_name)
    html = html.replace('{{CITY_NAME_GENITIVE}}', city_genitive)
    html = html.replace('{{CITY_NAME_PREPOSITIONAL}}', city_prepositional)

    # Генерируем блок других кластеров
    other_clusters_html = generate_other_clusters_html(cluster)
    html = html.replace('{{OTHER_CLUSTERS}}', other_clusters_html)

    return html


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Генератор кластерных страниц')
    parser.add_argument('--test', action='store_true', help='Тестовый режим (1 город)')
    parser.add_argument('--city', type=str, help='Генерировать только для города')
    parser.add_argument('--cluster', type=str, help='Генерировать только кластер')
    args = parser.parse_args()

    print("=== Генератор кластерных страниц ===\n")

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
            # Генерируем HTML
            html = generate_cluster_page(city_slug, cluster, template)

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

    print(f"\n=== Готово! ===")
    print(f"Создано страниц: {created}")
    print(f"Пропущено: {skipped}")


if __name__ == '__main__':
    main()
