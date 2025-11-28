"""
Microserviço: Pagamento
Porta: 5004
Responsabilidade: Processar pagamentos e enviar para notificação e analytics
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, jsonify
from flask_cors import CORS
from shared.filas import FILA_PAGAMENTOS, FILA_NOTIFICA, FILA_ANALYTICS
from datetime import datetime
import threading
import time
import random

app = Flask(__name__)
CORS(app)

worker_ativo = False

def simular_pagamento(valor):
    """
    Simula um gateway de pagamento externo (ex: Stripe/PayPal).
    Retorna True (aprovado) ou False (recusado) com base em probabilidade.
    """
    time.sleep(0.5)  # Simula latência de rede
    return random.random() < 0.95  # 95% de chance de aprovação

def processar_fila():
    """
    Worker (Consumer) Financeiro.
    
    [Conceito para o Estagiário]: FAN-OUT / FORK
    Quando um evento importante acontece (Pagamento Aprovado), vários outros sistemas
    precisam saber disso simultaneamente, mas para propósitos diferentes.
    
    Aqui, fazemos um "Fan-out" (espalhar):
    1. Avisamos o cliente (FILA_NOTIFICA)
    2. Avisamos a diretoria/BI (FILA_ANALYTICS)
    
    Isso garante que o envio de e-mail não trave a geração de relatórios e vice-versa.
    """
    global worker_ativo
    print("[PAGAMENTO] Worker de pagamento iniciado")

    while worker_ativo:
        try:
            if not FILA_PAGAMENTOS.empty():
                # --- Consumo ---
                pedido = FILA_PAGAMENTOS.get(timeout=1)

                print(f"[PAGAMENTO] Processando pagamento do pedido {pedido['pedido_id']} - Valor: R$ {pedido['total']:.2f}")

                # Lógica de negócio (Simulação)
                pagamento_aprovado = simular_pagamento(pedido['total'])

                if pagamento_aprovado:
                    pedido['status'] = 'pago'
                    pedido['data_pagamento'] = datetime.now().isoformat()
                    pedido['metodo_pagamento'] = 'cartao_credito'  # Mock

                    # --- FAN-OUT (Broadcast) ---
                    # Clona o objeto (pedido.copy()) para evitar que modificações em um fluxo afetem o outro
                    # Envia para duas filas distintas
                    FILA_NOTIFICA.put(pedido.copy())
                    FILA_ANALYTICS.put(pedido.copy())

                    print(f"[PAGAMENTO] Pagamento aprovado para pedido {pedido['pedido_id']}")
                else:
                    pedido['status'] = 'pagamento_recusado'
                    pedido['motivo_recusa'] = 'Pagamento não autorizado pela operadora'

                    # Em caso de erro, apenas notifica, não gera analytics de venda
                    FILA_NOTIFICA.put(pedido.copy())

                    print(f"[PAGAMENTO] Pagamento recusado para pedido {pedido['pedido_id']}")

            else:
                time.sleep(0.5)

        except Exception as e:
            print(f"[PAGAMENTO] Erro no worker: {str(e)}")
            time.sleep(1)

@app.route('/processar', methods=['POST'])
def iniciar_processamento():
    global worker_ativo

    if worker_ativo:
        return jsonify({"mensagem": "Worker já está rodando"}), 200

    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    return jsonify({"mensagem": "Worker de pagamento iniciado"}), 200

@app.route('/parar', methods=['POST'])
def parar_processamento():
    global worker_ativo
    worker_ativo = False
    return jsonify({"mensagem": "Worker de pagamento parado"}), 200

@app.route('/')
def index():
    return jsonify({
        "servico": "Pagamento",
        "porta": 5004,
        "worker_ativo": worker_ativo,
        "fila_entrada": "FILA_PAGAMENTOS",
        "filas_saida": ["FILA_NOTIFICA", "FILA_ANALYTICS"],
        "tamanho_fila_entrada": FILA_PAGAMENTOS.qsize(),
        "tamanho_fila_notifica": FILA_NOTIFICA.qsize(),
        "tamanho_fila_analytics": FILA_ANALYTICS.qsize()
    }), 200

if __name__ == '__main__':
    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    print("Microserviço Pagamento rodando na porta 5004")
    app.run(debug=True, port=5004, use_reloader=False)