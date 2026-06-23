# Общие настройки
Используй claude sonnet 4.5
Общайся со мной на русском языке
Общайся кратко, у меня СДВГ, мне трудно концентрироваться на длинных текстах

# О проекте
Мы разрабатываем сайт для экспедиторской компании "Динамика", которая осуществляет перевозки по РФ

# Workflow (процесс работы)
После каждого запуска отчитывайся прочитал ли ты все необходимые файлы
Читай PRD.md для понимания общей концепции проекта и отчитывайся что прочитал
Читай tasks.md для понимания стратегических задач, каждый раз отчитывайся что прочитал и пиши весь список задач
Читай strategy.md - SEO-стратегия контента (index + кластеры)
После каждого действия, спрашивай закоммитить или нет. Если да, то делай коммит и пуш
После выполнения каждой задачи отчет об использовании MCP отчет в чем была проблема и как ты ее решил
Производи мониторинг ответов в терминале на твои запросы, если есть ошибки, то анализируй их и пиши в конце действия в отчете что за ошибка и почему. Будем принимать решение о вписании некоторых ошибок в этот файл, чтобы в будущем их избежать.
Если не получается решить задачу c 3 раза, то на 4 раз запускай think harder
Если в процессе выполнения задач спрашивается разрешение на какое-то действие, то нужно изменить системный файл чтобы разрешения больше не спрашивалось.

# MCP инструменты
Если PW (Playwright) не смог сделать фото сайта, не нужно идти дальше. Остановись, перезапусти браузер и попробуй еще раз.

# Google Search Console API
Есть доступ к GSC API через Service Account: `clauderobot@ancient-binder-437314-m9.iam.gserviceaccount.com`
- Credentials: `gsc-credentials.json` (в .gitignore)
- Скрипт: `gsc_analytics.py`
- Сайт: `https://dinamika-cargo.ru/`

**Команды:**
```bash
python3 gsc_analytics.py queries 50   # топ запросов
python3 gsc_analytics.py pages 30     # топ страниц
python3 gsc_analytics.py page /path/  # запросы для конкретного раздела
python3 gsc_analytics.py export       # экспорт в JSON
```

**Что можно добавить:** URL Inspection (проверка индексации), сравнение периодов, управление сайтмапами.

# Яндекс.Вебмастер API
Есть доступ к API через OAuth токен.
- Credentials: `yandex-credentials.json` (в .gitignore)
- Скрипт: `yandex_webmaster.py`
- Host ID: `https:dinamika-cargo.ru:443`

**Команды:**
```bash
python3 yandex_webmaster.py hosts     # список сайтов
python3 yandex_webmaster.py summary   # сводка (ИКС, запросы)
python3 yandex_webmaster.py queries   # поисковые запросы JSON
```

**Доступные данные:** ИКС, поисковые запросы, показы/клики/позиции, sitemaps.

# Файлы и структура проекта
Стили CSS в папке /assets/css/
Шаблоны страниц в папке /templates/
SEO-тексты для кластеров в папке /seo-texts/{cluster}/
Фото для кластеров в папке /assets/images/clusters/{cluster}/
При перемещении блоков кода лучше использовать два отдельных Edit вместо одного MultiEdit, чтобы избежать конфликтов строк.

# Скрипты генерации страниц

## generate_cluster_pages.py — основные кластеры (5 шт)
Генерирует страницы кластеров: mezhgorod, transportnaya, dlinnomer, po-rossii, fura
  - Шаблон: /templates/cluster-template.html
  - SEO-тексты: /seo-texts/{cluster}/{cluster}-{город}.md
  - Фото: /assets/images/clusters/{cluster}/
  - Результат: /regions/{город}/{cluster}/index.html
  - Флаги: --test (1 город), --city X (конкретный город), --cluster Y (конкретный кластер)

