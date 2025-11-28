"""
Microserviço: Recomendação
Porta: 5007
Responsabilidade: Gerar recomendações de produtos baseadas no histórico
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, jsonify
from flask_cors import CORS
from shared.databases import Historico, Produtos, HistoricoQuery, ProdutoQuery
from collections import Counter

app = Flask(__name__)
CORS(app)

def obter_produtos_cliente(cliente_id):
    """Busca todos os produtos comprados por um cliente no histórico"""
    # [TinyDB Select]: Filtra registros onde cliente_id bate
    registros = Historico.search(HistoricoQuery.cliente_id == cliente_id)

    produtos = []
    for registro in registros:
        produtos.extend(registro.get('produtos', []))

    return produtos

def calcular_recomendacoes(cliente_id, num_recomendacoes=3):
    """
    Algoritmo de Recomendação Híbrido Simplificado.
    [Conceito para o Estagiário]: COLD START (Problema da Partida Fria)
    Sistemas de recomendação sofrem quando não têm dados do usuário.
    
    Estratégia em Camadas:
    1. (Hot): Se o usuário já comprou, recomendamos o que ele gosta (Frequência).
    2. (Warm): Se o usuário é novo, recomendamos o que TODO MUNDO gosta (Populares).
    3. (Cold): Se o site é novo e não tem vendas, mostramos qualquer coisa (Catálogo) para não ficar vazio.
    """
    # Busca histórico pessoal
    produtos_cliente = obter_produtos_cliente(cliente_id)

    # --- Estratégia 1: Recomendação Personalizada (HOT) ---
    if produtos_cliente:
        contador = Counter(produtos_cliente)
        # Pega os 'num_recomendacoes' mais frequentes
        mais_comprados = contador.most_common(num_recomendacoes)
        produto_ids = [pid for pid, count in mais_comprados]
    else:
        # --- Estratégia 2: Mais Populares (WARM) ---
        todos_registros = Historico.all()
        todos_produtos = []

        for registro in todos_registros:
            todos_produtos.extend(registro.get('produtos', []))

        if todos_produtos:
            contador = Counter(todos_produtos)
            mais_populares = contador.most_common(num_recomendacoes)
            produto_ids = [pid for pid, count in mais_populares]
        else:
            # --- Estratégia 3: Fallback (COLD) ---
            produtos_catalogo = Produtos.all()
            produto_ids = [p['id'] for p in produtos_catalogo[:num_recomendacoes]]

    # Enriquece os IDs com os dados reais do produto (Nome, Preço, etc.)
    recomendacoes = []
    for produto_id in produto_ids:
        produto = Produtos.search(ProdutoQuery.id == produto_id)
        if produto:
            recomendacoes.append(produto[0])

    return recomendacoes

@app.route('/recomendacoes/<cliente_id>', methods=['GET'])
def obter_recomendacoes(cliente_id):
    """Endpoint para obter recomendações para um usuário específico"""
    try:
        recomendacoes = calcular_recomendacoes(cliente_id, num_recomendacoes=3)

        produtos_cliente = obter_produtos_cliente(cliente_id)
        tem_historico = len(produtos_cliente) > 0

        return jsonify({
            "cliente_id": cliente_id,
            "tipo": "personalizado" if tem_historico else "popular",
            "total_recomendacoes": len(recomendacoes),
            "recomendacoes": recomendacoes,
            "mensagem": "Recomendações baseadas no seu histórico" if tem_historico else "Produtos mais populares"
        }), 200

    except Exception as e:
        print(f"[RECOMENDACAO] Erro ao gerar recomendações: {str(e)}")
        return jsonify({"erro": "Erro ao gerar recomendações", "detalhes": str(e)}), 500

@app.route('/produtos-populares', methods=['GET'])
def produtos_populares():
    """Endpoint auxiliar para dashboards: Retorna Top 5 Global"""
    try:
        todos_registros = Historico.all()
        todos_produtos = []

        for registro in todos_registros:
            todos_produtos.extend(registro.get('produtos', []))

        if not todos_produtos:
            return jsonify({
                "mensagem": "Nenhum histórico de vendas disponível",
                "produtos": []
            }), 200

        contador = Counter(todos_produtos)
        mais_vendidos = contador.most_common(5)

        produtos_detalhados = []
        for produto_id, quantidade in mais_vendidos:
            produto = Produtos.search(ProdutoQuery.id == produto_id)
            if produto:
                produto_info = produto[0].copy()
                produto_info['quantidade_vendida'] = quantidade
                produtos_detalhados.append(produto_info)

        return jsonify({
            "total": len(produtos_detalhados),
            "produtos_mais_vendidos": produtos_detalhados
        }), 200

    except Exception as e:
        print(f"[RECOMENDACAO] Erro ao buscar produtos populares: {str(e)}")
        return jsonify({"erro": "Erro ao buscar produtos populares", "detalhes": str(e)}), 500

@app.route('/')
def index():
    """Diagnóstico do serviço"""
    total_registros = len(Historico.all())
    total_produtos = len(Produtos.all())

    return jsonify({
        "servico": "Recomendação",
        "porta": 5007,
        "algoritmo": "Baseado em frequência de compra",
        "registros_historico": total_registros,
        "produtos_catalogo": total_produtos,
        "endpoints": {
            "/recomendacoes/<cliente_id>": "Recomendações personalizadas",
            "/produtos-populares": "Produtos mais vendidos"
        }
    }), 200

if __name__ == '__main__':
    print("Microserviço Recomendação rodando na porta 5007")
    app.run(debug=True, port=5007)
