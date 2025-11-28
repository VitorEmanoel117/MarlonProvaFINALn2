"""
Microserviço: Analytics
Porta: 5006
Responsabilidade: Coletar e analisar dados de pedidos
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, jsonify
from flask_cors import CORS
from shared.filas import FILA_ANALYTICS
from shared.databases import Historico
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

worker_ativo = False

def processar_fila():
    """
    Worker (Consumer) de Análise de Dados.
    
    [Conceito para o Estagiário]: ETL (Extract, Transform, Load)
    Este worker simula um processo de Data Engineering.
    
    1. EXTRACT (Extrair): Pega os dados brutos da FILA_ANALYTICS.
    2. TRANSFORM (Transformar): Seleciona apenas os campos relevantes para análise (KPIs), 
       como valor total e quantidade de itens, ignorando detalhes operacionais como endereço.
    3. LOAD (Carregar): Salva esses dados estruturados em uma tabela específica ('historico'), 
       que funciona como nosso Data Warehouse/Data Lake.
    """
    global worker_ativo
    print("[ANALYTICS] Worker de analytics iniciado")

    while worker_ativo:
        try:
            if not FILA_ANALYTICS.empty():
                # --- Consumo ---
                pedido = FILA_ANALYTICS.get(timeout=1)

                print(f"[ANALYTICS] Registrando dados do pedido {pedido['pedido_id']}")

                # --- Transformação (Schema para BI) ---
                registro = {
                    'pedido_id': pedido['pedido_id'],
                    'cliente_id': pedido['cliente_id'],
                    'total': pedido['total'],
                    'quantidade_itens': len(pedido['itens']),
                    'produtos': [item['produto_id'] for item in pedido['itens']],
                    'status': pedido['status'],
                    'data_registro': datetime.now().isoformat(),
                    'metodo_pagamento': pedido.get('metodo_pagamento', 'nao_informado')
                }

                # --- Carregamento (Load) no TinyDB ---
                Historico.insert(registro)

                print(f"[ANALYTICS] Dados registrados - Total: R$ {pedido['total']:.2f}, Itens: {len(pedido['itens'])}")

            else:
                time.sleep(0.5)

        except Exception as e:
            print(f"[ANALYTICS] Erro no worker: {str(e)}")
            time.sleep(1)

@app.route('/processar', methods=['POST'])
def iniciar_processamento():
    global worker_ativo

    if worker_ativo:
        return jsonify({"mensagem": "Worker já está rodando"}), 200

    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    return jsonify({"mensagem": "Worker de analytics iniciado"}), 200

@app.route('/parar', methods=['POST'])
def parar_processamento():
    global worker_ativo
    worker_ativo = False
    return jsonify({"mensagem": "Worker de analytics parado"}), 200

@app.route('/relatorio', methods=['GET'])
def gerar_relatorio():
    """
    Endpoint de BI (Business Intelligence).
    Gera um relatório consolidado em tempo real consultando o banco 'historico'.
    """
    registros = Historico.all()

    # --- Cálculo de KPIs (Key Performance Indicators) ---
    total_pedidos = len(registros)
    total_vendido = sum(r.get('total', 0) for r in registros)
    pedidos_pagos = [r for r in registros if r.get('status') == 'pago']
    total_pedidos_pagos = len(pedidos_pagos)
    ticket_medio = total_vendido / total_pedidos if total_pedidos > 0 else 0

    # --- Algoritmo de Ranking (Mais vendidos) ---
    contagem_produtos = {}
    for registro in registros:
        for produto_id in registro.get('produtos', []):
            contagem_produtos[produto_id] = contagem_produtos.get(produto_id, 0) + 1

    produtos_ranking = sorted(
        contagem_produtos.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]  # Top 5

    return jsonify({
        "periodo": "Total acumulado",
        "estatisticas": {
            "total_pedidos": total_pedidos,
            "pedidos_pagos": total_pedidos_pagos,
            "taxa_aprovacao": f"{(total_pedidos_pagos/total_pedidos*100):.2f}%" if total_pedidos > 0 else "0%",
            "total_vendido": f"R$ {total_vendido:.2f}",
            "ticket_medio": f"R$ {ticket_medio:.2f}"
        },
        "produtos_mais_vendidos": [
            {"produto_id": pid, "quantidade_vendida": qtd}
            for pid, qtd in produtos_ranking
        ]
    }), 200

@app.route('/')
def index():
    return jsonify({
        "servico": "Analytics",
        "porta": 5006,
        "worker_ativo": worker_ativo,
        "fila_entrada": "FILA_ANALYTICS",
        "tamanho_fila": FILA_ANALYTICS.qsize(),
        "registros_historico": len(Historico.all())
    }), 200

if __name__ == '__main__':
    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    print("Microserviço Analytics rodando na porta 5006")
    app.run(debug=True, port=5006, use_reloader=False)
