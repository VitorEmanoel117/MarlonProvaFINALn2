 Já	está	dizendo	que	é	qualquer	um.	Devem	elaborar	o	Diário	9	de	Arquitetura,	contendo	o
 máximo	possível	de	integrações	entre	os	componentes.	O	que	significa	isso	aqui,	galera?
 Diferente	das	outras	avaliações,	que	a	arquitetura	limitava	o	que	vocês	iam	implementar,	agora
 não.
 A	arquitetura	vai	ter	tudo	o	que	vocês	desejariam	para	essa	ideia.	Mesmo	que	vocês	não
 tenham	implementado.	Então,	sei	lá,	tem	cinco	lâmpadas	que	dão	suporte	para	o	CRUD,	para	a
 integração,	para	o	sistema	de	recomendação,	que	vocês	não	precisam	desenvolver.
 Mas	é	para	vocês	fazerem	o	máximo	possível	para	ver	se	vocês	conseguem	implementar	a
 arquitetura	de	uma	ideia	mais	complexa.	Entenderam	a	ideia?	Aí	já	não	vale	mais	duas
 lâmpadas	com	uma	fila	no	meio,	igual	foi	a	prova.	Tem	que	ser	um	negócio	robusto.
 Eu	vou	avaliar	justamente	isso	aqui.	Ideia,	criatividade	e	complexidade.	Eu	vou	analisar	se	o
 diagrama	está	mais	robusto.
 Beleza?	Aqui	tem	uma	questão.	Diferente	também	dos	outros,	a	gente	agora	vai	criar	um	app
 que	funcione.	Ele	roda.
 Você	abre	o	servidor	e	vai	testando	as	URLs.	E	aí,	qual	que	é	o	nosso	prelúdio?	Flash.	Que	é	o
 que	a	gente	já	está	vendo	aqui	nesse	exemplo.
 Lembrando	que	da	arquitetura	para	Flash,	que	é	coisa	mínima,	ou	seja,	só	nas	rotas	e	o	método
 get	ou	push.	Né?	Aí	vem	a	implementação	funcional.	Não	precisa	de	interface	gráfica.
 Você	vai	mostrar	testando	o	caminho	feliz	ali	do	que	vocês	fizeram	no	Postman	ou	em	qualquer
 requester	de	HTTP.	Tá	bom?	Tem	que	mandar	JSON	para	provar	que	está	funcionando.	Tudo
 isso	aí.
 Tá?	E	a	explicação	que	vocês	já	mandam	bem,	fluidamente,	explicando	a	ideia,	explicando	o
 que	vocês	fizeram	e	o	funcionamento.	Tá	bom?	Aqui	tem	uma	restrição,	galera.	A	gente	tem
 feito	o	nocicotopiniquim,	que	é	quando	a	gente	coloca	ali	um	JSON	e	manipula	ele	com	read	e
 write.
 O	TinyDB	faz	exatamente	isso,	mas	de	uma	forma	que	parece	o	Diamond.	Eu	vou	mostrar	aqui,
 porque	essa	aula	de	hoje	é	disso.	Tá?	E	aí	tem	que	me	mandar	o	vídeo	por	e-mail,	colocando	o
 nome	da	dupla.
 Tá	bom?	O	e-mail	tem	que	estar	ali.	Fulano	de	tal,	fulano	de	tal.	E	sem	atraso,	galera.
 Não	vou	considerar	atraso.	O	limite	aí	é	de	15	minutos?	De	vídeo?	Não.	Não	precisa,	não.
