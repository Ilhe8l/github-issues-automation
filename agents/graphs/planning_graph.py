from langgraph.graph import StateGraph, END
from stateTypes import State
from planning_agent.agent import CallPlanningAgent


async def get_planning_graph(checkpointer):
    builder = StateGraph(State)

    # único nó
    builder.add_node("planning_agent", CallPlanningAgent)

    builder.set_entry_point("planning_agent")
    builder.add_edge("planning_agent", END)

    return builder.compile(checkpointer=checkpointer)
