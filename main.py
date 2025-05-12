import streamlit as st
from Graph.Nodes import Search_Agent, KG_Agent, Supervisor_Agent
from langchain.schema import HumanMessage, AIMessage

# Page config
st.set_page_config(page_title="Agentic RAG with Supervisor Agent Architecture", layout="wide")

# CSS: sticky bottom-center input & scrollable history
st.markdown(
    """
    <style>
    .history-container {
        max-height: calc(100vh - 150px);
        overflow-y: auto;
        padding-bottom: 100px; /* space for input */
    }
    .chat-input-container {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        z-index: 100;
        padding: 8px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def get_supervisor():
    return Supervisor_Agent.Supervisor(
        search_agent=Search_Agent.Agent_search_engine,
        knowledgeGraph_agent=KG_Agent.knowledge_graph_agent
    ).compile()

supervisor = get_supervisor()

st.title("💬 Agentic RAG with Supervisor Agent Architecture")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, content)

# Display chat history
history_ph = st.container()
history_ph.markdown('<div class="history-container">', unsafe_allow_html=True)
for role, msg in st.session_state.history:
    if role == "user":
        st.chat_message("user").write(msg)
    elif role == "assistant":
        st.chat_message("assistant").write(msg)
    else:
        # agent-specific messages inside expander
        with st.expander(f"{role.replace('_', ' ').title()} Response"):
            st.write(msg)
history_ph.markdown('</div>', unsafe_allow_html=True)

# Pinned input at bottom center
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
user_input = st.chat_input("Your message...")
st.markdown('</div>', unsafe_allow_html=True)

if user_input:
    # record user
    st.session_state.history.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # agent thinking
    with st.spinner("Agent is thinking..."):
        msgs = [
            HumanMessage(content=c) if r == "user" else AIMessage(content=c)
            for r, c in st.session_state.history if r in ("user", "assistant")
        ]
        # invoke returns breakdown
        result = supervisor.invoke({"messages": msgs})

    # parse intermediate agent results
    agent_breakdown = result.get("agent_responses", {})
    for agent_name, response in agent_breakdown.items():
        st.session_state.history.append((agent_name, response))
        with st.expander(f"{agent_name.replace('_', ' ').title()} Response"):
            st.write(response)

    # record assistant
    final_msgs = result.get("messages", msgs)
    if len(final_msgs) > len(msgs):
        reply = final_msgs[-1].content
        st.session_state.history.append(("assistant", reply))
        st.chat_message("assistant").write(reply)