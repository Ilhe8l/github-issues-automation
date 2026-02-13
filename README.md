# GitHub Issues Automation Bot

Este projeto consiste em um bot de Discord integrado a agentes de IA para automatizar o gerenciamento de tarefas e projetos no GitHub. Ele permite criar issues e gerar planejamentos de sprint diretamente pelo chat do Discord.

## Funcionalidades

- **Planning Agent (`/planning_agent`)**: Transforma backlogs brutos ou anotações em documentos de planejamento de sprint estruturados.
  - Suporta múltiplos arquivos de entrada para unir contextos.
  - Gera arquivos Markdown persistidos diretamente no GitHub.
- **Issues Agent (`/issues_agent`)**: Converte itens de planejamento em issues do GitHub.
  - Cria tasks, features e bugs com templates padronizados.
  - Associa issues a projetos e squads automaticamente.
- **Comandos Utilitários**:
  - `/ping`: Verifica a latência e saúde do bot.
- **Feedback Visual**: Indicador de "Digitando..." persistente e mensagens de confirmação claras.

## Configuração e Instalação

### 1. Pré-requisitos
- Docker e Docker Compose instalados.
- Token do Discord (Bot).
- Token do GitHub (Personal Access Token).
- Chave de API de LLM (OpenAI, Gemini, etc.).

### 2. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto copiando o exemplo:
```bash
cp .env.example .env
```
Preencha as variáveis conforme `discord/config.py` e `agents/config.py`:
- `DISCORD_TOKEN`: Token do seu bot no Developer Portal.
- `GUILD_ID`: ID do servidor Discord onde os comandos serão registrados.
- `GITHUB_TOKEN`: Token com permissões de repo e project.
- `LLM_API_KEY`, `LLM_MODEL`, `LLM_PROVIDER`: Configurações da IA.

### 3. Configuração de Squads
O bot gerencia múltiplos times (squads) através de configurações no Redis.

1.  Edite o arquivo `squads.json` com os dados dos seus times. **Use este formato:**

```json
{
  "teams": [
    {
      "id": "nome-do-time",
      "display_name": "Nome Bonito do Time",
      "description": "Descrição do que o time faz.",
      "tech_lead": "Nome do Tech Lead",
      "mentors": ["Mentor 1", "Mentor 2"],
      "members": [
        {
          "name": "Nome do Dev",
          "github_user": "user-github",
          "role": "Desenvolvedor"
        }
      ],
      "resources": {
        "github_project": "https://github.com/orgs/ORG/projects/1",
        "github_issues_repo": "https://github.com/ORG/REPO-ISSUES",
        "github_planning_repo": "https://github.com/ORG/REPO-PLANNING"
      },
      "stack": [
        { "name": "Python", "version": "3.11" }
      ]
    }
  ]
}
```

2.  Carregue os dados para o Redis executando o script (necessário rodar sempre que alterar o `squads.json`):

```bash
# Se rodando localmente com python:
pip install redis
python update_redis.py
```

### 4. Executando o Projeto

O projeto é totalmente conteinerizado. Para iniciar:

```bash
docker compose up --build
```
Isso subirá os serviços:
- `redis`: Banco de dados em memória.
- `discord_bot_service`: Interface do bot Discord.
- `agents_service`: Cérebro da IA que processa as filas.

## Como Contribuir
1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças.
4. Abra um Pull Request.