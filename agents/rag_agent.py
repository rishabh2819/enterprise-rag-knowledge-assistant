from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

from retrieval.retrieval import search_knowledge_base

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful enterprise knowledge assistant. Use the "
    "search_knowledge_base tool to answer questions using company documents. "
    "Each retrieved chunk is tagged with its source document, e.g. "
    "'[Source: hr_leave_policy.md]'. When you answer, cite the source "
    "document(s) your answer is based on at the end of your response, "
    "e.g. 'Source: hr_leave_policy.md'.\n\n"
    "STRICT RULE: If the tool returns 'NO_RELEVANT_INFORMATION_FOUND', "
    "you must NOT attempt to answer the question using your own general "
    "knowledge. Instead, respond with exactly: "
    "'I don't have information about that in the knowledge base.' "
    "Do not add anything else in that case."
)

tools = [search_knowledge_base]

# bind_tools with default (no forced named tool_choice) -- Mistral's API
# only accepts the plain strings 'auto'/'any'/'none'/'required', and this
# avoids the structured "force this specific tool" object that create_agent
# sends internally and that langchain-mistralai can't translate correctly.
llm = ChatMistralAI(model="mistral-medium-3-5").bind_tools(tools)


def call_model(state: MessagesState):
    messages = state["messages"]
    # Prepend the system prompt only if not already present
    if not messages or messages[0].type != "system":
        from langchain_core.messages import SystemMessage
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)


def ask(query: str, thread_id: str = "default") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke({"messages": [{"role": "user", "content": query}]}, config=config)
    return result["messages"][-1].content


if __name__ == "__main__":
    thread_id = "cli-session"
    while True:
        query = input("Ask something (or 'quit'): ")
        if query.lower() == "quit":
            break
        print(ask(query, thread_id=thread_id))