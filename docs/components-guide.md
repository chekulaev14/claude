# Руководство по компонентам сайта

## Header (Шапка сайта)

### Расположение: `templates/header.html`
### Структура:
```html
<header class="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top">
  - Логотип (слева)
  - Навигационное меню (по центру)
  - Контактная информация (справа)
</header>
```

### Bootstrap классы:
- `navbar` - основа навигации
- `navbar-expand-lg` - адаптивность
- `fixed-top` - фиксированный верх
- `shadow-sm` - тень

### Компоненты header:
1. **Логотип**
   - Файл: `assets/images/color_big.png`
   - Размер: height: 45px (35px при скролле)
   - Ссылка на главную страницу

2. **Навигационное меню**
   - Главная
   - Услуги (dropdown с 4 пунктами)
   - Адаптивное бургер-меню для мобильных

3. **Контактная информация**
   - Телефон: 8-987-416-51-87 (кликабельный)
   - Время работы: 9:00-18:00 МСК

## Footer (Подвал сайта)

### Расположение: `templates/footer.html`
### Структура:
- Информация о компании
- Список услуг
- Контактные данные
- Copyright

## Service Cards (Карточки услуг)

### CSS класс: `.service-card`
### Структура каждой карточки:
1. **Иконка** - эмодзи символ
2. **Заголовок** - название услуги (заглавными буквами)
3. **Описание** - краткое описание услуги
4. **Список преимуществ** - маркированный список с ✓
5. **Кнопка "Перейти"** - `btn btn-outline-primary mt-3`

### Текущие карточки:
1. **ГРУЗОПЕРЕВОЗКИ МЕЖГОРОД** 🚛
   - Якорь: `#intercity`
   - Преимущества: загрузка, контроль, страхование

2. **ГРУЗОПЕРЕВОЗКИ ФУРА** 🏗️
   - Якорь: `#truck`
   - Преимущества: тентованные, открытые, рефрижераторы

3. **ГРУЗОПЕРЕВОЗКИ ДЛИННОМЕР ШАЛАНДА** 📏
   - Якорь: `#long-trailer`
   - Преимущества: до 16м, разрешения, сопровождение

4. **ГРУЗОПЕРЕВОЗКИ ДОГРУЗ ПОПУТНО** 📦
   - Якорь: `#partial`
   - Преимущества: стоимость, рейсы, упаковка

## Client Cards (Карточки клиентов)

### CSS класс: `.card` (Bootstrap)
### Расположение: `pages/clients.html`
### Управление: `assets/js/clients.js` (класс `ClientsManager`)

### Структура карточки клиента:
1. **Номер клиента** - badge с порядковым номером
2. **ИНН** - в правом углу мелким текстом  
3. **Название организации** - основной заголовок
4. **Дублированный ИНН** - в нижней части с иконкой

```html
<div class="card h-100 shadow-sm">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-start mb-2">
      <span class="badge bg-secondary">#1</span>
      <small class="text-muted">1234567890</small>
    </div>
    <h6 class="card-title">Название организации</h6>
    <div class="mt-auto pt-2">
      <small class="text-muted">
        <i class="bi bi-building"></i>
        ИНН: 1234567890
      </small>
    </div>
  </div>
</div>
```

### Особенности:
- Адаптивная сетка: col-md-6 col-lg-4 (2 колонки на планшете, 3 на десктопе)
- Одинаковая высота карточек: `.h-100`
- Тень: `.shadow-sm`
- 20 карточек на страницу

## Alphabet Navigation (Алфавитная навигация)

### CSS класс: `.alphabet-nav`
### Структура:
- Кнопка "Все" - показать всех клиентов
- 33 кнопки русских букв (А-Я)
- Bootstrap стили: `btn btn-outline-primary btn-sm`
- Активное состояние: `.active`

```html
<div class="alphabet-nav mb-4">
  <div class="d-flex flex-wrap justify-content-center gap-1" id="alphabetNav">
    <button class="btn btn-outline-secondary btn-sm">Все</button>
    <button class="btn btn-outline-primary btn-sm">А</button>
    <!-- ... остальные буквы ... -->
  </div>
</div>
```

