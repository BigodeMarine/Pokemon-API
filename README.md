# 🐾 Pokémon API

API REST para gerenciamento de Pokémon desenvolvida com **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Redis**, **Docker** e **Kubernetes**.

o projeto possui:

- Persistência em PostgreSQL
- Cache com Redis
- Migrations com Alembic
- Testes unitários e de integração com pytest
- Cobertura de testes
- Logs estruturados
- Logstash e Elasticsearch para processamento de logs
- Containerização com Docker
- Orquestração com Kubernetes
- Persistent Volume para PostgreSQL
- CI com GitHub Actions
- Publicação da imagem Docker no GitHub Container Registry (GHCR)
- Documentação automática com Swagger UI

---

# 📋 Sumário

- [Sobre o projeto]
- [Arquitetura]
- [Tecnologias]
- [Estrutura do projeto]
- [Pré-requisitos]
- [Executando localmente]
- [Executando com Docker Compose]
- [Executando com Kubernetes]
- [Endpoints]
- [Redis e Cache]
- [PostgreSQL e Alembic]
- [Testes]
- [Cobertura de testes]
- [Logs e ELK]
- [CI/CD]
- [GitHub Container Registry]

---

# 🚀 Sobre a Pokemon-API
A aplicação utiliza a **FastAPI** para disponibilizar os endpoints HTTP e a **PokeAPI** como fonte externa de informações sobre Pokémon.

Os dados consultados são persistidos no PostgreSQL e posteriormente podem ser utilizados pela API sem necessidade de consultar novamente a PokeAPI.

O Redis é utilizado como camada de cache para reduzir consultas repetidas ao banco de dados.

---

# 🏗️ Arquitetura

A arquitetura principal da aplicação é:

```text
                    ┌─────────────────┐
                    │     Cliente     │
                    │ Browser / HTTP  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │   REST API      │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
          ┌─────────────┐         ┌─────────────┐
          │    Redis    │         │ PostgreSQL  │
          │    Cache    │         │   Database  │
          └─────────────┘         └──────┬──────┘
                                         │
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │   PokeAPI   │
                                  │ API externa │
                                  └─────────────┘

A aplicação também possui uma infraestrutura de logs:

FastAPI
   │
   ▼
app.log
   │
   ▼
Logstash
   │
   ▼
Elasticsearch

🛠️ Tecnologias

| Tecnologia        | Finalidade                          |
| ----------------- | ----------------------------------- |
| Python 3.11       | Linguagem de programação            |
| FastAPI           | Desenvolvimento da API REST         |
| Pydantic          | Validação e serialização dos dados  |
| Pydantic Settings | Gerenciamento das configurações     |
| SQLAlchemy        | ORM e acesso ao banco               |
| PostgreSQL 16     | Banco de dados relacional           |
| Psycopg           | Driver PostgreSQL                   |
| Alembic           | Controle de migrations              |
| Redis 7           | Cache                               |
| HTTPX             | Comunicação com a PokeAPI           |
| Pytest            | Testes automatizados                |
| pytest-asyncio    | Suporte a testes assíncronos        |
| pytest-cov        | Cobertura dos testes                |
| Docker            | Containerização                     |
| Docker Compose    | Execução dos serviços em containers |
| Kubernetes        | Orquestração dos containers         |
| GitHub Actions    | Integração contínua                 |
| GHCR              | Armazenamento da imagem Docker      |
| Logstash          | Processamento dos logs              |
| Elasticsearch     | Armazenamento e consulta dos logs   |
| Swagger UI        | Documentação interativa da API      |

📁 Estrutura do projeto
pokemon-api/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── pokemon.py
│   │
│   ├── cache/
│   │   ├── pokemon_cache.py
│   │   └── redis.py
│   │
│   ├── clients/
│   │   └── pokeapi_client.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── json_logger.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── database.py
│   │   └── session.py
│   │
│   ├── dependencies/
│   │   ├── database.py
│   │   └── pokemon.py
│   │
│   ├── exceptions/
│   │   ├── handlers.py
│   │   └── pokemon.py
│   │
│   ├── middleware/
│   │   └── logging.py
│   │
│   ├── models/
│   │   └── pokemon.py
│   │
│   ├── repositories/
│   │   ├── base.py
│   │   └── pokemon_repository.py
│   │
│   ├── schemas/
│   │   ├── pagination.py
│   │   └── pokemon.py
│   │
│   ├── services/
│   │   ├── base.py
│   │   └── pokemon_service.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   │   └── ab4cbc29a03b_create_pokemons_table.py
│   ├── env.py
│   └── script.py.mako
│
├── k8s/
│   ├── deployment.yaml
│   ├── postgres.yaml
│   ├── redis.yaml
│   └── service.yaml
│
├── logstash/
│   └── logstash.conf
│
├── logs/
│   └── app.log
│
├── tests/
│   ├── integration/
│   │   ├── test_create_pokemon.py
│   │   ├── test_delete_pokemon.py
│   │   ├── test_get_pokemon.py
│   │   ├── test_get_pokemons.py
│   │   ├── test_health.py
│   │   ├── test_pagination.py
│   │   ├── test_pokemon_routes.py
│   │   └── test_update_pokemon.py
│   │
│   ├── unit/
│   │   ├── test_pokemon_service.py
│   │   └── test_repository.py
│   │
│   └── conftest.py
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── .dockerignore
├── .gitignore
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

## ⚙️ Pré-requisitos

Para executar o projeto, é necessário ter instalado:

- Docker Desktop
- Git


### Executando o projeto

Clone o repositório:

```bash
git clone https://github.com/BigodeMarine/Pokemon-API.git
cd pokemon-api

