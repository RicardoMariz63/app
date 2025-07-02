# 🔐 Credenciais de Acesso ao Sistema de Docagem

## Usuários Disponíveis

### Administrador
- **E-mail:** `admin@docagem.com`
- **Senha:** `admin123`
- **Perfil:** `admin` - Acesso total ao sistema, pode gerenciar usuários

### Operador 1
- **E-mail:** `operador@docagem.com`
- **Senha:** `operador123`
- **Perfil:** `operador` - Acesso operacional completo

### Operador 2
- **E-mail:** `ricardo@docagem.com`
- **Senha:** `1234`
- **Perfil:** `operador` - Acesso operacional completo

### Visualizador
- **E-mail:** `docagem@docagem.com`
- **Senha:** `1234`
- **Perfil:** `visualizador` - Apenas visualização de dados

## Como Acessar

1. Inicie o servidor com o arquivo `iniciar_servidor.bat`
2. Acesse `http://localhost:5000` no seu navegador
3. Use uma das credenciais acima para fazer login
4. Após o login, você será redirecionado para o dashboard principal
5. **Para administradores:** No dashboard aparecerá um botão "🛠️ Administração" para gerenciar usuários
6. **Controle de páginas:** Cada perfil vê apenas as páginas permitidas no dashboard

## Perfis de Acesso

### 🔴 Administrador (`admin`)
- **Permissões:** Acesso total ao sistema
- **Páginas permitidas:** TODAS (6/6)
  - ⚓ Proa Bombordo
  - ⚓ Proa Boreste  
  - 🚢 Popa Bombordo
  - 🚢 Popa Boreste
  - 🎛️ Controle Central
  - 🛠️ Administração
- **Pode fazer:**
  - Gerenciar usuários e permissões
  - Acessar todas as funcionalidades
  - Configurar acesso por páginas
  - Editar todos os dados

### 🔵 Operador (`operador`)
- **Permissões:** Acesso operacional completo
- **Páginas permitidas:** 5/6 (sem administração)
  - ⚓ Proa Bombordo
  - ⚓ Proa Boreste
  - 🚢 Popa Bombordo
  - 🚢 Popa Boreste
  - 🎛️ Controle Central
- **Pode fazer:**
  - Acessar todas as operações de docagem
  - Editar dados operacionais
  - Visualizar relatórios

### 🟡 Supervisor (`supervisor`)
- **Permissões:** Acesso de supervisão
- **Páginas permitidas:** 1/6 (apenas supervisão)
  - 🎛️ Controle Central
- **Pode fazer:**
  - Monitorar operações centralizadamente
  - Visualizar dados consolidados
  - Gerar relatórios

### ⚫ Visualizador (`visualizador`)
- **Permissões:** Apenas visualização
- **Páginas permitidas:** 0/6 (nenhuma página específica)
  - 📋 Apenas dashboard informativo
- **Pode fazer:**
  - Ver dashboard básico
  - Receber orientações do administrador

## Funcionalidades de Segurança

- ✅ **Tokens de sessão:** Cada login gera um token único com validade de 8 horas
- ✅ **Sistema de perfis:** Controle de acesso baseado em permissões
- ✅ **Painel administrativo:** Interface para gerenciar usuários e perfis
- ✅ **Verificação automática:** Todas as páginas verificam autenticação e permissões
- ✅ **Logout seguro:** Remove todos os dados de sessão
- ✅ **Redirecionamento:** Usuários não autenticados são redirecionados para o login
- ✅ **Responsivo:** Todas as interfaces otimizadas para celulares

## 🔐 Sistema de Controle de Páginas

### Como Funciona
- **Dashboard dinâmico:** Cada usuário vê apenas os links das páginas que pode acessar
- **Proteção de rotas:** Tentativas de acesso direto a páginas não permitidas redirecionam para login
- **Configuração por perfil:** Administradores podem definir exatamente quais páginas cada perfil acessa

### Gerenciar Permissões (apenas admins)
1. **Acessar administração:** Login como admin → Dashboard → "🛠️ Administração"
2. **Abrir gerenciador:** Clicar em "🔐 Gerenciar Permissões"
3. **Configurar perfis:** Marcar/desmarcar páginas para cada perfil
4. **Salvar alterações:** Aplicar mudanças em tempo real

### Exemplo Visual do Dashboard por Perfil

**Admin (vê tudo):**
```
⚓ Proa Bombordo    ⚓ Proa Boreste
🚢 Popa Bombordo    🚢 Popa Boreste  
🎛️ Controle Central  🛠️ Administração
```

**Operador (sem admin):**
```
⚓ Proa Bombordo    ⚓ Proa Boreste
🚢 Popa Bombordo    🚢 Popa Boreste
🎛️ Controle Central
```

**Supervisor (só controle):**
```
🎛️ Controle Central
```

**Visualizador (sem páginas):**
```
📋 Nenhuma página disponível para seu perfil.
Entre em contato com o administrador para solicitar acesso.
```

## Observações

- Os tokens expiram automaticamente após 8 horas de inatividade
- O sistema salva a sessão no localStorage do navegador
- Para adicionar novos usuários, edite o arquivo `controle.py` na seção `USUARIOS`

## Personalizações

Para adicionar um novo usuário, adicione uma entrada no dicionário `USUARIOS` no arquivo `controle.py`:

```python
USUARIOS = {
    'novo@usuario.com': {
        'senha': hashlib.sha256('suasenha'.encode()).hexdigest(),
        'nome': 'Nome do Usuário'
    }
}
```

⚠️ **Importante:** Em produção, use um banco de dados e senhas mais seguras! 

