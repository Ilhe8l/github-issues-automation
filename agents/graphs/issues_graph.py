from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode

from stateTypes import State
from issues_agent.agent import CallIssuesAgent
from issues_agent.issues_tool import close_issue_tool, create_issue_tool, edit_issue_tool, list_issues_tool, read_issues_tool

tools = [close_issue_tool, create_issue_tool, edit_issue_tool, list_issues_tool, read_issues_tool]

# nó de tools
# é preciso dizer qual a chave das mensagens no state (por padrão é "messages") :/
tools_node = ToolNode(tools=tools, messages_key="issues_messages") 


# decide se o agent chamou alguma tool
async def route_agent(state: State):
    messages = state.get("issues_messages", [])

    if not messages:
        return END

    last_msg = messages[-1]

    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return "tools"

    return END


async def get_issues_graph(checkpointer):

    builder = StateGraph(State)

    builder.add_node("issues_agent", CallIssuesAgent)
    builder.add_node("tools", tools_node)

    builder.set_entry_point("issues_agent")

    # após agent - verifica se há tool_call
    builder.add_conditional_edges("issues_agent", route_agent)

    # após tool - volta pro agent
    builder.add_edge("tools", "issues_agent")

    # quando não há tool_call - END
    builder.add_edge("issues_agent", END)

    return builder.compile(checkpointer=checkpointer)
