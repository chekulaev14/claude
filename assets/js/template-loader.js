// Template Loader - загружает header и footer на все страницы
class TemplateLoader {
    constructor() {
        this.init();
    }

    async init() {
        await this.loadHeader();
        await this.loadFooter();
        this.setActiveMenuItem();
        this.initializeBootstrapComponents();
    }

    async loadHeader() {
        try {
            const response = await fetch('/templates/header.html');
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
            const response = await fetch('/templates/footer.html');
            const html = await response.text();
            const footerPlaceholder = document.getElementById('footer-placeholder');
            if (footerPlaceholder) {
                footerPlaceholder.innerHTML = html;
            }
        } catch (error) {
            console.error('Error loading footer:', error);
        }
    }

    // Устанавливаем активный пункт меню
    setActiveMenuItem() {
        const currentPath = window.location.pathname;
        const menuLinks = document.querySelectorAll('.nav-link');

        menuLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href)) {
                link.classList.add('active');
            }
        });
    }

    // Инициализируем Bootstrap компоненты после загрузки header
    initializeBootstrapComponents() {
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined') {
                const dropdownElementList = document.querySelectorAll('.dropdown-toggle');

                if (dropdownElementList.length > 0) {
                    dropdownElementList.forEach(dropdownToggleEl => {
                        try {
                            if (!bootstrap.Dropdown.getInstance(dropdownToggleEl)) {
                                new bootstrap.Dropdown(dropdownToggleEl);
                            }
                        } catch (error) {
                            console.error('Failed to initialize dropdown:', error);
                        }
                    });
                }

                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarToggler && navbarCollapse) {
                    try {
                        if (!bootstrap.Collapse.getInstance(navbarCollapse)) {
                            new bootstrap.Collapse(navbarCollapse, { toggle: false });
                        }
                    } catch (error) {
                        console.error('Failed to initialize navbar collapse:', error);
                    }
                }
            } else {
                console.error('Bootstrap not available');
            }
        }, 200);
    }
}

// Инициализируем загрузчик шаблонов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new TemplateLoader();
});
