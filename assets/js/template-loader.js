// Template Loader - загружает header и footer на все страницы
class TemplateLoader {
    constructor() {
        this.basePath = this.getBasePath();
        this.init();
    }

    // Определяем базовый путь в зависимости от текущей страницы
    getBasePath() {
        const path = window.location.pathname;
        if (path.includes('/pages/')) {
            return '../'; // Для страниц в папке pages
        }
        return './'; // Для главной страницы
    }

    async init() {
        await this.loadHeader();
        await this.loadFooter();
        this.fixPaths();
        this.setActiveMenuItem();
        this.initializeBootstrapComponents();
    }

    async loadHeader() {
        try {
            const response = await fetch(`${this.basePath}templates/header.html`);
            const html = await response.text();
            const headerPlaceholder = document.getElementById('header-placeholder');
            if (headerPlaceholder) {
                headerPlaceholder.innerHTML = html;
            }
        } catch (error) {
            console.error('Error loading header:', error);
        }
    }

    async loadFooter() {
        try {
            const response = await fetch(`${this.basePath}templates/footer.html`);
            const html = await response.text();
            const footerPlaceholder = document.getElementById('footer-placeholder');
            if (footerPlaceholder) {
                footerPlaceholder.innerHTML = html;
            }
        } catch (error) {
            console.error('Error loading footer:', error);
        }
    }

    // Исправляем пути в загруженном header
    fixPaths() {
        const header = document.querySelector('header');
        if (!header) return;

        // Исправляем пути для страниц в папке pages
        if (this.basePath === '../') {
            // Логотип - ведет на главную страницу
            const logo = header.querySelector('.navbar-brand');
            if (logo) logo.href = '../';

            const logoImg = header.querySelector('.navbar-brand img');
            if (logoImg) logoImg.src = '../assets/images/color_big.png';

            // Ссылки в dropdown остаются как есть (относительные пути в папке pages)
            // Основные ссылки меню остаются как есть (относительные пути в папке pages)
        } else {
            // Для главной страницы
            const logo = header.querySelector('.navbar-brand');
            if (logo) logo.href = '/';

            const logoImg = header.querySelector('.navbar-brand img');
            if (logoImg) logoImg.src = 'assets/images/color_big.png';

            // Добавляем pages/ к ссылкам для главной страницы
            const allLinks = header.querySelectorAll('.dropdown-item, .nav-link:not(.dropdown-toggle)');
            allLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href && href.endsWith('.html') && !href.includes('pages/')) {
                    link.href = 'pages/' + href;
                }
            });
        }
    }

    // Устанавливаем активный пункт меню
    setActiveMenuItem() {
        const currentPath = window.location.pathname;
        const menuLinks = document.querySelectorAll('.nav-link');
        
        menuLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href.replace('../', '').replace('./', ''))) {
                link.classList.add('active');
            }
        });
    }

    // Инициализируем Bootstrap компоненты после загрузки header
    initializeBootstrapComponents() {
        // Ждем небольшое время чтобы убедиться, что header полностью загружен
        setTimeout(() => {
            // Проверяем что Bootstrap загружен
            if (typeof bootstrap !== 'undefined') {
                console.log('Bootstrap ready, initializing dropdowns...');
                
                // Найдем все dropdown элементы
                const dropdownElementList = document.querySelectorAll('.dropdown-toggle');
                console.log('Found dropdowns:', dropdownElementList.length);
                
                if (dropdownElementList.length > 0) {
                    // Инициализируем каждый dropdown
                    dropdownElementList.forEach(dropdownToggleEl => {
                        try {
                            // Убеждаемся что не инициализируем дважды
                            if (!bootstrap.Dropdown.getInstance(dropdownToggleEl)) {
                                new bootstrap.Dropdown(dropdownToggleEl);
                                console.log('Initialized dropdown:', dropdownToggleEl.id);
                            }
                        } catch (error) {
                            console.error('Failed to initialize dropdown:', error);
                        }
                    });
                } else {
                    console.warn('No dropdown elements found after header load');
                }
                
                // Инициализируем navbar collapse для мобильных
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarToggler && navbarCollapse) {
                    try {
                        if (!bootstrap.Collapse.getInstance(navbarCollapse)) {
                            new bootstrap.Collapse(navbarCollapse, { toggle: false });
                            console.log('Initialized navbar collapse');
                        }
                    } catch (error) {
                        console.error('Failed to initialize navbar collapse:', error);
                    }
                }
            } else {
                console.error('Bootstrap not available');
            }
        }, 200); // Увеличиваем задержку до 200ms
    }
}

// Инициализируем загрузчик шаблонов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new TemplateLoader();
});