#from graph import StateGraph, State

from config import LLM_API_KEY, LLM_MODEL, MAX_CHAT_HISTORY_TOKENS, SYSTEM_PROMPT
from stateTypes import State
from langchain_core.messages import trim_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    BaseMessage,
    SystemMessage,
    trim_messages,
    ToolMessage
)
import os
from dotenv import load_dotenv
from issues_tool import IssuesTool
from build_prompt import build_prompt

load_dotenv()

# Inicializa o agente diretamente com DeepSeek-R1 local
agent = ChatOpenAI(
    model=LLM_MODEL,
    api_key=LLM_API_KEY,
    #service_tier="priority",
    temperature=0.3,  # exemplo de outros parâmetros
)

agent_with_tools = agent.bind_tools([IssuesTool])
async def CallIssuesAgent(state: State) -> State:
    print("[i] Chamando o agente de issues...")

    if not isinstance(state["messages"][0], SystemMessage):
        system_prompt = await build_prompt()
        state["messages"].insert(0, SystemMessage(content=system_prompt))
        
    # Preparar mensagens
    messages = state["messages"]
    
    messages = trim_messages(
        messages,
        max_tokens=MAX_CHAT_HISTORY_TOKENS,
        allow_partial=False,
        include_system=True,
        strategy="last",
        token_counter=len,
        start_on="human"
    )

    # Chamar o agente
    response = await agent_with_tools.ainvoke(messages)

    # Atualizar o estado
    state["messages"].append(response)
    print("[i] Resposta do agente:", response.content)
    #state["response"] = response.content # salva a resposta para acesso fácil
    return state

    
    