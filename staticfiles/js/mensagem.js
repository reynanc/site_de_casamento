document.addEventListener('DOMContentLoaded', function () {
    // Contador de caracteres
    const textarea = document.getElementById('id_mensagem');
    const charCount = document.getElementById('char-count');

    if (textarea && charCount) {
        function updateCharCount() {
            const count = textarea.value.length;
            charCount.textContent = count;

            if (count > 1800) {
                charCount.classList.add('text-red-500');
                charCount.classList.remove('text-gray-500');
            } else {
                charCount.classList.add('text-gray-500');
                charCount.classList.remove('text-red-500');
            }
        }

        textarea.addEventListener('input', updateCharCount);
        updateCharCount();
    }

    // Auto-dismiss das mensagens após 15 segundos
    const messages = document.querySelectorAll('[id^="message-"]');
    const progressBars = document.querySelectorAll('[id^="progress-"]');

    messages.forEach((message, index) => {
        const progressBar = progressBars[index];

        // Inicia a animação da barra de progresso
        setTimeout(() => {
            if (progressBar) {
                progressBar.style.width = '0%';
            }
        }, 100);

        // Remove a mensagem após 15 segundos
        setTimeout(() => {
            dismissMessage(message.id);
        }, 10000);
    });
});

// Função para remover mensagem manualmente
function dismissMessage(messageId) {
    const messageElement = document.getElementById(messageId);
    if (messageElement) {
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            messageElement.remove();
        }, 500);
    }
}