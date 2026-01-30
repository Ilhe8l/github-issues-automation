from config import ISSUES_AGENT_SYSTEM_PROMPT, ISSUE_TASK_TEMPLATE, ISSUE_BUG_TEMPLATE, ISSUE_FEATURE_TEMPLATE
from services.squad import get_squad_info
from issues_agent.get_fields import get_project_info
import time, json

async def build_prompt(squad_id: str) -> str:
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # busca os dados 
    squad_data = await get_squad_info(squad_id)
    project_data = await get_project_info(squad_id)

    # identa e converte para string JSON
    squad_str = json.dumps(squad_data, indent=2, ensure_ascii=False)
    project_str = json.dumps(project_data, indent=2, ensure_ascii=False)

    prompt = f"""{ISSUES_AGENT_SYSTEM_PROMPT}

    **CONTEXT & METADATA**
    [1] CURRENT DATE/TIME: 
        {now}

    [2] SQUAD INFORMATION:
        {squad_str}

    [3] PROJECT FIELDS MAPPING (Use these IDs for the JSON fields):
        {project_str}

    [4] **ISSUE BODY TEMPLATES (Markdown)**
    --- TASK TEMPLATE ---
        {ISSUE_TASK_TEMPLATE}

    --- BUG TEMPLATE ---
        {ISSUE_BUG_TEMPLATE}

    --- FEATURE TEMPLATE ---
        {ISSUE_FEATURE_TEMPLATE}
    """

    print("[*] Prompt construído.")
    print(prompt)
    return prompt
#if __name__ == "__main__":
#    import asyncio
#    prompt = asyncio.run(build_prompt())
#    print(prompt)   