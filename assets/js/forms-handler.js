// Universal form handler for all callback forms
document.addEventListener('DOMContentLoaded', function() {

    // Phone number formatting function
    function formatPhoneNumber(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            // Ограничиваем максимум 11 цифр (7 + 10 цифр номера)
            if (value.length > 11) {
                value = value.slice(0, 11);
            }

            if (value.length > 0) {
                if (value[0] === '8') {
                    value = '7' + value.slice(1);
                }

                let formatted = '+7';
                if (value.length > 1) {
                    formatted += ' (' + value.slice(1, 4);
                    if (value.length >= 4) {
                        formatted += ') ' + value.slice(4, 7);
                        if (value.length >= 7) {
                            formatted += '-' + value.slice(7, 9);
                            if (value.length >= 9) {
                                formatted += '-' + value.slice(9, 11);
                            }
                        }
                    }
                }

                e.target.value = formatted;
            }
        });
    }

    // Send to Telegram (резервный канал + гарантированная доставка)
    function sendToTelegram(data) {
        const botToken = '7779064115:AAHlm2qSOU1v2YIohlcMPWger1RZjkIRJ5I';
        const chatId = '-5037073171'; // Группа Telegram (со знаком минус для групп)

        // Формируем сообщение
        let message = `🆕 НОВАЯ ЗАЯВКА с сайта\n\n`;
        message += `📱 Телефон: ${data.phone}\n`;
        if (data.fromCity) message += `📍 Откуда: ${data.fromCity}\n`;
        if (data.toCity) message += `📍 Куда: ${data.toCity}\n`;
        if (data.departureDate) message += `📅 Дата: ${data.departureDate}\n`;

        // Добавляем UTM метки если есть
        if (data.utmKeyword) {
            message += `\n🔑 Ключевое слово: ${data.utmKeyword}\n`;
        }
        if (data.utmSource) {
            message += `📊 Источник: ${data.utmSource}\n`;
        }
        if (data.utmCampaign) {
            message += `📢 Кампания: ${data.utmCampaign}\n`;
        }

        message += `\n🔖 Тип формы: ${data.formType}`;

        const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
        const params = new URLSearchParams({
            chat_id: chatId,
            text: message,
            parse_mode: 'HTML'
        });

        // Используем sendBeacon для гарантированной отправки даже при закрытии страницы
        if (navigator.sendBeacon) {
            navigator.sendBeacon(url, params);
        } else {
            // Fallback для старых браузеров
            fetch(url, {
                method: 'POST',
                body: params,
                keepalive: true
            }).catch(err => console.log('Telegram send error:', err));
        }
    }

    // Handle form submission
    async function handleFormSubmit(e, formType) {
        e.preventDefault();

        const form = e.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;

        // Get form data
        const phoneInput = form.querySelector('input[name="phone"]');
        const phone = phoneInput ? phoneInput.value : '';

        // Validation
        if (!phone || phone.length < 11) {
            alert('Пожалуйста, введите корректный номер телефона');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Отправка...';

        try {
            // Читаем UTM метки из URL
            const urlParams = new URLSearchParams(window.location.search);

            // Prepare data
            const data = {
                phone: phone,
                formType: formType
            };

            // Добавляем UTM параметры если есть
            const utmTerm = urlParams.get('utm_term');
            const utmSource = urlParams.get('utm_source');
            const utmCampaign = urlParams.get('utm_campaign');

            if (utmTerm) data.utmKeyword = decodeURIComponent(utmTerm);
            if (utmSource) data.utmSource = utmSource;
            if (utmCampaign) data.utmCampaign = utmCampaign;

            // Add additional fields for detailed form
            if (formType === 'detailed') {
                const fromCityInput = form.querySelector('#departure');
                const toCityInput = form.querySelector('#destination');
                const dateInput = form.querySelector('#date');

                if (fromCityInput) data.fromCity = fromCityInput.value;
                if (toCityInput) data.toCity = toCityInput.value;
                if (dateInput) data.departureDate = dateInput.value;
            }

            // Отправляем в Telegram (основной канал)
            sendToTelegram(data);

            // Пробуем отправить в Web3Forms (резервный канал, не критично если упадет)
            try {
                data.access_key = '2d53317e-70c5-4989-9fd8-c9beb10a4491';
                await fetch('https://api.web3forms.com/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data),
                    keepalive: true
                }).catch(() => {
                    // Игнорируем ошибки Web3Forms (может быть заблокирован)
                    console.log('Web3Forms недоступен, заявка отправлена в Telegram');
                });
            } catch (e) {
                // Web3Forms не критичен, продолжаем
            }

            // Формируем URL для thank-you страницы
            const thankYouParams = new URLSearchParams();
            thankYouParams.set('phone', phone);

            // Добавляем дополнительные параметры для детальной формы
            if (data.fromCity) {
                thankYouParams.set('from', data.fromCity);
            }
            if (data.toCity) {
                thankYouParams.set('to', data.toCity);
            }
            if (data.departureDate) {
                thankYouParams.set('date', data.departureDate);
            }

            // Добавляем UTM метки
            if (data.utmKeyword) {
                thankYouParams.set('utm_term', data.utmKeyword);
            }

            // Открываем thank-you страницу в новой вкладке
            window.open(`/thank-you.html?${thankYouParams.toString()}`, '_blank');

            // Показываем уведомление на текущей странице
            alert('✅ Заявка успешно отправлена!\n\nСтраница с подробностями открыта в новой вкладке.');

            // Очищаем форму
            form.reset();

            // Reset phone input to +7
            if (phoneInput) {
                phoneInput.value = '+7 ';
            }

            // Close modal if form is inside a modal
            const modal = form.closest('.modal');
            if (modal) {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            }

        } catch (error) {
            console.error('Form submission error:', error);
            alert('❌ Произошла ошибка при отправке заявки.\n\nПожалуйста, позвоните нам напрямую:\n8-800-707-29-36');
        } finally {
            // Restore button state
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    }

    // Initialize all forms

    // 1. Main contact form (detailed)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const phoneInput = contactForm.querySelector('#phone');
        if (phoneInput) formatPhoneNumber(phoneInput);

        contactForm.addEventListener('submit', (e) => handleFormSubmit(e, 'detailed'));
    }

    // 2. Callback form on index page
    const callbackForm = document.getElementById('callbackForm');
    if (callbackForm) {
        const phoneInput = callbackForm.querySelector('#callbackPhone');
        if (phoneInput) formatPhoneNumber(phoneInput);

        callbackForm.addEventListener('submit', (e) => handleFormSubmit(e, 'callback-index'));
    }

    // 3. Portfolio page callback
    const portfolioCallbackForm = document.getElementById('portfolioCallbackForm');
    if (portfolioCallbackForm) {
        const phoneInput = portfolioCallbackForm.querySelector('#portfolioPhone');
        if (phoneInput) formatPhoneNumber(phoneInput);

        portfolioCallbackForm.addEventListener('submit', (e) => handleFormSubmit(e, 'callback-portfolio'));
    }

    // 4. FAQ page callback
    const faqCallbackForm = document.getElementById('faqCallbackForm');
    if (faqCallbackForm) {
        const phoneInput = faqCallbackForm.querySelector('#faqPhone');
        if (phoneInput) formatPhoneNumber(phoneInput);

        faqCallbackForm.addEventListener('submit', (e) => handleFormSubmit(e, 'callback-faq'));
    }

    // 5. Clients page callback (callbackForm reused ID)
    // Note: This conflicts with index page, handled separately below

    // 6. Clients map page callback
    const mapCallbackForm = document.getElementById('mapCallbackForm');
    if (mapCallbackForm) {
        const phoneInput = mapCallbackForm.querySelector('#mapPhone');
        if (phoneInput) formatPhoneNumber(phoneInput);

        mapCallbackForm.addEventListener('submit', (e) => handleFormSubmit(e, 'callback-clients-map'));
    }

    // 7. Mobile callback modal (инициализируется позже, после загрузки footer)
    function initMobileCallbackForm() {
        const mobileCallbackForm = document.getElementById('mobileCallbackForm');
        if (mobileCallbackForm && !mobileCallbackForm.dataset.initialized) {
            const phoneInput = mobileCallbackForm.querySelector('#mobileCallbackPhone');
            if (phoneInput) formatPhoneNumber(phoneInput);

            mobileCallbackForm.addEventListener('submit', (e) => handleFormSubmit(e, 'callback-mobile'));
            mobileCallbackForm.dataset.initialized = 'true';
            console.log('✅ Mobile callback form initialized');
        }
    }

    // Пробуем инициализировать сразу
    initMobileCallbackForm();

    // Инициализируем при открытии модального окна (на случай если footer еще не загружен)
    document.addEventListener('shown.bs.modal', function(e) {
        if (e.target.id === 'mobileCallbackModal') {
            initMobileCallbackForm();
        }
    });

    // Инициализируем после небольшой задержки (на случай если footer загружается)
    setTimeout(() => {
        initMobileCallbackForm();
    }, 500);

    // Handle all .callback-form class (fallback for any callback forms)
    document.querySelectorAll('.callback-form').forEach(form => {
        // Skip if already handled by ID
        if (form.id && (
            form.id === 'contactForm' ||
            form.id === 'callbackForm' ||
            form.id === 'portfolioCallbackForm' ||
            form.id === 'faqCallbackForm' ||
            form.id === 'mapCallbackForm' ||
            form.id === 'mobileCallbackForm'
        )) {
            return;
        }

        const phoneInput = form.querySelector('input[name="phone"]');
        if (phoneInput) formatPhoneNumber(phoneInput);

        form.addEventListener('submit', (e) => {
            const pageName = window.location.pathname.split('/').pop().replace('.html', '') || 'home';
            handleFormSubmit(e, `callback-${pageName}`);
        });
    });

    console.log('✅ Forms handler initialized');
});
