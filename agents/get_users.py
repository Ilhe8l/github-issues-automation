import requests
from dotenv import load_dotenv
from config import ORG, REPO, TOKEN

async def get_users():
    url = f"https://api.github.com/repos/{ORG}/{REPO}/assignees"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    res = requests.get(url, headers=headers)
    
    if res.status_code == 200:
        assignees = res.json()
        return [user['login'] for user in assignees]
    else:
        print(f"[x] Erro {res.status_code}: {res.json()}")
        return []

# Teste
#if __name__ == "__main__":
#    users = get_users()
#    print(f"[*] Usuários disponíveis: {users}")