# Заметки по разработке

## Используемые технологии

### Frontend Framework: Bootstrap 5.3
```html
<!-- CDN подключение -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
```

### Шрифты: Google Fonts - Inter
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Swiper.js 11: для карусели услуг
```html
<!-- Swiper CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
<!-- Swiper JS -->
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
```

## CSS архитектура

### Основной файл стилей: `assets/css/styles.css`

### Структура CSS:
1. **Reset стили** - обнуление браузерных стилей
2. **Bootstrap overrides** - переопределение Bootstrap компонентов
3. **Custom components** - кастомные компоненты
4. **Utilities** - вспомогательные классы
5. **Media queries** - адаптивность

### Важные CSS классы:

#### Bootstrap переопределения:
```css
.navbar {
    padding: 0.8rem 0;
    transition: all 0.3s ease;
}

.navbar.scrolled {
    padding: 0.4rem 0;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1) !important;
}
```

#### Кастомные компоненты:
```css
.service-card {
    background-color: white;
    padding: 25px 20px;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}
```

### Цветовые переменные (рекомендуется добавить):
```css
:root {
    --primary-color: #2c5aa0;
    --secondary-color: #4d7cc7;
    --dark-blue: #003A8C;
    --text-gray: #666;
    --bg-light: #f8f9fa;
}
```

## JavaScript архитектура

### Основной файл: `assets/js/script.js`
### Специализированные файлы:
- `assets/js/clients.js` - управление страницей клиентов

### Основные функции:

#### 1. Navbar scroll effect
```javascript
window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});
```

#### 2. Smooth scrolling
```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        // smooth scroll logic
    });
});
```

#### 3. Intersection Observer для анимаций
```javascript
const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
});
```

#### 4. Swiper инициализация
```javascript
const servicesSwiper = new Swiper('.services-swiper', {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        768: { slidesPerView: 2 },
        992: { slidesPerView: 3 }
    }
});
```

#### 5. ClientsManager класс (`assets/js/clients.js`)
```javascript
class ClientsManager {
    constructor() {
        this.clients = [];
        this.filteredClients = [];
        this.currentPage = 1;
        this.itemsPerPage = 20;
        this.selectedLetter = '';
    }
    
    async loadClients() {
        // Загрузка данных из assets/data/clients.json
        // Очистка и форматирование данных
    }
    
    filterByLetter(letter) {
        // Фильтрация клиентов по первой букве
    }
    
    renderClients() {
        // Отрисовка карточек клиентов с пагинацией
    }
}
```

## Структура данных

### Файл `assets/data/clients.json`:
```json
[
  {
    "name": "Название организации", 
    "inn": "1234567890"
  }
]
```

**Особенности обработки данных:**
- Автоматическая обрезка пробелов в названиях
- Преобразование ИНН в строковый формат
- Валидация и обработка ошибок загрузки

## Файловая структура проекта

### Текущее состояние:
```
/
├── index.html              # Главная страница
├── pages/                  # Страницы сайта
│   ├── clients.html        # Страница клиентов
│   ├── contacts.html       # Страница контактов
│   ├── intercity.html      # Междугородние перевозки
│   ├── truck.html         # Грузовые перевозки фура
│   ├── long-trailer.html  # Длинномеры шаланда
│   └── partial.html       # Догруз попутно
├── assets/                 # Ресурсы
│   ├── css/
│   │   └── styles.css     # Основные стили
│   ├── js/
│   │   ├── script.js      # Основные скрипты
│   │   └── clients.js     # Управление клиентами
│   ├── images/
│   │   └── color_big.png  # Логотип
│   └── data/
│       └── clients.json   # База клиентов (880 записей)
├── docs/                   # Документация
├── convert_excel.py        # Скрипт конвертации Excel в JSON
├── CLAUDE.md              # Инструкции для AI
├── .mcp.json              # MCP конфигурация
└── .taskmaster/           # Task Master файлы
```

### Целевая структура:
```
/
├── docs/                  # Документация
├── templates/             # Шаблоны
├── pages/                 # Страницы
├── assets/               # Ресурсы
│   ├── css/
│   ├── js/
│   └── images/
├── index.html
└── конфигурационные файлы
```

## Bootstrap компоненты в использовании

### Navbar:
- `navbar` - основа навигации
- `navbar-expand-lg` - адаптивное раскрытие
- `navbar-toggler` - кнопка бургер-меню
- `collapse navbar-collapse` - скрываемое содержимое

### Buttons:
- `btn btn-outline-primary` - основные кнопки
- `btn btn-primary` - акцентные кнопки

### Grid:
- `container` - основной контейнер
- `row` и `col-*` - сетка (используется минимально)

### Utilities:
- `d-flex`, `align-items-center` - флексбокс
- `ms-auto`, `me-3` - margin утилиты
- `text-*` классы для выравнивания текста

## Performance оптимизации

### Текущие:
- CSS и JS минификация через CDN (Bootstrap)
- Оптимизация изображений (рекомендуется WebP)
- Ленивая загрузка изображений (планируется)

### Рекомендуемые улучшения:
- Critical CSS inline
- Preload ключевых ресурсов
- Service Worker для кэширования
- Image optimization pipeline

## MCP Серверы интеграция

### Task Master AI:
```json
"task-master-ai": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "--package=task-master-ai", "task-master-ai"],
    "env": { "OPENAI_API_KEY": "..." }
}
```

### Context7:
```json
"context7": {
    "type": "stdio", 
    "command": "npx",
    "args": ["@upstash/context7@latest"]
}
```

### Playwright:
```json
"playwright": {
    "type": "stdio",
    "command": "node",
    "args": ["./playwright-mcp/cli.js"]
}
```

## Debugging & Development

### Chrome DevTools:
- Используйте Lighthouse для аудита производительности
- Network tab для анализа загрузки ресурсов
- Console для JavaScript ошибок

### Playwright для тестирования:
- Автоматические скриншоты после изменений
- Тестирование адаптивности
- Проверка функциональности кнопок и ссылок

## Known Issues & Solutions

### Проблема: Логотип слишком большой
**Решение:** Использовать `height` вместо `width` для пропорционального масштабирования

### Проблема: Текст обрывается
**Решение:** Убрать `white-space: nowrap` и `text-overflow: ellipsis`

### Проблема: Меню не адаптивное  
**Решение:** Bootstrap navbar с правильными классами `navbar-expand-lg`

## TODO для будущих версий

- [ ] Добавить CSS переменные для цветов
- [ ] Создать компонентную систему
- [ ] Настроить build процесс (Webpack/Vite)
- [ ] Добавить TypeScript
- [ ] Интеграция с CMS (если понадобится)
- [ ] PWA функциональность
- [ ] Dark mode support

## Последнее обновление
Дата: 2025-09-10  
Версия: 1.1
Автор: Claude Code Assistant

### Обновления в версии 1.1:
- Добавлена информация о Swiper.js 11
- Добавлена инициализация карусели услуг
- Обновлена структура JavaScript с новыми функциями