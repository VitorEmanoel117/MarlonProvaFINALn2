"""
Microserviço: Validar Pedido
Porta: 5002
Responsabilidade: Validar cliente e produtos do pedido consultando o banco de dados
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask, jsonify
from flask_cors import CORS
from shared.filas import FILA_PEDIDOS, FILA_VALIDACAO
from shared.databases import Clientes, Produtos, ClienteQuery, ProdutoQuery
import threading
import time

app = Flask(__name__)
CORS(app)

# Flag para controlar o loop do worker (Consumer)
worker_ativo = False

def processar_fila():
    """
    [Conceito para o Estagiário]: WORKER / CONSUMER
    Esta função roda em uma thread separada, "escutando" a fila 24/7.
    Ela não é acionada por um Request HTTP, mas sim pela presença de dados na fila.
    
    Padrão PIPELINE:
    1. Consome da Fila A (FILA_PEDIDOS)
    2. Processa/Transforma
    3. Produz para Fila B (FILA_VALIDACAO)
    """
    global worker_ativo
    print("[VALIDAR_PEDIDO] Worker de validação iniciado")

    while worker_ativo:
        try:
            # Verifica se há itens na fila
            if not FILA_PEDIDOS.empty():
                # --- 1. CONSUMO DA FILA (DEQUEUE) ---
                # .get() remove o item da fila. Se não chamar, a fila entope.
                # timeout=1 é segurança para não travar a thread se a fila esvaziar subitamente.
                pedido = FILA_PEDIDOS.get(timeout=1)

                print(f"[VALIDAR_PEDIDO] Validando pedido {pedido['pedido_id']}")

                # --- 2. VALIDAÇÃO COM BANCO (TINYDB) ---
                
                # [TinyDB Query]: Verifica se o cliente existe na tabela 'clientes'
                # Clientes.search retorna uma lista. Se vazia, cliente não existe.
                cliente = Clientes.search(ClienteQuery.id == pedido['cliente_id'])
                
                if not cliente:
                    print(f"[VALIDAR_PEDIDO] Cliente {pedido['cliente_id']} não encontrado")
                    pedido['status'] = 'rejeitado'
                    pedido['motivo_rejeicao'] = 'Cliente não encontrado'
                    # [Fluxo Alternativo]: Se inválido, morre aqui. Não vai para a próxima fila.
                    continue

                total = 0
                itens_validos = []

                # Valida cada item do pedido
                for item in pedido['itens']:
                    # [TinyDB Query]: Busca produto pelo ID
                    produto = Produtos.search(ProdutoQuery.id == item['produto_id'])

                    if not produto:
                        print(f"[VALIDAR_PEDIDO] Produto {item['produto_id']} não encontrado")
                        pedido['status'] = 'rejeitado'
                        pedido['motivo_rejeicao'] = f"Produto {item['produto_id']} não encontrado"
                        break

                    produto = produto[0]
                    quantidade = item.get('quantidade', 1)

                    # [Lógica de Negócio]: Validação de Estoque
                    if produto.get('estoque', 0) < quantidade:
                        print(f"[VALIDAR_PEDIDO] Estoque insuficiente para {produto['nome']}")
                        pedido['status'] = 'rejeitado'
                        pedido['motivo_rejeicao'] = f"Estoque insuficiente: {produto['nome']}"
                        break

                    # Calcula subtotal do item com preço atual do banco (segurança)
                    subtotal = produto['preco'] * quantidade
                    total += subtotal

                    itens_validos.append({
                        'produto_id': item['produto_id'],
                        'nome': produto['nome'],
                        'preco': produto['preco'],
                        'quantidade': quantidade,
                        'subtotal': subtotal
                    })

                # --- 3. PRODUÇÃO PARA PRÓXIMA ETAPA (ENQUEUE) ---
                if pedido['status'] != 'rejeitado':
                    pedido['status'] = 'validado'
                    pedido['itens'] = itens_validos # Atualiza com dados enriquecidos
                    pedido['total'] = total

                    # [Fila]: Passa o bastão para o próximo microserviço
                    FILA_VALIDACAO.put(pedido)
                    print(f"[VALIDAR_PEDIDO] Pedido {pedido['pedido_id']} validado. Total: R$ {total:.2f}")

            else:
                # [Otimização]: Se a fila está vazia, dorme 0.5s para não gastar 100% de CPU à toa.
                time.sleep(0.5)

        except Exception as e:
            print(f"[VALIDAR_PEDIDO] Erro no worker: {str(e)}")
            time.sleep(1)

@app.route('/processar', methods=['POST'])
def iniciar_processamento():
    """Endpoint para ligar manualmente o worker de processamento"""
    global worker_ativo

    if worker_ativo:
        return jsonify({"mensagem": "Worker já está rodando"}), 200

    worker_ativo = True
    # Inicia o worker em uma Thread separada para não bloquear a API Flask
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    return jsonify({"mensagem": "Worker de validação iniciado"}), 200

@app.route('/parar', methods=['POST'])
def parar_processamento():
    """Endpoint para desligar o worker"""
    global worker_ativo
    worker_ativo = False
    return jsonify({"mensagem": "Worker de validação parado"}), 200

@app.route('/')
def index():
    """Diagnóstico de saúde do serviço"""
    return jsonify({
        "servico": "Validar Pedido",
        "porta": 5002,
        "worker_ativo": worker_ativo,
        "fila_entrada": "FILA_PEDIDOS",
        "fila_saida": "FILA_VALIDACAO",
        "tamanho_fila_entrada": FILA_PEDIDOS.qsize(),
        "tamanho_fila_saida": FILA_VALIDACAO.qsize()
    }), 200

if __name__ == '__main__':
    # Inicia o worker automaticamente ao rodar o script
    worker_ativo = True
    thread = threading.Thread(target=processar_fila, daemon=True)
    thread.start()

    print("[VALIDAR_PEDIDO] Microserviço rodando na porta 5002")
    app.run(debug=True, port=5002, use_reloader=False)
