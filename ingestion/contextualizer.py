from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatMistralAI(model="mistral-small")

CONTEXT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are given a full document and one chunk extracted from it. "
     "Write a 1-2 sentence description situating this chunk within the "
     "overall document (mention the document's topic and the chunk's "
     "specific subtopic/section). Return ONLY the description, nothing else."),
    ("human",
     "Full document:\n{full_document}\n\nChunk:\n{chunk}"),
])


def generate_context(full_document: str, chunk: str) -> str:
    chain = CONTEXT_PROMPT | llm
    result = chain.invoke({"full_document": full_document, "chunk": chunk})
    return result.content.strip()