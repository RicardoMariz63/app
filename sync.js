// Sistema de Sincronização entre Máquinas
class SistemaSync {
    constructor() {
        this.intervaloSync = 5000; // Atualizar a cada 5 segundos (aumentado de 2s para 5s)
        this.intervaloBase = 5000;
        this.maxIntervalo = 30000; // Máximo de 30 segundos entre atualizações
        this.falhasConsecutivas = 0;
        this.ultimaAtualizacao = {};
        this.valoresAnteriores = {}; // Para detectar mudanças vindas de outras páginas
        this.alarmeAtivo = false;
        this.audioElement = null;
        this.audioAlarme2 = null;
        this.alarme2Silenciado = false; // Controle de estado do alarme2
        this.ultimoComandoAlarme2 = null; // Para detectar novos comandos
        this.ultimaRequisicao = null;
        this.requisicaoEmAndamento = false;
        this.sistemaInicializado = false; // Flag para controlar inicialização
        this.iniciarSincronizacao();
        this.configurarAlarme();
    }

    // Configurar sistema de alarme (apenas na página de controle)
    configurarAlarme() {
        if (window.location.pathname.includes('controle.html') || window.location.pathname === '/') {
            // Criar elemento de áudio para o alarme
            this.audioElement = document.createElement('audio');
            this.audioElement.src = '/alarme1.mp3';
            this.audioElement.loop = false;
            this.audioElement.preload = 'auto';
            
            // Tentar habilitar contexto de áudio automaticamente
            setTimeout(() => {
                this.tentarHabilitarAudio();
            }, 1000);
        }
        
        // Configurar alarme2 para as páginas específicas
        if (this.isPaginaAlarme2()) {
            this.audioAlarme2 = new Audio('alarme2.mp3');
            this.audioAlarme2.preload = 'auto';
            this.audioAlarme2.volume = 0.8;
            console.log('🔊 Sistema de alarme2 configurado para:', window.location.pathname);
        }
    }

    // Tentar habilitar áudio automaticamente
    tentarHabilitarAudio() {
        if (this.audioElement) {
            // Tentar reproduzir em volume muito baixo
            const volumeOriginal = this.audioElement.volume;
            this.audioElement.volume = 0.01;
            
            this.audioElement.play().then(() => {
                // Parar imediatamente e restaurar volume
                this.audioElement.pause();
                this.audioElement.currentTime = 0;
                this.audioElement.volume = volumeOriginal;
                console.log('🔊 Sistema de áudio habilitado automaticamente');
            }).catch(() => {
                this.audioElement.volume = volumeOriginal;
                console.log('⚠️ Aguardando interação do usuário para habilitar áudio');
            });
        }
    }
    // Tocar alarme quando dados são alterados em outras páginas
    tocarAlarme() {
        if (this.audioElement && !this.alarmeAtivo) {
            this.alarmeAtivo = true;
            this.audioElement.currentTime = 0;
            
            const tentativa = this.audioElement.play();
            if (tentativa) {
                tentativa.then(() => {
                    console.log('🔊 Alarme tocando com sucesso!');
                }).catch(e => {
                    console.log('⚠️ Erro ao tocar alarme - áudio não habilitado:', e);
                    console.log('💡 Clique no botão "Habilitar" quando aparecer ou no botão "Silenciar Alarme"');
                });
            }
            
            // Adicionar indicador visual de alarme
            this.mostrarIndicadorAlarme();
            
            // Auto-desativar alarme após 10 segundos
            setTimeout(() => {
                this.alarmeAtivo = false;
                this.removerIndicadorAlarme();
                if (this.audioElement) {
                    this.audioElement.pause();
                    this.audioElement.currentTime = 0;
                }
            }, 700);
        }
    }

