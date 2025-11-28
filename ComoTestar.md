Para testar, o professor sugeriu usar o Postman (ou qualquer HTTP requester). Você sobe os serviços e faz as requisições manualmente pelo Postman, mostrando o JSON de entrada e saída.
O fluxo de teste no vídeo seria:

Subir todos os serviços (iniciar_todos.py)
No Postman, cadastrar um cliente (POST /api/clientes)
Cadastrar alguns produtos (POST /api/produtos)
Criar um pedido (POST /api/pedidos)
Disparar cada worker na sequência:

POST :5002/processar (validar)
POST :5003/processar (processar)
POST :5004/processar (pagamento)
POST :5005/processar (notifica)
POST :5006/processar (analytics)


Consultar o pedido (GET /api/pedidos)
Consultar recomendações (GET /api/recomendacoes/1)

Cada chamada mostra o JSON de resposta, provando que funciona. Isso é o "caminho feliz" que o professor mencionou.
Se quiser, pode criar um script Python que faz todas essas chamadas em sequência usando requests, mas não é obrigatório - o Postman já resolve.