Não	precisa	de	seguir,	não.	Não	tem	limite?	Tem,	não.	Sem	limite.
 Viu,	galera?	Se	vocês	quiserem	aí...	Porque	talvez	a	arquitetura,	vocês	queiram	dar	uma
 exploração...	Cada	pessoa	pode	fazer	algo	diferente.	É.	Aqui,	ó.	Tá	a	planilha.	Deixa	eu	ver	se
 vocês	já	conseguiram	achar.
 Porque	tem	duas	abas,	né?	Tem	a	turma	1,	turma	32,	que	são	vocês,	e	a	turma	33.	Tá	faltando
 gente	aqui,	né?	Não,	não	tem.	Não.
 Ó,	a	pergunta	que	talvez	vocês	talvez	não	perceberam,	mas	vão	perceber.	Não	precisa	ter
 repositório.	Por	quê?	Porque	eu	vou	cobrar,	vocês	explicando	no	vídeo,	o	código	funcionando,
 rodando,	entendeu?	Então,	pra	vocês	focarem	bastante	nessa	parte	lógica,	é	só	vocês
 demonstrarem	o	funcionamento.
 Tá	bom?	Então	toda	pontuação	que	era	pra	repositório,	agora	tá	em	mostrar	o	sistema
 funcionando.	Pode	estar	na	sua	máquina.	Pode.
 Mas	funcionando.	Tá	bom?	Tá	bom.	Bora	ver	quem	desenvolve.
 Certinho	aqui.	Puxou	de	volta.	Deixa	eu	abrir	um	quote	aqui.
 E	nós	vamos	começar	com	uma	questão,	galera.	Ó,	esse	aqui	é	um	cenário	exemplo	pra	essa
 aula.	Nada	diferente	do	que	a	gente	tem	feito	antes.
 Aqui	tá	o	JSON,	e	aqui	tá	uma	fila.	Tá	bom?	Qual	que	é	a	questão	agora?	Lembra	que	a	gente
 pegava,	criava	esse	JSON	aqui,	né,	banco.json,	por	exemplo,	e	criava	esse	motor	aqui,	essa
 estrutura.	Como	é	que	funciona?	No	Flash.
 Então	vamos	começar	pela	primeira	arquitetura	aqui,	que	é	o	realizar	pedido.	Realizar	pedido
 vai	pegar	o	JSON	do	cliente	lá	e	vai	jogar	numa	fila.	Só	isso.
 Aí	eu	vou	criar	a	fila,	que	muita	gente	errou	na	prova,	porque	a	fila,	pessoal,	é	fila,	é	memória.
 Fila	é	memória.	Quem	fez	Dynamo,	eu	tirei	pontinho.
 Por	quê?	Dynamo	é	disco.	Tá	bom?	São	ciências	da	computação	diferentes,	storage	e	memória.
 Por	que	a	fila	tem	que	ser	na	memória?	Pela	rapidez	e	ordenação.
 Todo	mundo	lembra	que	a	complexidade	de	ordenação	mais	barata	que	nós	temos	é	n	log	de
 n.	Isso	significa	que	ela	vai	demorar	um	pouquinho	ainda	mais	se	você	salvar	isso	num	storage.
 Isso	aumenta	muito	mais	a	latência.	Então	tem	que	ser	fila	pelos	limites	que	nós	temos	nos
 serviços	da	computação	moderna.
 Então	tem	que	ser	uma	memória.	Aqui	eu	estou	fazendo	exatamente	isso.	Para	eu	usar	ela,	eu
 dou	um	import.
 Aqui	eu	vou	criar	uma	rota.	Aqui	está	bem	tranquilo,	porque	eu	coloco	a	rota	que	eu	quero,
barra	API,	pesquisa	produto,	que	é	o	mesmo	nome	do	meu	diadrama	lá.	Aqui	está	a	função.
 Isso	daqui	eu	vou	receber	via	post.	Então,	vamos	compartilhar.	Deixa	eu	comentar	para	todo
 mundo.
 Vou	comentar	isso	aqui	por	enquanto.	Vou	dar	só	um	retorno.	O	que	eu	recebo	aqui?	Dados.
 Dados.	Pessoal,	a	única	coisa	que	vocês	vão	querer	trabalhar	é	profissionalizar	um	pouco	mais
 o	nosso	envio	de	JSON.	O	JSON	para	o	Python	é	um	dicionário,	mas	quando	a	gente	trabalha
 para	mandar	isso	como	resposta,	esse	JSONify	aqui,	ele	cria	a	estrutura,	ele	converte	a
 estrutura	de	dicionário	Python	para	um	oficial	mesmo	de	objeto	de	notícia.
 Tá	bom?	Então,	é	legal	usar	isso	daqui.	Ele	fica	redondinho,	sempre	que	você	sai	do	trabalho,
 ele	tem	força.	Então,	o	que	eu	vou	fazer?	Eu	vou	testar	essa	parte	aqui	que	vocês	vão	me
 seguir.
 Ajuda	eu.	Eu	vou	testar	essa	parte	aqui	que	vocês	já	vão	precisar	para	o	trabalho.	Eu	tenho	aqui
 um	testador	que	é	o	Dunder.
 Pode	ser	qualquer	um,	igual	eu	falei.	Então,	faz	aí.	Vou	subir	o	serviço	aqui	de	servidor.
 Tá	rodando	agora.	Personalizar	produto.	Eu	vou	digitar	a	rota	e	aqui,	pessoal,	no	bar,	eu	vou
 fingir	aqui	uma	payload,	tá	vendo?	Retorno	200,	ok.
 Como	eu	coloquei	para	retornar	só	a	payload	inicial,	tá	aqui.	Tá	bom?	Então,	é	isso	aqui	que
 vocês	vão	demonstrando,	mas	agora	a	gente	vai	carregar	com	logic,	tá	bom?	Ó,	eu	vou	apagar
 aqui	pra	vocês	verem,	ó.	Eu	vou	teletar.	Por	que,	pessoal?	Esse	timeDB,	ele	é	um	local	do
 Dynamo,	tipo	o	SQLite,	mas	para	NovoSQL.
 Então,	ele	é	que	vai	gerenciar	isso.	Eu	posso	chegar	aqui,	ó,	e	falar	o	seguinte,	eu	quero	uma
 tabela	nesse	diretório	chamada	produtos.	E	aí	eu	posso	simular,	por	exemplo,	o	insert	nele,	ó.
 Deixa	eu	desmarcar	aqui,	só	pra	gente	ver	como	funciona.
 Imagina	que	isso	aqui,	melhor,	né?	Vamos	salvar	o	que	o	usuário	mandou.	Dados.	Então,	ó,
 dados	ele	recebeu	no	endpoint	lá	e	ele	insere	no	filão.
 Aí	aqui	eu	vou	retornar	200.	200.	Vou	executar	aqui.
 Isso	aqui	complica,	né?	Adapção.	Under	cache.	Ó.	200.
 Aí	tinha	pedido	1,	2,	3.	Ele	criou	pra	mim	esse	banco	e	mandou	o	JSON	relativo	a	esse.	Vamos
 mandar	outro,	só	pra	mostrar.	1,	2,	3.	Vou	colocar	um	valor	diferente.
 9,	9,	9.	7.	Beleza.	Ó	lá.	E	ele	incrementou,	tá	vendo?	Tem	o	1,	tem	o	2.	É	meio	que	a	chave	de
 impotência	aqui,	né?	Em	sistema	de	verdade	a	gente	usa	hash.
 A	gente	usa	um	algoritmo	bem	mais	farrudo,	tá?	Mas	aqui	já	pode	usar	no	Android,	tá?	Deixa
