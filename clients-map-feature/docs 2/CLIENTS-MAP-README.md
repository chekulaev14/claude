# Карта клиентов - Инструкция

## Как это работает

Система автоматически собирает данные о клиентах и отображает их на карте с кластерами.

### Процесс:

1. **Сбор адресов** - функция запрашивает данные по ИНН из API egrul.itsoft.ru (85 клиентов/день)
2. **Геокодирование** - функция преобразует города в координаты через Google Maps
3. **Отображение** - карта показывает точки с количеством клиентов в каждом городе

## Запуск функций

### 1. Настроить переменные окружения в Netlify

Перейти в: **Site settings → Environment variables**

Добавить:
```
FETCH_ADDRESSES_TOKEN=ваш-секретный-токен-1
GEOCODE_TOKEN=ваш-секретный-токен-2
```

### 2. Запустить сбор адресов

Первый этап - собрать адреса по ИНН (793 клиента = ~10 дней по 85/день):

```bash
# Вручную через браузер или curl
https://dinamika-cargo.ru/.netlify/functions/fetch-client-addresses?token=ваш-секретный-токен-1
```

**Ответ:**
```json
{
  "success": true,
  "processed": 85,
  "totalProcessed": 85,
  "remaining": 708,
  "lastRun": "2025-10-20T12:00:00.000Z"
}
```

### 3. Запустить геокодирование

После сбора всех адресов (или части), запустить геокодирование:

```bash
https://dinamika-cargo.ru/.netlify/functions/geocode-addresses?token=ваш-секретный-токен-2
```

**Ответ:**
```json
{
  "success": true,
  "totalCities": 150,
  "geocoded": 148,
  "totalClients": 793,
  "outputFile": "clients-map-data.json"
}
```

## Автоматический запуск (опционально)

### Вариант 1: Бесплатный Cron сервис

Использовать [cron-job.org](https://cron-job.org) или [EasyCron](https://www.easycron.com/):

1. Зарегистрироваться
2. Создать задачу с URL: `https://dinamika-cargo.ru/.netlify/functions/fetch-client-addresses?token=...`
3. Расписание: **1 раз в день** (например, в 3:00 ночи)

### Вариант 2: GitHub Actions

Создать `.github/workflows/fetch-clients.yml`:

```yaml
name: Fetch Client Addresses

on:
  schedule:
    - cron: '0 3 * * *'  # Каждый день в 3:00 UTC
  workflow_dispatch:  # Ручной запуск

jobs:
  fetch:
    runs-on: ubuntu-latest
    steps:
      - name: Call Netlify Function
        run: |
          curl -X GET "https://dinamika-cargo.ru/.netlify/functions/fetch-client-addresses?token=${{ secrets.FETCH_TOKEN }}"
```

Добавить секрет `FETCH_TOKEN` в настройках репозитория.

## Файлы данных

После работы функций создаются файлы:

- `assets/data/clients-with-addresses.json` - клиенты с адресами
- `assets/data/clients-addresses-progress.json` - прогресс сбора
- `assets/data/clients-map-data.json` - полные данные для карты
- `assets/data/clients-map-simple.json` - упрощенная версия для быстрой загрузки

## Структура данных для карты

```json
[
  {
    "city": "Москва",
    "region": "Москва",
    "lat": 55.7558,
    "lng": 37.6173,
    "count": 125,
    "clients": [
      {"name": "Компания 1", "inn": "123456789"},
      {"name": "Компания 2", "inn": "987654321"}
    ]
  }
]
```

## Отображение на странице

Страница `/pages/clients-map.html` загружает `clients-map-simple.json` и отображает:

- **Маркеры** с количеством клиентов
- **Кластеры** для близких точек
- **Popup** с названиями клиентов при клике

## Мониторинг

Проверить статус:
- Логи Netlify Functions: **Site settings → Functions → Logs**
- Файлы данных в репозитории: `assets/data/`

## Ограничения API

- **egrul.itsoft.ru**: 100 запросов/день (используем 85 для запаса)
- **Google Maps Geocoding**: 2500 запросов/день (бесплатный уровень)
