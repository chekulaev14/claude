// Universal form handler for all callback forms
document.addEventListener('DOMContentLoaded', function() {

    // Phone number formatting function
    function formatPhoneNumber(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

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
            // Prepare data
            const data = {
                phone: phone,
                formType: formType
            };

            // Add additional fields for detailed form
            if (formType === 'detailed') {
                const fromCityInput = form.querySelector('#departure');
                const toCityInput = form.querySelector('#destination');
                const dateInput = form.querySelector('#date');

                if (fromCityInput) data.fromCity = fromCityInput.value;
                if (toCityInput) data.toCity = toCityInput.value;
                if (dateInput) data.departureDate = dateInput.value;
            }

            // Add Web3Forms access key
            data.access_key = '2d53317e-70c5-4989-9fd8-c9beb10a4491';

            // Send to Web3Forms
            const response = await fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                // Success
                alert('✅ Заявка успешно отправлена!\n\nМы свяжемся с вами в течение 5 минут.');
                form.reset();

                // Reset phone input to +7
                if (phoneInput) {
                    phoneInput.value = '+7 ';
                }
            } else {
                // Error from server
                throw new Error(result.error || 'Ошибка отправки');
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

    // Handle all .callback-form class (fallback for any callback forms)
    document.querySelectorAll('.callback-form').forEach(form => {
        // Skip if already handled by ID
        if (form.id && (
            form.id === 'contactForm' ||
            form.id === 'callbackForm' ||
            form.id === 'portfolioCallbackForm' ||
            form.id === 'faqCallbackForm' ||
            form.id === 'mapCallbackForm'
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
