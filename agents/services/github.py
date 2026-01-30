import requests
import re
from config import TOKEN, GITHUB_API, GRAPHQL_API, REST_HEADERS, GRAPHQL_HEADERS
from services.squad import get_squad_info

async def parse_repo_url(squad_id: str, repo_type: str) -> tuple[str, str]:
    squad = await get_squad_info(squad_id)

    repo_url = squad["resources"].get(repo_type)
    if not repo_url:
        raise ValueError(f"URL do repositório não encontrada para a squad {squad_id, repo_type}")

    match = re.search(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", repo_url)
    if not match:
        raise ValueError(f"URL de repositório inválida: {repo_url}")

    return match.group(1), match.group(2)

async def get_project_id(squad_id: str) -> str:
    squad = await get_squad_info(squad_id)

    project_url = squad["resources"].get("github_project")
    if not project_url:
        raise ValueError(f"URL do projeto não encontrada para a squad {squad_id}")

    # detecta se é user ou org
    user_match = re.search(r"/users/([^/]+)/projects/(\d+)", project_url)
    org_match = re.search(r"/orgs/([^/]+)/projects/(\d+)", project_url)

    if user_match: #só pra eu poder testar localmente com meu user
        owner_type = "user"
        owner = user_match.group(1)
        project_number = int(user_match.group(2))

        query = """
        query($login: String!, $number: Int!) {
          user(login: $login) {
            projectV2(number: $number) {
              id
            }
          }
        }
        """
        variables = {
            "login": owner,
            "number": project_number
        }

    elif org_match:
        owner_type = "organization"
        owner = org_match.group(1)
        project_number = int(org_match.group(2))

        query = """
        query($login: String!, $number: Int!) {
          organization(login: $login) {
            projectV2(number: $number) {
              id
            }
          }
        }
        """
        variables = {
            "login": owner,
            "number": project_number
        }

    else:
        raise ValueError(f"URL de projeto inválida: {project_url}")

    res = requests.post(
        GRAPHQL_API,
        headers=GRAPHQL_HEADERS,
        json={
            "query": query,
            "variables": variables
        }
    )

    res.raise_for_status()
    data = res.json()

    # valida erros GraphQL
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    root = data["data"].get(owner_type)
    if not root or not root.get("projectV2"):
        raise ValueError(
            f"Projeto não encontrado ou sem acesso ({owner_type}: {owner}, projeto #{project_number})"
        )

    return root["projectV2"]["id"]
