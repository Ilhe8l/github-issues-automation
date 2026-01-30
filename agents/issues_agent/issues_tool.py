import requests
import json
from typing import Optional, List
from langchain_core.tools import tool
from config import TOKEN, GITHUB_API, GRAPHQL_API, REST_HEADERS, GRAPHQL_HEADERS
from services.github import get_project_id, parse_repo_url


# rest api - issues

def _create_issue(
    title: str,
    body: str,
    assignees: list[str],
    labels: list[str],
    milestone_number: Optional[int],
    org: str,
    repo: str
) -> dict:
    print(f"[i] Criando issue: {title}")
    res = requests.post(
        f"{GITHUB_API}/repos/{org}/{repo}/issues",
        headers=REST_HEADERS,
        json={
            "title": title,
            "body": body,
            "assignees": assignees,
            "labels": labels,
            **({"milestone": milestone_number} if milestone_number else {})
        }
    )
    res.raise_for_status()
    issue = res.json()
    print(f"[*] Issue #{issue['number']} criada")
    return issue


def _update_issue(
    issue_number: int,
    org: str,
    repo: str,
    **fields
) -> dict:
    print(f"[i] Atualizando issue #{issue_number}")
    payload = {k: v for k, v in fields.items() if v is not None}

    res = requests.patch(
        f"{GITHUB_API}/repos/{org}/{repo}/issues/{issue_number}",
        headers=REST_HEADERS,
        json=payload
    )
    res.raise_for_status()
    issue = res.json()
    print(f"[*] Issue #{issue_number} atualizada")
    return issue


# graphql api - project

def _add_issue_to_project(issue_node_id: str, project_id: str) -> str:
    print(f"[i] Adicionando issue ao projeto")
    mutation = """
    mutation ($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {
        projectId: $projectId,
        contentId: $contentId
      }) {
        item { id }
      }
    }
    """
    res = requests.post(
        GRAPHQL_API,
        headers=GRAPHQL_HEADERS,
        json={
            "query": mutation,
            "variables": {
                "projectId": project_id,
                "contentId": issue_node_id
            }
        }
    )
    res.raise_for_status()
    data = res.json()
    
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    
    item_id = data["data"]["addProjectV2ItemById"]["item"]["id"]
    print(f"[*] Issue adicionada ao projeto")
    return item_id


def _format_graphql_value(value: dict) -> str:
    """
    Formata o valor corretamente para GraphQL.
    Valores como iterationId, singleSelectOptionId devem ser strings SEM aspas no campo,
    mas COM aspas no valor do ID.
    """
    formatted_parts = []
    for key, val in value.items():
        # O valor do ID deve ter aspas, mas o nome do campo não
        formatted_parts.append(f'{key}: "{val}"')
    return "{" + ", ".join(formatted_parts) + "}"


def _update_project_fields(item_id: str, updates: list[dict], project_id: str) -> dict:
    """
    updates = [
      {"fieldId": "...", "value": {"singleSelectOptionId": "..."}},
      {"fieldId": "...", "value": {"iterationId": "..."}},
      {"fieldId": "...", "value": {"date": "2025-11-24"}}
    ]
    """
    if not updates:
        print("[!] Nenhum campo para atualizar")
        return {}
        
    print(f"[i] Atualizando {len(updates)} campo(s) do projeto")
    mutations = []

    for i, upd in enumerate(updates):
        value_str = _format_graphql_value(upd['value'])
        mutations.append(f"""
        f{i}: updateProjectV2ItemFieldValue(input: {{
          projectId: "{project_id}"
          itemId: "{item_id}"
          fieldId: "{upd['fieldId']}"
          value: {value_str}
        }}) {{
          projectV2Item {{ id }}
        }}
        """)

    query = f"mutation {{ {' '.join(mutations)} }}"

    res = requests.post(
        GRAPHQL_API,
        headers=GRAPHQL_HEADERS,
        json={"query": query}
    )
    res.raise_for_status()
    data = res.json()
    
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")
    
    print(f"[*] Campos do projeto atualizados")
    return data


def _update_issue_project_fields(
    issue_node_id: str,
    updates: list[dict],
    project_id: str
):
    """
    Atualiza campos do Project a partir do node_id da issue.
    """
    item_id = _add_issue_to_project(issue_node_id, project_id)
    return _update_project_fields(item_id, updates, project_id)


# tools

