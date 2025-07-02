# 🔐 CREDENCIAIS DE LOGIN ATIVAS

## ✅ **PROBLEMA RESOLVIDO!**
✅ **Correção aplicada:** Campo de senha corrigido na API de login  
✅ **Inicialização:** Sistema carrega usuários do arquivo JSON automaticamente  
✅ **Status:** Servidor rodando em `http://192.168.0.12:5000`

---

## 🔑 **Usuários Funcionais no Sistema**

### 👑 **ADMINISTRADOR** (Acesso Total)
- **Email:** `admin@docagem.com`
- **Senha:** `admin123`
- **Acesso:** Todas as páginas + Painel administrativo

### ⚙️ **OPERADORES** (4 Seções do Navio)
- **Email:** `operador@docagem.com`
- **Senha:** `operador123`
- **Acesso:** ProaBombordo, ProaBoreste, PopaBombordo, PopaBoreste

- **Email:** `teste@docagem.com`
- **Senha:** `123`
- **Acesso:** ProaBombordo, ProaBoreste, PopaBombordo, PopaBoreste

### 👁️ **VISUALIZADOR** (Apenas Visualização)
- **Email:** `visual@docagem.com`
- **Senha:** `1234`
- **Acesso:** Apenas página Controle Central (modo leitura)

---

## 🌐 **Acesso ao Sistema**
1. **Abra o navegador**
2. **Acesse:** `http://192.168.0.12:5000`
3. **Use qualquer credencial acima**
4. **Login deve funcionar normalmente agora** ✅

---

## 🔧 **Correções Implementadas**

### **Problema Identificado:**
- Campo `password` vs `senha` na API de login
- Sistema não carregava arquivo `usuarios.json` na inicialização

### **Soluções Aplicadas:**
1. ✅ Corrigido campo `data.get('senha')` na função de login
2. ✅ Adicionado `carregar_usuarios()` na inicialização do servidor  
3. ✅ Adicionado `carregar_dados()` na inicialização do sistema
4. ✅ Verificado que todos os hashes de senha estão corretos

---

## 🚫 **Usuários Removidos**
- `ricardo@docagem.com` (deletado via painel admin)
- `docagem@docagem.com` (deletado via painel admin)

---

## 📊 **Status do Sistema**
- ✅ **Servidor:** Rodando na porta 5000
- ✅ **Autenticação:** Funcionando 
- ✅ **Usuários:** 4 ativos carregados
- ✅ **Interface:** Design moderno implementado
- ✅ **Sincronização:** Ativa entre máquinas

---
*Última atualização: 01/07/2025 15:45 - Login corrigido e funcionando* ✅ 