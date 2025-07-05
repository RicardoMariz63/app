from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, make_response
import json
import os
import hashlib
import secrets
import threading
from datetime import datetime, timedelta
from flask_cors import CORS

# Flask configurado para usar o diretório templates padrão
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Arquivo para armazenar dados persistentes
DATA_FILE = 'dados_docagem.json'

# Sistema de autenticação
USUARIOS = {
    'admin@docagem.com': {
        'senha': hashlib.sha256('admin123'.encode()).hexdigest(),
        'nome': 'Administrador',
        'perfil': 'admin',
        'ativo': True,
        'criado_em': '2024-01-01 00:00:00'
    },
    'operador@docagem.com': {
        'senha': hashlib.sha256('operador123'.encode()).hexdigest(),
        'nome': 'Operador',
        'perfil': 'operador',
        'ativo': True,
        'criado_em': '2024-01-01 00:00:00'
    },
    'ricardo@docagem.com': {
        'senha': hashlib.sha256('1234'.encode()).hexdigest(),
        'nome': 'Ricardo',
        'perfil': 'operador',
        'ativo': True,
        'criado_em': '2024-01-01 00:00:00'
    },
    'docagem@docagem.com': {
        'senha': hashlib.sha256('1234'.encode()).hexdigest(),
        'nome': 'Docagem',
        'perfil': 'visualizador',
        'ativo': True,
        'criado_em': '2024-01-01 00:00:00'
    }
}

# Páginas disponíveis no sistema
PAGINAS_DISPONIVEIS = {
    'ProaBombordo.html': {
        'nome': 'Proa Bombordo',
        'categoria': 'OPERACIONAL',
        'descricao': 'Controle da seção de proa bombordo do navio'
    },
    'ProaBoreste.html': {
        'nome': 'Proa Boreste',
        'categoria': 'OPERACIONAL',
        'descricao': 'Controle da seção de proa boreste do navio'
    },
    'PopaBombordo.html': {
        'nome': 'Popa Bombordo',
        'categoria': 'OPERACIONAL',
        'descricao': 'Controle da seção de popa bombordo do navio'
    },
    'PopaBoreste.html': {
        'nome': 'Popa Boreste',
        'categoria': 'OPERACIONAL',
        'descricao': 'Controle da seção de popa boreste do navio'
    },
    'controle.html': {
        'nome': 'Controle Central',
        'categoria': 'SUPERVISAO',
        'descricao': 'Painel central de supervisão e monitoramento'
    },
    'admin': {
        'nome': 'Administração',
        'categoria': 'ADMINISTRACAO',
        'descricao': 'Gerenciamento de usuários e permissões do sistema'
    }
}

# Perfis de acesso padrão
PERFIS_PADRAO = {
    'admin': {
        'nome': 'Administrador',
        'descricao': 'Acesso total ao sistema, pode gerenciar usuários',
        'permissoes': ['gerenciar_usuarios', 'acessar_todas_paginas', 'editar_dados', 'visualizar_relatorios'],
        'paginas_permitidas': []  # Será preenchido na inicialização
    },
    'operador': {
        'nome': 'Operador',
        'descricao': 'Acesso operacional às seções do navio',
        'permissoes': ['acessar_paginas_operacionais', 'editar_dados', 'visualizar_relatorios'],
        'paginas_permitidas': ['ProaBombordo.html', 'ProaBoreste.html', 'PopaBombordo.html', 'PopaBoreste.html']
    },
    'supervisor': {
        'nome': 'Supervisor',
        'descricao': 'Acesso de supervisão e relatórios',
        'permissoes': ['acessar_paginas_limitadas', 'editar_dados_limitados', 'visualizar_relatorios'],
        'paginas_permitidas': ['controle.html']
    },
    'visualizador': {
        'nome': 'Visualizador',
        'descricao': 'Apenas visualização de dados',
        'permissoes': ['visualizar_dados'],
        'paginas_permitidas': ['controle.html']
    },
    'popa_bombordo': {
        'nome': 'Popa Bombordo',
        'descricao': 'Acesso específico à seção de Popa Bombordo',
        'permissoes': ['acessar_paginas_operacionais', 'editar_dados'],
        'paginas_permitidas': ['PopaBombordo.html', 'controle.html']
    },
    'popa_boreste': {
        'nome': 'Popa Boreste',
        'descricao': 'Acesso específico à seção de Popa Boreste',
        'permissoes': ['acessar_paginas_operacionais', 'editar_dados'],
        'paginas_permitidas': ['PopaBoreste.html', 'controle.html']
    },
    'proa_bombordo': {
        'nome': 'Proa Bombordo',
        'descricao': 'Acesso específico à seção de Proa Bombordo',
        'permissoes': ['acessar_paginas_operacionais', 'editar_dados'],
        'paginas_permitidas': ['ProaBombordo.html', 'controle.html']
    },
    'proa_boreste': {
        'nome': 'Proa Boreste',
        'descricao': 'Acesso específico à seção de Proa Boreste',
        'permissoes': ['acessar_paginas_operacionais', 'editar_dados'],
        'paginas_permitidas': ['ProaBoreste.html', 'controle.html']
    }
}

