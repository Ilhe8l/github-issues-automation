import requests
from typing import Optional
from config import TOKEN, ORG, REPO, PROJECT_ID
from langchain_core.tools import tool

@tool
async def IssuesTool(
    issue_name: str,
    issue_description: str,
    assignees: list[str],
    labels: list[str],
    squad_id: str,
    status_id: str,
    priority_id: str,
    product_id: str,
    sprint_id: str,
    quarter_id: str,
    start_date: str,
    status_field_id: str,
    squad_field_id: str,
    priority_field_id: str ,
    product_field_id: str,
    sprint_field_id: str,
    quarter_field_id: str,
    start_date_field_id: str,
    milestone_id: int,
    #end_date: Optional[str] = None,
    #end_date_field_id: Optional[str] = None
) -> dict:
    """
    Ferramenta para criar uma issue no repositório GitHub e adicioná-la ao Project com campos customizados.
    
    Parâmetros obrigatórios:
    - issue_name: Título da issue
    - issue_description: Descrição/corpo da issue
    - assignees: Lista de usernames (ex: ["user1", "user2"])
    - labels: Lista de labels (ex: ["bug", "enhancement"])
    - milestone_number: Número da milestone (ex: 1, 2, 3)

    Parâmetros do Project (precisam do ID do campo e do valor):
    - status_id: ID da opção de status (ex: "f75ad846")
    - status_field_id: ID do campo Status (ex: "PVTSSF_lAHOBhP38s4BJKTczg5aD7U")
    - squad_id: ID da opção de squad
    - squad_field_id: ID do campo Squad
    - priority_id: ID da opção de prioridade
    - priority_field_id: ID do campo Priority
    - product_id: ID da opção de produto
    - product_field_id: ID do campo Product
    - sprint_id: ID da iteração do sprint
    - sprint_field_id: ID do campo Sprint
    - quarter_id: ID da iteração do quarter
    - quarter_field_id: ID do campo Quarter
    - start_date: Data de início ISO 8601 (ex: "2025-11-24")
    - start_date_field_id: ID do campo Start date
    """
    # - end_date: Data de fim ISO 8601 (ex: "2025-12-08")
    # - end_date_field_id: ID do campo End date
    # Passo 1: Criar a issue no repositório
    url_issue = f"https://api.github.com/repos/{ORG}/{REPO}/issues"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    issue_data = {
        "title": issue_name,
        "body": issue_description
    }
    
    if milestone_id:
        issue_data["milestone"] = milestone_id
    
    res_issue = requests.post(url_issue, headers=headers, json=issue_data)
    
    if res_issue.status_code != 201:
        print(f"[x] Erro ao criar issue: {res_issue.status_code}")
        print(f"[i] Mensagem: {res_issue.json()}")
        return {
            "success": False,
            "error": res_issue.json()
        }
    
    issue = res_issue.json()
    print(f"[*] Issue criada: {issue['html_url']}")
    print(f"[i] Número: {issue['number']}")
    
    # Passo 2: Adicionar a issue ao Project
    url_graphql = "https://api.github.com/graphql"
    headers_graphql = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    mutation_add = """
    mutation AddIssueToProject($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    
    payload_add = {
        "query": mutation_add,
        "variables": {
            "projectId": PROJECT_ID,
            "contentId": issue["node_id"]
        }
    }
    
    res_add = requests.post(url_graphql, headers=headers_graphql, json=payload_add)
    
    if res_add.status_code != 200 or "errors" in res_add.json():
        print(f"[x] Erro ao adicionar ao Project")
        return {
            "success": True,
            "url": issue["html_url"],
            "number": issue["number"],
            "warning": "Issue criada mas não foi adicionada ao Project"
        }
    
    item_id = res_add.json()["data"]["addProjectV2ItemById"]["item"]["id"]
    print(f"[*] Issue adicionada ao Project")
    
    # Passo 3: Atualizar campos customizados do Project
    mutation_update = """
    mutation UpdateProjectField($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: $value
      }) {
        projectV2Item {
          id
        }
      }
    }
    """
    
    updates_success = []
    updates_failed = []
    
    # Mapeamento de campos single-select
    single_select_fields = [
        ("Status", status_field_id, status_id, "singleSelectOptionId"),
        ("Squad", squad_field_id, squad_id, "singleSelectOptionId"),
        ("Priority", priority_field_id, priority_id, "singleSelectOptionId"),
        ("Product", product_field_id, product_id, "singleSelectOptionId")
    ]
    
    for field_name, field_id, value_id, value_key in single_select_fields:
        if field_id and value_id:
            payload_update = {
                "query": mutation_update,
                "variables": {
                    "projectId": PROJECT_ID,
                    "itemId": item_id,
                    "fieldId": field_id,
                    "value": {value_key: value_id}
                }
            }
            
            res_update = requests.post(url_graphql, headers=headers_graphql, json=payload_update)
            
            if res_update.status_code == 200 and "data" in res_update.json():
                updates_success.append(field_name)
                print(f"[*] Campo '{field_name}' atualizado")
            else:
                updates_failed.append(field_name)
                print(f"[!] Falha ao atualizar '{field_name}'")
    
    # Mapeamento de campos iteration
    iteration_fields = [
        ("Sprint", sprint_field_id, sprint_id, "iterationId"),
        ("Quarter", quarter_field_id, quarter_id, "iterationId")
    ]
    
    for field_name, field_id, value_id, value_key in iteration_fields:
        if field_id and value_id:
            payload_update = {
                "query": mutation_update,
                "variables": {
                    "projectId": PROJECT_ID,
                    "itemId": item_id,
                    "fieldId": field_id,
                    "value": {value_key: value_id}
                }
            }
            
            res_update = requests.post(url_graphql, headers=headers_graphql, json=payload_update)
            
            if res_update.status_code == 200 and "data" in res_update.json():
                updates_success.append(field_name)
                print(f"[*] Campo '{field_name}' atualizado")
            else:
                updates_failed.append(field_name)
                print(f"[!] Falha ao atualizar '{field_name}'")
    
    # Mapeamento de campos date
    date_fields = [
        ("Start date", start_date_field_id, start_date, "date"),
        #("End date", end_date_field_id, end_date, "date")
    ]
    
    for field_name, field_id, value, value_key in date_fields:
        if field_id and value:
            payload_update = {
                "query": mutation_update,
                "variables": {
                    "projectId": PROJECT_ID,
                    "itemId": item_id,
                    "fieldId": field_id,
                    "value": {value_key: value}
                }
            }
            
            res_update = requests.post(url_graphql, headers=headers_graphql, json=payload_update)
            
            if res_update.status_code == 200 and "data" in res_update.json():
                updates_success.append(field_name)
                print(f"[*] Campo '{field_name}' atualizado")
            else:
                updates_failed.append(field_name)
                print(f"[!] Falha ao atualizar '{field_name}'")
    
    return {
        "success": True,
        "url": issue["html_url"],
        "number": issue["number"],
        "item_id": item_id,
        "fields_updated": updates_success,
        "fields_failed": updates_failed
    }