@tool
async def create_issue_tool(
    issue_name: str,
    issue_description: str,
    assignees: list[str],
    labels: list[str],
    milestone_number: Optional[int],
    status_id: str,
    status_field_id: str,
    squad_id: str,
    squad_field_id: str,
    priority_id: str,
    priority_field_id: str,
    product_id: str,
    product_field_id: str,
    sprint_id: str,
    sprint_field_id: str,
    quarter_id: str,
    quarter_field_id: str,
    start_date: str,
    start_date_field_id: str,
    squad_id_param: str = "default"
) -> dict:
    """
    Ferramenta para criar uma issue no repositório GitHub e adicioná-la ao Project
    com campos customizados.
    O campo squad_id_param é usado para determinar qual squad está criando a issue,
    e assim buscar o repositório e projeto corretos.
    Exemplo: "plataforma", "ia", etc.
    """
    org, repo = await parse_repo_url(squad_id_param, "github_issues_repo")
    project_id = await get_project_id(squad_id_param)


    try:
        issue = _create_issue(
            issue_name,
            issue_description,
            assignees,
            labels,
            milestone_number, 
            org,
            repo
        )

        item_id = _add_issue_to_project(issue["node_id"], project_id)

        _update_project_fields(item_id, [
            {"fieldId": status_field_id, "value": {"singleSelectOptionId": status_id}},
            {"fieldId": squad_field_id, "value": {"singleSelectOptionId": squad_id}},
            {"fieldId": priority_field_id, "value": {"singleSelectOptionId": priority_id}},
            {"fieldId": product_field_id, "value": {"singleSelectOptionId": product_id}},
            {"fieldId": sprint_field_id, "value": {"iterationId": sprint_id}},
            {"fieldId": quarter_field_id, "value": {"iterationId": quarter_id}},
            {"fieldId": start_date_field_id, "value": {"date": start_date}},
        ], project_id)

        return {
            "success": True,
            "number": issue["number"],
            "url": issue["html_url"],
            "item_id": item_id,
            "error": None
        }
    except Exception as e:
        print(f"[x] Erro ao criar issue: {e}")
        return {
            "success": False,
            "number": None,
            "url": None,
            "item_id": None,
            "error": str(e)
        }


@tool
async def edit_issue_tool(
    issue_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    assignees: Optional[list[str]] = None,
    labels: Optional[list[str]] = None,
    milestone_number: Optional[int] = None,

    # project fields (opcionais)
    status_id: Optional[str] = None,
    status_field_id: Optional[str] = None,
    squad_id: Optional[str] = None,
    squad_field_id: Optional[str] = None,
    priority_id: Optional[str] = None,
    priority_field_id: Optional[str] = None,
    product_id: Optional[str] = None,
    product_field_id: Optional[str] = None,
    sprint_id: Optional[str] = None,
    sprint_field_id: Optional[str] = None,
    quarter_id: Optional[str] = None,
    quarter_field_id: Optional[str] = None,
    start_date: Optional[str] = None,
    start_date_field_id: Optional[str] = None,
    squad_id_param: str = "default"
) -> dict:
    """
    Edita uma issue existente no GitHub e opcionalmente
    atualiza campos do Project.
    O campo squad_id_param é usado para determinar qual squad está editando a issue,
    e assim buscar o repositório e projeto corretos.
    Exemplo: "plataforma", "ia", etc.
    """
    org, repo = await parse_repo_url(squad_id_param, "github_issues_repo")
    project_id = await get_project_id(squad_id_param)
    try:
        issue = _update_issue(
            issue_number,
            title=title,
            body=body,
            state=state,
            assignees=assignees,
            labels=labels,
            milestone=milestone_number,
            org=org,
            repo=repo
        )

        project_updates = []

        if status_id and status_field_id:
            project_updates.append({
                "fieldId": status_field_id,
                "value": {"singleSelectOptionId": status_id}
            })

        if squad_id and squad_field_id:
            project_updates.append({
                "fieldId": squad_field_id,
                "value": {"singleSelectOptionId": squad_id}
            })

        if priority_id and priority_field_id:
            project_updates.append({
                "fieldId": priority_field_id,
                "value": {"singleSelectOptionId": priority_id}
            })

        if product_id and product_field_id:
            project_updates.append({
                "fieldId": product_field_id,
                "value": {"singleSelectOptionId": product_id}
            })

        if sprint_id and sprint_field_id:
            project_updates.append({
                "fieldId": sprint_field_id,
                "value": {"iterationId": sprint_id}
            })

        if quarter_id and quarter_field_id:
            project_updates.append({
                "fieldId": quarter_field_id,
                "value": {"iterationId": quarter_id}
            })

        if start_date and start_date_field_id:
            project_updates.append({
                "fieldId": start_date_field_id,
                "value": {"date": start_date}
            })

        if project_updates:
            _update_issue_project_fields(
                issue["node_id"],
                project_updates,
                project_id
            )

        return {
            "success": True,
            "number": issue["number"],
            "state": issue["state"],
            "url": issue["html_url"],
            "project_fields_updated": bool(project_updates),
            "error": None
        }
    except Exception as e:
        print(f"[x] Erro ao editar issue #{issue_number}: {e}")
        return {
            "success": False,
            "number": issue_number,
            "state": None,
            "url": None,
            "project_fields_updated": False,
            "error": str(e)
        }


