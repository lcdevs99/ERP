# ERP - Módulo de Gestão de Pedidos

Este projeto implementa um módulo crítico de **gestão de pedidos** para um sistema ERP.  
O objetivo é fornecer uma **API REST robusta**, seguindo princípios de arquitetura limpa, SOLID e boas práticas de DevOps.

---

## 🚀 Tecnologias Utilizadas
- **Backend**: Python + Django Rest Framework (DRF)
- **Banco de Dados**: MySQL + Redis
- **Containerização**: Docker + Docker Compose (multi-stage builds)
- **Testes**: Pytest + pytest-django
- **Documentação**: Swagger disponível em `http://localhost:8000/api/docs`

---

## 📦 Pré-requisitos
- Docker e Docker Compose instalados
- Git para clonar o repositório

---

## ⚙️ Setup do Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/erp-pedidos.git
   cd erp-pedidos

2. 	Configure variáveis de ambiente:
    cp .env.example .env

3. 	Build dos containers:
    docker-compose build

4. 	Suba os serviços:
    docker-compose up

5. 	Acesse a API:
    http://localhost:8000/api/v1

6. 	Documentação interativa (Swagger):
    http://localhost:8000/api/docs

7. 	health:
    http://localhost:8000/health
## 🗄️ Migrations

Após subir os containers, é necessário aplicar as migrations para criar as tabelas no banco de dados MySQL.

1. Criar migrations para o app `orders`:
   ```bash
   docker-compose exec web python src/manage.py makemigrations orders

2. 	Aplicar todas as migrations:
    docker-compose exec web python src/manage.py migrate
    Observação: você também pode entrar no container manualmente com:
        docker exec -it erp-web-1 bash
    e rodar os comandos  diretamente lá dentro.
    Porém, o uso de  já executa os comandos no serviço  sem precisar abrir o bash.

ℹ️ Observação
Este projeto roda totalmente em containers Docker.
Não é necessário instalar Python, MySQL, Redis ou dependências manualmente na máquina local.
Basta ter Docker e Docker Compose instalados.

🧪 Rodando os Testes
Executar todos os testes com Pytest dentro do container:
docker-compose run --rm app pytest src

Executar testes com cobertura:
docker-compose run --rm app pytest --cov=src

Executar testes de integração apenas:
docker-compose run --rm app pytest src/orders/tests/test_customer.py


Todos os testes devem ser rodados a partir do root do projeto, direcionando para a pasta .



📂 Estrutura de Pastas
src/
 └── erp/
      ├── manage.py
      ├── pytest.ini
      └── orders/
           ├── __pycache__/
           ├── migrations/
           ├── models/
           ├── serializers/
           ├── tests/
           ├── views/
           ├── __init__.py
           ├── admin.py
           ├── apps.py
           ├── consumers.py
           ├── events.py
           ├── services.py
           ├── signals.py
           ├── tests.py
           ├── urls.py
           └── views.py
venv/
Include/


🔑 Endpoints Principais
POST /api/v1/customers/ → Criar cliente
GET /api/v1/customers/ → Listar clientes
GET /api/v1/customers/:id/ → Obter cliente
POST /api/v1/products/ → Criar produto
GET /api/v1/products/ → Listar produtos
PATCH /api/v1/products//:id/stock → Atualizar estoque
POST /api/v1/orders/ → Criar pedido
GET /api/v1/orders/ → Listar pedidos
GET /api/v1/orders/:id/ → Obter pedido
PATCH /api/v1/orders/:id/status → Alterar status
DELETE /api/v1/orders/:id/ → Cancelar pedido

📜 Regras de Negócio Implementadas
• 	Controle de estoque com atomicidade e concorrência
• 	Fluxo de status com histórico de transições
• 	Idempotência na criação de pedidos (Redis)
• 	Validações de cliente, produto e itens
• 	Soft delete para remoção lógica
• 	Paginação, filtros e ordenação nos endpoints de listagem
• 	Rate limiting básico via Redis

