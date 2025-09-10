# Руководство по компонентам сайта

## Обновления
- **10.09.2025**: Добавлен компонент Pricing Cards для страницы цен (упрощен)
- **10.09.2025**: Добавлена карусель Swiper для карточек услуг
- **10.09.2025**: Добавлена Hero-карусель с автосменой слайдов
- **10.09.2025**: Переструктурированы Service Cards в двухколоночный формат
- **10.09.2025**: Упрощена страница цен - удалены кнопки и лишние блоки

## Hero Carousel (Главная карусель)

### Расположение: `index.html` (строки 57-115)
### Класс: `.hero-carousel`

### Структура карусели:
```html
<section class="hero-carousel">
  <div id="heroCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="15000">
    <div class="carousel-indicators">...</div>
    <div class="carousel-inner">
      <div class="carousel-item active">...</div>
      <div class="carousel-item">...</div>
      <div class="carousel-item">...</div>
    </div>
    <button class="carousel-control-prev">...</button>
    <button class="carousel-control-next">...</button>
  </div>
</section>
```

### Настройки карусели:
- **Автосмена слайдов**: каждые 15 секунд (`data-bs-interval="15000"`)
- **Количество слайдов**: 3 слайда
- **Навигация**: индикаторы-точки внизу и стрелки по бокам
- **Автозапуск**: включен (`data-bs-ride="carousel"`)

### Содержание слайдов:
1. **Слайд 1**: "Надежные грузовые перевозки по России" + кнопка "Посмотреть" → #services
2. **Слайд 2**: "Более 850 довольных клиентов" + кнопка "Посмотреть" → pages/clients.html
3. **Слайд 3**: "Быстрое оформление заказа" + кнопка "Посмотреть" → pages/contacts.html

### Стили:
- Полноэкранная высота с фоновым изображением/градиентом
- Центрированный контент с белым текстом
- Bootstrap Carousel компоненты
- Адаптивные заголовки и подзаголовки

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
   - ~~Время работы удалено из menu по запросу~~

## Footer (Подвал сайта)

### Расположение: `templates/footer.html`
### Структура:
- Информация о компании
- Список услуг
- Контактные данные
- Copyright

## Service Cards (Карточки услуг)

### CSS класс: `.service-card`
### Контейнер: `.services-swiper` (Swiper карусель)

### Структура карусели:
```html
<div class="swiper services-swiper">
  <div class="swiper-wrapper">
    <div class="swiper-slide">
      <div class="service-card">...</div>
    </div>
  </div>
  <div class="swiper-pagination"></div>
  <div class="swiper-button-prev"></div>
  <div class="swiper-button-next"></div>
</div>
```

### Настройки карусели:
- **Десктоп (≥992px)**: 3 карточки одновременно
- **Планшет (≥768px)**: 2 карточки одновременно  
- **Мобильные (<768px)**: 1 карточка
- **Автопрокрутка**: каждые 5 секунд
- **Зацикливание**: включено
- **Навигация**: стрелки и точки

### Структура каждой карточки:
1. **Иконка** - эмодзи символ
2. **Заголовок** - название услуги (заглавными буквами)
3. **Спецификации в двухколоночном формате** - характеристики услуги
   ```html
   <div class="service-specs">
     <div class="spec-row">
       <span class="spec-label">Тип кузова</span>
       <span class="spec-value">Открытый / Закрытый</span>
     </div>
     <div class="spec-row">
       <span class="spec-label">Длина кузова</span>
       <span class="spec-value">до 7 метров</span>
     </div>
     <div class="spec-row">
       <span class="spec-label">Грузоподъемность</span>
       <span class="spec-value">до 7 тонн</span>
     </div>
   </div>
   ```
4. **Кнопка "Перейти"** - `btn btn-outline-primary mt-3`

### Текущие карточки (5 штук):
1. **ГРУЗОПЕРЕВОЗКИ МЕЖГОРОД** 🚛
   - ID: `#intercity`
   - Тип кузова: Открытый / Закрытый
   - Длина: до 7 метров
   - Грузоподъемность: до 7 тонн

2. **ГРУЗОПЕРЕВОЗКИ ФУРА** 🏗️
   - ID: `#truck`
   - Тип кузова: Закрытый
   - Длина: до 16 метров
   - Грузоподъемность: до 24 тонн

3. **ГРУЗОПЕРЕВОЗКИ ДЛИННОМЕР ШАЛАНДА** 📏
   - ID: `#long-trailer`
   - Тип кузова: Открытый
   - Длина: до 16 метров
   - Грузоподъемность: до 24 тонн

