import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG = os.getenv("GITHUB_ORG")
REPO_NAME = os.getenv("GITHUB_REPO")
PROJECT_NAME = os.getenv("GITHUB_PROJECT")
IS_USER = os.getenv("IS_USER", "true").lower() == "false"  # Define se é usuário ou org

def get_repo_id(org, repo_name, token):
    """
    Busca o ID do repositório usando a API REST do GitHub
    """
    url = f"https://api.github.com/repos/{org}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data["id"],
            "node_id": data["node_id"],
            "name": data["name"],
            "full_name": data["full_name"]
        }
    else:
        raise Exception(f"Erro ao buscar repositório: {response.status_code} - {response.text}")

def get_project_id(org, project_name, token, is_user=False):
    """
    Busca o ID do projeto (Projects V2) usando a API GraphQL do GitHub
    Funciona tanto para organizações quanto para usuários pessoais
    """
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Query GraphQL - muda entre organization e user
    if is_user:
        query = """
        query($login: String!, $cursor: String) {
          user(login: $login) {
            projectsV2(first: 100, after: $cursor) {
              nodes {
                id
                title
                number
                url
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
        }
        """
    else:
        query = """
        query($login: String!, $cursor: String) {
          organization(login: $login) {
            projectsV2(first: 100, after: $cursor) {
              nodes {
                id
                title
                number
                url
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
        }
        """
    
    all_projects = []
    cursor = None
    
    # Paginar através de todos os projetos
    while True:
        variables = {
            "login": org,
            "cursor": cursor
        }
        
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"Erro GraphQL: {data['errors']}")
            
            # Acessa a chave correta dependendo se é user ou organization
            owner_type = "user" if is_user else "organization"
            projects = data["data"][owner_type]["projectsV2"]["nodes"]
            all_projects.extend(projects)
            
            page_info = data["data"][owner_type]["projectsV2"]["pageInfo"]
            if not page_info["hasNextPage"]:
                break
            
            cursor = page_info["endCursor"]
        else:
            raise Exception(f"Erro ao buscar projeto: {response.status_code} - {response.text}")
    
    # Buscar o projeto pelo nome
    for project in all_projects:
        if project["title"] == project_name:
            return {
                "id": project["id"],
                "title": project["title"],
                "number": project["number"],
                "url": project["url"]
            }
    
    owner_label = "usuário" if is_user else "organização"
    raise Exception(f"Projeto '{project_name}' não encontrado no {owner_label} '{org}'")

def main():
    print("🔍 Buscando informações do GitHub...\n")
    
    owner_type = "usuário" if IS_USER else "organização"
    print(f"📍 Tipo de proprietário: {owner_type}")
    
    try:
        # Buscar ID do repositório
        print(f"📦 Buscando repositório: {ORG}/{REPO_NAME}")
        repo_info = get_repo_id(ORG, REPO_NAME, GITHUB_TOKEN)
        print(f"✅ Repositório encontrado!")
        print(f"   ID: {repo_info['id']}")
        print(f"   Node ID: {repo_info['node_id']}")
        print(f"   Nome completo: {repo_info['full_name']}\n")
        
        # Buscar ID do projeto
        print(f"📊 Buscando projeto: {PROJECT_NAME}")
        project_info = get_project_id(ORG, PROJECT_NAME, GITHUB_TOKEN, IS_USER)
        print(f"✅ Projeto encontrado!")
        print(f"   ID: {project_info['id']}")
        print(f"   Título: {project_info['title']}")
        print(f"   Número: {project_info['number']}")
        print(f"   URL: {project_info['url']}\n")
        
        # Retornar ambos os IDs
        return {
            "repo": repo_info,
            "project": project_info
        }
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    result = main()
    
    if result:
        print("\n" + "="*50)
        print("📋 RESUMO")
        print("="*50)
        print(f"Repo ID: {result['repo']['id']}")
        print(f"Repo Node ID: {result['repo']['node_id']}")
        print(f"Project ID: {result['project']['id']}")
        print("="*50)