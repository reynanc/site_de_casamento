function atualizarContagem() {
    const dataAlvo = new Date('December 13, 2025 00:00:00').getTime();

    function atualizar() {
        const agora = new Date().getTime();
        const diferenca = dataAlvo - agora;

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