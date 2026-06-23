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
        this.initHeaderScroll();
        this.initExitPopup();
    }

    // Exit-intent попап «Быстро рассчитаем перевозку» — на всех страницах, 1 раз за сессию
    initExitPopup() {
        const SHOWN_KEY = 'dn_exit_popup_shown';
        const ENDPOINT = 'https://agentiks.ru/dinamika/api/lead';

        // CSS (инжектим один раз, не зависим от styles.css)
        if (!document.getElementById('dn-popup-style')) {
            const st = document.createElement('style');
            st.id = 'dn-popup-style';
            st.textContent = `
.dn-popup-overlay{position:fixed;inset:0;background:rgba(17,24,39,.55);display:none;align-items:center;justify-content:center;z-index:3000;opacity:0;transition:opacity .25s ease}
.dn-popup-overlay.show{display:flex;opacity:1}
.dn-popup{background:#fff;width:100%;max-width:400px;margin:16px;border-radius:16px;padding:28px 26px 24px;position:relative;box-shadow:0 20px 60px rgba(0,0,0,.25);transform:translateY(12px) scale(.98);transition:transform .25s ease;font-family:'IBM Plex Sans',sans-serif}
.dn-popup-overlay.show .dn-popup{transform:none}
.dn-popup__close{position:absolute;top:12px;right:14px;border:none;background:none;font-size:26px;line-height:1;color:#9ca3af;cursor:pointer}
.dn-popup__close:hover{color:#374151}
.dn-popup__icon{font-size:34px}
.dn-popup__title{font-size:1.28rem;font-weight:700;margin:8px 0 6px;color:#1f2937}
.dn-popup__sub{color:#6b7280;font-size:.95rem;margin-bottom:18px}
.dn-popup__form input{height:52px;width:100%;font-size:1.05rem;border-radius:10px;border:1.5px solid #d1d5db;text-align:center;letter-spacing:.5px}
.dn-popup__form input:focus{outline:none;border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,.15)}
.dn-popup__btn{height:52px;border-radius:10px;font-weight:600;font-size:1.05rem;background:#2563eb;border:none;color:#fff;width:100%;margin-top:12px;cursor:pointer}
.dn-popup__btn:hover{background:#1d4ed8}
.dn-popup__btn:disabled{opacity:.6;cursor:default}
.dn-popup__note{font-size:.78rem;color:#9ca3af;text-align:center;margin-top:12px}
.dn-popup__ok{display:none;text-align:center;padding:14px 0}
.dn-popup__ok .big{font-size:40px}`;
            document.head.appendChild(st);
        }

        // DOM
        const overlay = document.createElement('div');
        overlay.className = 'dn-popup-overlay';
        overlay.innerHTML = `
<div class="dn-popup">
  <button class="dn-popup__close" aria-label="Закрыть">&times;</button>
  <div class="dn-popup__body">
    <div class="dn-popup__icon">🚚</div>
    <div class="dn-popup__title">Быстро рассчитаем перевозку, оставьте телефон!</div>
    <div class="dn-popup__sub">Перезвоним за 5 минут и назовём точную цену.</div>
    <form class="dn-popup__form">
      <input type="tel" inputmode="tel" placeholder="+7 (___) ___-__-__" required>
      <button type="submit" class="dn-popup__btn">Перезвоните мне</button>
      <div class="dn-popup__note">Нажимая кнопку, вы соглашаетесь с политикой конфиденциальности</div>
    </form>
  </div>
  <div class="dn-popup__ok">
    <div class="big">✅</div>
    <div class="dn-popup__title">Заявка принята!</div>
    <div class="dn-popup__sub">Скоро перезвоним. Спасибо!</div>
  </div>
</div>`;
        document.body.appendChild(overlay);

        const popup = overlay.querySelector('.dn-popup');
        const body = overlay.querySelector('.dn-popup__body');
        const okBox = overlay.querySelector('.dn-popup__ok');
        const form = overlay.querySelector('.dn-popup__form');
        const phone = overlay.querySelector('input');
        const btn = overlay.querySelector('.dn-popup__btn');

        // Маска телефона: всегда +7, ввод с 9
        phone.addEventListener('focus', () => { if (!phone.value) phone.value = '+7 '; });
        phone.addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '');
            if (v[0] === '8') v = '7' + v.slice(1);
            if (v[0] !== '7') v = '7' + v;
            v = v.slice(0, 11);
            let out = '+7';
            if (v.length > 1) out += ' (' + v.slice(1, 4);
            if (v.length >= 4) out += ') ' + v.slice(4, 7);
            if (v.length >= 7) out += '-' + v.slice(7, 9);
            if (v.length >= 9) out += '-' + v.slice(9, 11);
            e.target.value = out;
        });

        const show = (force) => {
            if (!force && sessionStorage.getItem(SHOWN_KEY)) return;
            overlay.classList.add('show');
            sessionStorage.setItem(SHOWN_KEY, '1');
        };
        const hide = () => overlay.classList.remove('show');

        overlay.querySelector('.dn-popup__close').addEventListener('click', hide);
        overlay.addEventListener('click', (e) => { if (e.target === overlay) hide(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hide(); });

        // Триггер: курсор ушёл вверх за окно (десктоп)
        document.addEventListener('mouseout', (e) => {
            if (!e.relatedTarget && e.clientY <= 0) show(false);
        });
        // Мобильный fallback: показать через 30 сек
        if (/Mobi|Android/i.test(navigator.userAgent)) {
            setTimeout(() => show(false), 30000);
        }

        // Отправка на наш сервис (Telegram + почта + лог)
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const digits = phone.value.replace(/\D/g, '');
            if (digits.length < 11) { phone.focus(); phone.style.borderColor = '#dc2626'; return; }

            const urlParams = new URLSearchParams(window.location.search);
            const data = {
                phone: phone.value,
                formType: 'exit-popup',
                page: window.location.href,
                utmKeyword: urlParams.get('utm_term') || undefined,
                utmSource: urlParams.get('utm_source') || undefined,
                utmCampaign: urlParams.get('utm_campaign') || undefined
            };

            // Автопереход на подробную форму — открываем СРАЗУ в жесте клика,
            // иначе браузер заблокирует новую вкладку (popup blocker после await).
            const tyParams = new URLSearchParams({ phone: phone.value });
            if (data.utmKeyword) tyParams.set('utm_term', data.utmKeyword);
            window.open('/thank-you.html?' + tyParams.toString(), '_blank');

            // Показываем «принято» и шлём заявку в фоне (телефон уже валиден)
            body.style.display = 'none';
            okBox.style.display = 'block';
            setTimeout(hide, 2500);

            fetch(ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
                keepalive: true
            }).then(r => r.json().catch(() => ({ ok: r.ok })))
              .then(res => { if (!res.ok) console.error('Exit-popup endpoint not ok'); })
              .catch(err => console.error('Exit-popup send error:', err));
        });
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

    // Header shrink on scroll
    initHeaderScroll() {
        setTimeout(() => {
            const header = document.querySelector('header.navbar');
            if (!header) return;

            const scrollThreshold = 50;

            const handleScroll = () => {
                if (window.scrollY > scrollThreshold) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            };

            window.addEventListener('scroll', handleScroll, { passive: true });
            handleScroll(); // Check initial state
        }, 100);
    }
}

// Инициализируем загрузчик шаблонов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new TemplateLoader();
});