Suba a aplicação utilizando o Docker Compose:
docker compose up --build

Após a inicialização, a API estará disponível em:

http://localhost:8000

A documentação interativa Swagger UI estará disponível em:

http://localhost:8000/docs

💻 Executando localmente

Crie e ative um ambiente virtual:
python -m venv .venv

Ative:
.venv\Scripts\Activate.ps1

Instale as dependências:
pip install -r requirements.txt

Execute a aplicação:
uvicorn app.main:app --reload

A API estará disponível em:
http://localhost:8000

🐳 Executando com Docker Compose

Para iniciar:
docker compose up -d --build

Verificar os containers:
docker compose ps

Para visualizar os logs:
docker compose logs -f api

☸️ Executando com Kubernetes

Antes de executar, certifique-se de que o Kubernetes do Docker Desktop está habilitado.

Verifique o contexto:
kubectl config current-context

Aplicar os manifestos
kubectl apply -f k8s/

Verifique os Pods:
kubectl get pods

Os principais componentes são:
pokemon-api
postgres
redis

📚 Swagger UI
A FastAPI fornece documentação automática através do Swagger UI.

Com a aplicação localmente:
http://localhost:8000/docs

🔌 Endpoints
Listar Pokémon:
GET /pokemons

Buscar Pokémon:
GET /pokemons/{id}

existem dois id:
id = da aplicaçao
pokemon_id = da pokeAPI

Cadastrar Pokémon:
POST /pokemons
usa o id da pokeAPI para cadastrar os pokemons ex:25
é o id do picachu

Atualizar Pokémon:
PUT /pokemons/{id}

Excluir Pokémon:
DELETE /pokemons/{id}

📄 Paginação

A listagem utiliza paginação através dos parâmetros:
limit
offset

Exemplo:
{
  "pagination": {
    "total": 10,
    "limit": 2,
    "offset": 2,
    "next": "/pokemons?limit=2&offset=4",
    "previous": "/pokemons?limit=2&offset=0"
  }
}

⚡ Redis e Cache

O Redis é utilizado como camada de cache.

Nas consultas de Pokémon por ID, a aplicação verifica primeiro se existe uma resposta armazenada no Redis.

GET /pokemons/{id}
        │
        ▼
     Redis?
     /     \
   HIT     MISS
    │        │
    ▼        ▼
 Retorna   PostgreSQL
              │
              ▼
           Retorna


🗄️ PostgreSQL e Alembic

O PostgreSQL é utilizado para persistência dos Pokémon.

O acesso ao banco é realizado através do SQLAlchemy.

A estrutura do banco é controlada pelo Alembic.

Para executar as migrations:
alembic upgrade head

🧪 Testes
Estrutura:
tests/
├── integration/
│   ├── test_create_pokemon.py
│   ├── test_delete_pokemon.py
│   ├── test_get_pokemon.py
│   ├── test_get_pokemons.py
│   ├── test_health.py
│   ├── test_pagination.py
│   ├── test_pokemon_routes.py
│   └── test_update_pokemon.py
│
└── unit/
    ├── test_pokemon_service.py
    └── test_repository.py

Executar todos os testes:
pytest -vv

📊 Cobertura de testes

A cobertura é gerada utilizando pytest-cov.
Execute:
pytest --cov=app --cov-report=term-missing

📝 Logs e ELK

A aplicação possui logging estruturado.

Os logs são armazenados em:
logs/app.log

O Logstash monitora o arquivo e envia os registros para o Elasticsearch.

Fluxo:
FastAPI
   │
   ▼
app.log
   │
   ▼
Logstash
   │
   ▼
Elasticsearch

O Docker Compose também disponibiliza o Kibana para visualização dos dados armazenados no Elasticsearch.
Elasticsearch
http://localhost:9200
Kibana
http://localhost:5601

🔄 CI/CD

O projeto possui uma pipeline GitHub Actions localizada em:
.github/workflows/python-app.yml
O fluxo principal é:
GitHub
   │
   ▼
Checkout
   │
   ▼
Configuração Python 3.11
   │
   ▼
Instalação das dependências
   │
   ▼
Alembic migrations
   │
   ▼
pytest
   │
   ▼
Cobertura
   │
   ▼
Docker Build
   │
   ▼
GitHub Container Registry

