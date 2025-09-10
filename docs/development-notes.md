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

## Файловая структура проекта

### Текущее состояние:
```
/
├── index.html              # Главная страница
├── styles.css              # Основные стили  
├── script.js              # Основные скрипты
├── color_big.png          # Логотип
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
Дата: 2024-01-10  
Версия: 1.0
Автор: Claude Code Assistant