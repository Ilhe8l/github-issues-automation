from langgraph.graph import StateGraph, END
from stateTypes import State
from graphs.planning_graph import get_planning_graph
from graphs.issues_graph import get_issues_graph


# node que só passa o state adiante
async def RouterNode(state: State):
    return state


# node que escolhe e executa o grafo correto
async def run_subgraph(state: State, checkpointer):
    command = state["command"]

    if command == "generate_planning":
        graph = await get_planning_graph(checkpointer)

    elif command == "generate_issues":
        graph = await get_issues_graph(checkpointer)

    else:
        print(f"[x] comando desconhecido: {command}")       
        raise ValueError(f"comando desconhecido: {command}")

    return await graph.ainvoke(state)


def make_run_graph_node(checkpointer):
    async def run_graph_node(state: State):
        return await run_subgraph(state, checkpointer)
    return run_graph_node


async def get_router_graph(checkpointer):
    builder = StateGraph(State)

    builder.add_node("router", RouterNode)
    builder.add_node(
        "run_graph",
        make_run_graph_node(checkpointer)
    )

    builder.set_entry_point("router")
    builder.add_edge("router", "run_graph")
    builder.add_edge("run_graph", END)

    return builder.compile(checkpointer=checkpointer)
