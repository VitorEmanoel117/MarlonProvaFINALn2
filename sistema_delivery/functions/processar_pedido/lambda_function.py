"""
Microserviço: Processar Pedido
Porta: 5003
Responsabilidade: Persistir pedidos validados no banco e encaminhar para pagamento
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, jsonify
from flask_cors import CORS
from shared.filas import FILA_VALIDACAO, FILA_PAGAMENTOS
from shared.databases import Pedidos
from datetime import datetime
import threading
import time

app = Flask(__name__)
CORS(app)

worker_ativo = False

def processar_fila():
    """
    Worker de Processamento e Persistência.
    
    [Conceito para o Estagiário]: PERSISTÊNCIA DE DADOS
    Até este momento, o pedido existia apenas na memória RAM (Volátil). Se a luz acabasse, perdíamos tudo.
    Este worker é responsável por "imortalizar" o pedido, salvando-o no disco (TinyDB).
    
    Fluxo:
    1. Consome da FILA_VALIDACAO
    2. Adiciona metadados (data de processamento)
    3. Salva no banco de dados (Pedidos.insert)
    4. Envia para pagamento (FILA_PAGAMENTOS)
    """
    global worker_ativo
    print("[PROCESSAR_PEDIDO] Worker de processamento iniciado")

    while worker_ativo:
        try:
            if not FILA_VALIDACAO.empty():
                # --- 1. Consumo (Consumer) ---
                # Retira o pedido validado da fila anterior
                pedido = FILA_VALIDACAO.get(timeout=1)

                print(f"[PROCESSAR_PEDIDO] Salvando pedido {pedido['pedido_id']}")

                # Atualiza status e data
                pedido['data_processamento'] = datetime.now().isoformat()
                pedido['status'] = 'processado'

                # --- 2. Persistência (Escrita no Banco) ---
                # [TinyDB Insert]: Grava o dicionário no arquivo 'db_pedidos.json'
                # A partir de agora, temos um registro histórico seguro.
                Pedidos.insert(pedido)

                # --- 3. Produção (Producer) ---
                # O pedido está salvo, agora precisa ser pago.
                # Jogamos para a fila do setor financeiro.
                FILA_PAGAMENTOS.put(pedido)

                print(f"[PROCESSAR_PEDIDO] Pedido {pedido['pedido_id']} salvo e enviado para pagamento")

            else:
                time.sleep(0.5)

        except Exception as e:
            print(f"[PROCESSAR_PEDIDO] Erro no worker: {str(e)}")
            time.sleep(1)

@app.route('/processar', methods=['POST'])
def iniciar_processamento():
    """Inicia worker manualmente"""
    global worker_ativo

    if worker_ativo:
        return jsonify({"mensagem": "Worker já está rodando"}), 200

    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    return jsonify({"mensagem": "Worker de processamento iniciado"}), 200

@app.route('/parar', methods=['POST'])
def parar_processamento():
    """Para worker manualmente"""
    global worker_ativo
    worker_ativo = False
    return jsonify({"mensagem": "Worker de processamento parado"}), 200

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    """
    Endpoint para listar pedidos SALVOS.
    Lê diretamente do TinyDB (db_pedidos.json), provando a persistência.
    """
    # [TinyDB Read]: Busca todos os registros salvos.
    pedidos = Pedidos.all()
    return jsonify({
        "total": len(pedidos),
        "pedidos": pedidos
    }), 200

@app.route('/')
def index():
    """Diagnóstico do serviço"""
    return jsonify({
        "servico": "Processar Pedido",
        "porta": 5003,
        "worker_ativo": worker_ativo,
        "fila_entrada": "FILA_VALIDACAO",
        "fila_saida": "FILA_PAGAMENTOS",
        "tamanho_fila_entrada": FILA_VALIDACAO.qsize(),
        "tamanho_fila_saida": FILA_PAGAMENTOS.qsize(),
        # Mostra quantos pedidos já foram salvos no banco
        "pedidos_processados_db": len(Pedidos.all())
    }), 200

if __name__ == '__main__':
    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    print("[PROCESSAR_PEDIDO] Microserviço rodando na porta 5003")
    app.run(debug=True, port=5003, use_reloader=False)
