/**
 * Context7 Glassmorphism Interactive Framework
 * @version 2.2.0-glassmorphism-enhanced
 * @author Context7 Development Team
 * @date 11 Ocak 2025
 * @description Modern glass effects with smooth animations
 */

Context7.Glassmorphism = {
    /**
     * Initialize glassmorphism effects
     */
    init: function() {
        this.initHoverEffects();
        this.initScrollEffects();
        this.initParallaxEffects();
        this.initGlassCards();
    },

    /**
     * Initialize hover effects for glass elements
     */
    initHoverEffects: function() {
        const glassElements = document.querySelectorAll('.glass-card, .glassmorphism-card, .glass-container');
        
        glassElements.forEach(element => {
            element.addEventListener('mouseenter', this.onGlassHover.bind(this));
            element.addEventListener('mouseleave', this.onGlassLeave.bind(this));
            element.addEventListener('mousemove', this.onGlassMove.bind(this));
        });
    },

    /**
     * Glass hover effect
     * @param {Event} e - Mouse event
     */
    onGlassHover: function(e) {
        const element = e.currentTarget;
        element.style.transform = 'translateY(-8px) scale(1.02)';
        element.style.boxShadow = '0 20px 40px rgba(31, 38, 135, 0.5)';
        element.style.borderColor = 'rgba(255, 255, 255, 0.4)';
    },

    /**
     * Glass leave effect
     * @param {Event} e - Mouse event
     */
    onGlassLeave: function(e) {
        const element = e.currentTarget;
        element.style.transform = 'translateY(0) scale(1)';
        element.style.boxShadow = '0 8px 32px rgba(31, 38, 135, 0.37)';
        element.style.borderColor = 'rgba(255, 255, 255, 0.18)';
    },

    /**
     * Glass mouse move effect (subtle tilt)
     * @param {Event} e - Mouse event
     */
    onGlassMove: function(e) {
        const element = e.currentTarget;
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / centerY * 5;
        const rotateY = (centerX - x) / centerX * 5;
        
        element.style.transform = `translateY(-8px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    },

    /**
     * Initialize scroll-based glass effects
     */
    initScrollEffects: function() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('glass-fade-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.glass-card, .glassmorphism-card').forEach(card => {
            observer.observe(card);
        });
    },

    /**
     * Initialize parallax effects for glass elements
     */
    initParallaxEffects: function() {
        const parallaxElements = document.querySelectorAll('.glass-parallax');
        
        window.addEventListener('scroll', Context7.Utils.throttle(() => {
            const scrollY = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrollY * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        }, 16));
    },

    /**
     * Initialize interactive glass cards
     */
    initGlassCards: function() {
        const cards = document.querySelectorAll('.interactive-glass-card');
        
        cards.forEach(card => {
            card.addEventListener('click', this.onCardClick.bind(this));
        });
    },

    /**
     * Handle glass card click
     * @param {Event} e - Click event
     */
    onCardClick: function(e) {
        const card = e.currentTarget;
        
        // Create ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'glass-ripple';
        
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        card.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 1000);
    },

    /**
     * Create floating glass particles effect
     * @param {HTMLElement} container - Container element
     */
    createFloatingParticles: function(container) {
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'glass-particle';
            
            const size = Math.random() * 4 + 2;
            const x = Math.random() * container.offsetWidth;
            const y = Math.random() * container.offsetHeight;
            const duration = Math.random() * 20 + 10;
            
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            particle.style.animationDuration = duration + 's';
            
            container.appendChild(particle);
        }
    }
}; 