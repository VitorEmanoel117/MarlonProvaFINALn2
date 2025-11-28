# Contexto: Trabalho de Sistemas Web - Arquitetura de Microserviços

## 📋 Situação Atual

Estamos trabalhando em um trabalho acadêmico de Sistemas Web que exige a criação de uma arquitetura de microserviços simulando serviços AWS usando Flask + TinyDB + Filas em memória.

---

## 🎓 Requisitos do Trabalho (Segundo o Professor)

### 1. Diagrama de Arquitetura (Diário 9)
- **Complexidade**: Arquitetura robusta com o máximo possível de integrações entre componentes
- **Não pode ser simples**: Professor criticou "duas lâmpadas com uma fila no meio igual foi a prova"
- **Deve incluir tudo que desejam**: Mesmo que não implementem tudo
- **Exemplo dado**: "cinco lâmpadas que dão suporte para o CRUD, para a integração, para o sistema de recomendação"
- **Critérios de avaliação**: Ideia, criatividade e complexidade

### 2. Implementação Técnica

**Obrigatório:**
- ✅ **Flask** como framework web
- ✅ **TinyDB** como banco de dados (simula DynamoDB localmente)
- ✅ **Filas em memória** (`queue.Queue()` do Python) - NÃO usar DynamoDB para fila
- ✅ Rotas com métodos GET/POST/PUT/DELETE
- ✅ Comunicação via JSON

**Importante:**
- ❌ **NÃO precisa** de interface gráfica
- ✅ Testar usando **Postman** ou qualquer HTTP requester
- ✅ Demonstrar o "caminho feliz" funcionando

### 3. Entrega
- **Formato**: Vídeo explicando a ideia, implementação e funcionamento
- **Conteúdo**:
  - Explicação da arquitetura
  - Demonstração do sistema rodando
  - Testes via Postman mostrando JSON
- **Envio**: Por e-mail com nome da dupla
- **Repositório**: NÃO é obrigatório (pontuação vai para demonstração funcionando)
- **Prazo**: Sem atraso aceito
- **Duração**: Sem limite de tempo

### 4. Exemplo Técnico da Aula

O professor mostrou um exemplo de arquitetura:

```
Cliente → [Realizar Pedido] → Fila (memória) → [Pesquisar Produto] → DynamoDB (TinyDB)
```

**Conceitos importantes enfatizados:**
- **Fila DEVE ser memória**: Por questões de rapidez e ordenação (complexidade O(n log n))
- **DynamoDB é disco**: Usar TinyDB para simular
- **Múltiplos componentes**: Cada "lâmpada" é um serviço/função independente
- **Processamento assíncrono**: Usar filas para desacoplar componentes

---

## 💻 Sistema Atual (FloraApp)

### Descrição
Sistema de inventário de plantas com CRUD completo.

### Tecnologias
- Flask
- TinyDB (db.json)
- Flask-CORS
- boto3 (não utilizado de verdade)

### Estrutura Atual
```python
# Rotas implementadas:
- POST   /api/plantas        # Criar planta
- GET    /api/plantas        # Listar todas
- GET    /api/plantas/<id>   # Buscar uma
- PUT    /api/plantas/<id>   # Atualizar
- DELETE /api/plantas/<id>   # Deletar
```

### Campos das Plantas
- id (UUID gerado automaticamente)
- nome_comum (obrigatório)
- nome_cientifico
- familia
- tipo
- luz
- agua
- temperatura
- toxicidade
- observacoes
- data_criacao
- data_atualizacao

### Problema
**SQS Mockado (não funcional):**
```python
def enviar_mensagem_sqs(planta_id):
    print(f"\n[SQS MOCK] Enviando notificação...")  # ← Apenas um print!
```

---

## 🔍 Análise: FloraApp vs Requisitos

### ✅ O que está correto:
- Usa Flask
- Usa TinyDB
- Tem rotas CRUD
- Funciona com JSON
- Sistema roda localmente

