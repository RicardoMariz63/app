# Guia de Teste - Sincronização Entre Máquinas 🧪

## 🎯 Objetivo
Verificar se os dados estão sendo sincronizados em tempo real entre diferentes dispositivos na rede.

## 🚀 Configuração do Teste

### 1. Iniciar o Servidor
```bash
python controle.py
```

### 2. Descobrir o IP
```cmd
ipconfig
```
**Seu IP atual:** `192.168.0.12`

### 3. URLs de Teste
- **Servidor:** `http://192.168.0.12:5000`
- **Menu:** `http://192.168.0.12:5000/`
- **Controle:** `http://192.168.0.12:5000/controle.html`
- **Proa Bombordo:** `http://192.168.0.12:5000/ProaBombordo.html`

## 🧪 Cenários de Teste

### Teste 1: Sincronização Básica
1. **Dispositivo A**: Acesse Proa Bombordo
2. **Dispositivo B**: Acesse página Controle
3. **No Dispositivo A**: Digite um operador e valores Y/Z
4. **Verificar**: Os valores aparecem no Dispositivo B em até 2 segundos

### Teste 2: Múltiplas Seções
1. **Dispositivo A**: Proa Bombordo - Digite "João" e valores
2. **Dispositivo B**: Popa Bombordo - Digite "Maria" e valores  
3. **Dispositivo C**: Controle - Verificar todos os valores

### Teste 3: Persistência
1. Digite valores em qualquer seção
2. Feche o navegador
3. Reabra a página
4. **Verificar**: Valores permanecem salvos

### Teste 4: Tempo Real
1. Abra Controle em dois dispositivos
2. Digite em um campo
3. **Verificar**: Atualização instantânea no outro dispositivo

## ✅ Checklist de Funcionalidades

### Sincronização de Dados
- [ ] Operador Proa Bombordo
- [ ] Valor Y Proa Bombordo  
- [ ] Valor Z Proa Bombordo
- [ ] Operador Proa Boreste
- [ ] Valor Z Proa Boreste
- [ ] Operador Popa Bombordo
- [ ] Valores X, Y, Z Popa Bombordo
- [ ] Operador Popa Boreste
- [ ] Valor Z Popa Boreste

### Funcionalidades Especiais
- [ ] Horário atualiza automaticamente ao digitar valores
- [ ] Valores persistem após reiniciar navegador
- [ ] Sincronização funciona entre diferentes dispositivos
- [ ] Interface não trava durante sincronização

## 🔧 Solução de Problemas

### Dados não sincronizam:
1. Verificar se todos acessam o mesmo IP
2. Verificar console do navegador (F12) por erros
3. Reiniciar o servidor Python

### Erro de conexão:
1. Verificar firewall do Windows
2. Confirmar que estão na mesma rede Wi-Fi
3. Tentar acessar `http://localhost:5000` no servidor

### Valores não aparecem:
1. Aguardar até 2 segundos (intervalo de sincronização)
2. Recarregar página (F5)
3. Verificar se o servidor está rodando

## 📊 APIs de Debug

### Verificar dados do servidor:
```
GET http://192.168.0.12:5000/api/dados
```

### Enviar dados manualmente:
```
POST http://192.168.0.12:5000/api/dados/operador_proa_bombordo
Body: {"valor": "Teste"}
```

## 🎉 Resultado Esperado

✅ **Sucesso**: Valores digitados em qualquer dispositivo aparecem automaticamente em todos os outros dispositivos da rede em tempo real.

✅ **Persistência**: Dados permanecem salvos mesmo após fechar e reabrir o navegador.

✅ **Performance**: Sistema responde rapidamente sem travamentos.

---

**Status do Sistema:** 🟢 ATIVO - Sincronização entre máquinas implementada com sucesso! 