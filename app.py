import uuid
import re
import streamlit as st

from agents.rag_agent import agent

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Nexus | Enterprise Knowledge Assistant",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }

    /* Top brand bar */
    .nexus-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1.25rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    .nexus-header h1 {
        color: #f8fafc;
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .nexus-header .subtitle {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 2px;
    }
    .nexus-status {
        display: flex;
        align-items: center;
        gap: 6px;
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .nexus-status .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 6px #4ade80;
    }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 0.25rem 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Source citation chips */
    .source-chip {
        display: inline-block;
        background: #eef2ff;
        color: #4338ca;
        border: 1px solid #c7d2fe;
        border-radius: 999px;
        padding: 3px 11px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 4px 6px 0 0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0f172a;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: #4338ca;
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #3730a3;
    }

    .example-btn button {
        text-align: left;
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
    }
    .example-btn button:hover {
        background: #334155 !important;
        border-color: #4338ca !important;
    }

    .disclaimer-box {
        background: #1e293b;
        border-left: 3px solid #4338ca;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 0.78rem;
        color: #94a3b8 !important;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

EXAMPLE_QUESTIONS = [
    "How many days of annual leave do I get?",
    "What are the password requirements?",
    "What discount can sales reps offer?",
    "How quickly must on-call engineers respond?",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def extract_sources(answer: str) -> list[str]:
    """Pull out cited source filenames like '[Source: hr_leave_policy.md]'
    or 'Source: hr_leave_policy.md' from the answer text."""
    matches = re.findall(r"Source:\s*([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)", answer)
    return sorted(set(matches))


def run_query(query: str) -> str:
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
    )
    return result["messages"][-1].content


def submit_query(query: str):
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.pending_query = query


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Nexus")
    st.caption("Enterprise Knowledge Assistant")
    st.divider()

    st.markdown("**Try asking:**")
    for q in EXAMPLE_QUESTIONS:
        st.markdown('<div class="example-btn">', unsafe_allow_html=True)
        if st.button(q, key=f"ex_{q}", use_container_width=True):
            submit_query(q)
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.pop("pending_query", None)
        st.rerun()

    st.caption(f"Session: `{st.session_state.thread_id[:8]}`")
    st.divider()

    st.markdown(
        '<div class="disclaimer-box">'
        "This assistant only answers from the internal knowledge base "
        "(HR, IT, Product, Sales, Engineering docs). If it doesn't have "
        "relevant information, it will say so rather than guess."
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("""
<div class="nexus-header">
    <div>
        <h1>🧭 Nexus Knowledge Assistant</h1>
        <div class="subtitle">Grounded answers from your company's internal documentation</div>
    </div>
    <div class="nexus-status"><span class="dot"></span>Knowledge Base Connected</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
if not st.session_state.messages:
    st.info("👋 Ask a question about company policies, IT security, product info, sales playbooks, or engineering onboarding — or pick an example from the sidebar.")

for message in st.session_state.messages:
    avatar = "🧑‍💼" if message["role"] == "user" else "🧭"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            sources = extract_sources(message["content"])
            if sources:
                chips = "".join(f'<span class="source-chip">📄 {s}</span>' for s in sources)
                st.markdown(chips, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Handle a pending query (from sidebar example button)
# ---------------------------------------------------------------------------
if "pending_query" in st.session_state:
    query = st.session_state.pop("pending_query")
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(query)
    with st.chat_message("assistant", avatar="🧭"):
        with st.spinner("Searching knowledge base..."):
            answer = run_query(query)
        st.markdown(answer)
        sources = extract_sources(answer)
        if sources:
            chips = "".join(f'<span class="source-chip">📄 {s}</span>' for s in sources)
            st.markdown(chips, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
user_query = st.chat_input("Ask something about company policies, IT, sales, etc...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="🧭"):
        with st.spinner("Searching knowledge base..."):
            answer = run_query(user_query)
        st.markdown(answer)
        sources = extract_sources(answer)
        if sources:
            chips = "".join(f'<span class="source-chip">📄 {s}</span>' for s in sources)
            st.markdown(chips, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer})