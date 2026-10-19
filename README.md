# 🎮 Pokémon API

API REST para gerenciamento de Pokémon desenvolvida com **FastAPI**, integrada à **PokeAPI**, **PostgreSQL** e **Redis**.

O projeto também possui suporte a **Docker**, **Docker Compose**, **Kubernetes**, **GitHub Actions**, **GitHub Container Registry (GHCR)** e monitoramento de logs utilizando a stack **ELK (Elasticsearch, Logstash e Kibana)**.

---

Deploy da aplicaçao feito na vercel:

[Acessar Pokemon API](https://pokemon-1ce5u1km6-bigodemarines-projects.vercel.app)

### 📚 Documentação

[Swagger UI](https://pokemon-1ce5u1km6-bigodemarines-projects.vercel.app/docs)

## 📋 Sobre o projeto

A aplicação permite consultar e gerenciar Pokémon através de uma API REST.

Os dados dos Pokémon podem ser obtidos através da [PokeAPI](https://pokeapi.co/) e persistidos localmente no PostgreSQL.

A aplicação possui:

- CRUD completo de Pokémon
- Integração com a PokeAPI
- PostgreSQL para persistência
- SQLAlchemy como ORM
- Alembic para migrations
- Redis para cache
- Paginação
- Validação utilizando Pydantic
- Tratamento de exceções
- Logging estruturado
- Testes unitários e de integração
- Cobertura de código com pytest-cov
- Docker e Docker Compose
- Kubernetes
- GitHub Actions para CI/CD
- Publicação de imagens no GHCR
- Elasticsearch
- Logstash
- Kibana
- Swagger UI para documentação interativa

---

# 🏗️ Arquitetura

A aplicação utiliza uma arquitetura dividida em camadas:

```text
Cliente
   │
   ▼
FastAPI
   │
   ├──────────────► Redis
   │                 │
   │              Cache HIT
   │                 │
   │                 ▼
   │              Resposta
   │
   │ Cache MISS
   ▼
Service
   │
   ▼
Repository
   │
   ▼
PostgreSQL
   │
   │ Pokémon não encontrado
   ▼
PokeAPI
   │
   ▼
PostgreSQL
   │
   ▼
Redis
   │
   ▼
Resposta
```

---

# 🛠️ Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python 3.11 | Linguagem de programação |
| FastAPI | Desenvolvimento da API REST |
| Uvicorn | Servidor ASGI |
| Pydantic | Validação e serialização dos dados |
| Pydantic Settings | Gerenciamento das configurações |
| SQLAlchemy | ORM e acesso ao banco |
| PostgreSQL 16 | Banco de dados |
| Psycopg | Driver PostgreSQL |
| Alembic | Controle de migrations |
| Redis 7 | Cache |
| HTTPX | Comunicação com a PokeAPI |
| Docker | Containerização |
| Docker Compose | Orquestração do ambiente local |
| Kubernetes | Orquestração dos containers |
| pytest | Testes automatizados |
| pytest-asyncio | Suporte a testes assíncronos |
| pytest-cov | Cobertura de código |
| GitHub Actions | CI/CD |
| GHCR | Armazenamento das imagens Docker |
| Elasticsearch | Armazenamento dos logs |
| Logstash | Processamento e envio dos logs |
| Kibana | Visualização dos logs |

---

# 📁 Estrutura do projeto

```text
pokemon-api/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── pokemon.py
│   │   └── __init__.py
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
│   │   └── logging.py
│   │
│   ├── database/
│   │   ├── base.py
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
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Executando o projeto

## Pré-requisitos

Para executar o projeto, é necessário ter instalado:

- Docker Desktop
- Git

O Docker Desktop já inclui o Docker Compose.

Não é necessário instalar Python, PostgreSQL ou Redis manualmente para executar a aplicação utilizando Docker Compose.

---

## 📥 Clonando o projeto

```bash
git clone https://github.com/bigodemarine/pokemon-api.git
```

Entre no diretório:

```bash
cd pokemon-api
```

---

# 🐳 Executando com Docker Compose

Essa é a forma recomendada para executar o projeto.

Execute:

```bash
docker compose up --build
```

O Docker Compose irá iniciar:

```text
Pokemon API
PostgreSQL
Redis
Elasticsearch
Logstash
Kibana
```

Após a inicialização, a API estará disponível em:

```text
http://localhost:8000
```

---

# 📖 Swagger UI

A documentação interativa da API é disponibilizada automaticamente pelo FastAPI.

Acesse:

```text
http://localhost:8000/docs
```

O Swagger UI permite executar diretamente pelo navegador:

- GET
- POST
- PUT
- DELETE

sem necessidade de utilizar ferramentas externas.

Também está disponível a documentação OpenAPI em:

```text
http://localhost:8000/openapi.json
```

---

# 🔎 Endpoints

## Health Check

```http
GET /
```

Retorna informações básicas sobre a aplicação.

---

## Listar Pokémon

```http
GET /pokemons
```

A API utiliza paginação através dos parâmetros:

```text
limit
offset
```

Exemplo:

```http
GET /pokemons?limit=20&offset=0
```

### Parâmetros

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---:|---|
| limit | integer | 20 | Quantidade máxima de registros |
| offset | integer | 0 | Posição inicial |

O `limit` aceita valores entre `1` e `100`.

---

### Exemplo de resposta

```json
{
  "data": [
    {
      "id": 1,
      "pokemon_id": 1,
      "name": "bulbasaur",
      "height": 7,
      "weight": 69,
      "types": [
        "grass",
        "poison"
      ],
      "sprites": {
        "front_default": "...",
        "back_default": "..."
      }
    }
  ],
  "pagination": {
    "total": 1281,
    "limit": 20,
    "offset": 0,
    "next": "/pokemons?limit=20&offset=20",
    "previous": null
  }
}
```

---

# 🔎 Buscar Pokémon

```http
GET /pokemons/{id}
```

Exemplo:

```http
GET /pokemons/1
```

Resposta:

```json
{
  "id": 1,
  "pokemon_id": 1,
  "name": "bulbasaur",
  "height": 7,
  "weight": 69,
  "types": [
    "grass",
    "poison"
  ],
  "sprites": {
    "front_default": "...",
    "back_default": "..."
  }
}
```

---

# ➕ Criar Pokémon

```http
POST /pokemons
```

O cadastro utiliza o ID do Pokémon na PokeAPI.

Exemplo:

```json
{
  "pokemon_id": 25
}
```
e gera um id da aplicaçao.
Exemplo:
Voce cadastra picachu(pokeapi = 25) e bubasauro(pokeapi = 1) nessa ordem.  
Entao o ID do picachu na API será 1 e do bubasauro será 2.
A aplicação:

1. verifica se o Pokémon já está cadastrado;
2. consulta a PokeAPI;
3. obtém os dados do Pokémon;
4. salva os dados no PostgreSQL;
5. limpa os caches de listagem;
6. retorna o Pokémon cadastrado.

---

# ✏️ Atualizar Pokémon

```http
PUT /pokemons/{id}
```

Permite atualizar os dados do Pokémon armazenado localmente.

---

# 🗑️ Excluir Pokémon

```http
DELETE /pokemons/{id}
```

Remove o Pokémon do PostgreSQL e também invalida seu cache.

---

# 🗄️ PostgreSQL

O PostgreSQL é utilizado como banco de dados principal da aplicação.

Configuração utilizada no ambiente Docker:

```text
Database: pokemon_db
User: postgres
Password: postgres
Port: 5432
```

O banco é persistido através de um volume Docker:

```text
postgres_data
```

Dessa forma, os dados não são perdidos simplesmente ao reiniciar os containers.

---

# 🔄 Alembic

O projeto utiliza Alembic para controlar as alterações do banco de dados.

Para executar as migrations manualmente:

```bash
alembic upgrade head
```

A migration inicial cria a tabela de Pokémon.

---

# ⚡ Redis

O Redis é utilizado como camada de cache.

Quando um Pokémon é consultado:

```text
GET /pokemons/25
```

o fluxo é:

```text
API
 │
 ▼
Redis
 │
 ├── HIT ─────► retorna o cache
 │
 └── MISS
       │
       ▼
   PostgreSQL
       │
       ▼
   retorna dados
       │
       ▼
   salva no Redis
       │
       ▼
   retorna resposta
```

As consultas de listagem também utilizam cache.

Quando um Pokémon é criado, atualizado ou removido, os caches relacionados são invalidados para evitar dados desatualizados.

---

# 🌐 PokeAPI

A aplicação utiliza a PokeAPI como fonte externa de informações sobre os Pokémon.

A integração é realizada através do `HTTPX`.

A aplicação consulta:

```text
https://pokeapi.co/
```

Os dados obtidos incluem informações como:

- ID
- nome
- altura
- peso
- tipos
- sprites

---

# 🧱 Arquitetura da aplicação

A aplicação está organizada em camadas.

## Routes

Responsáveis pelos endpoints HTTP.

```text
app/api/routes/
```

---

## Services

Contêm as regras de negócio.

```text
app/services/
```

---

## Repositories

Responsáveis pelo acesso aos dados através do SQLAlchemy.

```text
app/repositories/
```

---

## Models

Representam as tabelas do banco de dados.

```text
app/models/
```

---

## Schemas

Responsáveis pela validação e serialização dos dados através do Pydantic.

```text
app/schemas/
```

---

## Clients

Responsáveis pela comunicação com serviços externos.

```text
app/clients/pokeapi_client.py
```

---

## Cache

Responsável pela integração com Redis.

```text
app/cache/
```

---

# 🧪 Testes

O projeto possui testes unitários e de integração utilizando pytest.

Estrutura:

```text
tests/
├── integration/
└── unit/
```

Os testes cobrem:

- Health Check
- criação de Pokémon
- consulta de Pokémon
- listagem
- atualização
- exclusão
- paginação
- regras do service
- repository
- rotas

---

## Executando os testes

Com o ambiente Python configurado:

```bash
pytest -vv
```

Para executar especificamente os testes de paginação:

```bash
pytest tests/integration/test_pagination.py -vv
```

---

# 📊 Cobertura de testes

A cobertura pode ser gerada utilizando:

```bash
pytest --cov=app --cov-report=term-missing
```

A versão atual do projeto apresenta aproximadamente:

```text
92% de cobertura
```

---

# 🐳 Docker

O projeto possui um `Dockerfile` baseado em:

```text
python:3.11-slim
```

A imagem instala as dependências e executa a aplicação através do Uvicorn.

A porta utilizada é:

```text
8000
```

---

# 🐳 Docker Compose

O `docker-compose.yml` disponibiliza o ambiente completo da aplicação.

Serviços:

```text
api
db
redis
elasticsearch
logstash
kibana
```

Para iniciar:

```bash
docker compose up --build
```

Para executar em segundo plano:

```bash
docker compose up -d --build
```

Para visualizar os containers:

```bash
docker compose ps
```

Para visualizar os logs:

```bash
docker compose logs -f
```

Para finalizar:

```bash
docker compose down
```

---

# ☸️ Kubernetes

A aplicação também possui manifestos Kubernetes.

Os arquivos estão em:

```text
k8s/
```

```text
k8s/
├── deployment.yaml
├── postgres.yaml
├── redis.yaml
└── service.yaml
```

A aplicação utiliza:

- Deployment para a API
- Deployment para PostgreSQL
- PersistentVolumeClaim para PostgreSQL
- Deployment para Redis
- Services internos
- Service LoadBalancer para a API

---

# 🚀 Deploy no Kubernetes

Com o Kubernetes habilitado no Docker Desktop:

```bash
kubectl apply -f k8s/
```

Verificar os Pods:

```bash
kubectl get pods
```

Verificar os Services:

```bash
kubectl get services
```

Verificar o rollout da API:

```bash
kubectl rollout status deployment/pokemon-api
```

Para visualizar o Deployment:

```bash
kubectl get deployment
```

---

## Atualização da aplicação

O Deployment utiliza uma imagem Docker publicada no GitHub Container Registry.

Quando uma nova versão da imagem é disponibilizada e aplicada ao Deployment, o Kubernetes realiza a atualização dos Pods.

Verifique o rollout com:

```bash
kubectl rollout status deployment/pokemon-api
```

---

# 📦 GitHub Container Registry

As imagens Docker da aplicação são publicadas no:

```text
GitHub Container Registry (GHCR)
```

Formato utilizado:

```text
ghcr.io/bigodemarine/pokemon-api
```

---

# 🔄 CI/CD com GitHub Actions

O projeto possui uma pipeline configurada em:

```text
.github/workflows/python-app.yml
```

A pipeline é executada em:

```text
push na branch main
```

e:

```text
pull request para main
```

Fluxo:

```text
Git Push
   │
   ▼
GitHub Actions
   │
   ▼
Checkout
   │
   ▼
Python 3.11
   │
   ▼
Instalação das dependências
   │
   ▼
PostgreSQL + Redis
   │
   ▼
Alembic
   │
   ▼
pytest
   │
   ▼
Coverage
   │
   ▼
Docker Build
   │
   ▼
GitHub Container Registry
```

O workflow executa automaticamente os testes antes da publicação da imagem Docker.

---

# 📊 ELK Stack

O projeto possui integração para coleta e visualização dos logs da aplicação utilizando:

```text
Elasticsearch
Logstash
Kibana
```

Fluxo:

```text
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
   │
   ▼
Kibana
```

---

## Elasticsearch

Executado na porta:

```text
9200
```

Acesse:

```text
http://localhost:9200
```

---

## Kibana

Executado na porta:

```text
5601
```

Acesse:

```text
http://localhost:5601
```

---

## Logstash

O pipeline está configurado em:

```text
logstash/logstash.conf
```

Os logs da aplicação são lidos a partir de:

```text
/app/logs/app.log
```

e enviados para um índice Elasticsearch:

```text
pokemon-api-logs
```

---

# 📝 Logging

A aplicação possui logging estruturado em JSON.

Os logs são armazenados em:

```text
logs/app.log
```

O logging também possui middleware responsável por registrar informações das requisições HTTP.

---

# ⚙️ Variáveis de ambiente

As configurações da aplicação são controladas através de variáveis de ambiente.

Exemplo:

```env
APP_NAME=Pokemon API
APP_VERSION=1.0.0
APP_DESCRIPTION=API REST para gerenciamento de Pokémons

DEBUG=True

HOST=0.0.0.0
PORT=8000

DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/pokemon_db

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

---

# 🔐 Tratamento de exceções

A aplicação possui tratamento centralizado de exceções.

Entre os casos tratados estão:

- Pokémon não encontrado
- Pokémon já cadastrado
- erros de comunicação com a PokeAPI
- erros de validação

As respostas são retornadas em formato JSON.

---

# 📑 Documentação OpenAPI

O FastAPI gera automaticamente a especificação OpenAPI.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

---

# 🔧 Desenvolvimento local

Caso seja necessário executar a aplicação diretamente no Python, primeiro crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a migration:

```bash
alembic upgrade head
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

> Para uma execução completa e reproduzível do projeto, recomenda-se utilizar Docker Compose.

---

# 📌 Resumo dos principais comandos

## Docker

```bash
docker compose up --build
```

```bash
docker compose down
```

```bash
docker compose ps
```

```bash
docker compose logs -f
```

---

## Testes

```bash
pytest -vv
```

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Alembic

```bash
alembic upgrade head
```

---

## Kubernetes

```bash
kubectl apply -f k8s/
```

```bash
kubectl get pods
```

```bash
kubectl get services
```

```bash
kubectl rollout status deployment/pokemon-api
```

---

# 🎯 Objetivos acadêmicos

O projeto foi desenvolvido com o objetivo de demonstrar a aplicação prática de conceitos de desenvolvimento backend, incluindo:

- desenvolvimento de APIs REST;
- arquitetura em camadas;
- persistência de dados;
- ORM;
- migrations;
- cache;
- integração com API externa;
- validação de dados;
- tratamento de exceções;
- testes automatizados;
- cobertura de código;
- containerização;
- orquestração com Kubernetes;
- CI/CD;
- publicação de imagens Docker;
- monitoramento e gerenciamento de logs.

---

# 👨‍💻 Autor

**BigodeMarine**


## Pokédex web

Com a API em execução, abra a rota `/pokedex`. A interface é servida pelo próprio
FastAPI e não requer Node.js nem uma etapa de build. O endpoint `/` continua sendo
o health check; a documentação segue em `/docs`.

Digite o nome oficial do Pokémon (por exemplo, `pikachu`) ou seu ID nacional (`25`)
e selecione **Registrar**. O backend consulta a PokeAPI, resolve o ID oficial e
persiste nome, tipos, altura, peso e URLs dos sprites de frente e costas. A ficha e
a coleção recuperam os dados pelos endpoints GET existentes. O botão circular
alterna os sprites e as setas navegam pelos Pokémon da página atual. A coleção
possui paginação e pode ser recarregada sem perder os registros no banco.

O cadastro por ID segue compatível. Para cadastrar pelo nome:

```http
POST /pokemons
Content-Type: application/json

{"name": "pikachu"}
```

Informe **somente** `name` ou `pokemon_id`. Nomes são normalizados para minúsculas;
use o identificador oficial da PokeAPI, com hífen quando necessário. Um Pokémon já
registrado retorna HTTP 409 e a interface permite consultar o registro existente.
Altura e peso são convertidos para metros e quilogramas na interface.

É necessário permitir HTTPS para `pokeapi.co` no backend. O navegador também
precisa acessar os hosts das imagens retornadas (normalmente
`raw.githubusercontent.com`). Erros de rede e imagens indisponíveis são exibidos
na interface; nenhum registro de demonstração é inserido automaticamente.

Validação determinística do novo fluxo, usando PostgreSQL e mocks da PokeAPI:

```bash
pytest tests/unit tests/integration/test_pokedex.py -q
```

A suíte completa (`pytest -q`) inclui testes adicionais que acessam a PokeAPI real.

### Responsividade: mobile first

O CSS em `app/static/pokedex.css` parte de uma única coluna para telas pequenas.
Os painéis da Pokédex ficam empilhados e a busca apresenta o botão de registro
abaixo do campo. O layout cresce conforme o espaço disponível, usando media
queries com `min-width`:

| Largura disponível | Comportamento |
| --- | --- |
| Abaixo de `40rem` (640 px com fonte padrão) | Painéis empilhados, busca em duas linhas e coleção com colunas automáticas. |
| A partir de `40rem` | Campo e botão de busca na mesma linha; coleção com três colunas. |
| A partir de `58rem` (928 px com fonte padrão) | Painéis lado a lado e coleção com quatro colunas. |
| A partir de `70rem` (1120 px com fonte padrão) | Mais espaço interno e ajustes de apresentação para telas grandes. |

A largura do dispositivo é limitada a 1000 px para manter a leitura confortável
em monitores grandes. Espaçamentos e tamanhos de texto usam valores fluidos;
nomes longos, mensagens e tipos quebram linha. A coleção se reorganiza sem impor
uma largura mínima maior que a tela. As medidas do Pokémon também se reorganizam
quando falta espaço.

O campo de busca, o botão de cadastro e os controles de navegação têm altura
mínima de 44 px para facilitar o toque. O campo usa fonte de 16 px para evitar o
zoom automático ao receber foco em navegadores móveis. O viewport permite zoom,
o foco de teclado tem destaque visual e a animação dos cartões respeita
`prefers-reduced-motion`.

### Validações realizadas

- Suíte completa: **22 testes passaram**, incluindo cadastro por nome,
  normalização, validação de entrada, resolução de ID, persistência, consulta,
  sprites e prevenção de duplicatas.
- Fluxo real com a PokeAPI: cadastro de `pikachu`, resolução para ID nacional 25,
  consulta por GET e retorno dos sprites de frente e costas.
- Navegador automatizado: estado vazio, cadastro, seleção na coleção, alternância
  de sprites, duplicatas e mensagem de indisponibilidade da PokeAPI.
- Responsividade verificada em 18 tamanhos, com larguras de 240 a 2560 px,
  incluindo retrato, paisagem, limites dos breakpoints e textos longos a 320 px,
  sem rolagem horizontal nos cenários verificados.

Para repetir a validação do backend, com PostgreSQL, Redis e as variáveis de
ambiente configurados:

```bash
alembic upgrade head
pytest -q
```

Para conferir a sintaxe do JavaScript, caso Node.js esteja disponível:

```bash
node --check app/static/pokedex.js
```

Na revisão visual de `/pokedex`, teste a busca, a coleção e os controles em
larguras pequenas e intermediárias, em paisagem e com zoom. Os testes de navegador
usados durante o desenvolvimento foram executados por scripts auxiliares do
ambiente e não fazem parte da suíte versionada do repositório.

### Vercel e Redis da Upstash

Configure as variáveis em **Vercel → Settings → Environment Variables**, no
ambiente correspondente (Production ou Preview), e faça um novo deploy após
alterá-las. Os serviços locais de Docker não são transferidos para a Vercel.

- `DATABASE_URL`: conexão com o PostgreSQL de produção, com migrations aplicadas.
- `REDIS_URL`: URL **Redis TCP com TLS** fornecida pela Upstash, no formato
  `rediss://default:<senha>@<host>:6379`. Guarde a senha somente nas configurações
  protegidas. Não use a URL HTTPS ou o token REST da Upstash nesse campo: o cliente
  utilizado pelo projeto é Redis TCP.
- `REDIS_ENABLED=false`: permite operar diretamente pelo PostgreSQL sem acessar
  o Redis, caso o cache ainda não esteja disponível. O padrão é `true`.

Falhas de conexão ou timeout no cache são registradas como avisos e não impedem
leituras e gravações no banco. Cada operação Redis tem timeouts de conexão e
leitura de 2 segundos, sem novas tentativas automáticas. Falhas do PostgreSQL
continuam sendo erros: desativar o cache não substitui a configuração do banco.
Se uma invalidação de cache falhar, uma entrada antiga pode permanecer até seu
TTL de 300 segundos; desative o cache enquanto corrige uma indisponibilidade
persistente para evitar leituras desse conteúdo.

### Editar e excluir pela Pokédex

Selecione um Pokémon na coleção. Na parte inferior direita da Pokédex:

- **Atualizar** abre um formulário no painel para editar nome, altura em metros
  e peso em quilogramas. **Salvar** envia PUT para `/pokemons/{id}`; **Cancelar**
  mantém os dados anteriores. As medidas são convertidas para as unidades da API.
- **Deletar** exibe no próprio painel “Tem certeza que quer apagar esse Pokémon?”,
  junto do nome e ID nacional. **Sim** envia DELETE; **Não** cancela sem excluir.
  A coleção e o contador são atualizados após a exclusão.

Os botões ficam indisponíveis sem seleção ou durante operações. Erros mantêm o
formulário aberto para tentar novamente ou cancelar. A tecla Escape também
cancela a edição ou a confirmação. A confirmação começa com foco em **Não**.

Os indicadores LIVE e ONLINE usam luzes pulsantes, com pulso mais rápido durante
operações. São indicadores visuais de atividade, não monitoramento contínuo da
conectividade. A preferência `prefers-reduced-motion` desativa as animações.
Os botões usam rótulos de texto, sem setas. O comportamento mobile first é mantido.
