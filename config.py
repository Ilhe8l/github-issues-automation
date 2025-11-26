import os
from dotenv import load_dotenv
load_dotenv()

# LLM config
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4.1")
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
MAX_CHAT_HISTORY_TOKENS: int = int(os.getenv("MAX_CHAT_HISTORY_TOKENS", "1000000"))
MODEL_CONFIG: dict[str, str] = {
    "model": LLM_MODEL,
    "model_provider": LLM_PROVIDER,
    "api_key": LLM_API_KEY,
    "service_tier": "priority"
    #"model_kwargs": {"service_tier": "priority"}
}

# GitHub config
TOKEN: str = os.getenv("GITHUB_TOKEN", "")
ORG: str = os.getenv("GITHUB_ORG", "ilhe8l")
REPO: str = os.getenv("GITHUB_REPO", "teste_issues")
PROJECT_ID: str = os.getenv("GITHUB_PROJECT_ID", "")  
REPO_ID: str = os.getenv("GITHUB_REPO_ID", "")

# Redis config
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
TTL_TIME: int = int(os.getenv("TTL_TIME", 5))  
TTL_CONFIG = {
    "default_ttl": TTL_TIME, 
    "refresh_on_read": False, 
}

# Prompt templates

SYSTEM_PROMPT="""
You are an assistant specialized in creating GitHub issues from user messages.
Your task is to analyze the user's message, extract all relevant information, and create issues accordingly.

All issue **titles, descriptions, labels, and any other text** must be written in **Brazilian Portuguese**.

When a message is received, you must:

1. **Identify the issue title**

   * A short, descriptive sentence summarizing the problem or request, written in Brazilian Portuguese.
   * The title must contain a tag indicating the type of issue at the start:
      - For bugs, start with `[BUG]`
      - For features, start with `[FEATURE]`
      - For tasks and any other requests, start with `[TASK]`
   Example titles:
      - [BUG]: Erro ao salvar perfil de usuário
      - [FEATURE]: Adicionar suporte a autenticação via Google
      - [TASK]: Atualizar documentação da API

2. **Create a detailed issue description**

   * Clearly explain the context, problem, or request in Brazilian Portuguese.
   * Include all relevant details provided by the user.

3. **Set `assignees`**

   * Assign users when mentioned or reasonably inferred.

4. **Create multiple issues if needed**

   * If the message contains more than one task or problem, create separate issues.
   * Use the tool to register each issue individually.

To use the tool, you must provide all required parameters.
Assume the user will often send brief or incomplete messages; interpret them and produce fully structured GitHub issues in Brazilian Portuguese.
Be concise and clear in your issue titles and descriptions.
"""

# Templates

ISSUE_TASK_TEMPLATE = """
🚨 **Entregas são feitas via PR**🚨
> Associe a feature, ao qual esta task está vinculada, ao pull request correspondente. Caso seja uma task isolada associe-a ao pull requeste correspondente.

## Descrição
Descreva de forma detalhada o propósito da funcionalidade, inclua exemplos e possíveis dores a serem solucionadas.

## Requisitos
- Item 1
- Item 2

## Entregáveis
Para que essa tarefa seja considerada **concluída com sucesso**, o seguinte deve ser entregue: 

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Observações
Outras informações relevantes que devem ser consideradas neste desenvolvimento. Possíveis informações para este campo seriam links externos como figma, aplicação ou documentação diretamente relacionada.
"""

ISSUE_FEATURE_TEMPLATE = """
🚨 **Entregas são feitas via PR**🚨
> Associe esta feature ao pull request correspondente.

## Descrição
Descreva de forma detalhada o propósito da funcionalidade, inclua exemplos e possíveis dores a serem solucionadas.

## Requisitos Técnicos
- Item 1
- Item 2

## Critérios de Aceitação (Feature-Level)
Para que essa tarefa seja considerada **concluída com sucesso**, o seguinte deve ser entregue: 

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Observações
Outras informações relevantes que devem ser consideradas no desenvolvimento desta feature. Possíveis informações para este campo seriam links externos como figma, aplicação ou documentação diretamente relacionada a esta feature. A função da issue de feature é ser consultiva e englobar a visão de todo que aquela entrega precisa atingir, a visão detalhada de como será construída deverá ser através de tasks vinculadas a esta feature.
"""

ISSUE_BUG_TEMPLATE = """
🚨 **Correções devem ser validadas via PR**🚨
> Associe este bug ao pull request correspondente.

## Descrição do Bug  
Descreva o problema de forma objetiva, incluindo contexto se necessário.

## Comportamento Observado  
Descreva o que realmente acontece (incluindo mensagens de erro, se aplicável) ou poste uma evidência em vídeo/GIF.


### Comportamento Esperado  
Descreva o que deveria acontecer em condições normais.


## Informações Adicionais  
- Ambiente (ex: navegador, sistema operacional, versão):  
- Screenshots/logs (se relevante):
"""