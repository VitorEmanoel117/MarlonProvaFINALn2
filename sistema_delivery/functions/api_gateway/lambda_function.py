"""
API Gateway - Porta de entrada para o sistema de delivery
Porta: 5000
Responsabilidade: Roteia requisições para os microserviços apropriados (Padrão Gateway)

[Explicação para o Estagiário]:
O API Gateway funciona como um "porteiro" ou "recepcionista". O cliente (frontend, app mobile, postman) 
SÓ conversa com ele. Ele sabe para qual microserviço interno (Receber, Processar, Recomendação) 
deve encaminhar o pedido. Isso esconde a complexidade do sistema do mundo externo.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from shared.databases import Produtos, Clientes, ProdutoQuery, ClienteQuery
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# URLs dos microserviços internos (Service Discovery estático)
# Em um ambiente real AWS, isso seria resolvido via DNS ou Service Discovery
RECEBER_PEDIDO_URL = "http://localhost:5001/receber"
PROCESSAR_PEDIDO_URL = "http://localhost:5003/pedidos"
RECOMENDACAO_URL = "http://localhost:5007/recomendacoes"

# =============== ROTAS DE PEDIDOS ===============

@app.route('/api/pedidos', methods=['POST'])
def criar_pedido():
    """
    Rota Pública: Criar Pedido.
    Encaminha a requisição para o microserviço 'Receber Pedido'.
    
    [Conceito]: Proxy Reverso
    Nós recebemos a requisição aqui e a "repassamos" (requests.post) para o serviço real na porta 5001.
    O cliente nem sabe que o serviço 5001 existe.
    """
    try:
        dados = request.get_json()

        # Chamada HTTP síncrona para o microserviço interno
        response = requests.post(RECEBER_PEDIDO_URL, json=dados, timeout=5)

        # Retorna a resposta EXATA que o microserviço devolveu
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Serviço de pedidos indisponível", "detalhes": str(e)}), 503

@app.route('/api/pedidos', methods=['GET'])
def listar_pedidos():
    """
    Rota Pública: Listar Pedidos.
    Consulta o microserviço 'Processar Pedido' (porta 5003) para obter status.
    """
    try:
        response = requests.get(PROCESSAR_PEDIDO_URL, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Serviço de pedidos indisponível", "detalhes": str(e)}), 503

# =============== ROTAS DE PRODUTOS ===============
# [Atenção Estagiário]: 
# Para operações CRUD simples (Create, Read, Update, Delete) de cadastros básicos,
# o Gateway pode acessar o banco DIRETAMENTE. Isso evita criar microserviços "triviais"
# que só repassam dados. É uma otimização comum.

@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    """Cadastra um novo produto no catálogo (Acesso direto ao TinyDB)"""
    dados = request.get_json()

    if not dados or 'nome' not in dados or 'preco' not in dados:
        return jsonify({"erro": "Campos 'nome' e 'preco' são obrigatórios"}), 400

    dados['id'] = str(uuid.uuid4())
    dados['data_criacao'] = datetime.now().isoformat()
    dados['estoque'] = dados.get('estoque', 100)

    # [TinyDB - Escrita]: Insere o dicionário diretamente no arquivo JSON
    Produtos.insert(dados)

    return jsonify({"mensagem": "Produto cadastrado", "produto": dados}), 201

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos os produtos disponíveis"""
    # [TinyDB - Leitura]: Traz todos os registros da tabela
    produtos = Produtos.all()
    return jsonify(produtos), 200

@app.route('/api/produtos/<produto_id>', methods=['GET'])
def buscar_produto(produto_id):
    """Busca um produto específico"""
    # [TinyDB - Consulta]: Busca onde o campo 'id' é igual ao parametro
    produto = Produtos.search(ProdutoQuery.id == produto_id)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(produto[0]), 200

@app.route('/api/produtos/<produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """Atualiza dados de um produto"""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido"}), 400

    dados.pop('id', None)
    dados['data_atualizacao'] = datetime.now().isoformat()

    # [TinyDB - Update]: Atualiza apenas os campos enviados
    num_atualizados = Produtos.update(dados, ProdutoQuery.id == produto_id)

    if num_atualizados == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produto_atualizado = Produtos.search(ProdutoQuery.id == produto_id)[0]
    return jsonify({"mensagem": "Produto atualizado", "produto": produto_atualizado}), 200

@app.route('/api/produtos/<produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    """Remove um produto do catálogo"""
    # [TinyDB - Delete]: Remove o registro fisicamente do JSON
    num_removidos = Produtos.remove(ProdutoQuery.id == produto_id)

    if num_removidos == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify({"mensagem": "Produto removido"}), 200

# =============== ROTAS DE CLIENTES ===============

@app.route('/api/clientes', methods=['POST'])
def criar_cliente():
    """Cadastra um novo cliente"""
    dados = request.get_json()

    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({"erro": "Campos 'nome' e 'email' são obrigatórios"}), 400

    dados['id'] = str(uuid.uuid4())
    dados['data_criacao'] = datetime.now().isoformat()

    # [TinyDB]: Persistência na tabela de clientes
    Clientes.insert(dados)

    return jsonify({"mensagem": "Cliente cadastrado", "cliente": dados}), 201

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    """Lista todos os clientes"""
    clientes = Clientes.all()
    return jsonify(clientes), 200

@app.route('/api/clientes/<cliente_id>', methods=['GET'])
def buscar_cliente(cliente_id):
    """Busca um cliente específico"""
    cliente = Clientes.search(ClienteQuery.id == cliente_id)

    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify(cliente[0]), 200

@app.route('/api/clientes/<cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """Atualiza dados de um cliente"""
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado fornecido"}), 400

    dados.pop('id', None)
    dados['data_atualizacao'] = datetime.now().isoformat()

    num_atualizados = Clientes.update(dados, ClienteQuery.id == cliente_id)

    if num_atualizados == 0:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    cliente_atualizado = Clientes.search(ClienteQuery.id == cliente_id)[0]
    return jsonify({"mensagem": "Cliente atualizado", "cliente": cliente_atualizado}), 200

@app.route('/api/clientes/<cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    """Remove um cliente"""
    num_removidos = Clientes.remove(ClienteQuery.id == cliente_id)

    if num_removidos == 0:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({"mensagem": "Cliente removido"}), 200

# =============== ROTAS DE RECOMENDAÇÃO ===============

@app.route('/api/recomendacoes/<cliente_id>', methods=['GET'])
def buscar_recomendacoes(cliente_id):
    """
    Rota Pública: Obter Recomendações.
    Consulta o microserviço 'Recomendação' (porta 5007).
    """
    try:
        response = requests.get(f"{RECOMENDACAO_URL}/{cliente_id}", timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Serviço de recomendações indisponível", "detalhes": str(e)}), 503

# =============== ROTA RAIZ ===============

@app.route('/')
def index():
    """Documentação simplificada da API"""
    return jsonify({
        "servico": "API Gateway - Sistema de Delivery",
        "versao": "1.0",
        "porta": 5000,
        "endpoints": {
            "pedidos": "/api/pedidos [POST, GET]",
            "produtos": "/api/produtos [POST, GET, GET/<id>, PUT/<id>, DELETE/<id>]",
            "clientes": "/api/clientes [POST, GET, GET/<id>, PUT/<id>, DELETE/<id>]",
            "recomendacoes": "/api/recomendacoes/<cliente_id> [GET]"
        }
    }), 200

if __name__ == '__main__':
    print("[API GATEWAY] Rodando na porta 5000")
    app.run(debug=True, port=5000)
