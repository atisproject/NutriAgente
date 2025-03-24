// Dashboard para visualização de métricas e gerenciamento de leads

document.addEventListener('DOMContentLoaded', function() {
    // Iniciar carregamento das estatísticas
    loadStatistics();
    
    // Configurar botões de ação
    setupLeadButtons();
});

/**
 * Carrega estatísticas e renderiza gráficos
 */
function loadStatistics() {
    // Mostrar indicador de carregamento
    document.getElementById('statistics-loading').style.display = 'block';
    
    // Fazer requisição AJAX para obter dados
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            document.getElementById('statistics-loading').style.display = 'none';
            renderCharts(data);
        })
        .catch(error => {
            console.error('Erro ao carregar estatísticas:', error);
            document.getElementById('statistics-loading').style.display = 'none';
            document.getElementById('statistics-error').style.display = 'block';
        });
}

/**
 * Renderiza gráficos com dados recebidos
 */
function renderCharts(data) {
    // Gráfico de leads por dia
    const leadsCtx = document.getElementById('leadsChart').getContext('2d');
    new Chart(leadsCtx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Novos Leads',
                    data: data.leads,
                    backgroundColor: 'rgba(46, 204, 113, 0.2)',
                    borderColor: 'rgba(46, 204, 113, 1)',
                    borderWidth: 2,
                    tension: 0.4
                },
                {
                    label: 'Conversões',
                    data: data.conversions,
                    backgroundColor: 'rgba(243, 156, 18, 0.2)',
                    borderColor: 'rgba(243, 156, 18, 1)',
                    borderWidth: 2,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Leads e Conversões nos Últimos 30 Dias'
                }
            }
        }
    });
    
    // Gráfico de Taxa de Conversão
    const conversionCtx = document.getElementById('conversionRateChart').getContext('2d');
    
    // Calcular taxa de conversão por dia
    const conversionRates = data.dates.map((date, index) => {
        const leadCount = data.leads[index];
        const conversionCount = data.conversions[index];
        return leadCount > 0 ? (conversionCount / leadCount) * 100 : 0;
    });
    
    new Chart(conversionCtx, {
        type: 'bar',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Taxa de Conversão (%)',
                data: conversionRates,
                backgroundColor: 'rgba(52, 152, 219, 0.5)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw.toFixed(2) + '%';
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Taxa de Conversão Diária (%)'
                }
            }
        }
    });
}

/**
 * Configura botões de ação para leads
 */
function setupLeadButtons() {
    // Botões para marcar lead como convertido
    document.querySelectorAll('.convert-lead-btn').forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.getAttribute('data-lead-id');
            
            if (confirm('Marcar este lead como convertido?')) {
                fetch(`/api/lead/${leadId}/convert`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Atualizar UI
                        const statusElement = document.querySelector(`#lead-${leadId}-status`);
                        if (statusElement) {
                            statusElement.className = 'lead-status status-convertido';
                            statusElement.textContent = 'Convertido';
                        }
                        
                        // Desabilitar botão
                        this.disabled = true;
                        
                        // Mensagem de sucesso
                        alert('Lead marcado como convertido com sucesso!');
                    }
                })
                .catch(error => {
                    console.error('Erro ao atualizar lead:', error);
                    alert('Erro ao atualizar o status do lead. Tente novamente.');
                });
            }
        });
    });
    
    // Configurar ordenação de tabela
    const leadsTable = document.getElementById('leads-table');
    if (leadsTable) {
        new DataTable('#leads-table', {
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-BR.json'
            },
            order: [[0, 'desc']]
        });
    }
}

/**
 * Verifica formulários pendentes manualmente
 */
function checkPendingForms() {
    fetch('/schedule_check')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Erro ao verificar formulários pendentes:', error);
            alert('Erro ao verificar formulários pendentes. Tente novamente.');
        });
}
