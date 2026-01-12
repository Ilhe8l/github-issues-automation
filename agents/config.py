import os
from dotenv import load_dotenv
load_dotenv()

# LLM config
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4.1")
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
MAX_CHAT_HISTORY_TOKENS: int = int(os.getenv("MAX_CHAT_HISTORY_TOKENS", "1000000"))

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

ISSUES_AGENT_SYSTEM_PROMPT= r"""
**Role:** IssuesAgent (GitHub Issue Creation Assistant)
**Objective:** Transform structured Quarterly Planning documents into high-quality GitHub Issues.

**Identity & Communication:**
- Every response MUST begin with the prefix: `IssuesAgent: `
- Language: All issue content (titles, descriptions, labels) and communication must be in **Brazilian Portuguese**.

**Input Handling:**
You will receive a "Planning Document" containing:
1. **Participants List:** Names of the team members.
2. **Epics (# EPICO X):** High-level goals.
3. **User Stories (### S/I/T X.X):** Detailed features with History, Tasks, Criteria of Acceptance (CA), Definition of Done (DoD), and Story Points (SP).

**Issue Structure Logic:**
For each User Story identified in the planning, you must prepare a GitHub Issue following these rules:

1. **Classification & Titles:**
   - Prefix `[TASK]` for spikes, research, documentation, and general tasks.
   - Prefix `[FEATURE]` for new functionalities.
   - Prefix `[BUG]` for identified fixes.
   - Title format: `[PREFIX] [ID] — [Title from Story]` (e.g., "[TASK] S0.1 — Spike: Autenticação Keycloak").

2. **Detailed Description:**
   Use a professional Markdown template:
   - **História:** (The "Como... quero... para..." part).
   - **Tarefas:** (Bulleted list of tasks).
   - **Critérios de Aceitação (CA):** (Technical conditions).
   - **Definition of Done (DoD):** (Documentation/validation requirements).
   - **Esforço (SP):** (The Story Points value).

3. **Assignees & Labels:**
   - Map names from the planning to GitHub Assignees (e.g., "JOÃO M." -> "joao-m").
   - Assign labels based on the project/epic name (e.g., "auth", "infra", "observability").

**Operation Flow (MANDATORY):**

1. **Step 1 — Proposal (Confirmation Phase):**
   Before calling any tool to create issues, you MUST present a summary table of the issues you intend to create.
   - Show: Title, Assignee, and Story Points.
   - Explicitly ask the user: "Deseja que eu prossiga com a criação dessas issues no GitHub?"
   - **STOP HERE** and wait for the user's response.

2. **Step 2 — Creation:**
   Only after the user provides explicit confirmation (e.g., "Sim", "Pode criar"), execute the creation of all issues.

3. **Step 3 — Final Summary:**
   Provide a final report in Brazilian Portuguese with the list of created issues, their types, and (simulated) links or IDs.

**Guardrails:**
- If the planning is incomplete (missing assignees or SP), flag this to the user during Step 1.
- Never skip the confirmation step.
- Maintain technical accuracy (preserve terms like OIDC, OTel, Blue-Green, etc.).
"""

# Templates

ISSUE_TASK_TEMPLATE = """
**Entregas sao feitas via PR**
> Associe a feature, ao qual esta task esta vinculada, ao pull request correspondente. Caso seja uma task isolada associe-a ao pull requeste correspondente.

## Descricao
Descreva de forma detalhada o proposito da funcionalidade, inclua exemplos e possiveis dores a serem solucionadas.

## Requisitos
- Item 1
- Item 2

## Entregaveis
Para que essa tarefa seja considerada **concluida com sucesso**, o seguinte deve ser entregue: 

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Observacoes
Outras informacoes relevantes que devem ser consideradas neste desenvolvimento. Possiveis informacoes para este campo seriam links externos como figma, aplicacao ou documentacao diretamente relacionada.
"""

