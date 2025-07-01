# Guia de Teste - Sistema de Alarme 🚨

## 🎯 Objetivo
Testar o sistema de alarme que toca quando valores são modificados nas páginas de entrada de dados.

## 🔧 Configuração do Teste

### 1. Iniciar o Servidor
```bash
python controle.py
```

### 2. Abrir duas páginas
- **Dispositivo A:** `http://192.168.0.12:5000/controle.html` (página de controle)
- **Dispositivo B:** `http://192.168.0.12:5000/ProaBombordo.html` (ou qualquer outra página)

## 🧪 Cenários de Teste

### Teste 1: Alarme Básico 🔊
1. **Dispositivo A:** Abra página **Controle**
2. **Dispositivo B:** Abra página **Proa Bombordo**
3. **No Dispositivo B:** Digite "João" no campo operador
4. **Verificar no Dispositivo A:**
   - ✅ Alarme `alarme1.mp3` deve tocar
   - ✅ Indicador visual piscando aparece no topo
   - ✅ Console mostra: "🚨 Alarme: operador_proa_bombordo modificado para João"

### Teste 2: Múltiplas Modificações 📱
1. **Dispositivo B:** Digite valores Y e Z na Proa Bombordo
2. **Verificar:** Cada modificação dispara o alarme separadamente
3. **Dispositivo C:** Abra **Popa Boreste** e digite valores
4. **Verificar:** Alarme toca para cada modificação

### Teste 3: Botão Silenciar 🔇
1. **Dispositivo B:** Modifique um valor (alarme toca)
2. **Dispositivo A:** Clique no botão "🔇 Silenciar Alarme"
3. **Verificar:**
   - ✅ Áudio para imediatamente
   - ✅ Indicador visual desaparece
   - ✅ Botão mostra "✅ Silenciado" por 2 segundos

### Teste 4: Auto-desativação ⏰
1. **Dispositivo B:** Modifique um valor
2. **Aguarde 5 segundos sem clicar em silenciar**
3. **Verificar:**
   - ✅ Alarme para automaticamente
   - ✅ Indicador visual desaparece

### Teste 5: Não dispara na própria página 🚫
1. **Dispositivo A:** Na página **Controle**, modifique um valor
2. **Verificar:**
   - ❌ Alarme NÃO deve tocar
   - ❌ Indicador NÃO deve aparecer
   - ✅ Valor sincroniza normalmente

## 📋 Páginas que Disparam Alarme

### ✅ Páginas Monitoradas:
- **ProaBombordo.html** - Operador, Y, Z
- **ProaBoreste.html** - Operador, Z  
- **PopaBombordo.html** - Operador, X, Y, Z
- **PopaBoreste.html** - Operador, Z

### ❌ Páginas que NÃO disparam:
- **controle.html** - Não dispara alarme para si mesmo
- **index.html** - Página de menu

## 🔧 Funcionalidades Testadas

### Sistema de Áudio
- [ ] Arquivo `alarme1.mp3` carrega corretamente
- [ ] Áudio toca quando valor é modificado
- [ ] Volume audível e claro
- [ ] Não toca múltiplas vezes simultaneamente

### Indicador Visual
- [ ] Aparece no topo da página
- [ ] Cor vermelha piscando
- [ ] Texto claro: "🚨 ALARME: Dados alterados em outra estação!"
- [ ] Desaparece automaticamente ou ao silenciar

### Botão Silenciar
- [ ] Localizado na parte inferior da página
- [ ] Cor vermelha com ícone 🔇
- [ ] Para o áudio imediatamente
- [ ] Remove indicador visual
- [ ] Feedback visual "✅ Silenciado"

### Lógica de Detecção
- [ ] Detecta mudanças vindas de outras páginas
- [ ] Ignora mudanças da própria página de controle
- [ ] Funciona para todos os campos monitorados
- [ ] Não dispara para valores vazios

## 🐛 Possíveis Problemas

### Áudio não toca:
1. Verificar se arquivo `alarme1.mp3` existe
2. Verificar permissões de áudio no navegador
3. Tentar interagir com a página antes (clique)
4. Verificar console para erros

### Alarme não para:
1. Clicar no botão "Silenciar Alarme"
2. Recarregar a página (F5)
3. Aguardar 5 segundos para auto-desativação

### Indicador não aparece:
1. Verificar se estilo CSS foi aplicado
2. Abrir ferramentas de desenvolvedor (F12)
3. Verificar se elemento foi criado no DOM

## 📊 Logs de Debug

### Console do Navegador:
- `🔄 Sistema de sincronização ativado!`
- `🚨 Alarme: campo_modificado modificado para "valor"`
- `🔇 Alarme silenciado`

### Servidor Flask:
- `POST /api/dados/operador_proa_bombordo HTTP/1.1" 200`
- `GET /alarme1.mp3 HTTP/1.1" 200`

## 🎉 Resultado Esperado

✅ **Cenário Perfeito:**
1. Operador modifica dados em tablet na proa
2. **IMEDIATAMENTE** alarme toca na estação de controle
3. Supervisor vê indicador visual piscando
4. Supervisor clica "Silenciar" e continua monitoramento
5. Sistema continua funcionando normalmente

---

**Status:** 🟢 Sistema de alarme implementado e pronto para teste! 