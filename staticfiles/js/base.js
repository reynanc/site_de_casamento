// Função para controlar a navbar durante o scroll
function handleNavbarScroll() {
    const navbar = document.querySelector('nav');
    const scrollPosition = window.scrollY;

    if (scrollPosition > 50) {
        if (!navbar.classList.contains('navbar-fixed')) {
            navbar.classList.remove('navbar-transparent');
            navbar.classList.add('navbar-fixed');
        }
    } else {
        if (!navbar.classList.contains('navbar-transparent')) {
            navbar.classList.remove('navbar-fixed');
            navbar.classList.add('navbar-transparent');
        }
    }
}

// Adiciona os event listeners
document.addEventListener('DOMContentLoaded', function() {
    handleNavbarScroll(); // Checa a posição inicial
    window.addEventListener('scroll', handleNavbarScroll);
});
window.addEventListener('load', handleNavbarScroll);