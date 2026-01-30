#from graph import StateGraph, State

from config import MAX_CHAT_HISTORY_TOKENS
from stateTypes import State
from langchain_core.messages import trim_messages, SystemMessage
from llm_factory import create_llm
from issues_agent.issues_tool import read_issues_tool, close_issue_tool, list_issues_tool, edit_issue_tool, create_issue_tool
from issues_agent.build_prompt import build_prompt
import json

# inicializa o agente usando llm factory
agent = create_llm(temperature=0.3)
agent_with_tools = agent.bind_tools([read_issues_tool, close_issue_tool, list_issues_tool, edit_issue_tool, create_issue_tool])
async def CallIssuesAgent(state: State) -> State:
    try:
        if state.get("issues_system_prompt_added") is not True:
            squad_id = state.get("squad_id", "default")
            system_prompt = await build_prompt(squad_id)
            state["issues_messages"].insert(0, SystemMessage(content=system_prompt))
            state["issues_system_prompt_added"] = True
    except Exception as e:
        print(f"[x] erro ao adicionar prompt do sistema: {e}")
    
    # prepara mensagens
    messages = state["issues_messages"]
    
    messages = trim_messages(
        messages,
        max_tokens=MAX_CHAT_HISTORY_TOKENS,
        allow_partial=False,
        include_system=True,
        strategy="last",
        token_counter=len,
        start_on="human"
    )

    # chama o agente
    response = await agent_with_tools.ainvoke(messages)

    # atualiza o estado
    state["issues_messages"].append(response)
   
    return state
