# 🔐 Sistema de Controle de Acesso por Páginas

## Visão Geral

Foi implementado um sistema avançado de controle de acesso que permite ao administrador definir exatamente quais páginas HTML cada perfil de usuário pode acessar. Este sistema oferece controle granular sobre as funcionalidades disponíveis para cada tipo de usuário.

## Como Funciona

### 📋 Dashboard Dinâmico
- O dashboard principal (`index.html`) agora gera links **dinamicamente**
- Cada usuário vê apenas as páginas que tem permissão para acessar
- Links são coloridos por categoria e incluem ícones intuitivos

### 🛡️ Proteção das Rotas
- Todas as páginas HTML têm verificação de acesso no servidor
- Usuários sem permissão são redirecionados automaticamente para o login
- Verificação dupla: frontend (interface) + backend (segurança)

### 🎛️ Painel de Controle Administrativo
- Interface completa para gerenciar permissões por perfil
- Visualização clara de todas as páginas disponíveis
- Salvamento em lote de todas as alterações

## Páginas Disponíveis no Sistema

| Página | Nome | Categoria | Descrição |
|--------|------|-----------|-----------|
| `ProaBombordo.html` | ⚓ Proa Bombordo | Operacional | Controle da proa do lado bombordo |
| `ProaBoreste.html` | ⚓ Proa Boreste | Operacional | Controle da proa do lado boreste |
| `PopaBombordo.html` | 🚢 Popa Bombordo | Operacional | Controle da popa do lado bombordo |
| `PopaBoreste.html` | 🚢 Popa Boreste | Operacional | Controle da popa do lado boreste |
| `controle.html` | 🎛️ Controle Central | Supervisão | Painel de controle centralizado |
| `admin` | 🛠️ Administração | Administração | Gerenciamento de usuários |

## Configuração Padrão dos Perfis

### 🔴 Administrador
- **Acesso:** Todas as páginas
- **Controle:** Pode modificar permissões de outros perfis
- **Dashboard:** Mostra todas as funcionalidades + painel admin

### 🔵 Operador
- **Acesso:** Apenas páginas das seções do navio
- **Páginas:** Proa Bombordo, Proa Boreste, Popa Bombordo, Popa Boreste
- **Dashboard:** Links coloridos para as 4 seções operacionais

### 🟡 Supervisor
- **Acesso:** Apenas controle central
- **Páginas:** Controle Central
- **Dashboard:** Link único para supervisão

### ⚫ Visualizador
- **Acesso:** Nenhuma página (apenas dashboard básico)
- **Páginas:** Nenhuma
- **Dashboard:** Mensagem informativa sobre falta de permissões

## Como Gerenciar Permissões

### 🎯 Passo a Passo

1. **Acessar Painel Admin:**
   - Login como administrador
   - Ir para Dashboard
   - Clicar em "🛠️ Administração"

2. **Abrir Gerenciador de Permissões:**
   - No painel admin, clicar em "🔐 Gerenciar Permissões"
   - Aguardar carregamento das configurações atuais

3. **Configurar Perfis:**
   - Para cada perfil, marcar/desmarcar as páginas permitidas
   - Visualizar resumo de páginas permitidas em tempo real
   - Páginas são organizadas por categoria com badges coloridos

4. **Salvar Alterações:**
   - Clicar em "Salvar Todas as Alterações"
   - Aguardar confirmação de sucesso
   - Mudanças aplicadas imediatamente

### 🎨 Interface Visual

```
📊 Administrador
├── ✅ Proa Bombordo (OPERACIONAL)
├── ✅ Proa Boreste (OPERACIONAL)  
├── ✅ Popa Bombordo (OPERACIONAL)
├── ✅ Popa Boreste (OPERACIONAL)
├── ✅ Controle Central (SUPERVISÃO)
└── ✅ Administração (ADMINISTRAÇÃO)

🔵 Operador  
├── ✅ Proa Bombordo (OPERACIONAL)
├── ✅ Proa Boreste (OPERACIONAL)
├── ✅ Popa Bombordo (OPERACIONAL)
├── ✅ Popa Boreste (OPERACIONAL)
├── ❌ Controle Central (SUPERVISÃO)
└── ❌ Administração (ADMINISTRAÇÃO)
```

