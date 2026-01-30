import base64
import requests
from typing import Optional
from langchain_core.tools import tool
from config import TOKEN, GITHUB_API, REST_HEADERS
from services.github import parse_repo_url
from stateTypes import State


@tool
async def save_file_to_github_tool(
    file_path: str,
    content: str,
    commit_message: str,
    branch: str = "main",
    overwrite: bool = False,
    squad_id: str = "default"
) -> dict:
    """
    Salva (cria ou atualiza) um arquivo no repositório GitHub.

    Parâmetros:
    - file_path: Caminho completo do arquivo no repositório
      (ex: "docs/architecture.md", "src/config/settings.yaml")
    - content: Conteúdo completo do arquivo (texto puro)
    - commit_message: Mensagem do commit
      (ex: "docs: adiciona documentação de arquitetura")
    - branch: Branch onde o arquivo será salvo (default: main)
    - overwrite: 
        • false → falha se o arquivo já existir
        • true  → sobrescreve o arquivo existente

    Comportamento:
    - Se o arquivo não existir → cria
    - Se existir:
        • overwrite=false → erro
        • overwrite=true  → atualiza
    """

    print(f"[i] Salvando arquivo no GitHub: {file_path} (branch: {branch}, overwrite: {overwrite})")
    # verifica se o arquivo já existe
    ORG, REPO = await parse_repo_url(squad_id, "github_planning_repo")
    print("=======================", ORG, REPO)
    url = f"{GITHUB_API}/repos/{ORG}/{REPO}/contents/{file_path}"

    res = requests.get(
        url,
        headers=REST_HEADERS,
        params={"ref": branch}
    )

    sha = None
    if res.status_code == 200:
        if not overwrite:
            return {
                "success": False,
                "error": "Arquivo já existe e overwrite=false"
            }
        sha = res.json()["sha"]

    # encode Base64 (obrigatório pela API)
    encoded_content = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": commit_message,
        "content": encoded_content,
        "branch": branch
    }

    if sha:
        payload["sha"] = sha

    # cria ou atualiza o arquivo
    res = requests.put(
        url,
        headers=REST_HEADERS,
        json=payload
    )

    if res.status_code not in (200, 201):
        return {
            "success": False,
            "error": res.json()
        }

    data = res.json()

    return {
        "success": True,
        "path": data["content"]["path"],
        "commit": data["commit"]["sha"],
        "url": data["content"]["html_url"]
    }
