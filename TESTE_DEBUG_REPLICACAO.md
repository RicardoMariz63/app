# 🔍 Teste e Debug - Replicação de Valores

## 🎯 Problema Reportado
Valor do campo `input-z-popabombordo2` **não está sendo replicado** para os campos `input-x-popabombordo2` e `input-y-popabombordo2`.

## 🛠️ Logs de Debug Adicionados

### **1. Configuração de Listeners:**
- ✅ Log quando listener é configurado para cada campo
- ✅ Log quando elemento não é encontrado
- ✅ Verificação específica dos campos de replicação

### **2. Detecção de Eventos:**
- ✅ Log quando evento `input` é detectado
- ✅ Log do valor digitado

### **3. Função de Replicação:**
- ✅ Log quando função é chamada
- ✅ Log do mapeamento encontrado
- ✅ Log para cada campo destino
- ✅ Log quando campo destino é encontrado/não encontrado

## 🧪 Como Testar com Debug:

### **Passo 1: Acesse a página de controle**
```
http://192.168.0.12:5000/controle.html
```

### **Passo 2: Abra o Console do Navegador**
- **Chrome/Edge:** F12 → Console
- **Firefox:** F12 → Console
- **Safari:** Option+Cmd+C

### **Passo 3: Procure pelos logs iniciais**
Você deve ver logs como:
```
🎯 Configurando página de controle
🔍 DEBUG: Configurando listeners para campos: [array de IDs]
🎯 Configurando listener para input-z-popabombordo2 → operador_popa_bombordo
🔍 DEBUG: Verificando presença dos campos de replicação:
- input-z-popabombordo2: true
- input-x-popabombordo2: true  
- input-y-popabombordo2: true
```

### **Passo 4: Teste a digitação**
1. Localize o campo `input-z-popabombordo2` (segunda linha, coluna esquerda - operador)
2. Digite um valor (ex: "João Silva")
3. Observe os logs no console

### **Logs Esperados ao Digitar:**
```
📝 Evento input detectado em input-z-popabombordo2: "João Silva"
🔍 DEBUG: replicarValorSeNecessario chamado para input-z-popabombordo2 com valor "João Silva"
🔍 DEBUG: camposDestino para input-z-popabombordo2: ["input-x-popabombordo2", "input-y-popabombordo2"]
🔄 Replicando valor "João Silva" de input-z-popabombordo2 para 2 campos
🔍 DEBUG: Tentando encontrar campo input-x-popabombordo2
🔍 DEBUG: Campo input-x-popabombordo2 encontrado, definindo valor
✅ Valor replicado para input-x-popabombordo2: "João Silva"
🔍 DEBUG: Campo servidor para input-x-popabombordo2: operador_x_popa_bombordo
✅ operador_x_popa_bombordo atualizado: João Silva
🔍 DEBUG: Tentando encontrar campo input-y-popabombordo2
🔍 DEBUG: Campo input-y-popabombordo2 encontrado, definindo valor
✅ Valor replicado para input-y-popabombordo2: "João Silva"
🔍 DEBUG: Campo servidor para input-y-popabombordo2: operador_y_popa_bombordo
✅ operador_y_popa_bombordo atualizado: João Silva
```

## 🚨 Possíveis Problemas e Soluções:

### **❌ Problema 1: Elemento não encontrado na configuração**
**Log:** `❌ Elemento input-z-popabombordo2 não encontrado para configurar listener`

**Solução:** Verificar se o ID do campo está correto no HTML

### **❌ Problema 2: Evento input não detectado**
**Sintoma:** Não aparece log `📝 Evento input detectado`

**Possíveis causas:**
- Listener não foi configurado
- Elemento não existe
- Evento não está sendo disparado

### **❌ Problema 3: Campos destino não encontrados**
**Log:** `❌ Campo destino [ID] não encontrado`

**Solução:** Verificar se os IDs dos campos de destino estão corretos

### **❌ Problema 4: Nenhuma replicação configurada**
**Log:** `ℹ️ Nenhuma replicação configurada para [elementoId]`

**Possível causa:** ID do campo não corresponde ao mapeamento

## 📋 Checklist de Verificação:

- [ ] Página de controle carregou corretamente
- [ ] Console está aberto e visível
- [ ] Logs iniciais aparecem corretamente
- [ ] Campos estão presentes: input-z-popabombordo2, input-x-popabombordo2, input-y-popabombordo2
- [ ] Listener foi configurado para input-z-popabombordo2
- [ ] Evento input é detectado ao digitar
- [ ] Função de replicação é chamada
- [ ] Campos destino são encontrados
- [ ] Valores são replicados visualmente
- [ ] Dados são enviados para o servidor

## 🔧 Próximos Passos:

1. **Execute o teste** seguindo os passos acima
2. **Copie todos os logs** do console
3. **Relate qual etapa falhou** (se alguma)
4. **Informe se os valores aparecem nos campos** visualmente

Com essas informações detalhadas, poderemos identificar exatamente onde está o problema e corrigi-lo. 