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
    milestone_number: Optional[int] = None,
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

    # Cria a issue no repositório
    url_issue = f"https://api.github.com/repos/{ORG}/{REPO}/issues"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    issue_data = {
        "title": issue_name,
        "body": issue_description,
        "assignees": assignees,
        "labels": labels,
      
    }

    if milestone_number:
        issue_data["milestone"] = milestone_number
    
    
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
    
    # GraphQL headers
    url_graphql = "https://api.github.com/graphql"
    headers_graphql = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Adiciona a issue ao Project e atualiza todos os campos de uma vez
    # Primeira requisição: adiciona ao Project
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
    
    # Segunda requisição: atualiza todos os campos de uma vez
    mutation_batch = """
    mutation BatchUpdateFields(
      $projectId: ID!,
      $itemId: ID!,
      $statusFieldId: ID!,
      $statusValue: ProjectV2FieldValue!,
      $squadFieldId: ID!,
      $squadValue: ProjectV2FieldValue!,
      $priorityFieldId: ID!,
      $priorityValue: ProjectV2FieldValue!,
      $productFieldId: ID!,
      $productValue: ProjectV2FieldValue!,
      $sprintFieldId: ID!,
      $sprintValue: ProjectV2FieldValue!,
      $quarterFieldId: ID!,
      $quarterValue: ProjectV2FieldValue!,
      $startDateFieldId: ID!,
      $startDateValue: ProjectV2FieldValue!
    ) {
      updateStatus: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $statusFieldId
        value: $statusValue
      }) { projectV2Item { id } }
      updateSquad: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $squadFieldId
        value: $squadValue
      }) { projectV2Item { id } }
      updatePriority: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $priorityFieldId
        value: $priorityValue
      }) { projectV2Item { id } }
      updateProduct: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $productFieldId
        value: $productValue
      }) { projectV2Item { id } }
      updateSprint: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $sprintFieldId
        value: $sprintValue
      }) { projectV2Item { id } }
      updateQuarter: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $quarterFieldId
        value: $quarterValue
      }) { projectV2Item { id } }
      updateStartDate: updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $startDateFieldId
        value: $startDateValue
      }) { projectV2Item { id } }
    }
    """
    
    payload = {
        "query": mutation_batch,
        "variables": {
            "projectId": PROJECT_ID,
            "itemId": item_id,
            "statusFieldId": status_field_id,
            "statusValue": {"singleSelectOptionId": status_id},
            "squadFieldId": squad_field_id,
            "squadValue": {"singleSelectOptionId": squad_id},
            "priorityFieldId": priority_field_id,
            "priorityValue": {"singleSelectOptionId": priority_id},
            "productFieldId": product_field_id,
            "productValue": {"singleSelectOptionId": product_id},
            "sprintFieldId": sprint_field_id,
            "sprintValue": {"iterationId": sprint_id},
            "quarterFieldId": quarter_field_id,
            "quarterValue": {"iterationId": quarter_id},
            "startDateFieldId": start_date_field_id,
            "startDateValue": {"date": start_date}
        }
    }
    
    res_batch = requests.post(url_graphql, headers=headers_graphql, json=payload)
    
    if res_batch.status_code != 200:
        print(f"[x] Erro ao processar Project: {res_batch.status_code}")
        return {
            "success": True,
            "url": issue["html_url"],
            "number": issue["number"],
            "warning": "Issue criada mas houve erro ao atualizar o Project"
        }
    
    result = res_batch.json()
    
    if "errors" in result:
        print(f"[x] Erros GraphQL: {result['errors']}")
        return {
            "success": True,
            "url": issue["html_url"],
            "number": issue["number"],
            "warning": "Issue criada mas alguns campos podem não ter sido atualizados",
            "errors": result["errors"]
        }
    
    # erro Erro ao processar: 'addItem'
    # item_id = result["data"]["addItem"]["item"]["id"]
    print(f"[*] Issue adicionada ao Project e campos atualizados")
    
    return {
        "success": True,
        "url": issue["html_url"],
        "number": issue["number"],
        "item_id": item_id,
        "message": "Issue criada e todos os campos do Project atualizados"
    }