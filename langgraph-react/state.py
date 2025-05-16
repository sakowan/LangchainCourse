"""
state.py defines the "memory format" for what the agent knows and does as it runs.
"""
import operator
from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish


class AgentState(TypedDict):
    """
    This defines what the agent will remember during the flow.
    """
    
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]