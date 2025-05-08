from Config.llm import llm
from Graph.Tool.Tools import get_vector_response, add_data_to_kg
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from Graph.Prompt.prompts import kg_agent_prompt

tools_list = [get_vector_response, add_data_to_kg]

knowledge_graph_agent = create_react_agent(
    llm,
    tools=tools_list,
    name="knowledge_graph_agent",
    prompt= kg_agent_prompt 
)