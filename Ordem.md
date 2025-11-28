Preciso que você implemente um sistema de microserviços de delivery em Python usando Flask + TinyDB + filas em memória.

ESTRUTURA DE PASTAS:
sistema_delivery/
├── shared/
│   ├── filas.py
│   └── databases.py
├── functions/
│   ├── api_gateway/
│   │   └── lambda_function.py    # :5000
│   ├── receber_pedido/
│   │   └── lambda_function.py    # :5001
│   ├── validar_pedido/
│   │   └── lambda_function.py    # :5002
│   ├── processar_pedido/
│   │   └── lambda_function.py    # :5003
│   ├── pagamento/
│   │   └── lambda_function.py    # :5004
│   ├── notifica/
│   │   └── lambda_function.py    # :5005
│   ├── analytics/
│   │   └── lambda_function.py    # :5006
│   └── recomendacao/
│       └── lambda_function.py    # :5007
├── data/
├── iniciar_todos.py
└── requirements.txt

REGRAS TÉCNICAS:
1. Filas DEVEM usar queue.Queue() do Python (memória, não banco)
2. Bancos DEVEM usar TinyDB (simula DynamoDB)
3. Cada serviço roda em porta diferente (5000-5007)
4. Comunicação entre serviços via HTTP (requests) ou fila
5. Usar jsonify() para respostas
6. Usar Flask-CORS em todos os serviços

FLUXO DO PEDIDO:
Cliente → API Gateway → ReceberPedido → FilaPedidos → ValidarPedidos → FilaValidacao → ProcessaPedidos → FilaPagamentos → Pagamento → (FilaNotifica + FilaAnalytics) → Notifica e Analytics em paralelo

FILAS (shared/filas.py):
- FILA_PEDIDOS = Queue()
- FILA_VALIDACAO = Queue()
- FILA_PAGAMENTOS = Queue()
- FILA_NOTIFICA = Queue()
- FILA_ANALYTICS = Queue()

BANCOS (shared/databases.py):
- db_produtos_clientes = TinyDB('data/db_produtos_clientes.json')
- db_pedidos = TinyDB('data/db_pedidos.json')
- db_historico = TinyDB('data/db_historico.json')

ROTAS OBRIGATÓRIAS:

api_gateway (:5000):
- POST /api/pedidos → chama ReceberPedido :5001/receber
- GET /api/pedidos → chama ProcessaPedidos :5003/pedidos
- GET /api/recomendacoes/<id> → chama Recomendação :5007/recomendacoes/<id>
- CRUD /api/produtos e /api/clientes → acessa DB direto

receber_pedido (:5001):
- POST /receber → FILA_PEDIDOS.put(dados), retorna 202

validar_pedido (:5002):
- POST /processar → FILA_PEDIDOS.get(), valida cliente/produtos no DB, FILA_VALIDACAO.put()

processar_pedido (:5003):
- POST /processar → FILA_VALIDACAO.get(), salva no db_pedidos, FILA_PAGAMENTOS.put()
- GET /pedidos → lista do db_pedidos

pagamento (:5004):
- POST /processar → FILA_PAGAMENTOS.get(), simula aprovação, FILA_NOTIFICA.put() e FILA_ANALYTICS.put()

notifica (:5005):
- POST /processar → FILA_NOTIFICA.get(), print("[EMAIL] Pedido confirmado...")

analytics (:5006):
- POST /processar → FILA_ANALYTICS.get(), salva em db_historico
- GET /relatorio → retorna contagem de pedidos, total vendido

recomendacao (:5007):
- GET /recomendacoes/<cliente_id> → consulta db_historico, retorna 3 produtos mais comprados

SCRIPT iniciar_todos.py:
Use subprocess ou threading para subir todos os 8 serviços de uma vez. Lembre de adicionar o diretório raiz ao sys.path para os imports do shared/ funcionarem.

requirements.txt:
flask
flask-cors
tinydb
requests

Comece criando os arquivos na ordem: shared/ primeiro, depois cada lambda_function.py, por último o iniciar_todos.py.