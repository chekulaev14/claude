// Bootstrap navbar scroll effect
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    
    // Scroll effect for navbar
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.service-card, .advantage-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Initialize Swiper carousel for services
    const servicesSwiper = new Swiper('.services-swiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
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
        },
        autoplay: {
            delay: 15000,
            disableOnInteraction: false,
        },
    });

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = {
                fromCity: document.getElementById('fromCity').value,
                toCity: document.getElementById('toCity').value,
                departureDate: document.getElementById('departureDate').value,
                contactPhone: document.getElementById('contactPhone').value
            };

            // Simple validation
            if (!formData.fromCity || !formData.toCity || !formData.departureDate || !formData.contactPhone) {
                alert('Пожалуйста, заполните все поля');
                return;
            }

            // Show loading state
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = 'Отправляется...';
            submitBtn.disabled = true;

            // Simulate form submission
            setTimeout(() => {
                alert(`Заявка отправлена!

Детали:
• Откуда: ${formData.fromCity}
• Куда: ${formData.toCity}
• Дата: ${formData.departureDate}
• Телефон: ${formData.contactPhone}

Мы свяжемся с вами в течение 15 минут!`);

                // Reset form
                contactForm.reset();

                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });

        // Phone number formatting
        const phoneInput = document.getElementById('contactPhone');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
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

        // Date input placeholder management with aggressive autofill prevention
        const dateInput = document.getElementById('departureDate');
        const datePlaceholder = document.getElementById('datePlaceholder');
        if (dateInput && datePlaceholder) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;

            // Clear any autofilled values
            function clearAutofill() {
                if (dateInput.value) {
                    dateInput.value = '';
                }
            }

            // Hide placeholder when input has value or is focused
            function togglePlaceholder() {
                if (dateInput.value || document.activeElement === dateInput) {
                    datePlaceholder.classList.add('hidden');
                } else {
                    datePlaceholder.classList.remove('hidden');
                }
            }

            // More aggressive placeholder management
            function forceTogglePlaceholder() {
                clearAutofill();
                togglePlaceholder();
            }

            // Event listeners
            dateInput.addEventListener('focus', togglePlaceholder);
            dateInput.addEventListener('blur', togglePlaceholder);
            dateInput.addEventListener('input', togglePlaceholder);
            dateInput.addEventListener('change', togglePlaceholder);

            // Anti-autofill measures
            dateInput.addEventListener('animationstart', forceTogglePlaceholder);

            // Initial checks with delays to catch browser autofill
            forceTogglePlaceholder();
            setTimeout(forceTogglePlaceholder, 100);
            setTimeout(forceTogglePlaceholder, 500);
            setTimeout(forceTogglePlaceholder, 1000);

            // Periodic check to ensure placeholder visibility is correct
            setInterval(() => {
                if (!document.activeElement || document.activeElement !== dateInput) {
                    clearAutofill();
                    togglePlaceholder();
                }
            }, 2000);
        }
    }
});