eu	organizar	aqui	pra	ficar	mais	fácil	pra	ver	o	formato.	Tá	vendo?	Ele	cria	e	registra.	Ele
 gerencia	isso.
 Próximo	passo	então	seria	você,	por	exemplo,	buscar	isso.	Porque	na	nossa	arquitetura	aqui,
 você	tem	o	de	salvar	o	pedido.	Tá	errado,	tá?	Eu	só	mostrei	o	Dynamo	direto	pra	vocês	verem
 como	funciona	a	criação	dele.
 Mas	esse	realiza	pedido	tem	que	jogar	pra	fila.	O	próximo	passo	é	que	pesquisar	produto	vai
 puxar	nesse	catálogo	aqui.	Certo?	Realizar	pedido.
 Pesquisar	produto.	Que	é	essa	daqui.	Vai	ler	o	do	Dynamo	pra	poder	salvar.
 E	aí	não	é	insert	mais.	A	gente	vai	usar	o	query.	O	get.
 Assim.	Tá?	Então,	vou	desmarcar	agora	a	opção	de	ele	criar	o	downsert.	Tá?	E	aqui,	o	que	ele	tá
 fazendo?	Pessoal,	ele	tá	puxando	todos	os	dados	lá	do	nosso	Dynamo.
 E	aqui	ele	estaria	pesquisando,	mas	por	enquanto	o	que	eu	vou	fazer?	Vou	desmarcar	aqui.	E
 vou	só	mostrar	o	todos	aqui	na	tela.	Então,	ele	vai	dar	um	get	em	todo	o	ponto	de	dados.
 Olha	aqui.	Ó.	Viu?	É	um	dump	do	ponto	de	dados.	Então,	vamos	devagar.
 Vocês,	nesse	exato	momento,	vão	criar	uma	estrutura	dessa	que	tem	uma	fila,	uma	lâmpada	de
 realizar	pedido,	de	pesquisar,	e	o	Dynamo,	usando	o	timeDB.	Aí	eu	vou	ajudar	pra	todo	mundo
 conseguir,	porque	vai	precisar	para	o	trabalho.	Então	aí	é	melhor	que	todo	mundo	já	pratique.
 Pra	instalar,	pessoal,	é	moleza.	Primeiro,	ver	se	você	tá	num	ambiente	virtual	aqui.	No	caso	do
 Python,	o	ambiente	virtual.
 Não	terminar	o	novo,	então	pip	install	timeDB.	Assim.	Assim,	mínimo.
 Pip	install	timeDB.	Vamos	lá	que	eu	vou	ajudar.	Vou	começar	pela	estrutura	mínima.
 Lembrando,	a	estrutura	já	existe,	tá?	Essa	daqui