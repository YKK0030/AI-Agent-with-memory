# supervisor.py

from langgraph_supervisor import CompiledWorkflow
from langgraph_supervisor import create_supervisor
from Config.llm import llm
from Graph.Prompt.prompts import supervisor_agent_prompt


def Supervisor(
    search_agent,
    knowledgeGraph_agent,
    output_mode: str = "full_history",
    **compile_kwargs
) -> "CompiledWorkflow":

    supervisor = create_supervisor(
        agents=[search_agent, knowledgeGraph_agent],
        model=llm,
        prompt=supervisor_agent_prompt,
        output_mode=output_mode,
        **compile_kwargs
    )
    return supervisor