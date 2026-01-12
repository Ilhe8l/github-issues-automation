from config import PLANNING_AGENT_SYSTEM_PROMPT
from issues_agent.get_users import get_users
from issues_agent.get_fields import get_project_info
import time

async def build_prompt() -> str:
    prompt = PLANNING_AGENT_SYSTEM_PROMPT
    print ("[*] prompt construído.")
    return prompt

#if __name__ == "__main__":
#    import asyncio
#    prompt = asyncio.run(build_prompt())
#    print(prompt)   