## generate_cargo_pages.py — грузовые кластеры (truby и др.)
Генерирует страницы кластеров по типам грузов (перевозка труб, стройматериалов и т.д.)
  - Шаблоны: /templates/cargo-{cluster}-template.html (отдельный шаблон для каждого кластера!)
  - Конфиг: /data/cargo-clusters.json (title, icon, template, faq, image_alts, enabled)
  - Фото: /assets/images/clusters/{cluster}/
  - Маппинги: /data/cargo-images-mapping.json, /data/cargo-meta-mapping.json
  - Результат: /regions/{город}/{cluster}/index.html
  - Флаги: --test (1 город), --city X, --cluster Y
  - Плейсхолдеры в шаблоне: {{CITY_NAME}}, {{CITY_PREPOSITIONAL}}, {{CITY_URL}}, {{IMAGE_1-4}}, {{IMAGE_ALT_1-4}}, {{FAQ_ITEMS}}, {{FAQ_SCHEMA}}
  - **Активация кластера**: добавить `"enabled": true` в cargo-clusters.json → перегенерировать все страницы (city, cluster, cargo)

## generate_city_pages.py — главные страницы городов
Генерирует /regions/{город}/index.html
  - Шаблон: /templates/city-index-template.html
  - Данные: /data/cities.json, /data/city-addresses.json, /data/city-phones.json
  - Cargo-кластеры: /data/cargo-clusters.json (выводятся как теги)
  - Флаги: --city X (конкретный город)

## dashboard_server.py — SEO дашборд (локальный сервер)
Подробно: seo-dashboard/README.md. Открывать: http://localhost:8087

## generate_dashboard.py — SEO дашборд (разовая генерация)
Генерирует `/seo-dashboard/index.html` с данными GSC + Яндекс без сервера. Запустить: `python3 generate_dashboard.py`, затем пушнуть вручную.

## generate_route_pages.py — страницы маршрутов (1264 шт)
  - Шаблон: /templates/route-template.html
  - Результат: /routes/{откуда}-{куда}/index.html
  - Флаги: --test (ограниченная генерация)

# Git и деплой
Сайт выложен на Github Pages и деплоится с ветки main-secure (НЕ main!)
Команда для пуша: git push origin main-secure
После пуша изменения видны на dinamika-cargo.ru через 1-2 минуты
Python скрипты на GitHub Pages не работают - только статика
При коммите ВСЕГДА используй `git add .` - коммить все файлы, не выбирай вручную (кроме .env, ключи API и прочие секреты - они в .gitignore)

# Создание новых страниц
При создании новой страницы копируй <head> из index.html, меняй только <title> и meta-теги для SEO. Порядок подключения CSS всегда одинаковый: IBM Plex Sans → Bootstrap → styles.css

## Schema.org (обязательно!)
Каждая новая страница должна содержать:
1. **BreadcrumbList** — хлебные крошки
2. **Ссылка на родительскую организацию**: `"provider": {"@id": "https://dinamika-cargo.ru/#organization"}`
3. **ТГ бот** в potentialAction:
```json
"potentialAction": {
    "@type": "CommunicateAction",
    "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://t.me/dinamikus_bot",
        "actionPlatform": "https://telegram.org"
    },
    "name": "Связаться через Telegram бот"
}
```
4. **Alt для картинок** — если на странице есть фото, обязательно прописывай осмысленные alt-атрибуты

Пример Schema.org смотри в /contacts/index.html или /regions/index.html

# Ссылки (важно!)
ВСЕГДА используй абсолютные пути (начинающиеся с /) для ссылок на папки: /regions/, /assets/css/
Относительные пути для папок (regions/) работают непредсказуемо: на главной OK, на вложенных страницах ищет /page/regions/ вместо /regions/
Файлы .html могут работать с относительными путями, но для единообразия лучше тоже абсолютные

# Разное
Иногда спрашивай меня не забываю ли я есть творог по вечерам вместо сладкого
Иногда напоминай мне что один день в неделю нужно отказываться от мяса полностью и раз в 2 недели от еды на 24 часа