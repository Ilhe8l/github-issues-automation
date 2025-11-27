from langchain_core.messages import HumanMessage
from graph import get_graph
from stateTypes import State
import asyncio

async def process_message(user_message: str, thread_id: str, user_id: str) -> dict:
    print("[i] Chamando o agente de issues...")

    graph = await get_graph()

    # Executa o grafo com informações do usuário e da sessão
    response = await graph.ainvoke(
        {
            "messages": [HumanMessage(content=user_message)],
            "last_user_message": user_message
        },
        config={
            "configurable": { # interno do grafo
                "user_id": user_id,               
                "thread_id": thread_id
            }
        }
    )
    print("[*] Resposta do agente:", response)

    return {
        "response": response["messages"][-1].content,
        "thread_id": thread_id,
        "user_id": user_id
    }


#if __name__ == "__main__":
#    user_message = input("Digite sua mensagem: ")
#    thread_id = "thread"
#    user_id = "user"
#    response = asyncio.run(process_message(user_message, thread_id, user_id))
    #print(response)