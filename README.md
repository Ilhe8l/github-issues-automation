# Automatização de Criação de Issues com IA

Este projeto utiliza inteligência artificial para automatizar a criação de issues no GitHub com base em mensagens de usuários. Através de um agente configurado, o sistema interpreta as solicitações dos usuários e gera issues detalhadas, facilitando o gerenciamento de tarefas e problemas em repositórios GitHub.

## Funcionalidades
- Interpretação de mensagens de usuários para identificar problemas ou solicitações.
- Geração automática de issues no GitHub com título, descrição, assignees e labels.
- Utilização de Redis para armazenamento temporário do histórico de mensagens e gerenciamento de estado.
- Frontend simples com Streamlit para interação com o agente.
- Geração de issues por meio de texto ou áudio.

## Docker
O projeto foi dockerizado. Exemplo de uso:

- Build:
  ```
  docker compose build
  ```

- Up:
  ```
  docker compose up -d
  ```

- Frontend:
  Acesse `http://localhost:8501` para interagir com o agente via interface web.

## Configuração

1. **Variáveis de Ambiente**: Configure as seguintes variáveis de ambiente no arquivo `.env`:
   - `LLM_API_KEY`: Chave de API para o modelo de linguagem.
   - `LLM_PROVIDER`: Provedor do modelo de linguagem (ex: `gemini`).
   - `LLM_MODEL`: Modelo do provedor de linguagem (ex: `gpt-4.1`).
   - `GEMINI_API_KEY`: Chave de API para o modelo Gemini (para transcrição do áudio).
   - `GITHUB_TOKEN`: Token de autenticação do GitHub.
   - `GITHUB_REPO_ID`: ID do repositório GitHub onde as issues serão criadas.
   - `GITHUB_PROJECT_ID`: ID do projeto GitHub para associar as issues.
   - `GITHUB_ORG`: Nome da organização ou usuário do GitHub.
   - `GITHUB_REPO`: Nome do repositório GitHub.
   - `REDIS_URL`: URL de conexão com o Redis (padrão: `redis://localhost:6379`).
   - Outras variáveis específicas podem ser definidas em `agent/config.py`.

2. **Configurações do Redis**: Ajuste o tempo de vida (TTL) das entradas no Redis conforme necessário, utilizando a variável `TTL_TIME`.

## Estrutura do Código
- `agent/config.py`: Configurações do agente, incluindo o prompt para criação de issues.
- `agents/issues_tool.py`: Ferramenta que cria a issue no repositório e atualiza campos do Project via GraphQL.
- `agent/graph.py`: Definição do grafo de estados e roteamento do agente.
- `agent/send_message.py`: Script para enviar mensagens de usuários e processar as respostas.
- `agents/streamlit.py`: Frontend simples com Streamlit para interação com o agente via texto ou áudio.

## Formato da Issue (conforme `agents/issues_tool.py`)

A criação da issue usa a API REST do GitHub e depois adiciona o item ao Project via GraphQL, atualizando vários campos customizados. Campos enviados na criação e atualização:

- Campos básicos (REST / issues API):
  - title (issue_name): título da issue
  - body (issue_description): descrição/corpo da issue
  - assignees: lista de usernames (ex: ["user1", "user2"])
  - labels: lista de labels (ex: ["bug", "enhancement"])
  - milestone: número da milestone (ex: 1)

- Campos do Project (GraphQL — exigem IDs de campo e valores):
  - status_field_id / status_id -> {"singleSelectOptionId": status_id}
  - squad_field_id / squad_id -> {"singleSelectOptionId": squad_id}
  - priority_field_id / priority_id -> {"singleSelectOptionId": priority_id}
  - product_field_id / product_id -> {"singleSelectOptionId": product_id}
  - sprint_field_id / sprint_id -> {"iterationId": sprint_id}
  - quarter_field_id / quarter_id -> {"iterationId": quarter_id}
  - start_date_field_id / start_date -> {"date": "YYYY-MM-DD"} (ISO 8601)

Exemplo do payload usado pela tool para criar a issue (REST):
```json
{
  "title": "issue_name",
  "body": "issue_description",
  "assignees": ["user1", "user2"],
  "labels": ["bug"],
  "milestone": 1
}
```

Depois de criar a issue, o código adiciona o conteúdo ao Project com:
- mutation AddIssueToProject(projectId, contentId)

E atualiza os campos do item com a mutation BatchUpdateFields passando os IDs de campo e os valores conforme mostrado acima.

## Como Usar
1. Construa e rode o container 
2. Acesse o frontend via navegador em `http://localhost:8501`
3. Envie uma mensagem de texto ou áudio descrevendo o problema ou solicitação.
4. O agente processará a mensagem e criará uma issue no GitHub conforme necessário.
5. Verifique o repositório GitHub para ver a issue criada.

## Requisitos
- Python 3.11 ou superior
- Bibliotecas necessárias (LangChain, Redis, requests, etc.)

## Contribuição
- Sinta-se à vontade para abrir issues e enviar pull requests para melhorias.