# Inicializar PERFIS_ACESSO com os perfis padrão
PERFIS_ACESSO = PERFIS_PADRAO.copy()

# Lock para controle de concorrência no salvamento de perfis
perfis_lock = threading.Lock()

# Arquivo para armazenar usuários
USUARIOS_FILE = 'usuarios.json'

def carregar_usuarios():
    """Carrega usuários do arquivo JSON se existir"""
    global USUARIOS
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
                USUARIOS.update(json.load(f))
        except:
            pass

def salvar_usuarios():
    """Salva usuários no arquivo JSON"""
    try:
        with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(USUARIOS, f, ensure_ascii=False, indent=2)
    except:
        pass

def verificar_permissao(email, permissao):
    """Verifica se um usuário tem uma permissão específica"""
    if email in USUARIOS:
        usuario = USUARIOS[email]
        if not usuario.get('ativo', True):
            return False
        perfil = usuario.get('perfil', 'visualizador')
        if perfil in PERFIS_ACESSO:
            return permissao in PERFIS_ACESSO[perfil]['permissoes']
    return False

def verificar_acesso_pagina(email, pagina):
    """Verifica se um usuário pode acessar uma página específica"""
    if email in USUARIOS:
        usuario = USUARIOS[email]
        if not usuario.get('ativo', True):
            return False
        
        perfil = usuario.get('perfil', 'visualizador')
        if perfil in PERFIS_ACESSO:
            # Admin tem acesso a tudo
            if 'gerenciar_usuarios' in PERFIS_ACESSO[perfil]['permissoes']:
                return True
            
            # Verificar se a página está na lista de páginas permitidas
            paginas_permitidas = PERFIS_ACESSO[perfil].get('paginas_permitidas', [])
            return pagina in paginas_permitidas
    return False

def obter_paginas_usuario(email):
    """Obtém lista de páginas que o usuário pode acessar"""
    if email in USUARIOS:
        usuario = USUARIOS[email]
        perfil = usuario.get('perfil', 'visualizador')
        if perfil in PERFIS_ACESSO:
            return PERFIS_ACESSO[perfil].get('paginas_permitidas', [])
    return []

def admin_requerido():
    """Middleware para verificar se o usuário é admin"""
    email = autenticacao_requerida()
    if not email:
        return None

    if email not in USUARIOS:
        return None

    usuario = USUARIOS[email]
    if not usuario.get('ativo', True):
        return None

    perfil = usuario.get('perfil')
    if perfil != 'admin':
        return None

    return email

def pagina_requerida(pagina):
    """Middleware para verificar acesso a uma página específica"""
    email = autenticacao_requerida()
    if email and verificar_acesso_pagina(email, pagina):
        return email
    return None

# Tokens de sessão ativos (em produção, usar Redis ou banco de dados)
tokens_ativos = {}

def gerar_token():
    """Gera um token de sessão único"""
    return secrets.token_urlsafe(32)

def verificar_token(token):
    """Verifica se um token é válido e não expirou"""
    if token in tokens_ativos:
        if datetime.now() < tokens_ativos[token]['expira']:
            return tokens_ativos[token]['email']
        else:
            # Token expirado, remover
            del tokens_ativos[token]
    return None

