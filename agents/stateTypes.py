from typing import TypedDict, List, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    main_messages: Annotated[List[BaseMessage], add_messages]
    planning_messages: Annotated[List[BaseMessage], add_messages]
    issues_messages: Annotated[List[BaseMessage], add_messages]
    response: str
    last_user_message: str
    planning: Optional[str]
    command: str
    #tool_calls = int
