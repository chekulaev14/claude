# Структура сайта ТК "Динамика"

## Общая архитектура

```
/
├── docs/                    # Техническая документация
│   ├── site-structure.md    # Этот файл - архитектура сайта
│   ├── components-guide.md  # Описание компонентов
│   ├── content-rules.md     # Правила контента
│   ├── development-notes.md # Заметки по разработке
│   └── pages-info.md        # Описание страниц
├── templates/               # Шаблоны
│   ├── header.html         # Шапка сайта
│   ├── footer.html         # Подвал сайта
│   └── layout.html         # Базовый layout
├── pages/                  # Страницы сайта
│   ├── intercity.html      # Междугородние перевозки
│   ├── truck.html          # Грузовые перевозки (фура)
│   ├── long-trailer.html   # Длинномер шаланда
│   ├── partial.html        # Догруз попутно
│   ├── about.html          # О компании
│   └── contacts.html       # Контакты
├── assets/                 # Ресурсы
│   ├── css/               # Стили
│   │   └── styles.css     # Основные стили
│   ├── js/                # JavaScript
│   │   └── script.js      # Основные скрипты
│   └── images/            # Изображения
│       └── color_big.png  # Логотип компании
├── index.html             # Главная страница
├── CLAUDE.md              # Инструкции для Claude Code
├── .mcp.json             # Конфигурация MCP серверов
└── .taskmaster/          # Task Master AI
```

## Карта страниц

### Главная страница (`index.html`)
- URL: `/`
- Назначение: Презентация услуг, первый контакт с клиентом
- Компоненты: Header, Hero, Services Grid, Footer

### Страницы услуг
1. **ГРУЗОПЕРЕВОЗКИ МЕЖГОРОД** (`pages/intercity.html`)
   - URL: `/pages/intercity.html`
   - Якорь: `#intercity`

2. **ГРУЗОПЕРЕВОЗКИ ФУРА** (`pages/truck.html`)
   - URL: `/pages/truck.html`
   - Якорь: `#truck`

3. **ГРУЗОПЕРЕВОЗКИ ДЛИННОМЕР ШАЛАНДА** (`pages/long-trailer.html`)
   - URL: `/pages/long-trailer.html`
   - Якорь: `#long-trailer`

4. **ГРУЗОПЕРЕВОЗКИ ДОГРУЗ ПОПУТНО** (`pages/partial.html`)
   - URL: `/pages/partial.html`
   - Якорь: `#partial`

### Информационные страницы
- **Цены** (`pages/prices.html`) - тарифные планы и условия
- **Клиенты** (`pages/clients.html`) - клиентская база с фильтрацией
- **О компании** (`pages/about.html`)
- **Контакты** (`pages/contacts.html`)

## Навигация

### Главное меню
- Главная → `index.html`
- Услуги (dropdown):
  - Междугородние → `pages/intercity.html`
  - Фура → `pages/truck.html`  
  - Длинномер шаланда → `pages/long-trailer.html`
  - Догруз попутно → `pages/partial.html`
- Цены → `pages/prices.html`
- Клиенты → `pages/clients.html`
- Контакты → `pages/contacts.html`

### Контактная информация в header
- Телефон: 8-987-416-51-87
- ~~Время работы: удалено из header по запросу~~

## Технические особенности

### Bootstrap 5.3
- Используется для адаптивности и компонентов
- CDN подключение в layout

### Swiper.js 11
- Для карусели услуг на главной странице
- CDN подключение в index.html
- Настроена адаптивность: 1-2-3 слайда

### MCP Серверы
- **Task Master** - управление задачами
- **Context7** - документация библиотек  
- **Playwright** - тестирование UI

### Стили и скрипты
- `assets/css/styles.css` - кастомные стили поверх Bootstrap
- `assets/js/script.js` - интерактивность (меню, скролл)

## Последнее обновление
Дата: 2025-09-10
Версия: 1.1
Автор: Claude Code Assistant