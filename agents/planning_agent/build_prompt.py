from config import PLANNING_AGENT_SYSTEM_PROMPT
from issues_agent.get_fields import get_project_info
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from services.squad import get_squad_info


async def build_prompt(squad_id: str) -> str:
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))

    formatted = now.strftime("%Y-%m-%d %H:%M:%S (%A)")
    prompt = f"""{PLANNING_AGENT_SYSTEM_PROMPT}
    Squad ID: {squad_id}
    SQUAD INFO: {await get_squad_info(squad_id)}
    # Use the above squad information to tailor your planning suggestions.
    Current date and time: {formatted}
    """
    print ("[*] prompt construído.")
    return prompt

#if __name__ == "__main__":
#    import asyncio
#    prompt = asyncio.run(build_prompt())
#    print(prompt)   