### ❌ Problemas identificados:

1. **Arquitetura muito simples**
   - É apenas CRUD direto no banco
   - Não tem múltiplos microserviços interagindo
   - Não tem complexidade suficiente

2. **Fila SQS é fake**
   - Apenas um `print()` mockado
   - Não há fila real em memória
   - Não há processamento assíncrono

3. **Falta de componentes/lambdas**
   - Apenas 4 endpoints básicos
   - Sem sistema de recomendação
   - Sem integrações complexas
   - Sem processamento distribuído

4. **Interface gráfica desnecessária**
   - Tem um index.html de 730 linhas
   - Professor disse que não precisa de UI
   - Foco deve ser em testar via Postman

5. **Não simula arquitetura AWS**
   - Não tem modelo de microserviços
   - Não tem lambdas independentes
   - Não tem filas reais entre serviços

---

## 🎯 Conclusão

**O FloraApp atual NÃO atende os requisitos do trabalho.**

É um sistema monolítico simples de inventário de plantas, enquanto o professor exige uma **arquitetura de microserviços robusta** simulando AWS com:
- Múltiplas Lambdas (5+)
- Filas SQS reais (em memória)
- DynamoDB (TinyDB)
- Integrações complexas
- Processamento assíncrono

---

## ❓ Questões para Planejamento

### 1. **Qual será a ideia/domínio do sistema?**
Opções possíveis:
- E-commerce com processamento de pedidos
- Sistema de delivery com rastreamento
- Plataforma de reservas com confirmações
- Sistema de notificações com filas de prioridade
- Outro domínio que permita arquitetura complexa

### 2. **Como estruturar a arquitetura?**
Exemplo genérico de microserviços:
- Lambda 1: API Gateway (recebe requisições)
- Lambda 2: Validação/Processamento
- Lambda 3: Notificações
- Lambda 4: Analytics/Relatórios
- Lambda 5: Recomendações/IA

### 3. **Quais integrações criar?**
- Entre quais componentes teremos filas?
- Quais dados cada microserviço gerencia?
- Como simular processamento assíncrono?

### 4. **Aproveitar o FloraApp ou começar do zero?**
- Podemos adaptar a base do FloraApp?
- Ou é melhor criar uma nova ideia mais adequada?

---

## 🚀 Objetivo

**Precisamos planejar uma arquitetura de microserviços robusta** que:
1. Atenda todos os requisitos do professor
2. Seja implementável com Flask + TinyDB + Filas em memória
3. Demonstre complexidade e criatividade
4. Tenha múltiplas integrações entre componentes
5. Simule corretamente uma arquitetura AWS

---

## 📁 Estrutura do Projeto Atual

```
App-Flask-python/
├── FloraApp Sistemas Web/
│   ├── app.py              # Aplicação Flask atual
│   ├── db.json             # Banco TinyDB
│   ├── index.html          # Interface (não necessária)
│   ├── requirements.txt    # Dependências
│   └── run.sh
├── venv/                   # Ambiente virtual Python
└── CONTEXTO_TRABALHO_SISTEMAS_WEB.md  # Este arquivo
```

**Ambiente:**
- Python 3.12.10
- Flask 3.1.2
- TinyDB instalado
- Ambiente virtual ativo

---

## 💡 Pedido ao Opus 5

Por favor, analise este contexto e:

1. **Sugira uma ideia de sistema** que se encaixe perfeitamente nos requisitos do trabalho
2. **Projete uma arquitetura robusta** com:
   - 5+ microserviços (lambdas)
   - Filas SQS em memória entre componentes
   - Múltiplas integrações
   - Processamento assíncrono real
3. **Explique o fluxo** de dados entre os componentes
4. **Liste as rotas Flask** necessárias
5. **Detalhe como implementar** as filas e processamento assíncrono

**Critério importante**: A arquitetura deve ser complexa o suficiente para impressionar na avaliação de "ideia, criatividade e complexidade", mas ainda implementável em Flask com TinyDB.
