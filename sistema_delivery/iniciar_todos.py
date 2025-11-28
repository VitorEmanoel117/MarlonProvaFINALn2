"""
Script para iniciar todos os microserviços simultaneamente no MESMO PROCESSO.
Isso é necessário para que as filas em memória (queue.Queue) sejam compartilhadas.
"""

import threading
import time
import sys
import os
from pathlib import Path

# Configura o PATH para encontrar os módulos
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Importa as aplicações Flask e Workers
# Isso garante que todos importem o mesmo 'shared.filas'
try:
    from functions.api_gateway.lambda_function import app as app_gateway
    from functions.receber_pedido.lambda_function import app as app_receber
    
    from functions.validar_pedido.lambda_function import app as app_validar, processar_fila as worker_validar
    import functions.validar_pedido.lambda_function as mod_validar
    
    from functions.processar_pedido.lambda_function import app as app_processar, processar_fila as worker_processar
    import functions.processar_pedido.lambda_function as mod_processar
    
    from functions.pagamento.lambda_function import app as app_pagamento, processar_fila as worker_pagamento
    import functions.pagamento.lambda_function as mod_pagamento
    
    from functions.notifica.lambda_function import app as app_notifica, processar_fila as worker_notifica
    import functions.notifica.lambda_function as mod_notifica
    
    from functions.analytics.lambda_function import app as app_analytics, processar_fila as worker_analytics
    import functions.analytics.lambda_function as mod_analytics
    
    from functions.recomendacao.lambda_function import app as app_recomendacao
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Verifique se você está rodando o script do diretório correto ou se o PYTHONPATH está configurado.")
    sys.exit(1)

def run_flask(app_instance, port, nome):
    """Roda uma instância Flask em uma thread"""
    print(f" -> Iniciando {nome} na porta {port}")
    # use_reloader=False é crucial para rodar em threads
    app_instance.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def start_worker(module, worker_func, nome):
    """Inicia um worker em uma thread"""
    print(f" -> Iniciando Worker: {nome}")
    module.worker_ativo = True
    t = threading.Thread(target=worker_func, daemon=True)
    t.start()

def main():
    print("\n" + "="*70)
    print(" SISTEMA DE DELIVERY - MULTI-THREADED")
    print("="*70)
    print(" As filas queue.Queue agora são compartilhadas na memória RAM.\n")

    # 1. Iniciar Workers (Consumers)
    start_worker(mod_validar, worker_validar, "Validar Pedido")
    start_worker(mod_processar, worker_processar, "Processar Pedido")
    start_worker(mod_pagamento, worker_pagamento, "Pagamento")
    start_worker(mod_notifica, worker_notifica, "Notificação")
    start_worker(mod_analytics, worker_analytics, "Analytics")

    print("-" * 70)

    # 2. Iniciar Servidores Web (Flask)
    servicos = [
        (app_gateway, 5000, "API Gateway"),
        (app_receber, 5001, "Receber Pedido"),
        (app_validar, 5002, "Validar Pedido"),
        (app_processar, 5003, "Processar Pedido"),
        (app_pagamento, 5004, "Pagamento"),
        (app_notifica, 5005, "Notificação"),
        (app_analytics, 5006, "Analytics"),
        (app_recomendacao, 5007, "Recomendação"),
    ]

    threads = []
    for app_obj, port, nome in servicos:
        t = threading.Thread(target=run_flask, args=(app_obj, port, nome), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.2) # Pausa para não misturar logs demais

    print("\n" + "="*70)
    print(" TODOS OS SISTEMAS OPERACIONAIS")
    print("="*70)
    print(" Pressione CTRL+C para encerrar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Encerrando sistema...")
        sys.exit(0)

if __name__ == '__main__':
    main()