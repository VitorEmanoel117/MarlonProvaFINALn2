"""
Bancos de dados compartilhados usando TinyDB (simula DynamoDB).
Todos os bancos são salvos na pasta data/ como arquivos JSON.
"""

import os
from tinydb import TinyDB, Query

# Garantir que a pasta data/ existe
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Bancos de dados compartilhados
db_produtos_clientes = TinyDB(os.path.join(DATA_DIR, 'db_produtos_clientes.json'))
db_pedidos = TinyDB(os.path.join(DATA_DIR, 'db_pedidos.json'))
db_historico = TinyDB(os.path.join(DATA_DIR, 'db_historico.json'))

# Tabelas
Produtos = db_produtos_clientes.table('produtos')
Clientes = db_produtos_clientes.table('clientes')
Pedidos = db_pedidos.table('pedidos')
Historico = db_historico.table('historico')

# Query objects para busca
ProdutoQuery = Query()
ClienteQuery = Query()
PedidoQuery = Query()
HistoricoQuery = Query()
