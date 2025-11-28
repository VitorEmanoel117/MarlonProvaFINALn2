"""
Microserviço: Notificação
Porta: 5005
Responsabilidade: Enviar notificações de pedidos para clientes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, jsonify
from flask_cors import CORS
from shared.filas import FILA_NOTIFICA
from shared.databases import Clientes, ClienteQuery
import threading
import time

app = Flask(__name__)
CORS(app)

# Flag para controlar o worker
worker_ativo = False

def enviar_email(cliente_email, pedido):
    """Simula envio de email de notificação"""
    print(f"\n{'='*60}")
    print(f"[EMAIL] Para: {cliente_email}")
    print(f"[EMAIL] Assunto: Pedido {pedido['pedido_id']} - {pedido['status'].upper()}")
    print(f"{'='*60}")

    if pedido['status'] == 'pago':
        print(f"Seu pedido foi confirmado e pago com sucesso!")
        print(f"Valor total: R$ {pedido['total']:.2f}")
        print(f"Itens ({len(pedido['itens'])}):")
        for item in pedido['itens']:
            print(f"   - {item['quantidade']}x {item['nome']} - R$ {item['subtotal']:.2f}")
        print(f"Endereço de entrega: {pedido.get('endereco_entrega', 'Não informado')}")
        print(f"Data prevista de entrega: 3-5 dias úteis")
    elif pedido['status'] == 'pagamento_recusado':
        print(f"Infelizmente seu pagamento foi recusado.")
        print(f"Motivo: {pedido.get('motivo_recusa', 'Não especificado')}")
        print(f"Por favor, tente novamente ou entre em contato conosco.")

    print(f"{'='*60}\n")

def processar_fila():
    """
    Worker (Consumer) de notificações.
    
    [Conceito para o Estagiário]: ENRIQUECIMENTO DE DADOS
    A mensagem na fila geralmente é enxuta (contém IDs e status).
    Para mandar um e-mail bonito, precisamos "enriquecer" essa mensagem buscando
    dados cadastrais (nome, e-mail) no banco de dados (TinyDB).
    
    Fluxo:
    1. Consome da FILA_NOTIFICA
    2. Usa o 'cliente_id' do pedido para buscar o e-mail real no TinyDB (Select)
    3. 'Envia' o e-mail (print no console)
    """
    global worker_ativo
    print("[NOTIFICA] Worker de notificação iniciado")

    while worker_ativo:
        try:
            if not FILA_NOTIFICA.empty():
                # --- Consumo ---
                pedido = FILA_NOTIFICA.get(timeout=1)

                print(f"[NOTIFICA] Processando notificação do pedido {pedido['pedido_id']}")

                # --- Enriquecimento de Dados (TinyDB) ---
                # Select * from Clientes where id = pedido.cliente_id
                cliente = Clientes.search(ClienteQuery.id == pedido['cliente_id'])

                if cliente:
                    cliente = cliente[0]
                    enviar_email(cliente.get('email', 'nao-informado@example.com'), pedido)
                    print(f"[NOTIFICA] Notificação enviada para {cliente.get('nome', 'Cliente')}")
                else:
                    print(f"[NOTIFICA] Cliente não encontrado para pedido {pedido['pedido_id']}")

            else:
                time.sleep(0.5)

        except Exception as e:
            print(f"[NOTIFICA] Erro no worker: {str(e)}")
            time.sleep(1)

@app.route('/processar', methods=['POST'])
def iniciar_processamento():
    """Inicia o worker de notificação se não estiver rodando"""
    global worker_ativo

    if worker_ativo:
        return jsonify({"mensagem": "Worker já está rodando"}), 200

    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    return jsonify({"mensagem": "Worker de notificação iniciado"}), 200

@app.route('/parar', methods=['POST'])
def parar_processamento():
    """Para o worker de notificação"""
    global worker_ativo
    worker_ativo = False
    return jsonify({"mensagem": "Worker de notificação parado"}), 200

@app.route('/')
def index():
    """Informações sobre o microserviço"""
    return jsonify({
        "servico": "Notificação",
        "porta": 5005,
        "worker_ativo": worker_ativo,
        "fila_entrada": "FILA_NOTIFICA",
        "tamanho_fila": FILA_NOTIFICA.qsize()
    }), 200

if __name__ == '__main__':
    # Inicia o worker automaticamente
    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    print("Microserviço Notificação rodando na porta 5005")
    app.run(debug=True, port=5005, use_reloader=False)