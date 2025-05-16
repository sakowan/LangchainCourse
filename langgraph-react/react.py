"""
react.py sets up the agent with tools, a model, and a prompt. It's the "agent factory."
"""
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")

@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled -> multiplied by 3
    """
    return 3 * float(num)

tools = [
    TavilySearch(max_results=1),
    triple
]

llm = ChatOpenAI(model="gpt-4o-mini")

# Populates the ReAct prompt with:  user-input, tools, scratch pad etc.
# Creates an invokable calling-object to the llm - importable by other files.
# Returns AgentAction or AgentFinish
react_agent_runnable = create_react_agent(llm, tools, react_prompt)