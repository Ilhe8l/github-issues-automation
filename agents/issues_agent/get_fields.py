import requests
import json
from config import TOKEN, PROJECT_ID, REPO_ID

async def get_project_info():
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    # todo:
    # falta o type da issue lá do github 
    # erro ao cadastrar quarter "The iteration Id does not belong to the field"
    query = """
    query GetProjectFullInfo($projectId: ID!, $repoId: ID!) {
      project: node(id: $projectId) {
        ... on ProjectV2 {
          id
          title
          fields(first: 50) {
            nodes {
              ... on ProjectV2FieldCommon {
                id
                name
                dataType
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                dataType
                options {
                  id
                  name
                  description
                  color
                }
              }
              ... on ProjectV2IterationField {
                id
                name
                dataType
                configuration {
                  iterations {
                    id
                    title
                    startDate
                    duration
                  }
                }
              }
            }
          }
        }
      }
      repo: node(id: $repoId) {
        ... on Repository {
          id
          name
          milestones(first: 100) {
            nodes {
              id
              title
              description
              dueOn
              state
              number
            }
          }
        }
      }
    }
    """
    
    payload = {
        "query": query,
        "variables": {
            "projectId": PROJECT_ID,
            "repoId": REPO_ID
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    # Estrutura o output
    result = {
        "project": {
            "id": data["data"]["project"]["id"],
            "title": data["data"]["project"]["title"],
            "fields": []
        },
        "repository": {
            "id": data["data"]["repo"]["id"],
            "name": data["data"]["repo"]["name"],
            "milestones": []
        }
    }
    
    # Processa os campos do projeto
    for field in data["data"]["project"]["fields"]["nodes"]:
        field_info = {
            "id": field["id"],
            "name": field["name"],
            "dataType": field["dataType"]
        }
        
        # Adiciona opções para campos single-select
        if "options" in field:
            field_info["options"] = [
                {
                    "id": opt["id"],
                    "name": opt["name"],
                    "description": opt["description"],
                    "color": opt["color"]
                }
                for opt in field["options"]
            ]
        
        # Adiciona iterações para campos iteration
        if "configuration" in field and "iterations" in field["configuration"]:
            field_info["iterations"] = [
                {
                    "id": it["id"],
                    "title": it["title"],
                    "startDate": it["startDate"],
                    "duration": it["duration"]
                }
                for it in field["configuration"]["iterations"]
            ]
        
        result["project"]["fields"].append(field_info)
    
    # Processa as milestones
    for milestone in data["data"]["repo"]["milestones"]["nodes"]:
        result["repository"]["milestones"].append({
            "id": milestone["id"],
            "title": milestone["title"],
            "description": milestone["description"],
            "dueOn": milestone["dueOn"],
            "state": milestone["state"],
            "number": milestone["number"]
        })
    print(result)
    return result


#if __name__ == "__main__":
#    # Executa e imprime o resultado formatado
#    import asyncio
#    info = asyncio.run(get_project_info())
#    print(json.dumps(info, indent=2, ensure_ascii=False))
