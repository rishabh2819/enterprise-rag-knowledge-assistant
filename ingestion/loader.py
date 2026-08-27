import json
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
)
from dotenv import load_dotenv

load_dotenv()

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
METADATA_FILE = Path(__file__).resolve().parent / "metadata.json"


def load_metadata_map() -> dict:
    if not METADATA_FILE.exists():
        return {}
    with open(METADATA_FILE, "r") as f:
        return json.load(f)


def loader():
    metadata_map = load_metadata_map()
    docs = []

    for file in DATA_DIRECTORY.glob("*"):
        if file.suffix in (".md", ".txt"):
            file_docs = TextLoader(str(file)).load()
        elif file.suffix == ".pdf":
            file_docs = PyPDFLoader(str(file)).load()
        elif file.suffix == ".docx":
            file_docs = Docx2txtLoader(str(file)).load()
        elif file.suffix == ".csv":
            file_docs = CSVLoader(str(file)).load()
        else:
            continue

        # Attach custom metadata (department, access_level, doc_type) if defined
        extra_metadata = metadata_map.get(file.name, {})
        for doc in file_docs:
            doc.metadata.update(extra_metadata)

        docs += file_docs

    return docs


if __name__ == "__main__":
    documents = loader()
    print(f"Loaded {len(documents)} documents")
    for doc in documents:
        print(doc.metadata)