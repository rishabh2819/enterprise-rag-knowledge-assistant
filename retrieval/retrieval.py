from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain.tools import tool
from pathlib import Path
from dotenv import load_dotenv

from .query_rewriter import rewrite_query
from .department_classifier import classify_department

load_dotenv()

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
PERSIST_DIR = ROOT_DIRECTORY / "vectorstore"

embedding_model = MistralAIEmbeddings(model="mistral-embed")


def get_retriever(k: int = 5, department: str | None = None, use_mmr: bool = True):
    db = Chroma(persist_directory=str(PERSIST_DIR), embedding_function=embedding_model)

    search_kwargs = {"k": k}

    # Metadata filtering — only search chunks tagged with this department
    if department:
        search_kwargs["filter"] = {"department": department}

    if use_mmr:
        # MMR: balances relevance with diversity, avoids near-duplicate chunks
        search_kwargs["fetch_k"] = k * 4      # candidate pool before MMR reranks
        search_kwargs["lambda_mult"] = 0.5    # 0 = max diversity, 1 = max relevance
        return db.as_retriever(search_type="mmr", search_kwargs=search_kwargs)

    # Alternative mode: reject weak matches outright instead of diversifying
    search_kwargs["score_threshold"] = 0.7
    return db.as_retriever(search_type="similarity_score_threshold", search_kwargs=search_kwargs)


@tool
def search_knowledge_base(query: str) -> str:
    """Search the company's policies, FAQs, and knowledge base."""

    search_query = rewrite_query(query)
    department = classify_department(query)

    retriever = get_retriever(department=department)
    documents = retriever.invoke(search_query)

    if not documents:
        return "NO_RELEVANT_INFORMATION_FOUND"

    formatted_chunks = []
    for document in documents:
        source_path = document.metadata.get("source", "unknown source")
        source_name = Path(source_path).name  # just the filename, not full path
        formatted_chunks.append(f"[Source: {source_name}]\n{document.page_content}")

    return "\n\n".join(formatted_chunks)