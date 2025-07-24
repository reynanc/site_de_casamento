document.addEventListener('DOMContentLoaded', function () {
    // Função para traçar a rota
    function tracarRota() {
        const origem = document.getElementById('endereco-partida').value;
        if (!origem) {
            alert('Por favor, digite seu endereço de origem.');
            return;
        }

        // Codificar o endereço para URL
        const origemEncoded = encodeURIComponent(origem);
        const destinoEncoded = encodeURIComponent('Espaço Bouganville, R. Iracema - Ouro Preto, Olinda - PE');

        // Abrir o Google Maps em uma nova aba com a rota
        window.open(`https://www.google.com/maps/dir/${origemEncoded}/${destinoEncoded}`, '_blank');
        
        // Limpar o campo de input após traçar a rota
        document.getElementById('endereco-partida').value = '';
    }

    // Event listener para o botão
    document.getElementById('tracar-rota').addEventListener('click', tracarRota);

    // Event listener para a tecla Enter no campo de input
    document.getElementById('endereco-partida').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Previne o comportamento padrão do Enter
            tracarRota();
        }
    });
});

// API de previsão do tempo
const apiKey = "8bfd19439a92e99e85f80320fb1bf16a";
const cidade = "Olinda";

fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${cidade},br&appid=${apiKey}&units=metric&lang=pt_br`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const previsao = data.list[0]; // primeira previsão futura
        const temp = previsao.main.temp.toFixed(1);
        const desc = previsao.weather[0].description;
        const icon = previsao.weather[0].icon;
        const dt = new Date(previsao.dt_txt).toLocaleString("pt-BR");

        document.getElementById("weather").innerHTML = `
                    <div class="flex flex-col items-center gap-4">
                        <div class="flex items-center gap-4">
                            <img src="https://openweathermap.org/img/wn/${icon}@2x.png" alt="${desc}" class="w-16 h-16" />
                            <div class="text-center">
                                <div class="text-3xl font-serif text-gray-800">${temp}°C</div>
                                <div class="text-lg text-gray-600">${cidade}</div>
                                <div class="text-sm text-gray-500 capitalize">${desc}</div>
                                <div class="text-xs text-gray-400">Previsão para: ${dt}</div>
                            </div>
                        </div>
                    </div>
                `;
    })
    .catch(err => {
        document.getElementById("weather").innerHTML = `
                    <div class="text-center text-red-500">
                        <p>Erro ao carregar previsão do tempo.</p>
                        <p class="text-sm text-gray-500 mt-2">${err.message}</p>
                    </div>
                `;
        console.error("Erro na API do tempo:", err);
    });