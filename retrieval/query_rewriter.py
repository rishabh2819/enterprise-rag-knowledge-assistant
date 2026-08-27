from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatMistralAI(model="mistral-small")

REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You rewrite user questions into clear, keyword-rich search queries "
     "for a document retrieval system. Expand vague pronouns, fix typos, "
     "and make the query specific. Return ONLY the rewritten query, "
     "nothing else."),
    ("human", "{query}"),
])


def rewrite_query(query: str) -> str:
    chain = REWRITE_PROMPT | llm
    result = chain.invoke({"query": query})
    return result.content.strip()


if __name__ == "__main__":
    test_query = "how many days do i get"
    print(f"Original: {test_query}")
    print(f"Rewritten: {rewrite_query(test_query)}")