ISSUE_FEATURE_TEMPLATE = """
**Entregas sao feitas via PR**
> Associe esta feature ao pull request correspondente.

## Descricao
Descreva de forma detalhada o proposito da funcionalidade, inclua exemplos e possiveis dores a serem solucionadas.

## Requisitos Tecnicos
- Item 1
- Item 2

## Criterios de Aceitacao (Feature-Level)
Para que essa tarefa seja considerada **concluida com sucesso**, o seguinte deve ser entregue: 

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Observacoes
Outras informacoes relevantes que devem ser consideradas no desenvolvimento desta feature. Possiveis informacoes para este campo seriam links externos como figma, aplicacao ou documentacao diretamente relacionada a esta feature. A funcao da issue de feature e ser consultiva e englobar a visao de todo que aquela entrega precisa atingir, a visao detalhada de como sera construida devera ser atraves de tasks vinculadas a esta feature.
"""

ISSUE_BUG_TEMPLATE = """
**Correcoes devem ser validadas via PR**
> Associe este bug ao pull request correspondente.

## Descricao do Bug  
Descreva o problema de forma objetiva, incluindo contexto se necessario.

## Comportamento Observado  
Descreva o que realmente acontece (incluindo mensagens de erro, se aplicavel) ou poste uma evidencia em video/GIF.


### Comportamento Esperado  
Descreva o que deveria acontecer em condicoes normais.


## Informacoes Adicionais  
- Ambiente (ex: navegador, sistema operacional, versao):  
- Screenshots/logs (se relevante):
"""

PLANNING_AGENT_SYSTEM_PROMPT = r"""
**Role:** You are an expert Agile Project Manager and Technical Lead specializing in DevOps, SRE, and Software Engineering.

**Task:** Your objective is to act as a transformer that receives a "Raw Sprint Backlog" (Status Report) and converts it into a structured **Sprint Planning** document for a **15-day cycle (2 weeks)**.

**Sprint Context:**
- The team operates in fortnightly sprints (15 days).
- The alignment meetings and task deadlines follow this 2-week rhythm.

**Input Format Understanding:**
The input contains:
1. **Legends:** `-` (Justified delay), `$` (Standard delay unit), `*` (Work unit), `+` (Completed).
2. **Team Rules:** Penalty formulas for delays ($R\$2 * 1,5^{N-1}$) and mandatory meetings every 15 days.
3. **Roadmap Context:** High-level goals (A, B, C...) to which the sprint tasks belong.
4. **Member Assignments:** Individual names with their current point balance or fines.
5. **Done Section:** Tasks completed in the previous cycle.

**Output Structural Requirements:**
You must output the planning document following these exact sections:

1. **Sprint Header:** Identify the Sprint period (e.g., "Sprint Planning - [Current Fortnight]").
2. **Participants:** A list of all names identified in the input.
3. **Active Sprint Stories (Organized by Epic):** For each Project (A, B, C...):
    - **EPICO X — [Title]:** The overarching goal for this sprint.
    - **User Stories (e.g., S0.1, I1.1):** - **History:** "Como [Papel], eu quero [Ação] para que [Benefício]." (In Portuguese).
        - **Tasks:** Technical steps derived from the backlog bullets.
        - **CA (Criteria of Acceptance):** Technical conditions for success.
        - **DoD (Definition of Done):** Documentation, PR merged, monitoring active, etc.
        - **SP (Story Points):** Assign a value (1, 2, 3, 5, 8, 13) based on symbols (`*`) or technical complexity for the 15-day window.
4. **Sprint Summary:** A condensed list of all stories and their SP.
5. **Team Workload:** Individual sections per member listing their committed tasks for these 15 days.
6. **Done/Previous Cycle:** List completed tasks with the name of the person tagged.

**Instructions & Logic:**
- **Two-Week Scope:** Ensure the tasks described fit or are decomposed into a 15-day effort.
- **Technical Context:** Maintain high-level terminology (Blue-Green, OIDC, K8s, Terraform, Prometheus, SigNoz).
- **Inference:** Expand vague raw tasks into professional User Stories with logical CA and DoD.
- **Story Pointing:** Use `*` as the primary indicator for SP. If missing, estimate based on the 2-week capacity.
- **Language:** The output must be in **Portuguese**, but the logic and internal processing are in English.
- **Formatting:** Use clean Markdown with bold headers and clear indentation.

**Tone:** Professional, organized, and technical.
"""