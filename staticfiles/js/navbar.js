// Função para alternar o menu mobile
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('navbar-sticky');
    mobileMenu.classList.toggle('hidden');
}

// Função para controlar o menu mobile
function setupMobileMenu() {
    const toggleButton = document.querySelector('[data-collapse-toggle="navbar-sticky"]');
    const mobileMenu = document.getElementById('navbar-sticky');

    if (toggleButton && mobileMenu) {
        toggleButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Atualiza o aria-expanded
            const isExpanded = !mobileMenu.classList.contains('hidden');
            toggleButton.setAttribute('aria-expanded', isExpanded);
        });

        // Fechar menu ao clicar fora dele
        document.addEventListener('click', function(event) {
            if (!mobileMenu.contains(event.target) && !toggleButton.contains(event.target)) {
                if (!mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    toggleButton.setAttribute('aria-expanded', 'false');
                }
            }
        });
    }
}

// Função para destacar a página atual
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('#navbar-sticky a');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        
        // Remove classes ativas de todos os links
        link.classList.remove('bg-violet-300', 'text-white', 'md:bg-transparent', 'md:text-violet-300');
        link.classList.add('text-gray-800', 'hover:bg-gray-100', 'md:hover:bg-transparent', 'md:hover:text-violet-900');
        
        // Adiciona classes ativas ao link atual
        if (linkPath === currentPath) {
            link.classList.remove('text-gray-800', 'hover:bg-gray-100');
            link.classList.add('text-white', 'bg-violet-300', 'md:bg-transparent', 'md:text-violet-300');
            link.setAttribute('aria-current', 'page');
        } else {
            link.removeAttribute('aria-current');
        }
    });
}

// Inicializa as funcionalidades quando o documento estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    setupMobileMenu();
    highlightCurrentPage();
});

