from flask import Flask, render_template, send_from_directory, request, jsonify
import json
import os

# O argumento template_folder='.' diz ao Flask para procurar 
# o arquivo html na mesma pasta que este script.
app = Flask(__name__, template_folder='.')

# Arquivo para armazenar dados persistentes
DATA_FILE = 'dados_docagem.json'

# Dados globais do sistema
dados_sistema = {
    'operador_proa_bombordo': '',
    'y_proa_bombordo': '',
    'z_bombordo': '',
    'operador_proa_boreste': '',
    'valor_proa_boreste': '',
    'operador_popa_bombordo': '',
    'valor_popa_bombordo': '',
    'operador_popa_boreste': '',
    'valor_popa_boreste': '',
    'operador_y_proa_bombordo': '',
    'operador_x_popa_bombordo': '',
    'x_popa_bombordo': '',
    'operador_y_popa_bombordo': '',
    'y_popa_bombordo': '',
    'comando_alarme2': None
}

def carregar_dados():
    """Carrega dados do arquivo JSON se existir"""
    global dados_sistema
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                dados_sistema.update(json.load(f))
        except:
            pass

def salvar_dados():
    """Salva dados no arquivo JSON (exceto comandos temporários)"""
    try:
        # Filtrar comandos temporários
        dados_para_salvar = {k: v for k, v in dados_sistema.items() 
                           if not k.startswith('comando_')}
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, ensure_ascii=False, indent=2)
    except:
        pass

# Carregar dados na inicialização
carregar_dados()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ProaBombordo.html')
def proa_bombordo():
    return render_template('ProaBombordo.html')

@app.route('/ProaBoreste.html')
def proa_boreste():
    return render_template('ProaBoreste.html')

@app.route('/PopaBombordo.html')
def popa_bombordo():
    return render_template('PopaBombordo.html')

@app.route('/PopaBoreste.html')
def popa_boreste():
    return render_template('PopaBoreste.html')

@app.route('/controle.html')
def controle():
    return render_template('controle.html')

@app.route('/navio.png')
def navio_image():
    return send_from_directory('.', 'navio.png')

@app.route('/sync.js')
def sync_js():
    return send_from_directory('.', 'sync.js', mimetype='application/javascript')

@app.route('/alarme1.mp3')
def alarme1_audio():
    return send_from_directory('.', 'alarme1.mp3', mimetype='audio/mpeg')

@app.route('/alarme2.mp3')
def alarme2_audio():
    return send_from_directory('.', 'alarme2.mp3', mimetype='audio/mpeg')

# APIs para sincronização de dados
@app.route('/api/dados', methods=['GET'])
def obter_dados():
    """Retorna todos os dados atuais"""
    return jsonify(dados_sistema)

@app.route('/api/dados', methods=['POST'])
def atualizar_dados():
    """Atualiza um ou mais valores"""
    try:
        novos_dados = request.get_json()
        if novos_dados:
            dados_sistema.update(novos_dados)
            salvar_dados()
            return jsonify({'status': 'sucesso', 'dados': dados_sistema})
        return jsonify({'status': 'erro', 'mensagem': 'Dados inválidos'}), 400
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/api/dados/<campo>', methods=['POST'])
def atualizar_campo(campo):
    """Atualiza um campo específico"""
    try:
        data = request.get_json()
        
        # Tratamento especial para comando de alarme2
        if campo == 'comando_alarme2':
            dados_sistema[campo] = data
            print(f"🔊 Comando de alarme2 recebido: {data}")
            # Não salva comandos no arquivo (são temporários)
            return jsonify({'status': 'sucesso', 'campo': campo, 'comando': data})
        
        # Tratamento normal para outros campos
        valor = data.get('valor', '')
        if campo in dados_sistema:
            dados_sistema[campo] = valor
            salvar_dados()
            return jsonify({'status': 'sucesso', 'campo': campo, 'valor': valor})
        return jsonify({'status': 'erro', 'mensagem': 'Campo não encontrado'}), 404
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

if __name__ == '__main__':
    # Roda a aplicação em modo de desenvolvimento.
    # host='0.0.0.0' permite conexões de qualquer IP da rede
    # port=5000 define a porta padrão
    print("🚢 Sistema de Controle de Docagem iniciado!")
    print("📱 Acesse de qualquer dispositivo na rede em:")
    print("   http://[IP_DO_SERVIDOR]:5000")
    print("💡 Para descobrir seu IP, execute 'ipconfig' no terminal")
    print("🔄 Sincronização entre máquinas ativada!")
    app.run(debug=True, host='0.0.0.0', port=5000)
