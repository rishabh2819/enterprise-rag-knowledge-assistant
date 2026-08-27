from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma
from pathlib import Path
from dotenv import load_dotenv
from chunking import splitter

load_dotenv()

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
PERSIST_DIR = ROOT_DIRECTORY / "vectorstore"

embedding_model = MistralAIEmbeddings(model="mistral-embed")

def build_vectorstore():

    db = Chroma.from_documents(
        documents=splitter(),
        embedding=embedding_model,
        persist_directory=str(PERSIST_DIR)
    )

    return db


if __name__ == "__main__":
    build_vectorstore()
    print(f"Vector store created at {PERSIST_DIR}")