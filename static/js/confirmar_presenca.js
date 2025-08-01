document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss das mensagens após 10 segundos
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

        // Remove a mensagem após 10 segundos
        setTimeout(() => {
            dismissMessage(message.id);
        }, 10000);
    });

    // Validação em tempo real do formulário
    const form = document.querySelector('form');
    const nomeInput = document.querySelector('input[name="nome"]');
    const telefoneInput = document.querySelector('input[name="telefone"]');

    // Função para validar telefone (formato brasileiro)
    function isValidPhone(phone) {
        const phoneRegex = /^\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}$/;
        return phoneRegex.test(phone) || phone.trim() === '';
    }

    // Máscara para telefone
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length === 0) {
                e.target.value = '';
                return;
            }

            if (value.length <= 11) {
                if (value.length <= 2) {
                    value = value.replace(/(\d{0,2})/, '($1');
                } else if (value.length <= 6) {
                    value = value.replace(/(\d{2})(\d{0,4})/, '($1) $2');
                } else if (value.length <= 10) {
                    value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
                } else {
                    value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
                }
            }

            e.target.value = value;

            isValidPhone(e.target.value);
        });
    }
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

function incrementCounter(fieldId) {
    const field = document.getElementById(fieldId);
    const currentValue = parseInt(field.value) || 0;
    const maxValue = parseInt(field.getAttribute('max')) || 10;
    if (currentValue < maxValue) {
        field.value = currentValue + 1;
        toggleNamesContainer(fieldId);
        updateFormValidation();
    }
}

function decrementCounter(fieldId, minValue = 0) {
    const field = document.getElementById(fieldId);
    const currentValue = parseInt(field.value) || 0;
    if (currentValue > minValue) {
        field.value = currentValue - 1;
        toggleNamesContainer(fieldId);
        updateFormValidation();
    }
}

function toggleNamesContainer(fieldId) {
    const value = parseInt(document.getElementById(fieldId).value) || 0;
    const isAdultos = fieldId.includes('adultos');
    const isCriancas = fieldId.includes('criancas');
    const isAdolescentes = fieldId.includes('adolescentes');
    
    let container, textarea;
    
    if (isAdultos) {
        container = document.getElementById('nomes-adultos-container');
        textarea = document.getElementById('id_nomes_adultos');
    } else if (isCriancas) {
        container = document.getElementById('nomes-criancas-container');
        textarea = document.getElementById('id_nomes_criancas');
    } else if (isAdolescentes) {
        container = document.getElementById('nomes-adolescentes-container');
        textarea = document.getElementById('id_nomes_adolescentes');
    }

    if ((isAdultos && value > 1) || (isCriancas && value > 0) || (isAdolescentes && value > 0)) {
        container.style.display = 'block';
        textarea.required = true;
    } else {
        container.style.display = 'none';
        textarea.required = false;
        textarea.value = '';
    }
}

function updateFormValidation() {
    const qtdAdultos = parseInt(document.getElementById('id_qtd_adultos').value) || 1;
    const qtdCriancas = parseInt(document.getElementById('id_qtd_criancas').value) || 0;
    const qtdAdolescentes = parseInt(document.getElementById('id_qtd_adolescentes').value) || 0;
    const nomesAdultos = document.getElementById('id_nomes_adultos');
    const nomesCriancas = document.getElementById('id_nomes_criancas');
    const nomesAdolescentes = document.getElementById('id_nomes_adolescentes');

    // Atualizar placeholder com a quantidade esperada
    if (qtdAdultos > 1) {
        nomesAdultos.placeholder = `Digite ${qtdAdultos - 1} nome(s) de acompanhante(s) adulto(s) (um por linha)`;
    }
    if (qtdCriancas > 0) {
        nomesCriancas.placeholder = `Digite ${qtdCriancas} nome(s) de criança(s) (um por linha)`;
    }
    if (qtdAdolescentes > 0) {
        nomesAdolescentes.placeholder = `Digite ${qtdAdolescentes} nome(s) de adolescente(s) ou crianças(s) (um por linha)`;
    }
}

// Inicializar ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    toggleNamesContainer('id_qtd_adultos');
    toggleNamesContainer('id_qtd_criancas');
    updateFormValidation();

    // Adicionar listeners para os contadores
    document.getElementById('id_qtd_adultos').addEventListener('change', function () {
        toggleNamesContainer('id_qtd_adultos');
        updateFormValidation();
    });
    document.getElementById('id_qtd_criancas').addEventListener('change', function () {
        toggleNamesContainer('id_qtd_criancas');
        updateFormValidation();
    });
    
    // Adicionar listener para adolescentes
    document.getElementById('id_qtd_adolescentes').addEventListener('change', function () {
        toggleNamesContainer('id_qtd_adolescentes');
        updateFormValidation();
    });
    
    // Inicializar adolescentes
    toggleNamesContainer('id_qtd_adolescentes');
});