def autenticacao_requerida():
    """Middleware para verificar autenticação"""
    # Primeiro tenta pegar do header Authorization (para APIs)
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        email = verificar_token(token)
        if email:
            return email
    
    # Se não tem header, tenta pegar do cookie (para navegação HTML)
    token = request.cookies.get('authToken')
    if token:
        email = verificar_token(token)
        if email:
            return email
    
    return None

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

# Função para inicializar perfis
def inicializar_perfis():
    """Inicializa os perfis com valores padrão"""
    global PERFIS_ACESSO
    PERFIS_ACESSO = PERFIS_PADRAO.copy()
    # Garantir que admin tenha acesso a todas as páginas
    PERFIS_ACESSO['admin']['paginas_permitidas'] = list(PAGINAS_DISPONIVEIS.keys())

# Função para salvar alterações nos perfis (versão simplificada)
def salvar_perfis():
    """Salva as alterações nos perfis em um arquivo JSON"""
    try:
        print("🔄 Iniciando salvamento simplificado de perfis...")
        print(f"📊 Dados atuais dos perfis: {len(PERFIS_ACESSO)} perfis encontrados")

        # Salvar diretamente no arquivo
        print("📝 Escrevendo arquivo perfis.json...")
        with open('perfis.json', 'w', encoding='utf-8') as f:
            json.dump(PERFIS_ACESSO, f, ensure_ascii=False, indent=2)
        print("✅ Arquivo salvo com sucesso")

        print("✅ Perfis salvos com sucesso")
        return True

    except Exception as e:
        print(f"❌ Erro ao salvar perfis: {e}")
        print(f"🔍 Tipo do erro final: {type(e).__name__}")
        print(f"🔍 Detalhes do erro final: {str(e)}")
        return False
# Função para carregar perfis
def carregar_perfis():
    """Carrega os perfis do arquivo JSON se existir, mantendo valores padrão"""
    global PERFIS_ACESSO
    try:
        print("🔄 Iniciando carregamento de perfis...")
        # Inicializar com valores padrão
        inicializar_perfis()
        
        # Tentar carregar arquivo principal
        if os.path.exists('perfis.json'):
            try:
                print("📖 Lendo arquivo de perfis...")
                with open('perfis.json', 'r', encoding='utf-8') as f:
                    perfis_salvos = json.load(f)
                print("✅ Arquivo lido com sucesso")
            except Exception as e:
                print(f"⚠️ Erro ao ler arquivo principal: {e}")
                # Se falhar, tentar carregar backup
                if os.path.exists('perfis.json.bak'):
                    print("🔄 Arquivo principal corrompido, tentando backup...")
                    with open('perfis.json.bak', 'r', encoding='utf-8') as f:
                        perfis_salvos = json.load(f)
                    print("✅ Backup carregado com sucesso")
                    # Restaurar backup como arquivo principal
                    with open('perfis.json', 'w', encoding='utf-8') as f:
                        json.dump(perfis_salvos, f, ensure_ascii=False, indent=2)
                    print("✅ Backup restaurado como arquivo principal")
                else:
                    raise Exception("Arquivo de perfis corrompido e sem backup")
                
            # Validar dados carregados
            print("🔍 Validando dados carregados...")
            for perfil_id, perfil in perfis_salvos.items():
                if not isinstance(perfil, dict):
                    raise ValueError(f"Perfil {perfil_id} inválido no arquivo")
                if 'nome' not in perfil or 'permissoes' not in perfil:
                    raise ValueError(f"Perfil {perfil_id} com campos obrigatórios ausentes")
                
            # Mesclar perfis salvos com padrões
            print("🔄 Mesclando com configurações padrão...")
            for perfil_id, perfil in perfis_salvos.items():
                if perfil_id in PERFIS_ACESSO:
                    PERFIS_ACESSO[perfil_id].update(perfil)
                        
        # Garantir que admin sempre tenha todas as páginas
        PERFIS_ACESSO['admin']['paginas_permitidas'] = list(PAGINAS_DISPONIVEIS.keys())
        
        print("✅ Perfis carregados com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar perfis: {e}")
        # Em caso de erro, manter os valores padrão
        print("⚠️ Mantendo valores padrão devido ao erro")
        inicializar_perfis()
        return False