@tool
async def close_issue_tool(issue_number: int, squad_id_param: str = "default") -> dict:
    """
    Fecha uma issue no GitHub (remoção lógica).
    O campo squad_id_param é usado para determinar qual squad está fechando a issue,
    e assim buscar o repositório correto.
    Exemplo: "plataforma", "ia", etc.
    """
    org, repo = await parse_repo_url(squad_id_param, "github_issues_repo")
    try:
        issue = _update_issue(issue_number, state="closed", org=org, repo=repo)
        return {
            "success": True,
            "number": issue["number"],
            "state": issue["state"],
            "error": None
        }
    except Exception as e:
        print(f"[x] Erro ao fechar issue #{issue_number}: {e}")
        return {
            "success": False,
            "number": issue_number,
            "state": None,
            "error": str(e)
        }


@tool
async def read_issues_tool(issue_numbers: List[int], squad_id_param: str = "default") -> list[dict]:
    """
    Lê uma ou várias issues e retorna informações relevantes,
    incluindo status de workflow via labels (status:*).
    O campo squad_id_param é usado para determinar qual squad está lendo as issues,
    e assim buscar o repositório correto.
    Exemplo: "plataforma", "ia", etc.
    """
    org, repo = await parse_repo_url(squad_id_param, "github_issues_repo")
    results = []

    for n in issue_numbers:
        try:
            print(f"[i] Lendo issue #{n}")
            res = requests.get(
                f"{GITHUB_API}/repos/{org}/{repo}/issues/{n}",
                headers=REST_HEADERS
            )
            res.raise_for_status()
            i = res.json()

            labels = [l["name"] for l in i.get("labels", [])]

            status = next(
                (label.split("status:", 1)[1].strip()
                 for label in labels
                 if label.lower().startswith("status:")),
                "unknown"
            )

            results.append({
                "number": i["number"],
                "title": i["title"],
                "state": i["state"],
                "status": status,
                "assignees": [u["login"] for u in i.get("assignees", [])],
                "labels": labels,
                "milestone": i["milestone"]["title"] if i.get("milestone") else None,
                "url": i["html_url"],
                "error": None
            })
            print(f"[*] Issue #{n} lida")
        except Exception as e:
            print(f"[x] Erro ao ler issue #{n}: {e}")
            results.append({
                "number": n,
                "title": None,
                "state": None,
                "status": None,
                "assignees": [],
                "labels": [],
                "milestone": None,
                "url": None,
                "error": str(e)
            })

    return results


@tool
async def list_issues_tool(state: Optional[str] = None, squad_id_param: str = "default") -> list[dict]:
    """
    Lista número e título das issues.
    Útil para perguntar ao usuário quais deseja manipular.
    O campo squad_id_param é usado para determinar qual squad está listando as issues,
    e assim buscar o repositório correto.
    Exemplo: "plataforma", "ia", etc.
    """
    org, repo = await parse_repo_url(squad_id_param, "github_issues_repo")
    try:
        print(f"[i] Listando issues (state={state or 'all'})")
        params = {"state": state} if state else {}
        res = requests.get(
            f"{GITHUB_API}/repos/{org}/{repo}/issues",
            headers=REST_HEADERS,
            params=params
        )
        res.raise_for_status()

        issues = [
            {
                "number": i["number"],
                "title": i["title"],
                "state": i["state"],
                "error": None
            }
            for i in res.json()
            if "pull_request" not in i
        ]
        print(f"[*] {len(issues)} issue(s) encontrada(s)")
        return issues
    except Exception as e:
        print(f"[x] Erro ao listar issues: {e}")
        return [{
            "number": None,
            "title": None,
            "state": None,
            "error": str(e)
        }]