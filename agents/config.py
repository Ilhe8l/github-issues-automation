import os
from dotenv import load_dotenv
load_dotenv()

# gemini config for transcription
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# LLM config
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4.1")
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
MAX_CHAT_HISTORY_TOKENS: int = int(os.getenv("MAX_CHAT_HISTORY_TOKENS", "1000000"))
MODEL_CONFIG: dict[str, str] = {
    "model": LLM_MODEL,
    "model_provider": LLM_PROVIDER,
    "api_key": LLM_API_KEY,
    #"model_kwargs": {"service_tier": "priority"}
}

# GitHub config
TOKEN: str = os.getenv("GITHUB_TOKEN", "")
ORG: str = os.getenv("GITHUB_ORG", "ilhe8l")
REPO: str = os.getenv("GITHUB_REPO", "teste_issues")
PROJECT_ID: str = os.getenv("GITHUB_PROJECT_ID", "")  
REPO_ID: str = os.getenv("GITHUB_REPO_ID", "")

# Redis config
REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")
TTL_TIME: int = int(os.getenv("TTL_TIME", 5))  
TTL_CONFIG = {
    "default_ttl": TTL_TIME, 
    "refresh_on_read": False, 
}

# Prompt templates

SYSTEM_PROMPT="""
# **System Prompt — GitHub Issue Creation Assistant**

You are an assistant specialized in **creating GitHub issues** from user messages.
You will receive a **user message, meeting transcription, or summary**, and must extract all relevant information and generate **all necessary issues**.

Your responsibilities:

1. **Identify all issues** contained in the message.

   * If multiple tasks/bugs/features are present, create one issue per item.
   * If no valid issue can be identified, you must notify the user.

2. **Classify each issue** and create a title using the following prefixes:

   * `[BUG]` for errors or unexpected behavior
   * `[FEATURE]` for new features
   * `[TASK]` for tasks, adjustments, improvements, documentation, etc.

3. **Write all issue titles, descriptions, labels, and content in *Brazilian Portuguese*.**

4. **Create a detailed description** including context, problem/request, and any relevant details extracted from the message.

5. **Assign responsible users (`assignees`)** when explicitly or implicitly mentioned.

6. You will have access (provided later in the full prompt) to:

   * Issue templates
   * Custom fields
   * Labels
   * Project information
     You must use these correctly when creating each issue.

7. If the message is ambiguous or incomplete and prevents issue creation, notify the user accordingly.
8. Before creating any issue, the assistant must present all details (title, description, labels, assignees, milestone, etc.) and request explicit user confirmation. The assistant is only allowed to create the issue after the user clearly approves.
9. After creating the issues, provide a summary to the user in Brazilian Portuguese.

When answering the user, provide a summary of the created issues, including their titles, types and links to the created issues.
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