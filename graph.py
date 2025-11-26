from langgraph.graph import StateGraph
from agent import CallIssuesAgent
from stateTypes import State
from langgraph.graph import END
from langchain_core.messages import AIMessage
from issues_tool import IssuesTool
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.redis.aio import AsyncRedisSaver
from config import REDIS_URL, TTL_CONFIG
import logging
logging.basicConfig(level=logging.CRITICAL)

# Desabilita logs específicos do redisvl e langgraph
logging.getLogger("redisvl").setLevel(logging.CRITICAL)
logging.getLogger("langgraph").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("langgraph.checkpoint.redis.aio").setLevel(logging.CRITICAL)
logging.getLogger("redisvl.index.index").setLevel(logging.CRITICAL)


tools = [IssuesTool]
tools_node = ToolNode(tools=tools)

_checkpointer = None
_graph = None

async def route_agent(state):
    last_msg = state["messages"][-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return "tools"
    return END

async def get_graph():
    global _checkpointer, _graph
    
    # Se já existe, reutiliza
    if _graph is not None:
        return _graph
    
    # Cria uma vez só
    if _checkpointer is None:
        async with AsyncRedisSaver.from_conn_string(REDIS_URL, ttl=TTL_CONFIG) as _checkpointer:
            await _checkpointer.asetup()

    builder = StateGraph(State)
    builder.add_node("agent", CallIssuesAgent)
    builder.add_node("tools", tools_node)
    builder.set_entry_point("agent")
    builder.add_edge("tools", "agent")
    builder.add_conditional_edges("agent", route_agent)
    _graph = builder.compile(checkpointer=_checkpointer)
    return _graph

if __name__ == "__main__":
    import asyncio
    graph = asyncio.run(get_graph())
