/**
 * Динамический движок шаблонов для сайта "Динамика"
 * Загружает шаблон и подставляет данные из JSON конфигурации
 */

class TemplateEngine {
    constructor() {
        this.templateCache = {};
        this.dataCache = {};
    }

    /**
     * Загружает HTML файл по URL
     */
    async loadTemplate(templatePath) {
        if (this.templateCache[templatePath]) {
            return this.templateCache[templatePath];
        }

        try {
            const response = await fetch(templatePath);
            if (!response.ok) {
                throw new Error(`Ошибка загрузки шаблона: ${response.status}`);
            }
            const html = await response.text();
            this.templateCache[templatePath] = html;
            return html;
        } catch (error) {
            console.error('Ошибка загрузки шаблона:', error);
            throw error;
        }
    }

    /**
     * Загружает JSON данные
     */
    async loadData(dataPath) {
        if (this.dataCache[dataPath]) {
            return this.dataCache[dataPath];
        }

        try {
            const response = await fetch(dataPath);
            if (!response.ok) {
                throw new Error(`Ошибка загрузки данных: ${response.status}`);
            }
            const data = await response.json();
            this.dataCache[dataPath] = data;
            return data;
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            throw error;
        }
    }

    /**
     * Заменяет переменные в шаблоне на реальные значения
     */
    processTemplate(template, data) {
        let result = template;

        // Замена простых переменных вида {{VARIABLE_NAME}}
        for (const [key, value] of Object.entries(data)) {
            if (typeof value === 'string') {
                const placeholder = `{{${key}}}`;
                const regex = new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
                result = result.replace(regex, value || '');
            }
        }

        // Обработка списков {{#ARRAY_NAME}}...{{/ARRAY_NAME}}
        result = this.processArrays(result, data);

        // Обработка специальных блоков
        result = this.processSpecialBlocks(result, data);

        return result;
    }

    /**
     * Обрабатывает массивы в шаблоне
     */
    processArrays(template, data) {
        let result = template;

        // Ищем блоки вида {{#ARRAY_NAME}}...{{/ARRAY_NAME}}
        const arrayRegex = /\{\{#(\w+)\}\}([\s\S]*?)\{\{\/\1\}\}/g;

        result = result.replace(arrayRegex, (match, arrayName, blockContent) => {
            const arrayData = data[arrayName];

            if (!Array.isArray(arrayData)) {
                return '';
            }

            return arrayData.map(item => {
                let itemHtml = blockContent;

                if (typeof item === 'string') {
                    // Простая строка
                    itemHtml = itemHtml.replace(/\{\{item\}\}/g, item);
                } else if (typeof item === 'object') {
                    // Объект - заменяем все его свойства
                    for (const [prop, val] of Object.entries(item)) {
                        const regex = new RegExp(`\\{\\{${prop}\\}\\}`, 'g');
                        itemHtml = itemHtml.replace(regex, val || '');
                    }
                }

                return itemHtml;
            }).join('');
        });

        return result;
    }

    /**
     * Обрабатывает специальные блоки (например, SEO текст)
     */
    processSpecialBlocks(template, data) {
        let result = template;

        // Обработка SEO_TEXT массива в виде параграфов
        if (data.SEO_TEXT && Array.isArray(data.SEO_TEXT)) {
            const seoHtml = data.SEO_TEXT.map(text => `<p>${text}</p>`).join('\n                    ');
            result = result.replace(/\{\{SEO_TEXT_PARAGRAPHS\}\}/g, seoHtml);
        }

        return result;
    }

    /**
     * Основная функция рендеринга страницы
     */
    async renderPage(config) {
        try {
            console.log('Загрузка страницы с конфигурацией:', config);

            // Загружаем шаблон и данные параллельно
            const [template, serviceData] = await Promise.all([
                this.loadTemplate(config.templatePath),
                this.loadData(config.dataPath)
            ]);

            // Получаем данные для конкретной услуги
            const pageData = serviceData[config.serviceKey];
            if (!pageData) {
                throw new Error(`Данные для услуги "${config.serviceKey}" не найдены`);
            }

            // Обрабатываем шаблон
            const processedHTML = this.processTemplate(template, pageData);

            // Вставляем результат в DOM
            const targetElement = document.querySelector(config.targetSelector || 'main');
            if (targetElement) {
                targetElement.innerHTML = processedHTML;
                console.log('Страница успешно отрендерена');
            } else {
                throw new Error(`Элемент "${config.targetSelector}" не найден`);
            }

            // Запускаем пост-обработку
            this.postProcess();

        } catch (error) {
            console.error('Ошибка рендеринга страницы:', error);
            this.showError(error.message);
        }
    }

    /**
     * Пост-обработка после рендеринга
     */
    postProcess() {
        // Инициализируем Bootstrap компоненты если они есть
        if (typeof bootstrap !== 'undefined') {
            // Переинициализация Bootstrap компонентов
            const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
        }

        // Подгружаем header/footer если нужно
        if (typeof loadTemplates === 'function') {
            loadTemplates();
        }
    }

    /**
     * Показ ошибки пользователю
     */
    showError(message) {
        const errorHTML = `
            <div class="container py-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="alert alert-danger" role="alert">
                            <h4 class="alert-heading">Ошибка загрузки</h4>
                            <p>${message}</p>
                            <hr>
                            <p class="mb-0">Пожалуйста, попробуйте перезагрузить страницу.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const mainElement = document.querySelector('main');
        if (mainElement) {
            mainElement.innerHTML = errorHTML;
        }
    }
}

// Создаем глобальный экземпляр
window.templateEngine = new TemplateEngine();

/**
 * Утилитарная функция для быстрого рендеринга страницы услуги
 */
window.renderServicePage = function(serviceKey) {
    const config = {
        templatePath: '../templates/content-page-template.html',
        dataPath: '../data/services.json',
        serviceKey: serviceKey,
        targetSelector: 'main'
    };

    return window.templateEngine.renderPage(config);
};