# Carregar dados na inicialização
carregar_dados()
carregar_usuarios()
inicializar_perfis()  # Inicializar os perfis
carregar_perfis()     # Carregar perfis salvos se existirem

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard principal - requer autenticação"""
    email = autenticacao_requerida()
    if not email:
        return redirect('/')
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de autenticação"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower()
        senha = data.get('senha', '')
        
        if not email or not senha:
            return jsonify({'status': 'erro', 'mensagem': 'E-mail e senha são obrigatórios'}), 400
        
        if email not in USUARIOS:
            return jsonify({'status': 'erro', 'mensagem': 'Usuário não encontrado'}), 401
        
        usuario = USUARIOS[email]
        if not usuario.get('ativo', True):
            return jsonify({'status': 'erro', 'mensagem': 'Usuário inativo'}), 401
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        if senha_hash != usuario['senha']:
            return jsonify({'status': 'erro', 'mensagem': 'Senha incorreta'}), 401
        
        # Gerar token com validade de 24 horas
        token = gerar_token()
        tokens_ativos[token] = {
            'email': email,
            'expira': datetime.now() + timedelta(hours=24)
        }
        
        # Preparar resposta
        response = jsonify({
            'status': 'sucesso',
            'token': token,
            'email': email,
            'perfil': usuario['perfil'],
            'paginas_permitidas': obter_paginas_usuario(email)
        })
        
        # Configurar cookie de autenticação
        response.set_cookie(
            'authToken', 
            token,
            httponly=False,  # Permitir acesso via JavaScript
            secure=False,    # Permitir HTTP em desenvolvimento
            samesite='Lax', # Mais permissivo que Strict
            max_age=86400   # 24 horas em segundos
        )
        
        return response
        
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/api/verificar-token', methods=['GET'])
def verificar_token_endpoint():
    """Verifica se o token de autenticação é válido"""
    email = autenticacao_requerida()
    if email:
        # Obter informações completas do usuário
        perfil_usuario = USUARIOS[email].get('perfil', 'visualizador')
        return jsonify({
            'status': 'sucesso',
            'email': email,
            'usuario': USUARIOS[email]['nome'],
            'perfil': perfil_usuario,
            'permissoes': PERFIS_ACESSO.get(perfil_usuario, {}).get('permissoes', []),
            'paginas_permitidas': PERFIS_ACESSO.get(perfil_usuario, {}).get('paginas_permitidas', [])
        })
    else:
        return jsonify({
            'status': 'erro',
            'mensagem': 'Token inválido ou expirado'
        }), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Endpoint de logout"""
    # Pegar token do header ou cookie
    token = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    else:
        token = request.cookies.get('authToken')
    
    # Remover token da lista de tokens ativos
    if token and token in tokens_ativos:
        del tokens_ativos[token]
    
    # Criar resposta e limpar cookie
    response = make_response(jsonify({'status': 'sucesso', 'mensagem': 'Logout realizado'}))
    response.set_cookie('authToken', '', expires=0)
    return response

@app.route('/ProaBombordo.html')
def proa_bombordo():
    email = pagina_requerida('ProaBombordo.html')
    if not email:
        return redirect('/')
    return render_template('ProaBombordo.html')

@app.route('/ProaBoreste.html')
def proa_boreste():
    email = pagina_requerida('ProaBoreste.html')
    if not email:
        return redirect('/')
    return render_template('ProaBoreste.html')

@app.route('/PopaBombordo.html')
def popa_bombordo():
    email = pagina_requerida('PopaBombordo.html')
    if not email:
        return redirect('/')
    return render_template('PopaBombordo.html')

@app.route('/PopaBoreste.html')
def popa_boreste():
    email = pagina_requerida('PopaBoreste.html')
    if not email:
        return redirect('/')
    return render_template('PopaBoreste.html')

@app.route('/controle.html')
def controle():
    email = pagina_requerida('controle.html')
    if not email:
        return redirect('/')
    return render_template('controle.html')

