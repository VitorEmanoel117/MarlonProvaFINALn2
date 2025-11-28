"""
Filas compartilhadas em memória para comunicação entre microserviços.
Todas as filas usam queue.Queue() do Python (memória, não banco de dados).
"""

from queue import Queue

# Filas para comunicação assíncrona entre microserviços
FILA_PEDIDOS = Queue()       # Receber → Validar
FILA_VALIDACAO = Queue()     # Validar → Processar
FILA_PAGAMENTOS = Queue()    # Processar → Pagamento
FILA_NOTIFICA = Queue()      # Pagamento → Notifica
FILA_ANALYTICS = Queue()     # Pagamento → Analytics
