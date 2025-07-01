# Sistema de Controle de Docagem 🚢

Sistema web para controle de docagem de navios utilizando Python Flask.

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Execução

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o servidor
```bash
python controle.py
```

### 3. Descobrir o IP do servidor
No Windows, execute no terminal:
```cmd
ipconfig
```
Procure pelo "Endereço IPv4" da sua rede (geralmente algo como 192.168.1.xxx)

### 4. Acessar de outros dispositivos
Em qualquer dispositivo na mesma rede, abra o navegador e acesse:
```
http://[IP_DO_SERVIDOR]:5000
```
Exemplo: `http://192.168.1.100:5000`

## 📱 Funcionalidades

- **Menu Principal**: Navegação entre diferentes seções do navio
- **Proa Bombordo/Boreste**: Controle das medidas Y e Z da proa
- **Popa Bombordo/Boreste**: Controle das medidas X, Y e Z da popa  
- **Controle Centralizado**: Visualização de todos os valores em tempo real
- **Sincronização em Tempo Real**: Dados sincronizados automaticamente entre máquinas diferentes
- **Persistência**: Dados salvos no servidor e mantidos entre sessões
- **Timestamp Automático**: Horário atualizado automaticamente ao inserir valores

## 🌐 Uso em Rede

1. **Servidor**: Execute `python controle.py` no computador principal
2. **Clientes**: Acesse via navegador usando o IP do servidor
3. **Sincronização**: Os dados são compartilhados entre todos os dispositivos conectados

## 🔧 Configuração de Firewall

Se outros dispositivos não conseguirem acessar, verifique:
- Firewall do Windows permite conexões na porta 5000
- Antivírus não está bloqueando a aplicação
- Todos os dispositivos estão na mesma rede Wi-Fi

## 📞 Solução de Problemas

**Erro "Endereço já em uso"**: 
- A porta 5000 já está sendo usada
- Termine outros processos Python ou reinicie o computador

**Não consegue acessar de outros dispositivos**:
- Verifique se o IP está correto
- Desabilite temporariamente o firewall para testar
- Confirme que estão na mesma rede

**Dados não sincronizam**:
- Aguarde até 2 segundos (intervalo automático de sincronização)
- Recarregue a página (F5)
- Verifique se todos estão acessando o mesmo servidor
- Verificar console do navegador (F12) por erros de JavaScript

## 🔄 Sistema de Sincronização

### Como Funciona
- **Servidor Central**: Armazena todos os dados em `dados_docagem.json`
- **APIs REST**: Endpoints para enviar/receber dados entre dispositivos
- **Polling Automático**: Atualização a cada 2 segundos
- **Sincronização Instantânea**: Dados enviados imediatamente ao digitar

### APIs Disponíveis
- `GET /api/dados` - Obter todos os dados
- `POST /api/dados/{campo}` - Atualizar campo específico

### Arquivo de Teste
Consulte `TESTE_SINCRONIZACAO.md` para cenários detalhados de teste. 