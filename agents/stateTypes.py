from typing import TypedDict, List, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    main_messages: Annotated[List[BaseMessage], add_messages]
    planning_messages: Annotated[List[BaseMessage], add_messages]
    planning_system_prompt_added: bool 
    issues_messages: Annotated[List[BaseMessage], add_messages]
    issues_system_prompt_added: bool
    squad_id: str
    #issues_data_json: Optional[str]
    #issues_data_markdown: Optional[str]
    response: str
    last_user_message: str
    planning: Optional[str]
    command: str
    #tool_calls = int