## Funcionalidades Técnicas

### 🔄 Sincronização em Tempo Real
- Mudanças aplicadas imediatamente após salvar
- Usuários afetados terão permissões atualizadas no próximo login
- Interface mostra contador de páginas permitidas

### 🛡️ Segurança Multicamada
- **Frontend:** Links só aparecem se permitidos
- **Backend:** Verificação em cada rota
- **Middleware:** Função `pagina_requerida()` para cada página
- **Redirecionamento:** Usuários sem acesso voltam ao login

### 📱 Interface Responsiva
- Modal otimizado para celulares
- Grid adaptativo de páginas
- Checkboxes grandes e fáceis de usar
- Badges categorizadas com cores

### 💾 Persistência
- Configurações salvas em estrutura de perfis
- Backup automático a cada mudança
- Carregamento rápido das permissões

## APIs Disponíveis

### Listar Perfis e Páginas
```http
GET /api/perfis
Authorization: Bearer {admin_token}
```

**Resposta:**
```json
{
  "status": "sucesso",
  "perfis": {...},
  "paginas_disponiveis": {...}
}
```

### Atualizar Páginas de um Perfil
```http
PUT /api/perfis/{perfil_id}/paginas
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "paginas_permitidas": ["ProaBombordo.html", "controle.html"]
}
```

### Consultar Páginas de um Usuário
```http
GET /api/usuarios/{email}/paginas
Authorization: Bearer {admin_token}
```

## Exemplos de Uso

### 📋 Cenário 1: Operador Especializado
**Situação:** Criar perfil para operador que só trabalha com proa
**Solução:**
1. Editar perfil "Operador"
2. Desmarcar "Popa Bombordo" e "Popa Boreste"
3. Manter apenas "Proa Bombordo" e "Proa Boreste"
4. Salvar alterações

### 📋 Cenário 2: Supervisor de Plantão
**Situação:** Usuário que só precisa monitorar via controle central
**Solução:**
1. Criar usuário com perfil "Supervisor"
2. Verificar se só tem acesso a "Controle Central"
3. Dashboard mostrará apenas link do controle

### 📋 Cenário 3: Visitante/Auditoria
**Situação:** Pessoa que precisa apenas visualizar sem interagir
**Solução:**
1. Criar usuário com perfil "Visualizador"
2. Não marcar nenhuma página específica
3. Dashboard mostrará mensagem informativa

## Benefícios Implementados

- ✅ **Segurança Granular:** Controle exato do que cada usuário acessa
- ✅ **Interface Limpa:** Usuários veem apenas o necessário
- ✅ **Gerenciamento Fácil:** Interface visual para admins
- ✅ **Flexibilidade Total:** Perfis customizáveis por necessidade
- ✅ **Segurança Robusta:** Múltiplas camadas de proteção
- ✅ **Responsivo:** Funciona perfeitamente em celulares
- ✅ **Tempo Real:** Mudanças aplicadas imediatamente

## Monitoramento e Auditoria

### 📊 Informações Disponíveis
- Quais páginas cada perfil pode acessar
- Quantos usuários por perfil
- Histórico de tentativas de acesso (via logs do servidor)

### 🔍 Como Verificar Acesso
1. **Via Painel Admin:** Ver configurações atuais de cada perfil
2. **Via Dashboard:** Fazer login como usuário teste
3. **Via Logs:** Monitorar tentativas de acesso indevido

---

🎯 **Sistema pronto para uso!** O controle de acesso por páginas oferece flexibilidade total para adequar o sistema às necessidades específicas de cada organização. 