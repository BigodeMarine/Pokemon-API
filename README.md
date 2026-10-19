# 🎮 Pokédex · Pokémon API

**[Abrir a Pokédex no deploy da Vercel](https://pokemon-1ce5u1km6-bigodemarines-projects.vercel.app/pokedex)**

[Swagger / testar a API](https://pokemon-1ce5u1km6-bigodemarines-projects.vercel.app/docs) · [Health check](https://pokemon-1ce5u1km6-bigodemarines-projects.vercel.app/)

Pokédex web com API REST em **FastAPI**, integração com a **PokeAPI**, persistência
em **PostgreSQL** e cache opcional em **Redis**. Digite o nome ou ID de um Pokémon
para registrá-lo, consultar sua ficha e gerenciar sua coleção.

O frontend é servido pelo próprio backend: **HTML, CSS e JavaScript sem build
separado**. A interface segue o visual de uma Pokédex vermelha, com telas escuras,
detalhes azuis e verdes e favicon de Pokébola.

## Funcionalidades atuais

- Cadastro pelo nome oficial ou ID nacional, consultando a PokeAPI.
- Resolução do nome para o ID oficial e prevenção de cadastro duplicado.
- Ficha com sprites de frente e costas, tipos, altura e peso.
- Coleção persistida, paginada e selecionável; atualização manual da listagem.
- Botão **↻** para alternar os sprites e **◀ / ▶** para navegar na página atual.
- Botões **Atualizar** e **Deletar** na parte inferior direita da Pokédex.
- Edição de nome, altura e peso no próprio painel, com **Salvar / Cancelar**.
- Exclusão com pergunta no painel e opções **Sim / Não**, sem popup do navegador.
- Estados vazios, mensagens de erro, bloqueio de ações durante operações e
  indicação de imagem indisponível.
- Indicadores LIVE e ONLINE animados e pulso de atividade durante requisições.
- Interface mobile first, navegação por teclado e suporte a movimento reduzido.
- Cache com TTL e continuidade pelo PostgreSQL quando o Redis fica indisponível.
- Logs estruturados, migrations, testes e pipeline de CI/CD.

## Como usar a interface

1. Abra `/pokedex` e digite, por exemplo, `pikachu` ou `25`.
2. Clique em **Registrar**. O backend consulta a PokeAPI e salva o Pokémon no banco.
3. A ficha recupera o registro via GET e exibe os sprites e dados físicos.
4. Selecione um cartão da coleção para consultar outro registro. **↻** alterna
   frente/costas; as setas navegam pelos registros da página atual.
5. Use **Atualizar** para editar os dados locais. As medidas são apresentadas em
   metros e quilogramas e convertidas para as unidades da API ao salvar.
6. Use **Deletar** para abrir a confirmação. **Não** cancela; **Sim** remove o
   registro e atualiza a coleção e o contador.

Os botões de edição/exclusão dependem de um Pokémon selecionado. Escape cancela
a edição ou confirmação; o foco inicial da confirmação fica em **Não**. Uma falha
ao salvar ou excluir mantém o painel aberto para cancelar ou tentar novamente.
Editar um registro não altera o ID oficial nem os dados originais da PokeAPI.

## Responsividade e animações

O CSS começa com uma coluna, painéis empilhados e busca com botão abaixo do campo.
As media queries usam `min-width`, ampliando o layout apenas quando há espaço:

| Largura disponível | Layout |
| --- | --- |
| Abaixo de `40rem` | Painéis empilhados; coleção com colunas automáticas. |
| A partir de `40rem` (640 px com fonte padrão) | Busca em uma linha; coleção com três colunas. |
| A partir de `58rem` (928 px com fonte padrão) | Painéis lado a lado; coleção com quatro colunas. |
| A partir de `70rem` (1120 px com fonte padrão) | Ajustes de espaçamento para telas grandes. |

A Pokédex tem largura máxima de 1000 px. Espaçamentos fluidos, quebra de nomes e
mensagens e reorganização das medidas evitam cortes em telas pequenas. Os
controles de toque principais têm pelo menos 44 px; o botão ↻ mede 48 px, com
símbolo de 36 px. O campo de busca usa fonte de 16 px e o viewport permite zoom.

As luzes têm pulso suave; durante operações, o pulso fica mais rápido.
São indicadores visuais de atividade, não monitoramento contínuo da conexão.
`prefers-reduced-motion` desativa as animações, e o foco de teclado é destacado.

## Tecnologias e organização

| Componente | Tecnologia |
| --- | --- |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Validação/configuração | Pydantic, Pydantic Settings, `.env` |
| Banco e migrations | PostgreSQL 16, SQLAlchemy, Psycopg, Alembic |
| Cache | Redis 7; cliente Redis TCP assíncrono |
| Integração externa | HTTPX / PokeAPI |
| Frontend | HTML, CSS, JavaScript e SVG |
| Testes | pytest, pytest-asyncio, pytest-cov |
| Infraestrutura | Docker Compose, Kubernetes, Vercel, GitHub Actions / GHCR |
| Observabilidade opcional | Elasticsearch, Logstash, Kibana |

```text
app/
├── api/routes/       # Endpoints de Pokémon
├── cache/            # Redis, TTL e tolerância a falhas
├── clients/          # Cliente da PokeAPI
├── core/             # Configuração e logging JSON
├── database/         # Engine, sessões e Base do ORM
├── dependencies/     # Injeção de banco, repository e service
├── exceptions/       # Exceções e respostas HTTP
├── middleware/       # Logs de requisições
├── models/           # Persistência SQLAlchemy
├── repositories/     # Consultas e gravações
├── schemas/          # Validação e serialização
├── services/         # Regras de negócio
├── static/           # Pokédex: HTML, CSS, JS e favicon
└── main.py           # Aplicação, health check e frontend
api/index.py          # Entrada que exporta o app para o deploy
alembic/              # Migrations
tests/               # Testes unitários e de integração
k8s/                  # Manifestos Kubernetes
logstash/             # Pipeline de logs
.github/workflows/    # CI/CD
```

Fluxo de cadastro: interface → rota → service → PokeAPI → repository → PostgreSQL
→ invalidação do cache de listas. Nas consultas, a API tenta o cache e recorre ao
PostgreSQL quando não há uma entrada válida ou o Redis está indisponível.

## Executar com Docker Compose

Pré-requisitos: Git, Docker e Docker Compose.

```bash
git clone https://github.com/BigodeMarine/Pokemon-API.git
cd Pokemon-API
cp .env.example .env
```

O `.env.example` contém as configurações básicas. Para Compose, configure também
no `.env`:

```dotenv
DEBUG=false
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/pokemon_db
REDIS_ENABLED=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

As credenciais acima são exemplos locais de desenvolvimento. Não as reutilize
em produção. Se definir `REDIS_URL`, ela tem prioridade sobre host, porta e senha.

Para iniciar somente a API e seus serviços de desenvolvimento:

```bash
docker compose up -d --build api
docker compose exec api alembic upgrade head
```

O Compose inicia PostgreSQL e Redis como dependências da API. A migration é um
passo separado: o comando da API no Compose não a executa automaticamente.

- Pokédex: `http://localhost:8000/pokedex`
- Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

```bash
docker compose logs -f api
docker compose ps
docker compose down
```

O PostgreSQL usa o volume `postgres_data`. `docker compose down` preserva o volume.
Para incluir também a stack ELK, execute `docker compose up -d --build` sem limitar
o serviço; ela consome recursos adicionais e não é necessária para usar a Pokédex.

## Desenvolvimento direto em Python

Use Python 3.11, PostgreSQL e, opcionalmente, Redis. Crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

No PowerShell, a ativação é `.venv\Scripts\Activate.ps1`. Ajuste o `.env` para o
banco local; os nomes `db` e `redis` são do Compose, não do host:

```dotenv
DEBUG=false
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/pokemon_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_ENABLED=true
```

Para iniciar apenas os serviços com Docker e executar o backend no host:

```bash
docker compose up -d db redis
alembic upgrade head
uvicorn app.main:app --reload
```

A interface fica em `/pokedex`. Node.js não é necessário para executar o frontend.

## Variáveis de ambiente

| Variável | Uso / padrão |
| --- | --- |
| `APP_NAME` | Obrigatória; nome da aplicação. |
| `APP_VERSION` | Obrigatória; versão. |
| `APP_DESCRIPTION` | Obrigatória; descrição. |
| `DEBUG` | Obrigatória; booleano, prefira `false` em produção. |
| `HOST` / `PORT` | Obrigatórias nas configurações; o comando do servidor define o bind efetivo. |
| `DATABASE_URL` | Obrigatória; URL SQLAlchemy do PostgreSQL. |
| `REDIS_ENABLED` | `true`; `false` desativa as operações de cache. |
| `REDIS_URL` | Vazia por padrão; quando presente, prevalece sobre as opções abaixo. |
| `REDIS_HOST` / `REDIS_PORT` | `localhost` / `6379`. |
| `REDIS_DB` | `0`. |
| `REDIS_PASSWORD` | Vazia por padrão; senha Redis quando usada a configuração por host. |

Os valores são lidos do processo e do `.env` local. Não versione senhas nem URLs
com credenciais. O `.env.example` não lista todas as opções opcionais acima.

## Deploy na Vercel e Redis da Upstash

O frontend é servido por FastAPI em `/pokedex`, com arquivos em `/static`.
A rota `/` continua sendo o health check. Não configure um build Node.js separado.

1. Conecte o repositório e configure a branch de produção `main`.
2. Configure as variáveis obrigatórias em **Settings → Environment Variables**.
3. Use um PostgreSQL acessível pela Vercel e aplique `alembic upgrade head` contra
   esse banco em um ambiente autorizado com a configuração de produção.
4. Para Upstash, configure `REDIS_URL` com a conexão **Redis TCP com TLS**:

   ```text
   rediss://default:SENHA_DO_REDIS@HOST_DA_UPSTASH:6379
   ```

   Use a senha Redis, não `UPSTASH_REDIS_REST_TOKEN` nem a URL HTTPS da API REST.
   Prefira uma região próxima da Function Region configurada na Vercel.
5. Defina `REDIS_ENABLED=true`, ou `false` para operar sem cache.
6. Aplique as variáveis ao ambiente correto (Production/Preview) e faça Redeploy
   após alterações. Confira o commit do deploy antes de testar `/pokedex`.

PostgreSQL e Redis do ambiente local não são transferidos para a Vercel. É
necessário permitir acesso HTTPS à `pokeapi.co` pelo backend e aos hosts dos
sprites pelo navegador, normalmente `raw.githubusercontent.com`.

### Falhas de cache

O Redis tem TTL de 300 segundos, timeouts de conexão e leitura de 2 segundos e
nenhuma nova tentativa automática. Falhas de conexão, timeout ou conteúdo JSON
inválido no cache geram avisos; a API continua consultando o PostgreSQL. Falhas do
banco não são resolvidas pela desativação do cache.

Se uma invalidação falhar, uma entrada antiga pode permanecer até o TTL expirar.
Use `REDIS_ENABLED=false` durante uma indisponibilidade persistente para evitar
leituras desse cache. Se um Redis tiver sido excluído por inatividade, crie outro
e atualize a conexão: para este projeto, não é necessário restaurar o cache antigo,
pois os registros persistentes ficam no PostgreSQL.

## API REST

`id` é o identificador interno do registro; `pokemon_id` é o ID nacional retornado
pela PokeAPI. Consultas individuais, edição e exclusão usam o **ID interno**.

| Método | Rota | Comportamento |
| --- | --- | --- |
| GET | `/` | Status básico da aplicação; não comprova saúde de banco/Redis. |
| GET | `/pokedex` | Interface web. |
| GET | `/docs`, `/redoc`, `/openapi.json` | Documentação e contrato da API. |
| POST | `/pokemons` | Registra por nome ou ID da PokeAPI; retorna 201. |
| GET | `/pokemons?limit=20&offset=0` | Lista paginada; `limit` entre 1 e 100. |
| GET | `/pokemons/{id}` | Consulta um registro pelo ID interno. |
| PUT | `/pokemons/{id}` | Atualiza nome, altura e/ou peso. |
| DELETE | `/pokemons/{id}` | Remove o registro; retorna 204, sem corpo. |

Cadastro por nome:

```json
{"name": "pikachu"}
```

Ou por ID nacional:

```json
{"pokemon_id": 25}
```

Informe somente um desses campos. O nome é normalizado removendo espaços externos
e convertendo para minúsculas. Use o identificador oficial da PokeAPI, com hífen
quando necessário; nomes com espaços internos ou acentos são rejeitados.

Exemplo de atualização local:

```json
{"name": "pikachu", "height": 4, "weight": 60}
```

Na API, altura é um inteiro em **decímetros** e peso em **hectogramas**. Nesse
exemplo, a interface apresenta 0,4 m e 6 kg. A resposta inclui `types` e `sprites`
com `front_default` e `back_default`.

A listagem retorna `data` e `pagination` com `total`, `limit`, `offset`, `next` e
`previous`. Erros previstos incluem 404 para Pokémon ausente, 409 para duplicata,
422 para entrada inválida e 503 para indisponibilidade da PokeAPI. Um erro 500
exige examinar os logs da função/servidor; a resposta pública não expõe detalhes.

## Testes e validação

A suíte atual possui **26 casos**, incluindo testes parametrizados. Use um banco
de desenvolvimento/testes: os testes de integração criam, editam e removem dados.
`tests/conftest.py` fixa a conexão em
`postgresql+psycopg://postgres:postgres@localhost:5432/pokemon_db`. Tenha esse banco
preparado e execute as migrations com a mesma configuração antes de testar.

```bash
alembic upgrade head
pytest -q
pytest --cov=app --cov-report=term-missing
```

| Grupo | O que verifica |
| --- | --- |
| `tests/unit/` | Regras do service, duplicatas e falha da PokeAPI; inclui um teste básico de sanity no arquivo de repository. |
| `tests/integration/test_pokedex.py` | Entrada por nome/ID, normalização, consulta à PokeAPI por nome, persistência real, GET, sprites, duplicatas e arquivos do frontend. |
| `tests/integration/test_cache_failure.py` | Erros de conexão/timeout do Redis, cache desativado e GET/POST funcionando durante falha simulada do cache. |
| Demais testes de integração | Saúde, cadastro, consulta, listagem, paginação, atualização e exclusão. |

Para executar apenas os testes unitários e os novos cenários determinísticos:

```bash
pytest tests/unit tests/integration/test_pokedex.py tests/integration/test_cache_failure.py -q
```

Os novos cenários simulam a PokeAPI e falhas do Redis, mas a persistência de
integração usa PostgreSQL real. A fixture padrão simula o cache; os testes de
falha recuperam as implementações reais e simulam o cliente Redis. A suíte
completa também contém testes que consultam a PokeAPI real e dependem de rede.

O resultado mais recente é **26 testes passando**. Não há limite de cobertura
configurado; gere o relatório para medir a cobertura da versão atual.

### Validação do frontend

```bash
node --check app/static/pokedex.js
```

Node.js é opcional e usado aqui apenas para verificar a sintaxe. Durante o
desenvolvimento, scripts auxiliares com Playwright validaram estados vazios,
cadastro, edição, cancelamento, exclusão, erros e novas tentativas. Esses scripts
não integram a suíte versionada; `test_frontend_assets` verifica a entrega dos
arquivos, não toda a interação do navegador.

Foram verificadas 18 dimensões entre 240 e 2560 px para o layout mobile first, e
11 larguras para o painel de edição/exclusão, incluindo textos longos e orientação
horizontal. Ao alterar a interface, revise também teclado, zoom, frente/costas,
confirmação de exclusão e `prefers-reduced-motion`.

## CI/CD, containers e observabilidade

O workflow `.github/workflows/python-app.yml` roda em pushes e pull requests para
`main`: Python 3.11, PostgreSQL 16, Redis 7, migrations, pytest, cobertura e build
Docker. No push para `main`, publica a imagem em `ghcr.io/bigodemarine/pokemon-api`
com tags `latest` e `sha-…`. A implantação Vercel depende da integração do projeto
com o GitHub, não de uma etapa de deploy nesse workflow.

O `Dockerfile` usa Python 3.11 slim e inicia Uvicorn na porta 8000.

Os manifestos em `k8s/` incluem PostgreSQL com PVC, Redis, API, initContainer de
migration, probes e Service LoadBalancer. Eles referenciam uma tag fixa de imagem;
antes de usar uma versão nova, atualize a referência tanto no initContainer quanto
no container e configure credenciais adequadas ao cluster.

```bash
kubectl apply -f k8s/
kubectl rollout status deployment/pokemon-api
kubectl get pods
kubectl get services
```

A stack ELK opcional do Compose usa Elasticsearch (9200), Logstash (5044) e Kibana
(5601). O Logstash lê `logs/app.log` e envia ao índice `pokemon-api-logs`. Localmente,
a aplicação escreve JSON no terminal e nesse arquivo. Na Vercel, quando
`VERCEL=1`, escreve somente em stdout, disponível nos logs da plataforma.

Kubernetes e ELK são alternativas/complementos de infraestrutura; não são
necessários para usar a interface ou executar a suíte de desenvolvimento.

## Autor e objetivo

**BigodeMarine**. Projeto de estudo de desenvolvimento backend e frontend,
integração de APIs, persistência, cache, testes, containerização e CI/CD.
Pokémon pertence à Nintendo / Game Freak / The Pokémon Company.
