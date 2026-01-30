from langgraph.graph import StateGraph, END
from stateTypes import State
from planning_agent.agent import CallPlanningAgent
from langgraph.prebuilt import ToolNode
from planning_agent.github_tool import save_file_to_github_tool
from langchain_core.messages import AIMessage

tools = [save_file_to_github_tool]

# nó de tools
tools_node = ToolNode(tools=tools, messages_key="planning_messages")


# decide se o agent chamou alguma tool
async def route_agent(state: State):
    messages = state.get("planning_messages", [])

    if not messages:
        return END

    last_msg = messages[-1]

    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return "tools"

    return END

async def get_planning_graph(checkpointer):
    builder = StateGraph(State)

    # único nó
    builder.add_node("planning_agent", CallPlanningAgent)
    builder.add_node("tools", tools_node)
    builder.set_entry_point("planning_agent")


    # após agent - verifica se há tool_call
    builder.add_conditional_edges("planning_agent", route_agent)
    # após tool - volta pro agent
    builder.add_edge("tools", "planning_agent")
    # quando não há tool_call - END
    builder.add_edge("planning_agent", END)

    return builder.compile(checkpointer=checkpointer)
