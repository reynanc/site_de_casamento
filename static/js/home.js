function atualizarContagem() {
    const dataAlvo = new Date('December 13, 2025 00:00:00').getTime();
    const dataCasados = new Date('December 14, 2025 00:00:00').getTime(); // 1 dia após o casamento

    function atualizar() {
        const agora = new Date().getTime();
        
        // Verifica se já passou do dia 14/12/2025 (1 dia após o casamento)
        if (agora >= dataCasados) {
            // Oculta a contagem regressiva e mostra a mensagem de casados
            document.getElementById('contagem-section').classList.add('hidden');
            document.getElementById('casados-section').classList.remove('hidden');
            return; // Para a execução da função
        }
        
        const diferenca = dataAlvo - agora;

        // Se a diferença for negativa (já passou da data do casamento mas ainda não chegou no dia 14)
        if (diferenca < 0) {
            // Mostra zeros na contagem
            document.getElementById('dias').textContent = '0';
            document.getElementById('horas').textContent = '00';
            document.getElementById('minutos').textContent = '00';
            document.getElementById('segundos').textContent = '00';
            return;
        }

        const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
        const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
        const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);

        document.getElementById('dias').textContent = dias;
        document.getElementById('horas').textContent = horas.toString().padStart(2, '0');
        document.getElementById('minutos').textContent = minutos.toString().padStart(2, '0');
        document.getElementById('segundos').textContent = segundos.toString().padStart(2, '0');
    }

    atualizar();
    setInterval(atualizar, 1000);
}

document.addEventListener('DOMContentLoaded', atualizarContagem);