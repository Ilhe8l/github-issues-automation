from config import ISSUES_AGENT_SYSTEM_PROMPT, ISSUE_TASK_TEMPLATE, ISSUE_BUG_TEMPLATE, ISSUE_FEATURE_TEMPLATE
from issues_agent.get_users import get_users
from issues_agent.get_fields import get_project_info
import time

async def build_prompt() -> str:
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    users = await get_users()
    users_str = ", ".join(users)
    project_info = await get_project_info()
    prompt = ISSUES_AGENT_SYSTEM_PROMPT + f"""\n\nUsers available to assign issues: 
    {users_str}\n\nTemplates available:\nTASK TEMPLATE: {ISSUE_TASK_TEMPLATE}\nBUG TEMPLATE: {ISSUE_BUG_TEMPLATE}\nFEATURE TEMPLATE: 
    {ISSUE_FEATURE_TEMPLATE}\n\nProject fields and options:\n{project_info}\n\nCurrent date and time: {now}. Use this to set due dates or start dates if needed."""
    print ("[*] prompt construído.")
    return prompt

#if __name__ == "__main__":
#    import asyncio
#    prompt = asyncio.run(build_prompt())
#    print(prompt)   