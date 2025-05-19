from dotenv import load_dotenv
load_dotenv()

from typing import List, Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import END, MessageGraph
from chains import generate_chain, reflect_chain # Functions we wrote ourselves

# Keys for our nodes
REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    result = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content = result.content)]

builder = MessageGraph()
builder.add_node(REFLECT, reflection_node)
builder.add_node(GENERATE, generation_node)
builder.set_entry_point(GENERATE)

def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
print(graph.get_graph().draw_mermaid())

if __name__ == "__main__":
    print("Running reflection agent...")
    inputs = HumanMessage(content="Just uploaded my new video to youtube https://www.youtube.com/watch?v=683VMCDeGrU go over there and watch it now!")
    response = graph.invoke(inputs)