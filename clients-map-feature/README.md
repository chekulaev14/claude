# Фича: Карта клиентов

Интерактивная карта клиентов ТК Динамика с автоматическим сбором данных через API.

## 📁 Структура

```
clients-map-feature/
├── functions/               # Netlify Functions для сбора данных
│   ├── fetch-client-addresses.js  # Сбор адресов по ИНН (85/день)
│   └── geocode-addresses.js       # Геокодирование городов
├── pages/
│   └── clients-map.html    # Страница с картой
├── assets/
│   ├── js/
│   │   └── clients-map.js  # JavaScript для карты
│   └── data/
│       ├── clients-map-simple.json  # Упрощенные данные
│       └── clients-map-data.json    # Полные данные с клиентами
└── docs/
    └── CLIENTS-MAP-README.md  # Подробная инструкция

```

## 🚀 Быстрый старт

### 1. Установка

Скопировать файлы в основной проект:

```bash
# Functions
cp functions/*.js ../netlify/functions/

# Страница
cp pages/clients-map.html ../pages/

# Assets
cp assets/js/clients-map.js ../assets/js/
cp assets/data/*.json ../assets/data/
```

### 2. Настройка Netlify

В настройках сайта добавить переменные:

```
FETCH_ADDRESSES_TOKEN=твой-секретный-токен-1
GEOCODE_TOKEN=твой-секретный-токен-2
```

### 3. Запуск сбора данных

**Этап 1: Сбор адресов (10 дней)**
```
https://твой-сайт.ru/.netlify/functions/fetch-client-addresses?token=токен-1
```

**Этап 2: Геокодирование**
```
https://твой-сайт.ru/.netlify/functions/geocode-addresses?token=токен-2
```

### 4. Готово!

Карта доступна по адресу: `/pages/clients-map.html`

## 📊 Данные

- **Исходные:** 793 клиента с валидными ИНН
- **Mock-данные:** 20 городов, 693 клиента (для тестирования)
- **Формат:** JSON с координатами и списком клиентов

## 🔧 API используемые

1. **egrul.itsoft.ru** - бесплатно 100 запросов/день
2. **Google Maps Geocoding API** - бесплатно 2500 запросов/день
3. **Google Maps JavaScript API** - для отображения карты

## 📖 Документация

Полная документация: `docs/CLIENTS-MAP-README.md`

## ✅ Статус

- [x] Netlify Functions созданы
- [x] Страница с картой готова
- [x] Mock-данные для теста
- [x] Проверен Google API ключ
- [x] Добавлено в меню сайта
- [ ] Настроены токены в Netlify
- [ ] Запущен сбор данных
- [ ] Заполнена карта реальными данными