    // Silenciar alarme
    silenciarAlarme() {
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement.currentTime = 0;
            this.alarmeAtivo = false;
            this.removerIndicadorAlarme();
        }
    }

    // Mostrar indicador visual de alarme
    mostrarIndicadorAlarme() {
        // Verificar se já existe um indicador
        if (document.getElementById('indicador-alarme')) return;
        
        const indicador = document.createElement('div');
        indicador.id = 'indicador-alarme';
    /*    indicador.innerHTML = '🚨 ALARME: Dados alterados em outra estação!';
        indicador.style.cssText = `
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #ff4444;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            z-index: 9999;
            animation: piscar 1s infinite;
        `;
        
        // Adicionar animação de piscar
          if (!document.getElementById('estilo-alarme')) {
            const estilo = document.createElement('style');
            estilo.id = 'estilo-alarme';
            estilo.textContent = `
                @keyframes piscar {
                    0% { opacity: 1; }
                    50% { opacity: 0.5; }
                    100% { opacity: 1; }
                }
            `;
            document.head.appendChild(estilo);
        }*/
        
        document.body.appendChild(indicador);

    }

    // Remover indicador visual de alarme
    removerIndicadorAlarme() {
        const indicador = document.getElementById('indicador-alarme');
        if (indicador) {
            indicador.remove();
        }
    }

    // Verificar se mudança veio de outra página
    verificarMudancaExterna(campo, novoValor) {
        const valorAnterior = this.valoresAnteriores[campo] || '';
        const mudouExternamente = valorAnterior !== novoValor && novoValor !== '';

        // Campos que devem disparar alarme quando modificados
        const camposAlarme = [
            'operador_proa_bombordo', 'y_proa_bombordo', 'z_bombordo',
            'operador_proa_boreste', 'valor_proa_boreste',
            'operador_popa_bombordo', 'valor_popa_bombordo', 'x_popa_bombordo', 'y_popa_bombordo',
            'operador_popa_boreste', 'valor_popa_boreste'
        ];

        if (mudouExternamente && camposAlarme.includes(campo)) {
            // Verificar se estamos na página de controle
            if (window.location.pathname.includes('controle.html') || window.location.pathname === '/') {
                this.tocarAlarme();
                console.log(`🚨 Alarme: ${campo} modificado para "${novoValor}"`);

                // Atualizar hora apenas se o sistema foi inicializado (evita atualização no carregamento inicial)
                if (this.sistemaInicializado) {
                    this.atualizarHoraPorCampoServidor(campo);
                } else {
                    console.log(`ℹ️ Sistema não inicializado - alarme tocou mas hora não foi atualizada para ${campo}`);
                }
            }
        }

        this.valoresAnteriores[campo] = novoValor;
    }

    // Atualizar hora baseado no campo do servidor (dados chegando de outras páginas)
    atualizarHoraPorCampoServidor(campoServidor) {
        const mapeamentoServidorParaHora = {
            'y_proa_bombordo': 'input-y-proabombordo4',
            'z_bombordo': 'input-z-bombordo4',
            'valor_popa_bombordo': 'input-z-popabombordo4',
            'x_popa_bombordo': 'input-x-bombordo4',
            'valor_popa_boreste': 'input-z-popaboreste4',
            'y_popa_bombordo': 'input-y-popabombordo4',
            'valor_proa_boreste': 'input-z-boreste4'
        };

        const campoHoraId = mapeamentoServidorParaHora[campoServidor];
        if (campoHoraId) {
            console.log(`🕒 Sincronização: Atualizando hora para ${campoServidor} → ${campoHoraId} (dados de outra página)`);
            this.inserirHoraAtual(campoHoraId, true); // Forçar atualização quando dados chegam de outras páginas
        }
    }

    // Enviar dados para o servidor
    async enviarDados(campo, valor) {
        if (this.requisicaoEmAndamento) {
            console.log('Requisição em andamento, aguardando...');
            return;
        }

        try {
            this.requisicaoEmAndamento = true;
            const response = await fetch(`/api/dados/${campo}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ valor: valor })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Resetar contadores em caso de sucesso
            this.falhasConsecutivas = 0;
            this.intervaloSync = this.intervaloBase;
            
            const data = await response.json();
            console.log(`✅ Dados enviados com sucesso: ${campo} = ${valor}`);
            return data;
        } catch (error) {
            console.error('❌ Erro ao enviar dados:', error);
            this.aumentarIntervalo();
        } finally {
            this.requisicaoEmAndamento = false;
        }
    }

    // Buscar dados do servidor
    async buscarDados() {
        // Evitar requisições simultâneas
        if (this.requisicaoEmAndamento) {
            console.log('Já existe uma requisição em andamento...');
            return;
        }

        // Verificar tempo mínimo entre requisições (1 segundo)
        const agora = Date.now();
        if (this.ultimaRequisicao && (agora - this.ultimaRequisicao) < 1000) {
            console.log('Aguardando tempo mínimo entre requisições...');
            return;
        }

        try {
            this.requisicaoEmAndamento = true;
            this.ultimaRequisicao = agora;

            const response = await fetch('/api/dados');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const dados = await response.json();
            
            // Resetar contadores em caso de sucesso
            this.falhasConsecutivas = 0;
            this.intervaloSync = this.intervaloBase;
            
            this.atualizarInterface(dados);
        } catch (error) {
            console.error('❌ Erro ao buscar dados:', error);
            this.aumentarIntervalo();
        } finally {
            this.requisicaoEmAndamento = false;
        }
    }

    // Aumentar intervalo em caso de falhas (backoff exponencial)
    aumentarIntervalo() {
        this.falhasConsecutivas++;
        this.intervaloSync = Math.min(
            this.intervaloBase * Math.pow(2, this.falhasConsecutivas),
            this.maxIntervalo
        );
        console.log(`⏰ Intervalo ajustado para ${this.intervaloSync}ms após ${this.falhasConsecutivas} falhas`);
    }

    // Atualizar interface com dados do servidor
    atualizarInterface(dados) {
        // Verificar comando de alarme2
        if (dados.comando_alarme2 && dados.comando_alarme2.comando === 'tocar_alarme2') {
            // Verificar se é um novo comando (timestamp diferente)
            const novoTimestamp = dados.comando_alarme2.timestamp;
            if (novoTimestamp !== this.ultimoComandoAlarme2) {
                console.log('🔊 Novo comando de alarme2 recebido!', novoTimestamp);
                this.ultimoComandoAlarme2 = novoTimestamp;
                this.alarme2Silenciado = false; // Resetar estado de silenciado
                this.tocarAlarme2();
            }
        }
        
        // Mapear campos do servidor para elementos da interface
        const mapeamento = {
            'operador_proa_bombordo': ['nomeproabombordo', 'input-z-bombordo2'],
            'y_proa_bombordo': ['input-y-row4', 'input-y-proabombordo'],
            'z_bombordo': ['input-z-row4', 'input-z-bombordo'],
            'operador_y_proa_bombordo': ['nomeproabombordo', 'input-y-proabombordo2', 'input-row1'],
            'operador_proa_boreste': ['nomeproaboreste', 'input-z-boreste2'],
            'valor_proa_boreste': ['input-z-proaboreste', 'input-z-boreste'],
            'operador_popa_bombordo': ['nomepopabombordo', 'input-z-popabombordo2'],
            'valor_popa_bombordo': ['input-z-row4', 'input-z-popabombordo'],
            'operador_popa_boreste': ['nomepopaboreste', 'input-z-popaboreste2'],
            'valor_popa_boreste': ['input-zpopaboreste', 'input-z-popaboreste'],
            'operador_x_popa_bombordo': ['nomepopabombordo', 'input-x-popabombordo2'],
            'x_popa_bombordo': ['input-x-row4', 'input-x-bombordo'],
            'operador_y_popa_bombordo': ['nomepopabombordo', 'input-y-popabombordo2'],
            'y_popa_bombordo': ['input-y-row4', 'input-y-popabombordo']
        };

        for (const [campo, elementIds] of Object.entries(mapeamento)) {
            const valor = dados[campo] || '';
            
            // Verificar se houve mudança externa (para disparar alarme)
            this.verificarMudancaExterna(campo, valor);
            
            // Só atualizar se o valor mudou
            if (this.ultimaAtualizacao[campo] !== valor) {
                this.ultimaAtualizacao[campo] = valor;
                
                elementIds.forEach(elementId => {
                    const elemento = document.getElementById(elementId);
                    if (elemento && elemento !== document.activeElement) {
                        elemento.value = valor;

                        // Aplicar formatação condicional se a função existir (controle.html)
                        if (typeof window.aplicarFormatacaoCondicional === 'function') {
                            window.aplicarFormatacaoCondicional(elemento);
                        }

                        // Tornar tick verde se a função existir (controle.html)
                        if (typeof window.tornarTickVerde === 'function') {
                            window.tornarTickVerde(elementId);
                        }
                    }
                });
            }
        }
    }

    // Iniciar sincronização
    iniciarSincronizacao() {
        // Primeira busca imediata
        this.buscarDados();

        // Configurar intervalo dinâmico
        setInterval(() => {
            if (!document.hidden) { // Só atualiza se a página estiver visível
                this.buscarDados();
            }
        }, this.intervaloSync);

        // Atualizar quando a página voltar a ficar visível
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.buscarDados();
            }
        });
    }

    // Configurar listeners para um elemento
    configurarListener(elementoId, campoServidor) {
        const elemento = document.getElementById(elementoId);
        if (elemento) {
            elemento.addEventListener('input', (e) => {
                this.enviarDados(campoServidor, e.target.value);
                
                // Atualizar hora automaticamente para campos específicos
                this.atualizarHoraSeNecessario(elementoId);
                
                // Replicar valor para outros campos se necessário
                this.replicarValorSeNecessario(elementoId, e.target.value);
            });
        } else {
            console.error(`❌ Elemento ${elementoId} não encontrado para configurar listener`);
        }
    }

    // Atualizar hora automaticamente para campos específicos (quando usuário digita)
    atualizarHoraSeNecessario(elementoId) {
        const mapeamentoHora = {
            'input-y-proabombordo': 'input-y-proabombordo4',
            'input-z-bombordo': 'input-z-bombordo4',
            'input-z-popabombordo': 'input-z-popabombordo4',
            'input-x-bombordo': 'input-x-bombordo4',
            'input-z-popaboreste': 'input-z-popaboreste4',
            'input-y-popabombordo': 'input-y-popabombordo4',
            'input-z-boreste': 'input-z-boreste4'
        };

        const campoHoraId = mapeamentoHora[elementoId];
        if (campoHoraId) {
            console.log(`🕒 Atualizando hora para ${elementoId} → ${campoHoraId} (usuário digitou)`);
            this.inserirHoraAtual(campoHoraId, true); // Forçar atualização quando usuário digita
        }
    }

    // Inserir hora atual em um campo (apenas quando necessário)
    inserirHoraAtual(campoHoraId, forcarAtualizacao = false) {
        const campoHora = document.getElementById(campoHoraId);
        if (campoHora) {
            // Se o sistema não foi inicializado e não está forçando, não atualizar
            if (!this.sistemaInicializado && !forcarAtualizacao) {
                console.log(`ℹ️ Sistema não inicializado - não atualizando ${campoHoraId}`);
                return;
            }

            // Se não forçar atualização e o campo já tem valor, não atualizar
            if (!forcarAtualizacao && campoHora.value && campoHora.value.trim() !== '') {
                console.log(`ℹ️ Campo ${campoHoraId} já tem valor: ${campoHora.value} - não atualizando`);
                return;
            }

            const agora = new Date();
            const hora = agora.getHours().toString().padStart(2, '0');
            const min = agora.getMinutes().toString().padStart(2, '0');
            const seg = agora.getSeconds().toString().padStart(2, '0');
            const horaFormatada = `${hora}:${min}:${seg}`;

            campoHora.value = horaFormatada;
            console.log(`✅ Hora inserida em ${campoHoraId}: ${horaFormatada}`);

            // Salvar hora no localStorage para persistência
            this.salvarHoraLocalStorage(campoHoraId, horaFormatada);

            // Feedback visual
            campoHora.style.backgroundColor = '#90EE90'; // Verde claro
            setTimeout(() => {
                campoHora.style.backgroundColor = '';
            }, 1000);
        } else {
            console.error(`❌ Campo hora ${campoHoraId} não encontrado`);
        }
    }

    // Salvar hora no localStorage
    salvarHoraLocalStorage(campoHoraId, hora) {
        try {
            const horasArmazenadas = JSON.parse(localStorage.getItem('horasControle') || '{}');
            horasArmazenadas[campoHoraId] = hora;
            localStorage.setItem('horasControle', JSON.stringify(horasArmazenadas));
            console.log(`💾 Hora salva no localStorage: ${campoHoraId} = ${hora}`);
        } catch (error) {
            console.error('❌ Erro ao salvar hora no localStorage:', error);
        }
    }

    // Restaurar horas do localStorage
    restaurarHorasLocalStorage() {
        try {
            const horasArmazenadas = JSON.parse(localStorage.getItem('horasControle') || '{}');
            let horasRestauradas = 0;

            for (const [campoHoraId, hora] of Object.entries(horasArmazenadas)) {
                const campoHora = document.getElementById(campoHoraId);
                if (campoHora && hora) {
                    campoHora.value = hora;
                    horasRestauradas++;
                    console.log(`🔄 Hora restaurada: ${campoHoraId} = ${hora}`);
                }
            }

            if (horasRestauradas > 0) {
                console.log(`✅ ${horasRestauradas} horas restauradas do localStorage`);
            } else {
                console.log('ℹ️ Nenhuma hora encontrada no localStorage para restaurar');
            }

            // Marcar sistema como inicializado após restaurar as horas
            this.sistemaInicializado = true;
            console.log('🚀 Sistema de horas inicializado - atualizações automáticas habilitadas');
        } catch (error) {
            console.error('❌ Erro ao restaurar horas do localStorage:', error);
            // Mesmo com erro, marcar como inicializado para permitir funcionamento normal
            this.sistemaInicializado = true;
        }
    }

    // Limpar horas do localStorage (função utilitária)
    limparHorasLocalStorage() {
        try {
            localStorage.removeItem('horasControle');
            console.log('🗑️ Horas do localStorage foram limpas');
        } catch (error) {
            console.error('❌ Erro ao limpar horas do localStorage:', error);
        }
    }

    // Replicar valor entre campos específicos (LEGACY - mantido para compatibilidade)
    replicarValorSeNecessario(elementoId, valor) {
        // Função legacy - nova implementação em configurarReplicacaoDireta()
        // Mantida para compatibilidade com outros possíveis campos
        console.log(`ℹ️ Função legacy chamada para ${elementoId} - usando replicação direta`);
    }

    // Obter nome do campo do servidor baseado no ID do elemento
    obterCampoServidor(elementoId) {
        const mapeamentoCampos = {
            'input-x-popabombordo2': 'operador_x_popa_bombordo',
            'input-y-popabombordo2': 'operador_y_popa_bombordo',
            'input-z-popabombordo2': 'operador_popa_bombordo'
        };
        
        return mapeamentoCampos[elementoId] || null;
    }

    // Função removida - agora usando sistema unificado de mapeamento

    // Função de teste manual para replicação
    testarReplicacao() {
        console.log('🧪 TESTE MANUAL: Testando replicação...');
        const campoOrigem = document.getElementById('input-z-popabombordo2');
        if (campoOrigem) {
            campoOrigem.value = 'TESTE';
            campoOrigem.dispatchEvent(new Event('input'));
            console.log('✅ Evento de teste disparado');
        } else {
            console.error('❌ Campo origem não encontrado para teste');
        }
    }

    // Verificar se é uma página que deve tocar alarme2
    isPaginaAlarme2() {
        const paginas = ['PopaBombordo.html', 'PopaBoreste.html', 'ProaBoreste.html', 'ProaBombordo.html'];
        return paginas.some(pagina => window.location.pathname.includes(pagina));
    }

    // Tocar alarme2 nas páginas específicas
    tocarAlarme2() {
        if (this.audioAlarme2 && this.isPaginaAlarme2() && !this.alarme2Silenciado) {
            console.log('🔊 Tocando alarme2 em:', window.location.pathname);
            this.audioAlarme2.currentTime = 0;
            this.audioAlarme2.loop = true; // Fazer loop até ser silenciado
            
            const tentativa = this.audioAlarme2.play();
            if (tentativa) {
                tentativa.then(() => {
                    console.log('🔊 Alarme2 tocando com sucesso!');
                    
                    // Feedback visual na página
                    document.body.style.border = '5px solid #FF5722';
                    document.body.style.animation = 'piscar 1s infinite';
                    
                    // Adicionar CSS de animação se não existir
                    if (!document.getElementById('css-alarme-piscar')) {
                        const style = document.createElement('style');
                        style.id = 'css-alarme-piscar';
                        style.textContent = `
                            @keyframes piscar {
                                0% { border-color: #FF5722; }
                                50% { border-color: #FFC107; }
                                100% { border-color: #FF5722; }
                            }
                        `;
                        document.head.appendChild(style);
                    }
                    
                }).catch(e => {
                    console.log('⚠️ Erro ao tocar alarme2:', e);
                });
            }
        } else if (this.alarme2Silenciado) {
            console.log('🔇 Alarme2 silenciado - não tocando');
        }
    }

    // Silenciar alarme2 permanentemente
    silenciarAlarme2Permanente() {
        if (this.audioAlarme2) {
            this.audioAlarme2.pause();
            this.audioAlarme2.currentTime = 0;
            this.audioAlarme2.loop = false;
            this.alarme2Silenciado = true;
            
            // Remover feedback visual
            document.body.style.border = '';
            document.body.style.animation = '';
            
            console.log('🔇 Alarme2 silenciado permanentemente em:', window.location.pathname);
        }
    }
}

// Inicializar sistema quando a página carregar
let sistemaSync;
document.addEventListener('DOMContentLoaded', function() {
    sistemaSync = new SistemaSync();
    
    // Tornar sistemaSync acessível globalmente para controle do alarme
    window.sistemaSync = sistemaSync;
    
    // Função global para teste manual
    window.testarReplicacao = function() {
        if (window.sistemaSync) {
            window.sistemaSync.testarReplicacao();
        } else {
            console.error('❌ Sistema de sincronização não disponível');
        }
    };
    
    // Configurar listeners baseado na página atual
    // NOTA: Mantendo apenas sincronização de recebimento, envio será manual via botões

    if (window.location.pathname.includes('ProaBombordo.html')) {
        // Não configurar listeners de envio automático - apenas botões manuais
        console.log('🔄 ProaBombordo: Configurado para envio manual via botão');
    }

    if (window.location.pathname.includes('ProaBoreste.html')) {
        // Não configurar listeners de envio automático - apenas botões manuais
        console.log('🔄 ProaBoreste: Configurado para envio manual via botão');
    }

    if (window.location.pathname.includes('PopaBombordo.html')) {
        // Não configurar listeners de envio automático - apenas botões manuais
        console.log('🔄 PopaBombordo: Configurado para envio manual via botão');
    }

    if (window.location.pathname.includes('PopaBoreste.html')) {
        // Não configurar listeners de envio automático - apenas botões manuais
        console.log('🔄 PopaBoreste: Configurado para envio manual via botão');
    }
    
    if (window.location.pathname.includes('controle.html')) {
        // Configurar todos os campos da página de controle
        const camposControle = {
            'input-y-proabombordo2': 'operador_y_proa_bombordo',
            'input-y-proabombordo': 'y_proa_bombordo',
            'input-z-bombordo2': 'operador_proa_bombordo',
            'input-z-bombordo': 'z_bombordo',
            'input-z-boreste2': 'operador_proa_boreste',
            'input-z-boreste': 'valor_proa_boreste',
            'input-z-popabombordo2': 'operador_popa_bombordo',
            'input-z-popabombordo': 'valor_popa_bombordo',
            'input-z-popaboreste2': 'operador_popa_boreste',
            'input-z-popaboreste': 'valor_popa_boreste',
            'input-x-popabombordo2': 'operador_x_popa_bombordo',
            'input-x-bombordo': 'x_popa_bombordo',
            'input-y-popabombordo2': 'operador_y_popa_bombordo',
            'input-y-popabombordo': 'y_popa_bombordo'
        };
        
        for (const [elementoId, campo] of Object.entries(camposControle)) {
            sistemaSync.configurarListener(elementoId, campo);
        }

        // Restaurar horas salvas do localStorage após um pequeno delay
        setTimeout(() => {
            sistemaSync.restaurarHorasLocalStorage();
        }, 500);

        console.log('🕒 Sistema de persistência de horas ativado para controle.html');
    }

    console.log('🔄 Sistema de sincronização ativado!');
});

// Funções globais para gerenciamento de horas persistentes
window.limparHorasSalvas = function() {
    if (window.sistemaSync) {
        window.sistemaSync.limparHorasLocalStorage();
        // Limpar também os campos na tela
        const camposHora = [
            'input-y-proabombordo4',
            'input-z-bombordo4',
            'input-z-popabombordo4',
            'input-x-bombordo4',
            'input-z-boreste4',
            'input-z-popaboreste4',
            'input-y-popabombordo4'
        ];

        camposHora.forEach(campoId => {
            const campo = document.getElementById(campoId);
            if (campo) {
                campo.value = '';
            }
        });

        console.log('🗑️ Todas as horas foram limpas da tela e do localStorage');
    }
};

window.mostrarHorasSalvas = function() {
    try {
        const horasArmazenadas = JSON.parse(localStorage.getItem('horasControle') || '{}');
        console.log('📋 Horas salvas no localStorage:', horasArmazenadas);
        return horasArmazenadas;
    } catch (error) {
        console.error('❌ Erro ao ler horas do localStorage:', error);
        return {};
    }
};