4. **ГРУЗОПЕРЕВОЗКИ ДОГРУЗ ПОПУТНО** 📦
   - ID: `#partial`
   - Тип кузова: Открытый / Закрытый
   - Длина: до 16 метров
   - Грузоподъемность: до 5 тонн

5. **ГРУЗОПЕРЕВОЗКИ ДОГРУЗ ПОПУТНО** 📦 (дубль)
   - ID: `#partial-2`
   - Тип кузова: Открытый / Закрытый
   - Длина: до 16 метров
   - Грузоподъемность: до 5 тонн

### CSS стили карусели:
- `.services-swiper` - контейнер с отступами для навигации
- `.swiper-button-next/prev` - круглые кнопки навигации
- `.swiper-pagination-bullet` - точки навигации
- `.swiper-pagination-bullet-active` - активная точка (увеличенная)

### CSS стили спецификаций (новое):
```css
.service-specs {
  text-align: left;
  margin: 15px 0;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.spec-row:last-child {
  border-bottom: none;
}

.spec-label {
  font-weight: 500;
  color: #666;
  font-size: 14px;
}

.spec-value {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}
```

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
4. **Swiper initialization** - инициализация карусели услуг с настройками адаптивности

### Скрипты в `assets/js/clients.js`:
1. **ClientsManager** - основной класс управления клиентами
2. **Data loading** - асинхронная загрузка из JSON
3. **Alphabet filtering** - фильтрация по буквам алфавита
4. **Pagination** - разбиение на страницы
5. **Error handling** - обработка ошибок загрузки данных

## Pricing Cards (Карточки тарифов) - УПРОЩЕННАЯ ВЕРСИЯ

### CSS классы:
- `.pricing-section` - основная секция с градиентным фоном
- `.pricing-header` - заголовок секции
- `.pricing-cards` - контейнер для карточек (flex)
- `.pricing-card` - индивидуальная карточка тарифа
- ~~`.pricing-card.recommended` - удалена метка "Рекомендуем"~~

### Структура карточки (упрощенная):
```html
<div class="pricing-card">
  <div class="pricing-card-header">
    <h3 class="pricing-plan-name">Название тарифа</h3>
    <div class="pricing-price">
      <span class="price-amount">5000</span>
      <span class="price-currency">₽</span>
    </div>
    <div class="pricing-commission">+ X% от стоимости</div>
  </div>
  <ul class="pricing-features">
    <li>✓ Функция (простые галочки вместо Font Awesome)</li>
  </ul>
  <!-- CTA кнопки удалены -->
</div>
```

### Изменения в версии 10.09.2025:
- ❌ **Удалены CTA кнопки** из карточек по запросу
- ❌ **Удалена метка "Рекомендуем"** для тарифа с НДС
- ❌ **Удалены Font Awesome иконки** - заменены на простые галочки ✓
- ❌ **Удален блок "Как формируется цена"** с кнопкой расчета
- ✅ **Сокращены описания** каждого тарифа до 3 пунктов

### Особенности:
- Hover эффект: поднятие карточки и усиление тени
- ~~Градиентные кнопки удалены~~
- Полностью адаптивный дизайн
- Простые текстовые галочки без иконок

### Цветовая схема:
- Основной цвет: #2c5aa0 (синий)
- ~~Акцентный цвет для "рекомендуемого" удален~~
- Фон секции: градиент от #f5f7fa до #c3cfe2

## Statistics Section (Секция статистики)

### Расположение: `index.html` (строки 254-261)
### CSS класс: `.stats-section`

### Структура:
```html
<section class="stats-section py-5 bg-primary text-white">
  <div class="container text-center">
    <h2 class="mb-3">Более 850 клиентов за 7 лет работы</h2>
    <p class="lead mb-4">Выполнено более 3500 рейсов</p>
    <a href="pages/clients.html" class="btn btn-light btn-lg">Ознакомиться</a>
  </div>
</section>
```

### Особенности:
- Синий фон (`bg-primary`) с белым текстом
- Отступы сверху и снизу (`py-5`)
- Центрированный контент
- CTA кнопка ведет на страницу клиентов
- Отображает ключевую статистику компании

## Swiper.js Integration

### Подключение:
```html
<!-- Swiper CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
<!-- Swiper JS -->
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
```

### JavaScript инициализация:
```javascript
// В assets/js/script.js
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
        768: {
            slidesPerView: 2,
        },
        992: {
            slidesPerView: 3,
        }
    }
});
```

## Последнее обновление
Дата: 2025-09-10
Версия: 1.2