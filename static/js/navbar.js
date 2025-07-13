// Função para alternar o menu mobile
    function toggleMobileMenu() {
        const mobileMenu = document.getElementById('mobile-menu');
        mobileMenu.classList.toggle('hidden');
    }

    // Função para controlar os dropdowns
    function setupDropdowns() {
        const dropdownButtons = document.querySelectorAll('[data-dropdown-toggle]');

        dropdownButtons.forEach(button => {
            const dropdownId = button.getAttribute('data-dropdown-toggle');
            const dropdown = document.getElementById(dropdownId);

            // Adiciona evento de clique no botão
            button.addEventListener('click', (e) => {
                e.stopPropagation(); // Evita que o clique se propague
                dropdown.classList.toggle('hidden');

                // Fecha outros dropdowns abertos
                dropdownButtons.forEach(otherButton => {
                    const otherId = otherButton.getAttribute('data-dropdown-toggle');
                    if (otherId !== dropdownId) {
                        const otherDropdown = document.getElementById(otherId);
                        otherDropdown.classList.add('hidden');
                    }
                });
            });
        });

        // Fecha os dropdowns quando clicar fora deles
        document.addEventListener('click', (e) => {
            const isDropdownButton = e.target.closest('[data-dropdown-toggle]');
            if (!isDropdownButton) {
                dropdownButtons.forEach(button => {
                    const dropdownId = button.getAttribute('data-dropdown-toggle');
                    const dropdown = document.getElementById(dropdownId);
                    dropdown.classList.add('hidden');
                });
            }
        });
    }

    // Inicializa os dropdowns quando o documento estiver carregado
    document.addEventListener('DOMContentLoaded', setupDropdowns);