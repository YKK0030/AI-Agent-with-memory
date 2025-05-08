from Config.llm import llm
from Graph.Tool.Tools import SearchEngine
from langgraph.prebuilt.chat_agent_executor import create_react_agent
from Graph.Memory.memory import short_term_memory_store
from Graph.Memory.memory import short_term_memory_store, load_and_save_long_term
from Graph.Prompt.prompts import search_agent_prompt

tools_list = [SearchEngine]

Agent_search_engine = create_react_agent(
    llm,
    tools=tools_list,
    name="search_engine",
    prompt=search_agent_prompt
)