# Динамика — сайт грузоперевозок (dinamika-cargo.ru)

Статический SEO-сайт на GitHub Pages (ветка **main-secure**). ~2300 страниц: 48 городов × кластеры + 1264 маршрута.
Подробности концепции — [PRD.md](PRD.md), задачи — [tasks.md](tasks.md), SEO — [strategy.md](strategy.md).

## Готчи (важное, неочевидное)
- Деплой только с ветки **main-secure**, не main. Push: `git push origin main-secure`. Живёт через 1-2 мин.
- Python-скрипты на GitHub Pages не работают — только статика. Скрипты генерации запускаются локально.
- Ссылки на папки — всегда абсолютные (`/regions/`), иначе ломаются на вложенных страницах.
- Домен dinamika-cargo.ru → GitHub Pages. VPS (82.22.47.114) — отдельная машина для серверной логики (см. заявки).

## Приём заявок (свой сервис на VPS)
Формы НЕ шлют напрямую в Telegram — раньше так было, токен светился в публичном коде, а почта терялась через Web3Forms. Сейчас:
- Все формы → `POST https://agentiks.ru/dinamika/api/lead` → сервис на VPS → Telegram + почта kontekst-rt@yandex.ru + лог каждой заявки.
- Токен бота и SMTP-пароль живут только на сервере (`/home/deploy/dinamika-forms/.env`), в публичный код не попадают.
- Сервис: pm2 `dinamika-forms`, порт 3100. Логи: `pm2 logs dinamika-forms` или `/home/deploy/dinamika-forms/logs/`.
- Подробно — README в папке сервиса на VPS: `/home/deploy/dinamika-forms/README.md`.
- Формы на сайте: `assets/js/forms-handler.js` (все callback), `thank-you.html` (дополнение), `calculator-new.html` (калькулятор).

**Проверка форм:** `python3 audit_forms.py` — статический аудит всех форм (отправка в сервис, поле телефона, нет ли старого токена/Web3Forms). Прогонять после правок форм.

## SEO-аналитика и генерация
- GSC: `python3 gsc_analytics.py` · Яндекс: `python3 yandex_webmaster.py` · дашборд: `python3 generate_dashboard.py`
- Генераторы страниц: `generate_cluster_pages.py`, `generate_cargo_pages.py`, `generate_city_pages.py`, `generate_route_pages.py` (см. CLAUDE.md).
