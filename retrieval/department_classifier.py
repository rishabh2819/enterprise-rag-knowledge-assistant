from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatMistralAI(model="mistral-small")

KNOWN_DEPARTMENTS = ["HR", "IT", "Product", "Sales", "Engineering"]

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     f"Classify which department a user's question is most likely about. "
     f"Choose exactly one from this list: {', '.join(KNOWN_DEPARTMENTS)}. "
     f"If the question doesn't clearly belong to any one department, or "
     f"could span multiple departments, respond with: None. "
     f"Return ONLY the department name or 'None', nothing else."),
    ("human", "{query}"),
])


def classify_department(query: str) -> str | None:
    chain = CLASSIFY_PROMPT | llm
    result = chain.invoke({"query": query})
    department = result.content.strip()

    if department not in KNOWN_DEPARTMENTS:
        return None

    return department


if __name__ == "__main__":
    tests = [
        "how many sick days do I get",
        "what's our password rotation policy",
        "tell me about the company",
    ]
    for t in tests:
        print(f"{t!r} -> {classify_department(t)}")