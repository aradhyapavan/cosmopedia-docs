document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const hamburger = document.querySelector('.hamburger');
    const navLinksContainer = document.querySelector('.nav-links');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {

                    navLinks.forEach(l => l.classList.remove('active'));

                    this.classList.add('active');

                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY + 100;

        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
        }

        const sections = ['home', 'features', 'endpoints'];
        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                const sectionTop = section.offsetTop - 100;
                const sectionBottom = sectionTop + section.offsetHeight;

                if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                    navLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === `#${sectionId}`) {
                            link.classList.add('active');
                        }
                    });
                }
            }
        });
    });

    hamburger.addEventListener('click', function() {
        navLinksContainer.classList.toggle('active');
        this.classList.toggle('active');
    });

    const typedTextSpan = document.querySelector('.typed-text');
    const textArray = [
        'Explore the Universe',
        'Discover Space Data',
        'Access NASA Images',
        'Learn About Planets',
        'Meet Astronauts',
        'Study Telescopes'
    ];
    const typingDelay = 100;
    const erasingDelay = 50;
    const newTextDelay = 2000;
    let textArrayIndex = 0;
    let charIndex = 0;

    function type() {
        if (charIndex < textArray[textArrayIndex].length) {
            typedTextSpan.textContent += textArray[textArrayIndex].charAt(charIndex);
            charIndex++;
            setTimeout(type, typingDelay);
        } else {
            setTimeout(erase, newTextDelay);
        }
    }

    function erase() {
        if (charIndex > 0) {
            typedTextSpan.textContent = textArray[textArrayIndex].substring(0, charIndex - 1);
            charIndex--;
            setTimeout(erase, erasingDelay);
        } else {
            textArrayIndex++;
            if (textArrayIndex >= textArray.length) textArrayIndex = 0;
            setTimeout(type, typingDelay + 1100);
        }
    }

    if (typedTextSpan) {
        setTimeout(type, newTextDelay + 250);
    }

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.feature-card, .endpoint-category');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    const cards = document.querySelectorAll('.feature-card, .endpoint-category');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    const endpointItems = document.querySelectorAll('.endpoint-item');
    endpointItems.forEach(item => {
        item.addEventListener('click', function() {
            const code = this.querySelector('code');
            if (code) {
                const endpoint = code.textContent;

                navigator.clipboard.writeText(`${window.location.origin}${endpoint}`).then(() => {

                    const originalText = code.textContent;
                    code.textContent = 'Copied!';
                    code.style.background = 'rgba(16, 185, 129, 0.2)';
                    code.style.color = '#10b981';

                    setTimeout(() => {
                        code.textContent = originalText;
                        code.style.background = 'rgba(99, 102, 241, 0.1)';
                        code.style.color = '#6366f1';
                    }, 1000);
                });
            }
        });
    });

    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.planet-system');

        parallaxElements.forEach(element => {
            const speed = 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });

    window.addEventListener('load', function() {
        const heroContent = document.querySelector('.hero-content');
        if (heroContent) {
            heroContent.style.opacity = '0';
            heroContent.style.transform = 'translateY(30px)';

            setTimeout(() => {
                heroContent.style.transition = 'opacity 1s ease, transform 1s ease';
                heroContent.style.opacity = '1';
                heroContent.style.transform = 'translateY(0)';

                setTimeout(() => {
                    const statsSection = document.querySelector('.hero-stats');
                    if (statsSection) {
                        const numbers = statsSection.querySelectorAll('.stat-number');
                        numbers.forEach(number => {

                            const originalText = number.getAttribute('data-original') || number.textContent;

                            const numMatch = originalText.match(/\d+/);
                            if (numMatch) {
                                const finalValue = parseInt(numMatch[0]);
                                const hasPlus = originalText.includes('+');
                                number.textContent = '0';
                                animateValue(number, 0, finalValue, 2000, hasPlus);
                            }
                        });
                    }
                }, 500);
            }, 100);
        }
    });

    function animateValue(element, start, end, duration, hasPlus = false) {
        const range = end - start;
        let current = start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));

        const timer = setInterval(() => {
            current += increment;
            element.textContent = current;
            if (current === end) {
                clearInterval(timer);

                element.textContent = hasPlus ? end + '+' : end;
            }
        }, stepTime);
    }

    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const numbers = entry.target.querySelectorAll('.stat-number');
                numbers.forEach(number => {

                    const originalText = number.getAttribute('data-original') || number.textContent;

                    const numMatch = originalText.match(/\d+/);
                    if (numMatch) {
                        const finalValue = parseInt(numMatch[0]);
                        const hasPlus = originalText.includes('+');
                        number.textContent = '0';
                        animateValue(number, 0, finalValue, 2000, hasPlus);
                    }
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
        statsObserver.observe(statsSection);

        setTimeout(() => {
            const numbers = statsSection.querySelectorAll('.stat-number');
            numbers.forEach((number, index) => {
                if (number.textContent === '0') {

                    const statItems = statsSection.querySelectorAll('.stat-item .stat-number');
                    if (statItems[index]) {

                        const originalElement = statItems[index];
                        const originalText = originalElement.getAttribute('data-original') || originalElement.textContent;
                        number.textContent = originalText;
                    }
                }
            });
        }, 3000);
    }

    function createFloatingParticle() {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.width = Math.random() * 4 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = `hsl(${Math.random() * 60 + 200}, 70%, 60%)`;
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * window.innerWidth + 'px';
        particle.style.top = window.innerHeight + 'px';
        particle.style.pointerEvents = 'none';
        particle.style.opacity = Math.random() * 0.5 + 0.3;
        particle.style.zIndex = '-1';

        document.body.appendChild(particle);

        const animation = particle.animate([
            { transform: 'translateY(0px)', opacity: particle.style.opacity },
            { transform: `translateY(-${window.innerHeight + 100}px)`, opacity: 0 }
        ], {
            duration: Math.random() * 3000 + 2000,
            easing: 'linear'
        });

        animation.onfinish = () => particle.remove();
    }

    setInterval(createFloatingParticle, 2000);
});

if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {

        console.log('🚀 Space API loaded successfully!');
    });
}