document.addEventListener('DOMContentLoaded', function() {

    // --- БЛОК 1: Эффект печатающегося текста (с исправлением курсора) ---
    if (document.getElementById('typed-text')) {
        new Typed('#typed-text', {
            strings: ['Современные IT-решения', 'Надежные веб-сервисы', 'Продукты для вашего бизнеса'],
            typeSpeed: 70,
            backSpeed: 40,
            backDelay: 1500,
            startDelay: 500,
            loop: true,
            smartBackspace: true,
            showCursor: true,
            cursorChar: '',
        });
    }

    // --- БЛОК 2: Слайдер преимуществ ---
    if (document.querySelector('.advantages-slider')) {
        new Swiper('.advantages-slider', {
            effect: 'coverflow',
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: 'auto',
            loop: true,
            autoplay: { delay: 6000, disableOnInteraction: false },
            coverflowEffect: { rotate: 20, stretch: 0, depth: 100, modifier: 1, slideShadows: true },
            navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
        });
    }

    // --- БЛОК 3: Логика для COOKIE баннера ---
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptButton = document.getElementById('accept-cookies');
    if (cookieBanner && acceptButton) {
        if (!localStorage.getItem('cookiesAccepted')) {
            cookieBanner.style.transform = 'translateY(0)';
        }
        acceptButton.addEventListener('click', function() {
            localStorage.setItem('cookiesAccepted', 'true');
            cookieBanner.style.transform = 'translateY(100%)';
        });
    }

    // --- БЛОК 4: Логика для КОНТАКТНОЙ ФОРМЫ (на странице /contacts) ---
    const contactFormPage = document.getElementById('contactForm');
    const successModalPage = document.getElementById('form-success-modal');
    const closeModalButtonPage = document.getElementById('formCloseModal');
    if (contactFormPage && successModalPage) {
        contactFormPage.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(contactFormPage);
            fetch(contactFormPage.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    successModalPage.style.display = 'flex';
                    contactFormPage.reset();
                } else {
                    alert('Произошла ошибка. Пожалуйста, проверьте введенные данные.');
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке формы контактов:', error);
                alert('Произошла непредвиденная ошибка. Пожалуйста, проверьте консоль.');
            });
        });
    }
    if (closeModalButtonPage) {
        closeModalButtonPage.addEventListener('click', () => { successModalPage.style.display = 'none'; });
    }
    if (successModalPage) {
        window.addEventListener('click', (event) => {
            if (event.target === successModalPage) {
                successModalPage.style.display = 'none';
            }
        });
    }

    // --- БЛОК 5: Интеграция Isotope для фильтра портфолио ---
    const grid = document.querySelector('.projects-grid');
    if (grid && typeof Isotope !== 'undefined') {
        const iso = new Isotope(grid, {
            itemSelector: '.project-card-link',
            layoutMode: 'fitRows'
        });
        const filterBar = document.querySelector('.filter-bar');
        if (filterBar) {
            filterBar.addEventListener('click', function(event) {
                if (!event.target.matches('button.filter-btn')) return;
                const filterValue = event.target.getAttribute('data-filter');
                iso.arrange({ filter: filterValue });
                filterBar.querySelector('.active').classList.remove('active');
                event.target.classList.add('active');
            });
        }
    }

    // --- БЛОК 6: Инициализация Fancybox ---
    if (typeof Fancybox !== 'undefined') {
        Fancybox.bind("[data-fancybox]", { /* кастомные опции */ });
    }

    // --- БЛОК 7: Анимации появления при скролле (Общие) ---
    const faders = document.querySelectorAll('.fade-in, .slide-left, .slide-right');
    if ('IntersectionObserver' in window && faders.length > 0) {
        const fadersObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        faders.forEach(el => fadersObserver.observe(el));
    } else {
        faders.forEach(el => el.classList.add('active'));
    }

    // --- БЛОК 8: Анимация для контейнера этапов работы ---
    const animatedGrid = document.querySelector('.process-steps-grid.anim-on-scroll');
    if (animatedGrid && 'IntersectionObserver' in window) {
        const stepsObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('start-animation');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.25 });
        stepsObserver.observe(animatedGrid);
    } else if (animatedGrid) {
        animatedGrid.classList.add('start-animation');
    }

    // --- БЛОК 9: Логика для модального окна консультации + Анимация распада ---
    const consultationModal = document.getElementById('consultation-modal');
    const openModalBtn = document.getElementById('open-consultation-modal');
    const closeModalConsultationBtn = document.getElementById('close-consultation-modal');
    const consultationForm = document.getElementById('consultation-form');

    const successModal = document.getElementById('success-animation-modal');
    const closeSuccessBtn = document.getElementById('close-success-modal');
    const contentToCapture = document.getElementById('success-content-to-capture');
    const particleCanvas = document.getElementById('particle-canvas');

    if (consultationModal && openModalBtn && consultationForm && successModal && closeSuccessBtn && contentToCapture && particleCanvas) {

        const openConsultationModal = () => {
            consultationModal.style.display = 'flex';
            consultationModal.querySelector('.modal-content').classList.remove('roll-out');
            consultationModal.querySelector('.modal-content').classList.add('roll-in');
        };

        const closeConsultationModal = (reset = true) => {
            consultationModal.querySelector('.modal-content').classList.remove('roll-in');
            consultationModal.querySelector('.modal-content').classList.add('roll-out');
            setTimeout(() => {
                consultationModal.style.display = 'none';
                if (reset) {
                    consultationForm.reset();
                    consultationForm.querySelector('button[type="submit"]').disabled = true;
                }
            }, 700);
        };

        openModalBtn.addEventListener('click', openConsultationModal);
        closeModalConsultationBtn.addEventListener('click', () => closeConsultationModal(true));

        consultationForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = e.target.querySelector('button[type="submit"]');
            if (submitBtn.disabled) return;

            submitBtn.disabled = true;
            submitBtn.textContent = 'Отправка...';

            const formData = new FormData(consultationForm);

            fetch(window.location.pathname, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
                body: formData,
            })
            .then(response => {
                if (!response.ok) { throw new Error('Network response was not ok'); }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    closeConsultationModal(true);
                    setTimeout(() => { successModal.style.display = 'flex'; }, 750);
                } else {
                    alert('Ошибка валидации: \n' + Object.values(data.errors).join('\n'));
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при отправке. Попробуйте позже.');
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Отправить';
            });
        });

        closeSuccessBtn.addEventListener('click', () => {
            if (typeof html2canvas === 'undefined') {
                console.error('Библиотека html2canvas не подключена!');
                successModal.style.display = 'none';
                return;
            }

            html2canvas(contentToCapture, { backgroundColor: null, scale: window.devicePixelRatio }).then(canvas => {
                contentToCapture.style.visibility = 'hidden';
                const ctx = particleCanvas.getContext('2d');
                particleCanvas.width = window.innerWidth;
                particleCanvas.height = window.innerHeight;

                const particles = [];
                const imageData = canvas.getContext('2d').getImageData(0, 0, canvas.width, canvas.height);
                const modalRect = contentToCapture.getBoundingClientRect();

                for (let y = 0; y < imageData.height; y += 4) {
                    for (let x = 0; x < imageData.width; x += 4) {
                        const alpha = imageData.data[(y * imageData.width + x) * 4 + 3];
                        if (alpha > 128) {
                            const r = imageData.data[(y * imageData.width + x) * 4];
                            const g = imageData.data[(y * imageData.width + x) * 4 + 1];
                            const b = imageData.data[(y * imageData.width + x) * 4 + 2];

                            particles.push({
                                x: modalRect.left + (x / window.devicePixelRatio),
                                y: modalRect.top + (y / window.devicePixelRatio),
                                color: `rgba(${r},${g},${b},1)`,
                                size: Math.random() * 2 + 1,
                                vx: (Math.random() - 0.5) * 3,
                                vy: (Math.random() * -4) - 1.5,
                                alpha: 1,
                            });
                        }
                    }
                }

                function animateParticles() {
                    ctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
                    let activeParticles = 0;
                    particles.forEach(p => {
                        if (p.alpha > 0) {
                            p.x += p.vx;
                            p.y += p.vy;
                            p.vy += 0.08;
                            p.alpha -= 0.015;

                            ctx.globalAlpha = Math.max(0, p.alpha);
                            ctx.fillStyle = p.color;
                            ctx.fillRect(p.x, p.y, p.size, p.size);
                            activeParticles++;
                        }
                    });

                    if (activeParticles > 0) {
                        requestAnimationFrame(animateParticles);
                    } else {
                        successModal.style.display = 'none';
                        contentToCapture.style.visibility = 'visible';
                        ctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
                    }
                }
                requestAnimationFrame(animateParticles);
            });
        });

        const inputs = {
            fullName: consultationForm.querySelector('#fullname'),
            company: consultationForm.querySelector('#company'),
            phone: consultationForm.querySelector('#phone'),
            email: consultationForm.querySelector('#email')
        };
        const submitBtn = consultationForm.querySelector('button[type="submit"]');

        const validateField = (field) => {
            if (!field.checkValidity()) return false;
            if (field.pattern) {
                return new RegExp(field.pattern).test(field.value);
            }
            return true;
        };

        const checkFormValidity = () => {
            const isFormValid = Object.values(inputs).every(validateField);
            submitBtn.disabled = !isFormValid;
        };

        consultationForm.addEventListener('input', checkFormValidity);
    }

    // --- НОВЫЙ БЛОК 10: Анимации для страницы проекта ---
    const projectAnimatedElements = document.querySelectorAll('.anim-on-scroll-project');

    if (projectAnimatedElements.length > 0) {
        const projectObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const animation = entry.target.dataset.animation;
                    if (animation) {
                        entry.target.style.opacity = 1;
                        entry.target.classList.add('animate__animated', animation);
                    }
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        projectAnimatedElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const inViewport = rect.top < window.innerHeight && rect.bottom > 0;
            if (inViewport) {
                const animation = el.dataset.animation;
                el.style.opacity = 1;
                if (animation) {
                    el.classList.add('animate__animated', animation);
                }
                if (typeof projectObserver.unobserve === 'function') {
                    projectObserver.unobserve(el);
                }
            } else {
                projectObserver.observe(el);
            }
        });
    }

});
