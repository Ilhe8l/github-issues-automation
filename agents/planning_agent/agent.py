#from graph import StateGraph, State
from config import MAX_CHAT_HISTORY_TOKENS
from stateTypes import State
from langchain_core.messages import trim_messages, SystemMessage
from llm_factory import create_llm
from planning_agent.build_prompt import build_prompt

# inicializa o agente usando llm factory
agent = create_llm(temperature=0.3)

async def CallPlanningAgent(state: State) -> State:
    if not isinstance(state["planning_messages"][0], SystemMessage):
        system_prompt = await build_prompt()
        state["planning_messages"].insert(0, SystemMessage(content=system_prompt))
    
    # prepara mensagens
    messages = state["planning_messages"]
    
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
    response = await agent.ainvoke(messages)
    
    # atualiza o estado
    state["planning_messages"].append(response)
    state["planning"] = response.content
    return state
