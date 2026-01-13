document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Animate elements when they come into view
    const animatedElements = document.querySelectorAll('.animate-up, .feature-card, .process-step');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.2
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Testimonial carousel (if present on the page)
    const testimonialCarousel = document.querySelector('.testimonial-carousel');
    if (testimonialCarousel) {
        let currentSlide = 0;
        const slides = testimonialCarousel.querySelectorAll('.testimonial-item');
        const totalSlides = slides.length;
        const dots = testimonialCarousel.querySelectorAll('.carousel-dot');
        
        // Initialize first slide
        slides[0].classList.add('active');
        dots[0].classList.add('active');
        
        // Next/Prev buttons
        const nextBtn = testimonialCarousel.querySelector('.carousel-next');
        const prevBtn = testimonialCarousel.querySelector('.carousel-prev');
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                goToSlide((currentSlide + 1) % totalSlides);
            });
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                goToSlide((currentSlide - 1 + totalSlides) % totalSlides);
            });
        }
        
        // Dot navigation
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                goToSlide(index);
            });
        });
        
        function goToSlide(slideIndex) {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            
            currentSlide = slideIndex;
            
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
        }
        
        // Auto advance
        setInterval(() => {
            goToSlide((currentSlide + 1) % totalSlides);
        }, 5000);
    }
    
    // Gallery filter (if present on gallery page)
    const filterButtons = document.querySelectorAll('.filter-btn');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.getAttribute('data-filter');
                
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Filter gallery items
                const galleryItems = document.querySelectorAll('.gallery-item');
                galleryItems.forEach(item => {
                    if (filter === 'all') {
                        item.style.display = 'block';
                    } else {
                        item.style.display = item.classList.contains(filter) ? 'block' : 'none';
                    }
                });
                
                // Trigger animation for visible items
                setTimeout(() => {
                    galleryItems.forEach(item => {
                        if (item.style.display === 'block') {
                            item.classList.add('fade-in');
                        } else {
                            item.classList.remove('fade-in');
                        }
                    });
                }, 100);
            });
        });
    }
});