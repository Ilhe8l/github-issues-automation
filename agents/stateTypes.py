from typing import TypedDict, List, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    response: str
    last_user_message: str
    tool_results: List[str]
    #tool_calls = int
