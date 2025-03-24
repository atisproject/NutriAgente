// Dashboard.js - Funcionalidades para a página de dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Detecta se há formulários pendentes para destacar na UI
    const formPendentes = document.querySelectorAll('.formularios-pendentes .list-group-item');
    if (formPendentes.length > 0) {
        const badgeCount = document.querySelector('.formularios-pendentes-badge');
        if (badgeCount) {
            badgeCount.classList.add('pulse');
        }
    }

    // Configura o recarregamento automático dos dados do dashboard a cada 5 minutos
    setInterval(function() {
        const dashboardContainer = document.querySelector('#dashboard-container');
        if (dashboardContainer) {
            // Apenas recarrega se estiver na página do dashboard
            fetch('/dashboard/data')
                .then(response => response.json())
                .then(data => atualizarEstatisticas(data))
                .catch(error => console.error('Erro ao atualizar dados:', error));
        }
    }, 300000); // 5 minutos

    // Inicializa os eventos dos botões de filtro de data para os gráficos
    const periodoBtns = document.querySelectorAll('.periodo-btn');
    periodoBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            periodoBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            atualizarGraficos(this.dataset.periodo);
        });
    });
});

/**
 * Atualiza as estatísticas do dashboard sem recarregar a página
 * @param {Object} data - Dados recebidos da API
 */
function atualizarEstatisticas(data) {
    if (!data) return;

    // Atualiza os contadores
    if (data.total_leads) {
        document.getElementById('total-leads-counter').textContent = data.total_leads;
    }
    if (data.leads_convertidos) {
        document.getElementById('leads-convertidos-counter').textContent = data.leads_convertidos;
    }
    if (data.leads_novos) {
        document.getElementById('leads-novos-counter').textContent = data.leads_novos;
    }
    if (data.taxa_conversao) {
        document.getElementById('taxa-conversao-counter').textContent = data.taxa_conversao + '%';
    }

    // Atualiza o gráfico se ele existir
    if (window.performanceChart && data.chart_data) {
        window.performanceChart.data.labels = data.chart_data.labels;
        window.performanceChart.data.datasets[0].data = data.chart_data.novos_leads;
        window.performanceChart.data.datasets[1].data = data.chart_data.leads_convertidos;
        window.performanceChart.update();
    }

    // Se houver novas interações, mostrar notificação
    if (data.novas_interacoes && data.novas_interacoes > 0) {
        mostrarNotificacao(`${data.novas_interacoes} nova(s) interação(ões)`, 'info');
    }
}

/**
 * Atualiza os gráficos com base no período selecionado
 * @param {string} periodo - Período selecionado (dia, semana, mes, ano)
 */
function atualizarGraficos(periodo) {
    const loadingIndicator = document.getElementById('loading-graficos');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }

    fetch(`/dashboard/graficos?periodo=${periodo}`)
        .then(response => response.json())
        .then(data => {
            if (window.performanceChart) {
                window.performanceChart.data.labels = data.labels;
                window.performanceChart.data.datasets[0].data = data.novos_leads;
                window.performanceChart.data.datasets[1].data = data.leads_convertidos;
                window.performanceChart.update();
            }

            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Erro ao carregar dados dos gráficos:', error);
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
            mostrarNotificacao('Erro ao carregar dados dos gráficos', 'danger');
        });
}

/**
 * Mostra uma notificação na interface
 * @param {string} mensagem - Mensagem a ser exibida
 * @param {string} tipo - Tipo de alerta (success, danger, warning, info)
 */
function mostrarNotificacao(mensagem, tipo = 'info') {
    const notificacaoContainer = document.getElementById('notificacoes-container');
    if (!notificacaoContainer) return;

    const notificacao = document.createElement('div');
    notificacao.className = `alert alert-${tipo} alert-dismissible fade show`;
    notificacao.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    `;
    
    notificacaoContainer.appendChild(notificacao);

    // Remove a notificação após 5 segundos
    setTimeout(() => {
        notificacao.classList.remove('show');
        setTimeout(() => {
            notificacaoContainer.removeChild(notificacao);
        }, 150);
    }, 5000);
}
