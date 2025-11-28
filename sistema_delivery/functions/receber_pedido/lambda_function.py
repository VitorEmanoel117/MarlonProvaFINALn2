"""
Microserviço: Receber Pedido
Porta: 5001
Responsabilidade: Receber pedidos e colocá-los na fila para validação
"""

import sys
import os
# Adiciona o diretório raiz ao sys.path para permitir a importação do módulo 'shared'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, request, jsonify
from flask_cors import CORS
from shared.filas import FILA_PEDIDOS  # Importa a fila em memória compartilhada
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/receber', methods=['POST'])
def receber_pedido():
    """
    Endpoint principal para recepção de pedidos.
    
    [Conceito para o Estagiário]: Padrão PRODUCER (Produtor)
    Este serviço NÃO processa o pedido. Ele apenas "produz" uma mensagem e a coloca na fila.
    
    Vantagens:
    1. Alta performance: O cliente recebe o "OK" em milissegundos, sem esperar validações pesadas.
    2. Resiliência: Se o validador cair, os pedidos ficam seguros na fila esperando ele voltar.
    3. Desacoplamento: Este serviço não sabe quem vai consumir, ele apenas joga na fila.
    
    Fluxo:
    1. Recebe JSON do cliente (via API Gateway)
    2. Valida estrutura básica dos dados (Defesa rápida)
    3. Cria objeto do pedido com ID único
    4. FILA.PUT(): Escreve na fila de memória
    5. Retorna 202 Accepted (Padrão HTTP para "Aceitei, mas vou processar depois")
    """
    try:
        dados = request.get_json()

        # --- 1. Validação de Entrada (Camada de Defesa) ---
        if not dados:
            return jsonify({"erro": "Nenhum dado fornecido"}), 400

        if 'cliente_id' not in dados:
            return jsonify({"erro": "Campo 'cliente_id' é obrigatório"}), 400

        if 'itens' not in dados or not isinstance(dados['itens'], list):
            return jsonify({"erro": "Campo 'itens' deve ser uma lista"}), 400

        # --- 2. Enriquecimento do Pedido ---
        # Cria um dicionário completo do pedido antes de ir para a fila
        pedido = {
            'pedido_id': str(uuid.uuid4()),  # Gera ID único para rastreamento
            'cliente_id': dados['cliente_id'],
            'itens': dados['itens'],
            'endereco_entrega': dados.get('endereco_entrega', ''),
            'observacoes': dados.get('observacoes', ''),
            'status': 'recebido',  # Status inicial
            'data_recebimento': datetime.now().isoformat()
        }

        # --- 3. Enfileiramento (Ação Crítica de Fila) ---
        # [Fila]: Escrevendo na memória (RAM). O consumidor (Worker) vai ler daqui.
        FILA_PEDIDOS.put(pedido)

        print(f"[RECEBER_PEDIDO] Pedido {pedido['pedido_id']} recebido e enviado para fila")

        # Retorna 202 Accepted: "Recebi, mas ainda vou processar"
        return jsonify({
            "mensagem": "Pedido recebido e enviado para processamento",
            "pedido_id": pedido['pedido_id'],
            "status": "aceito"
        }), 202

    except Exception as e:
        print(f"[RECEBER_PEDIDO] Erro: {str(e)}")
        return jsonify({"erro": "Erro ao processar pedido", "detalhes": str(e)}), 500

@app.route('/')
def index():
    """Rota de diagnóstico para verificar saúde do serviço"""
    return jsonify({
        "servico": "Receber Pedido",
        "porta": 5001,
        "status": "ativo",
        "fila": "FILA_PEDIDOS",
        # qsize() é útil para monitoramento: Se estiver muito alto, os consumers estão lentos
        "tamanho_fila_atual": FILA_PEDIDOS.qsize()  
    }), 200

if __name__ == '__main__':
    print("[RECEBER_PEDIDO] Microserviço rodando na porta 5001")
    app.run(debug=True, port=5001)
