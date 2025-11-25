// Custom JavaScript for E-Commerce

document.addEventListener('DOMContentLoaded', function () {

    // Reveal-on-scroll animations (respects reduced motion)
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const revealTargets = document.querySelectorAll('.reveal, .card');
    if (!prefersReduced && 'IntersectionObserver' in window) {
        revealTargets.forEach(el => el.classList.add('reveal'));
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('show');
                    obs.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
        revealTargets.forEach(el => observer.observe(el));
    }

    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach((link) => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Collapse navbar on link click (better hamburger UX on mobile)
    const navbarCollapse = document.getElementById('navbarNav');
    if (navbarCollapse) {
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach((navLink) => {
            navLink.addEventListener('click', () => {
                const bsCollapse = window.bootstrap && window.bootstrap.Collapse;
                if (bsCollapse) {
                    const instance = bsCollapse.getInstance(navbarCollapse);
                    if (instance && navbarCollapse.classList.contains('show')) {
                        instance.hide();
                    }
                }
            });
        });
    }

    // Animated hamburger state sync with offcanvas
    const toggler = document.querySelector('.navbar-toggler .hamburger');
    const offcanvasEl = document.getElementById('swiftrentMenu');
    if (toggler && offcanvasEl) {
        offcanvasEl.addEventListener('show.bs.offcanvas', () => toggler.classList.add('is-open'));
        offcanvasEl.addEventListener('hide.bs.offcanvas', () => toggler.classList.remove('is-open'));
        // Also close when any offcanvas nav link clicked
        offcanvasEl.querySelectorAll('.nav-link, .dropdown-item').forEach(el => {
            el.addEventListener('click', () => {
                const oc = window.bootstrap && window.bootstrap.Offcanvas.getOrCreateInstance(offcanvasEl);
                if (oc) oc.hide();
            });
        });
    }

    // Prevent double form submissions
    document.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', function (e) {
            if (form.dataset.submitted === 'true') {
                e.preventDefault();
                return false;
            }
            form.dataset.submitted = 'true';
            const submitBtns = form.querySelectorAll('button[type="submit"], input[type="submit"]');
            submitBtns.forEach(btn => {
                btn.disabled = true;
                btn.classList.add('disabled');
            });
        });
    });

    // (Dark mode removed by request)

    // Auto-dismiss alerts after 2 seconds
    const autoDismiss = document.querySelectorAll('.alert');
    if (autoDismiss.length && window.bootstrap) {
        autoDismiss.forEach((el) => {
            setTimeout(() => {
                try {
                    const inst = window.bootstrap.Alert.getOrCreateInstance(el);
                    inst.close();
                } catch (e) { /* no-op */ }
            }, 2000);
        });
    }
});