### Функциональность:
- Фильтрация клиентов по первой букве названия
- Обновление счетчика показанных клиентов
- Сброс на первую страницу при фильтрации
- Визуальная индикация активной буквы

## Statistics Panel (Панель статистики)

### CSS класс: `.alert-info`
### Отображаемая информация:
1. **Всего клиентов** - общее количество в базе (880)
2. **Показано** - количество после фильтрации  
3. **Страница** - текущая страница из общего количества

```html
<div class="alert alert-info">
  <div class="row text-center">
    <div class="col-md-4">
      <strong>Всего клиентов:</strong> <span id="totalClients">880</span>
    </div>
    <div class="col-md-4">
      <strong>Показано:</strong> <span id="shownClients">880</span>
    </div>
    <div class="col-md-4">
      <strong>Страница:</strong> <span id="currentPage">1</span> из <span id="totalPages">44</span>
    </div>
  </div>
</div>
```

## Pagination (Пагинация)

### CSS класс: `.pagination` (Bootstrap)
### Функциональность:
- Кнопки "Предыдущая" и "Следующая"
- Номера страниц (показывается 5 страниц: текущая ±2)
- Автоматическая прокрутка наверх при переходе
- Адаптация к количеству результатов фильтрации

```html
<nav aria-label="Навигация по страницам">
  <ul class="pagination justify-content-center" id="pagination">
    <li class="page-item"><a class="page-link" href="#" data-page="1">Предыдущая</a></li>
    <li class="page-item active"><a class="page-link" href="#" data-page="1">1</a></li>
    <li class="page-item"><a class="page-link" href="#" data-page="2">2</a></li>
    <li class="page-item"><a class="page-link" href="#" data-page="2">Следующая</a></li>
  </ul>
</nav>
```

## Кнопки

### Основные стили:
- `btn btn-outline-primary` - основные кнопки действий
- `btn-primary` - акцентные кнопки
- `mt-3` - отступ сверху

### Состояния:
- `:hover` - изменение цвета
- `:focus` - фокус для доступности

## Grid Layout (Сетка)

### Bootstrap Grid:
- `container` - основной контейнер (max-width: 1400px)
- `services-grid` - CSS Grid для карточек услуг
- Адаптивность: 4 колонки → 2 колонки → 1 колонка

## Цветовая схема

### Основные цвета:
- Синий корпоративный: `#2c5aa0`
- Светло-синий: `#4d7cc7`
- Темно-синий: `#003A8C`
- Серый текст: `#666`
- Фон: `#f8f9fa`

## Шрифты

### Основной шрифт: Inter
- Подключение: Google Fonts
- Использование: все текстовые элементы
- Веса: 300, 400, 500, 600, 700

## Адаптивность

### Breakpoints (Bootstrap):
- xs: < 576px (мобильные)
- sm: ≥ 576px (мобильные горизонтально)
- md: ≥ 768px (планшеты)
- lg: ≥ 992px (десктопы)
- xl: ≥ 1200px (большие десктопы)

### Адаптивные изменения:
- Header: бургер-меню на мобильных
- Services grid: 4→2→1 колонки
- Отступы и размеры шрифтов уменьшаются

## JavaScript компоненты

### Скрипты в `assets/js/script.js`:
1. **Navbar scroll effect** - уменьшение header при скролле
2. **Smooth scrolling** - плавный скролл по якорям
3. **Intersection Observer** - анимации появления элементов

### Скрипты в `assets/js/clients.js`:
1. **ClientsManager** - основной класс управления клиентами
2. **Data loading** - асинхронная загрузка из JSON
3. **Alphabet filtering** - фильтрация по буквам алфавита
4. **Pagination** - разбиение на страницы
5. **Error handling** - обработка ошибок загрузки данных

## Последнее обновление
Дата: 2024-01-10
Версия: 1.0