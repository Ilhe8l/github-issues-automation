from langchain_core.messages import HumanMessage
from typing import Optional
from graphs.router_graph import get_router_graph
from graphs.checkpointer import get_checkpointer

async def process_message(
    user_message: str,
    thread_id: str,
    user_id: str,
    squad_id: Optional[str] = None,
    command: Optional[str] = None

) -> dict:

    checkpointer = await get_checkpointer()
    graph = await get_router_graph(checkpointer)

    target = await target_messages(command)

    response = await graph.ainvoke(
        {
            target: [HumanMessage(content=user_message)],
            "last_user_message": user_message,
            "command": command,  
            "squad_id": squad_id,
        },
        config={
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
                
            }
        }
    )

    return {
        "response": response[f"{target}"][-1].content,
        "thread_id": thread_id,
        "user_id": user_id,
    }

# gerencia o histórico de mensagens de acordo com o comando
async def target_messages(command: Optional[str]) -> str:
    target = "main_messages"
    if command == "generate_planning":
        target = "planning_messages"
    elif command == "generate_issues":
        target = "issues_messages"

    print(f"[i] usando target_messages: {target}")
    return target