# Automatização de Criação de Issues com IA
Este projeto utiliza inteligência artificial para automatizar a criação de issues no GitHub com base em mensagens de usuários. Através de um agente configurado, o sistema interpreta as solicitações dos usuários e gera issues detalhadas, facilitando o gerenciamento de tarefas e problemas em repositórios GitHub.
## Funcionalidades
- Interpretação de mensagens de usuários para identificar problemas ou solicitações.
- Geração automática de issues no GitHub com título, descrição, assignes e labels.
- Utilização de Redis para armazenamento temporário do histórico de mensagens e gerenciamento de estado.S
## Configuração
1. **Variáveis de Ambiente**: Configure as seguintes variáveis de ambiente no arquivo `.env`:
   - `LLM_API_KEY`: Chave de API para o modelo de linguagem.
   - `GITHUB_TOKEN`: Token de autenticação do GitHub.
   - `GITHUB_REPO_ID`: ID do repositório GitHub onde as issues serão criadas.
   - `GITHUB_PROJECT_ID`: ID do projeto GitHub para associar as issues.
   - `GITHUB_ORG`: Nome da organização ou usuário do GitHub.
   - `GITHUB_REPO`: Nome do repositório GitHub.
   - `REDIS_URL`: URL de conexão com o Redis (padrão: `redis://localhost:6379`).
2. **Configurações do Redis**: Ajuste o tempo de vida (TTL) das entradas no Redis conforme necessário, utilizando a variável `TTL_TIME`.
## Estrutura do Código
- `agent/config.py`: Configurações do agente, incluindo o prompt para criação de issues.
- `agent/graph.py`: Definição do grafo de estados e roteamento do agente.
- `agent/send_message.py`: Script para enviar mensagens de usuários e processar as respostas.
## Como Usar
1. Execute o script `send_message.py`.
2. Insira a mensagem do usuário quando solicitado.
3. O agente processará a mensagem e criará as issues correspondentes no GitHub.
## Requisitos
- Python 3.8 ou superior
- Bibliotecas necessárias (LangChain, Redis, etc.)
## Contribuição 
- Sinta-se à vontade para abrir issues e enviar pull requests para melhorias.