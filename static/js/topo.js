// Função para controlar o botão "Voltar ao Topo"
function handleBackToTopButton() {
    const backToTopButton = document.getElementById('backToTop');
    if (!backToTopButton) return;
    
    const scrollPosition = window.scrollY;

    if (scrollPosition > 300) {
        backToTopButton.classList.remove('opacity-0', 'invisible');
        backToTopButton.classList.add('opacity-100', 'visible');
    } else {
        backToTopButton.classList.remove('opacity-100', 'visible');
        backToTopButton.classList.add('opacity-0', 'invisible');
    }
}

// Função para rolar suavemente ao topo
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Adiciona os event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Event listener para o botão voltar ao topo
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        backToTopButton.addEventListener('click', scrollToTop);
    }
    
    // Executa a função imediatamente após o DOM carregar
    handleBackToTopButton();
});

// Event listener para scroll - essencial para funcionar durante a navegação
window.addEventListener('scroll', handleBackToTopButton);

window.addEventListener('load', function() {
    handleBackToTopButton();
});