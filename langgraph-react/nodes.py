"""
nodes.py holds the actual logic that runs the agent using the info in the state.
"""

from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode
from react import react_agent_runnable, tools
from state import AgentState

load_dotenv()

# Tool executor gets invoked with an AgentAction.
# The AgentAction has the information of which tool to run (TavilySearch/Triple) and the arguments to send these tools.
# It returns the output of the tool used. eg. Tool:Triple, In:3, Out:9
tool_executor = ToolNode(tools)

def run_agent_reasoning_engine(state: AgentState):
    """ Reasoning Node """
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}


def execute_tools(state: AgentState):
    """ Acting Node """
    
    agent_action = state["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}