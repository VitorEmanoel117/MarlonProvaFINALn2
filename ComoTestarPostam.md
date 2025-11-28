 Para testar no Postman, você vai seguir o fluxo lógico de criação de dados e execução do pedido. Lembre-se que o API Gateway (Porta 5000) 
  é o único ponto de contato que você precisa usar.

  Aqui está o roteiro passo a passo para o Postman:

  1. Cadastrar um Produto (Para ter o que comprar)
   * Método: POST
   * URL: http://localhost:5000/api/produtos
   * Body (Raw JSON):

   1     {
   2       "nome": "Hambúrguer Artesanal",
   3       "preco": 35.90,
   4       "estoque": 50
   5     }
   * O que esperar: Um JSON de retorno com o produto criado e um campo "id". Copie esse ID.

  2. Cadastrar um Cliente (Para ter quem compre)
   * Método: POST
   * URL: http://localhost:5000/api/clientes
   * Body (Raw JSON):

   1     {
   2       "nome": "Seu Nome",
   3       "email": "seu.email@exemplo.com"
   4     }
   * O que esperar: Um JSON com o cliente criado e um campo "id". Copie esse ID também.

  3. Realizar o Pedido (Ação Principal)
   * Método: POST
   * URL: http://localhost:5000/api/pedidos
   * Body (Raw JSON): (Use os IDs que você copiou)

    1     {
    2       "cliente_id": "COLE_O_ID_DO_CLIENTE_AQUI",
    3       "itens": [
    4         {
    5           "produto_id": "COLE_O_ID_DO_PRODUTO_AQUI",
    6           "quantidade": 2
    7         }
    8       ],
    9       "endereco_entrega": "Rua Teste do Postman, 100"
   10     }
   * O que esperar: Um status 202 Accepted.

   1     {
   2         "mensagem": "Pedido recebido e enviado para processamento",
   3         "pedido_id": "um-uuid-gerado",
   4         "status": "aceito"
   5     }
   * Observação: Neste momento, olhe para o terminal onde o iniciar_todos.py está rodando. Você verá os logs dos workers processando o      
     pedido em tempo real (Receber -> Validar -> Processar -> Pagamento...).

  4. Verificar se Deu Certo (Consultar Pedidos)
   * Método: GET
   * URL: http://localhost:5000/api/pedidos
   * O que esperar: Uma lista com os pedidos. Procure o seu pedido lá. O status deve estar como processado ou pago (dependendo da velocidade     que você consultou).

  5. Consultar Recomendações (Bônus)
   * Método: GET
   * URL: http://localhost:5000/api/recomendacoes/COLE_O_ID_DO_CLIENTE_AQUI
   * O que esperar: Como você acabou de comprar um Hambúrguer, o sistema deve recomendar mais Hambúrguer (lógica "Hot/Personalizada").      

  6. Ver Relatório de BI (Analytics)
   * Método: GET
   * URL: http://localhost:5006/relatorio
       * Nota: Este endpoint é o único que acessamos direto na porta 5006 no script de teste, mas você pode acessá-lo direto também.        
   * O que esperar: Um resumo financeiro mostrando o valor total vendido e a contagem de vendas do Hambúrguer.

  ---

  Dica Pro:
  Se você quiser testar o cenário de Erro (Estoque Insuficiente):
   1. Faça um pedido com quantidade: 1000.
   2. O terminal vai mostrar o log [VALIDAR_PEDIDO] Estoque insuficiente....
   3. O pedido NÃO vai aparecer na lista de pedidos processados (passo 4), pois foi rejeitado na validação.

   Exatamente, você tem duas formas principais de rodar e testar:

  Opção 1: O Jeito Fácil (Recomendado para o Trabalho)

  Você NÃO precisa rodar cada lambda individualmente. O script iniciar_todos.py foi feito exatamente para resolver isso.

   1. Abra um terminal (PowerShell ou CMD).
   2. Execute: python sistema_delivery/iniciar_todos.py
   3. DEIXE ESSE TERMINAL ABERTO.

  Enquanto esse terminal estiver aberto, todos os 8 serviços (Flask) e os 5 workers (Threads de Fila) estarão rodando simultaneamente,      
  esperando requisições.

  Agora você pode abrir o Postman (ou o navegador) e fazer as requisições à vontade. O sistema estará "vivo" localmente. Você verá os logs
  de processamento pipocando no terminal que ficou aberto conforme você clica em "Send" no Postman.

  Quando terminar, volte nesse terminal e aperte CTRL+C para desligar tudo.

  ---

  Opção 2: O Jeito Difícil (Rodar Individualmente)

  Se você quisesse testar ou debugar UM serviço específico isoladamente, aí sim você faria:
   1. Abrir Terminal 1: python sistema_delivery/functions/api_gateway/lambda_function.py
   2. Abrir Terminal 2: python sistema_delivery/functions/receber_pedido/lambda_function.py
   3. ... teria que abrir 8 terminais.

  Mas tem um problema grave: Como estamos usando queue.Queue (filas em memória RAM), se você rodar em terminais separados, eles serão       
  processos diferentes. A memória RAM do processo 1 não é acessível pelo processo 2.
   * Resultado: O Receber Pedido colocaria o item na fila DELE, mas o Validar Pedido estaria olhando para a fila DELE (que estaria vazia). O     sistema não funcionaria.

   3. ... teria que abrir 8 terminais.

    Sim, os dois são importantes, mas têm finalidades completamente diferentes:

  1. sistema_delivery/iniciar_todos.py (O SERVIDOR)
   * O que faz: Sobe o sistema inteiro. Inicia as APIs Flask e os Workers de fila.
   * Importância: CRÍTICA. Sem rodar esse script, o sistema não existe. Ele é o equivalente a "ligar o servidor".
   * Quando usar: Sempre que você quiser que o sistema funcione (seja para testar com Postman, seja para gravar o vídeo do trabalho).       
   * Analogia: É como abrir a loja e destrancar a porta.

  2. testar_sistema.py (O CLIENTE ROBÔ)
   * O que faz: É um script de automação que finge ser um usuário. Ele faz as requisições HTTP (cadastra cliente, cria produto, faz pedido) 
     sozinho e verifica se a resposta foi 200 OK.
   * Importância: OPCIONAL (mas útil). Ele serve para você validar rapidamente se tudo está funcionando sem ter que ficar clicando
     manualmente no Postman toda vez.
   * Quando usar: Antes de gravar o vídeo, rode ele uma vez só para ter certeza que não quebrou nada.
   * Analogia: É como um cliente misterioso que entra na loja rapidinho só para ver se os atendentes estão trabalhando direito.

  Resumo para sua apresentação:
   1. Você VAI rodar o iniciar_todos.py e deixar ele rodando.
   2. Você PODE usar o testar_sistema.py para mostrar pro professor: "Olha, criei um script de teste automatizado que valida o fluxo inteiro      em 5 segundos". Isso conta pontos de "complexidade e capricho".
   3. Depois, você mostra o teste manual no Postman (que é mais visual e didático para o vídeo).

  Detalhe Técnico Importante:
  O testar_sistema.py atual tenta iniciar o iniciar_todos.py automaticamente no começo e matar ele no final.
  Então, se você for rodar o testar_sistema.py, certifique-se de que você NÃO tem outro iniciar_todos.py já rodando em outro terminal, senão  vai dar conflito de porta (Erro: "Address already in use").