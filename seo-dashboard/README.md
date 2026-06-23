# SEO Dashboard

## Как открыть
Перейди по адресу: http://localhost:8087

## Как обновить данные
Нажми кнопку «Обновить данные» на странице. Занимает ~15-30 сек.

## Как это работает
- `dashboard_server.py` — Python-сервер на localhost:8087, работает в фоне
- Кнопка делает запрос к серверу → он идёт в GSC и Яндекс API → возвращает данные → страница обновляется
- Сервер стартует автоматически при входе в macOS (LaunchAgent)

## Если кнопка не работает (сервер упал)
```
launchctl load ~/Library/LaunchAgents/com.dinamika.dashboard.plist
```

## Файлы
- `dashboard_server.py` — API сервер (порт 8087)
- `generate_dashboard.py` — разовая генерация index.html без сервера
- `seo-dashboard/index.html` — сам дашборд
- `~/Library/LaunchAgents/com.dinamika.dashboard.plist` — автозапуск macOS