@app.route('/admin')
def admin_page():
    email = pagina_requerida('admin')
    if not email:
        return redirect('/')
    return render_template('admin.html')

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    """Lista todos os usuários - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    usuarios_lista = []
    for email_usuario, dados in USUARIOS.items():
        usuarios_lista.append({
            'email': email_usuario,
            'nome': dados['nome'],
            'perfil': dados.get('perfil', 'visualizador'),
            'ativo': dados.get('ativo', True),
            'criado_em': dados.get('criado_em', ''),
            'perfil_nome': PERFIS_ACESSO.get(dados.get('perfil', 'visualizador'), {}).get('nome', 'Desconhecido')
        })
    
    return jsonify({
        'status': 'sucesso',
        'usuarios': usuarios_lista,
        'perfis_disponiveis': PERFIS_ACESSO,
        'paginas_disponiveis': PAGINAS_DISPONIVEIS
    })

@app.route('/api/usuarios/<email_usuario>', methods=['PUT'])
def atualizar_usuario(email_usuario):
    """Atualiza dados de um usuário - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    try:
        data = request.get_json()
        
        if email_usuario not in USUARIOS:
            return jsonify({'status': 'erro', 'mensagem': 'Usuário não encontrado'}), 404
        
        # Atualizar campos permitidos
        if 'perfil' in data and data['perfil'] in PERFIS_ACESSO:
            USUARIOS[email_usuario]['perfil'] = data['perfil']
        
        if 'ativo' in data:
            USUARIOS[email_usuario]['ativo'] = bool(data['ativo'])
        
        if 'nome' in data and data['nome'].strip():
            USUARIOS[email_usuario]['nome'] = data['nome'].strip()
        
        # Salvar mudanças
        salvar_usuarios()
        
        return jsonify({
            'status': 'sucesso',
            'mensagem': 'Usuário atualizado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/api/usuarios', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    try:
        data = request.get_json()
        
        email_novo = data.get('email', '').lower().strip()
        nome = data.get('nome', '').strip()
        senha = data.get('senha', '').strip()
        perfil = data.get('perfil', 'visualizador')
        
        # Validações
        if not email_novo or '@' not in email_novo:
            return jsonify({'status': 'erro', 'mensagem': 'E-mail inválido'}), 400
        
        if email_novo in USUARIOS:
            return jsonify({'status': 'erro', 'mensagem': 'E-mail já existe'}), 400
        
        if not nome:
            return jsonify({'status': 'erro', 'mensagem': 'Nome é obrigatório'}), 400
        
        if not senha:
            return jsonify({'status': 'erro', 'mensagem': 'Senha é obrigatória'}), 400
        
        if perfil not in PERFIS_ACESSO:
            return jsonify({'status': 'erro', 'mensagem': 'Perfil inválido'}), 400
        
        # Criar usuário
        USUARIOS[email_novo] = {
            'senha': hashlib.sha256(senha.encode()).hexdigest(),
            'nome': nome,
            'perfil': perfil,
            'ativo': True,
            'criado_em': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Salvar
        salvar_usuarios()
        
        return jsonify({
            'status': 'sucesso',
            'mensagem': 'Usuário criado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/api/usuarios/<email_usuario>', methods=['DELETE'])
def deletar_usuario(email_usuario):
    """Deleta um usuário - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    try:
        if email_usuario not in USUARIOS:
            return jsonify({'status': 'erro', 'mensagem': 'Usuário não encontrado'}), 404
        
        if email_usuario == email:
            return jsonify({'status': 'erro', 'mensagem': 'Não é possível deletar seu próprio usuário'}), 400
        
        # Verificar se não é o último admin
        admins = [e for e, u in USUARIOS.items() if u.get('perfil') == 'admin' and u.get('ativo', True)]
        if USUARIOS[email_usuario].get('perfil') == 'admin' and len(admins) <= 1:
            return jsonify({'status': 'erro', 'mensagem': 'Não é possível deletar o último administrador'}), 400
        
        del USUARIOS[email_usuario]
        salvar_usuarios()
        
        return jsonify({
            'status': 'sucesso',
            'mensagem': 'Usuário deletado com sucesso'
        })
        
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/api/perfis', methods=['GET'])
def listar_perfis():
    """Lista todos os perfis com suas configurações - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    # Preparar dados estruturados para o frontend
    perfis_formatados = {}
    for perfil_id, perfil in PERFIS_ACESSO.items():
        perfis_formatados[perfil_id] = {
            'nome': perfil['nome'],
            'descricao': perfil['descricao'],
            'permissoes': perfil['permissoes'],
            'paginas_permitidas': perfil.get('paginas_permitidas', [])
        }
    
    # Preparar lista de páginas com categorias
    paginas_formatadas = []
    for arquivo, info in PAGINAS_DISPONIVEIS.items():
        paginas_formatadas.append({
            'arquivo': arquivo,
            'nome': info['nome'],
            'categoria': info['categoria'],
            'descricao': info.get('descricao', '')
        })
    
    return jsonify({
        'status': 'sucesso',
        'perfis': perfis_formatados,
        'paginas': paginas_formatadas
    })


@app.route('/api/perfis/<perfil_id>/paginas', methods=['PUT'])
def atualizar_paginas_perfil(perfil_id):
    """Atualiza as páginas permitidas para um perfil específico - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    try:
        print(f"🔄 Iniciando atualização do perfil: {perfil_id}")
        
        if perfil_id not in PERFIS_ACESSO:
            print(f"❌ Perfil não encontrado: {perfil_id}")
            return jsonify({'status': 'erro', 'mensagem': 'Perfil não encontrado'}), 404
        
        data = request.get_json()
        if not isinstance(data, dict) or 'paginas_permitidas' not in data:
            print("❌ Dados inválidos recebidos")
            return jsonify({'status': 'erro', 'mensagem': 'Dados inválidos'}), 400
            
        paginas_permitidas = data.get('paginas_permitidas', [])
        if not isinstance(paginas_permitidas, list):
            print("❌ Lista de páginas inválida")
            return jsonify({'status': 'erro', 'mensagem': 'Lista de páginas inválida'}), 400
        
        print(f"📋 Páginas recebidas: {paginas_permitidas}")
        
        # Validar se todas as páginas existem
        paginas_invalidas = [pagina for pagina in paginas_permitidas if pagina not in PAGINAS_DISPONIVEIS]
        if paginas_invalidas:
            print(f"❌ Páginas inválidas encontradas: {paginas_invalidas}")
            return jsonify({
                'status': 'erro', 
                'mensagem': f'Páginas inválidas: {", ".join(paginas_invalidas)}'
            }), 400
        
        # Se for admin, garantir que tenha todas as páginas
        if perfil_id == 'admin':
            print("👑 Perfil admin: garantindo acesso a todas as páginas")
            paginas_permitidas = list(PAGINAS_DISPONIVEIS.keys())
        
        # Garantir que perfis específicos mantenham suas páginas principais
        paginas_obrigatorias = {
            'popa_bombordo': ['PopaBombordo.html'],
            'popa_boreste': ['PopaBoreste.html'],
            'proa_bombordo': ['ProaBombordo.html'],
            'proa_boreste': ['ProaBoreste.html']
        }
        
        if perfil_id in paginas_obrigatorias:
            print(f"🔒 Garantindo páginas obrigatórias para {perfil_id}")
            for pagina in paginas_obrigatorias[perfil_id]:
                if pagina not in paginas_permitidas:
                    print(f"➕ Adicionando página obrigatória: {pagina}")
                    paginas_permitidas.append(pagina)
        
        # Fazer backup do estado atual antes da atualização
        print("📑 Criando backup do estado atual do perfil")
        perfil_backup = PERFIS_ACESSO[perfil_id].copy()
        
        # Atualizar apenas as páginas permitidas, mantendo outras configurações
        print("📝 Atualizando páginas permitidas")
        PERFIS_ACESSO[perfil_id]['paginas_permitidas'] = paginas_permitidas
        
        # Tentar salvar alterações
        print("💾 Tentando salvar alterações...")
        if not salvar_perfis():
            # Se falhar, restaurar estado anterior
            print("⚠️ Falha ao salvar, restaurando estado anterior")
            PERFIS_ACESSO[perfil_id] = perfil_backup
            return jsonify({
                'status': 'erro',
                'mensagem': 'Erro ao salvar alterações. As mudanças foram revertidas.'
            }), 500
        
        # Forçar revalidação de tokens para todos os usuários deste perfil (exceto o admin que está fazendo a alteração)
        print("🔄 Atualizando tokens dos usuários afetados")
        usuarios_afetados = [email_user for email_user, dados in USUARIOS.items() if dados.get('perfil') == perfil_id and email_user != email]
        for email_usuario in usuarios_afetados:
            print(f"🔑 Invalidando tokens para: {email_usuario}")
            tokens_para_remover = [token for token, dados in tokens_ativos.items() if dados['email'] == email_usuario]
            for token in tokens_para_remover:
                del tokens_ativos[token]

        if usuarios_afetados:
            print(f"🔑 Tokens invalidados para {len(usuarios_afetados)} usuários")
        else:
            print("ℹ️ Nenhum token foi invalidado (apenas o admin atual)")
        
        print("✅ Atualização concluída com sucesso")
        return jsonify({
            'status': 'sucesso',
            'mensagem': f'Páginas do perfil {PERFIS_ACESSO[perfil_id]["nome"]} atualizadas com sucesso',
            'perfil': PERFIS_ACESSO[perfil_id]
        })
        
    except Exception as e:
        print(f"❌ Erro ao atualizar perfil: {str(e)}")
        # Se houver backup e ocorrer erro, tentar restaurar
        if 'perfil_backup' in locals():
            print("🔄 Restaurando backup após erro")
            PERFIS_ACESSO[perfil_id] = perfil_backup
        
        return jsonify({
            'status': 'erro', 
            'mensagem': f'Erro ao atualizar perfil: {str(e)}'
        }), 500

@app.route('/api/usuarios/<email_usuario>/paginas', methods=['GET'])
def obter_paginas_usuario_api(email_usuario):
    """Obtém as páginas que um usuário específico pode acessar - apenas admin"""
    email = admin_requerido()
    if not email:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 403
    
    try:
        if email_usuario not in USUARIOS:
            return jsonify({'status': 'erro', 'mensagem': 'Usuário não encontrado'}), 404
        
        paginas_permitidas = obter_paginas_usuario(email_usuario)
        perfil = USUARIOS[email_usuario].get('perfil', 'visualizador')
        
        return jsonify({
            'status': 'sucesso',
            'email': email_usuario,
            'perfil': perfil,
            'paginas_permitidas': paginas_permitidas,
            'paginas_disponiveis': PAGINAS_DISPONIVEIS
        })
        
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/navio.png')
def navio_image():
    return send_from_directory('.', 'navio.png')

@app.route('/sync.js')
def sync_js():
    return send_from_directory('.', 'sync.js', mimetype='application/javascript')

@app.route('/auth.js')
def auth_js():
    return send_from_directory('.', 'auth.js', mimetype='application/javascript')

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

@app.route('/api/dados/solicitar', methods=['POST'])
def solicitar_dados():
    """Endpoint para solicitar dados - dispara alarme2 nas páginas operacionais"""
    try:
        data = request.get_json()
        comando = data.get('comando', '')
        timestamp = data.get('timestamp', '')

        print(f"📡 Solicitação de dados recebida: {comando} em {timestamp}")

        if comando == 'solicitar_dados':
            # Criar comando de alarme2 para disparar nas páginas operacionais
            comando_alarme2 = {
                'comando': 'tocar_alarme2',
                'timestamp': timestamp,
                'origem': 'solicitar_dados'
            }

            # Armazenar o comando no sistema (temporário)
            dados_sistema['comando_alarme2'] = comando_alarme2
            print(f"🔊 Comando de alarme2 criado para solicitação de dados: {comando_alarme2}")

            return jsonify({
                'status': 'sucesso',
                'mensagem': 'Solicitação de dados enviada com sucesso',
                'comando_alarme2': comando_alarme2
            })
        else:
            return jsonify({
                'status': 'erro',
                'mensagem': 'Comando inválido'
            }), 400

    except Exception as e:
        print(f"❌ Erro ao processar solicitação de dados: {e}")
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
    print("🚢 Sistema de Controle de Docagem iniciando...")
    
    print("📂 Carregando dados do sistema...")
    carregar_dados()
    
    print("👥 Carregando usuários...")
    carregar_usuarios()
    
    print("🔐 Inicializando perfis...")
    inicializar_perfis()
    
    print("📋 Carregando configurações de perfis...")
    carregar_perfis()
    
    print("\n✅ Sistema inicializado com sucesso!")
    print("📱 Acesse de qualquer dispositivo na rede em:")
    print("   http://[IP_DO_SERVIDOR]:5000")
    print("💡 Para descobrir seu IP, execute 'ipconfig' no terminal")
    print("🔄 Sincronização entre máquinas ativada!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
