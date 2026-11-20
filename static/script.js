// static/script.js
// MozAssist Pro - Cliente Web

let isLoading = false;

// Elementos DOM
const messagesContainer = document.getElementById('messagesContainer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const modeLabel = document.getElementById('modeLabel');
const modeToggle = document.getElementById('modeToggle');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    carregarEstatisticas();
    
    // Event listeners
    sendBtn.addEventListener('click', enviarMensagem);
    modeToggle.addEventListener('click', alternarModo);
    
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            enviarMensagem();
        }
    });
    
    // Auto-resize do textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Chips de exemplo
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const pergunta = chip.getAttribute('data-question');
            messageInput.value = pergunta;
            enviarMensagem();
        });
    });
});

// Enviar mensagem
async function enviarMensagem() {
    const pergunta = messageInput.value.trim();
    
    if (!pergunta || isLoading) return;
    
    // Mostrar mensagem do usuário
    adicionarMensagem(pergunta, 'user');
    
    // Limpar input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Mostrar indicador de carregamento
    isLoading = true;
    const loadingId = adicionarLoading();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pergunta: pergunta })
        });
        
        const data = await response.json();
        
        // Remover loading
        removerLoading(loadingId);
        
        if (data.status === 'success') {
            adicionarMensagem(data.resposta, 'bot');
            carregarEstatisticas();
        } else {
            adicionarMensagem('❌ Erro: ' + data.erro, 'bot');
        }
    } catch (error) {
        removerLoading(loadingId);
        adicionarMensagem('❌ Erro de conexão: ' + error.message, 'bot');
    } finally {
        isLoading = false;
    }
}

// Adicionar mensagem ao chat
function adicionarMensagem(texto, tipo) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${tipo}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Converter markdown simples para HTML
    let htmlTexto = texto
        .replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]))
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
    
    contentDiv.innerHTML = htmlTexto;
    
    const metaDiv = document.createElement('div');
    metaDiv.className = 'message-meta';
    metaDiv.textContent = new Date().toLocaleTimeString('pt-PT', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(metaDiv);
    
    // Remover welcome card se existir e for a primeira mensagem
    const welcomeCard = messagesContainer.querySelector('.welcome-card');
    if (welcomeCard && messagesContainer.children.length === 1) {
        welcomeCard.remove();
    }
    
    messagesContainer.appendChild(messageDiv);
    
    // Scroll para o final
    const chatArea = document.getElementById('chatArea');
    chatArea.scrollTop = chatArea.scrollHeight;
}

// Adicionar indicador de loading
function adicionarLoading() {
    const id = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.id = id;
    loadingDiv.className = 'loading-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'loading-content';
    contentDiv.innerHTML = `
        <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <span>Pensando...</span>
    `;
    
    loadingDiv.appendChild(contentDiv);
    messagesContainer.appendChild(loadingDiv);
    
    const chatArea = document.getElementById('chatArea');
    chatArea.scrollTop = chatArea.scrollHeight;
    
    return id;
}

function removerLoading(id) {
    const element = document.getElementById(id);
    if (element) element.remove();
}

// Alternar modo de busca
async function alternarModo() {
    try {
        const response = await fetch('/api/alternar_modo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        });
        
        const data = await response.json();
        
        modeLabel.textContent = textoModo(data.modo);
        
        adicionarMensagem(data.mensagem, 'bot');
        carregarEstatisticas();
    } catch (error) {
        adicionarMensagem('❌ Erro ao alternar modo', 'bot');
    }
}

function textoModo(modo) {
    if (modo === 'local') return '📚 Modo Local (offline)';
    if (modo === 'web') return '🌐 Modo Web (Google)';
    return '🔀 Modo Híbrido (Recomendado)';
}

// Carregar estatísticas
async function carregarEstatisticas() {
    try {
        const response = await fetch('/api/estatisticas');
        const stats = await response.json();
        
        modeLabel.textContent = textoModo(stats.modo_busca);
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}