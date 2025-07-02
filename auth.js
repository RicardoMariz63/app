// Sistema de autenticação - auth.js

let tentativasVerificacao = 0;
const MAX_TENTATIVAS = 3;

function verificarAutenticacao() {
    const token = localStorage.getItem('authToken');
    
    if (!token) {
        // Se não há token, redirecionar para login
        if (window.location.pathname !== '/') {
            window.location.href = '/';
        }
        return false;
    }
    
    // Verificar se o token ainda é válido
    fetch('/api/verificar-token', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status !== 'sucesso') {
            tentativasVerificacao++;
            if (tentativasVerificacao >= MAX_TENTATIVAS) {
                // Só remove o token após 3 tentativas falhas
                localStorage.removeItem('authToken');
                localStorage.removeItem('userEmail');
                localStorage.removeItem('userProfile');
                localStorage.removeItem('userPermissions');
                localStorage.removeItem('userPages');
                if (window.location.pathname !== '/') {
                    window.location.href = '/';
                }
            }
        } else {
            // Resetar contador de tentativas em caso de sucesso
            tentativasVerificacao = 0;
        }
    })
    .catch((error) => {
        console.error('Erro na verificação de token:', error);
        // Não remover token em caso de erro de rede
        // Apenas incrementar contador
        tentativasVerificacao++;
        if (tentativasVerificacao >= MAX_TENTATIVAS) {
            localStorage.removeItem('authToken');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('userProfile');
            localStorage.removeItem('userPermissions');
            localStorage.removeItem('userPages');
            if (window.location.pathname !== '/') {
                window.location.href = '/';
            }
        }
    });
    
    return true;
}

function logout() {
    if (confirm('Deseja realmente sair do sistema?')) {
        // Chamar endpoint de logout no servidor
        fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('authToken')
            }
        })
        .catch(() => {
            // Se erro na requisição, apenas limpar dados locais
        })
        .finally(() => {
            // Limpar dados locais e redirecionar
            localStorage.removeItem('authToken');
            localStorage.removeItem('userEmail');
            localStorage.removeItem('userProfile');
            localStorage.removeItem('userPermissions');
            localStorage.removeItem('userPages');
            window.location.href = '/';
        });
    }
}

// Verificar autenticação quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    // Não verificar autenticação na página de login
    if (window.location.pathname === '/') {
        return;
    }
    
    verificarAutenticacao();
});

// Adicionar cabeçalho de autenticação em todas as requisições fetch
const originalFetch = window.fetch;
window.fetch = function(url, options = {}) {
    const token = localStorage.getItem('authToken');
    if (token && !url.includes('/api/login')) {
        options.headers = options.headers || {};
        options.headers['Authorization'] = 'Bearer ' + token;
    }
    return originalFetch(url, options);
}; 