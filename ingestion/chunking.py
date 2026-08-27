from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import loader
from contextualizer import generate_context
from dotenv import load_dotenv

load_dotenv()


def splitter():
    docs = loader()

    # Map each source file to its full text, so we can pass full context
    # to the LLM when contextualizing each chunk from that source.
    full_text_by_source = {
        doc.metadata.get("source"): doc.page_content for doc in docs
    }

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(docs)

    for chunk in chunks:
        source = chunk.metadata.get("source")
        full_document = full_text_by_source.get(source, "")

        context = generate_context(full_document, chunk.page_content)

        # Prepend the context to the chunk so it's embedded together
        chunk.page_content = f"{context}\n\n{chunk.page_content}"

    return chunks


if __name__ == "__main__":
    parts = splitter()
    print(f"Loaded {len(parts)} chunks")
    print(parts[0].page_content[:300])