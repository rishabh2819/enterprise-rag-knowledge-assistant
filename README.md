# 🧠 Enterprise RAG Knowledge Assistant

An enterprise-focused Retrieval-Augmented Generation (RAG) knowledge assistant built with **LangGraph, Mistral AI, ChromaDB, and Streamlit**.

The system allows users to ask questions about internal enterprise documents and generates context-aware answers by retrieving relevant information from a private knowledge base before sending the context to the LLM.

---

## 🚀 Project Overview

Enterprise organizations often have large amounts of internal documentation such as:

- HR policies
- IT security policies
- Product documentation
- Sales playbooks
- Engineering onboarding guides
- FAQs

Finding relevant information across these documents manually can be time-consuming.

This project solves that problem by building an **AI-powered enterprise knowledge assistant**.

Instead of relying only on an LLM's general knowledge, the system:

1. Accepts a user's query
2. Classifies and processes the query
3. Rewrites the query when necessary
4. Retrieves relevant document chunks
5. Generates an answer using retrieved context
6. Returns a grounded response to the user

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      User Query     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    │   Agent Workflow    │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Department /     │        │ Query Rewriter   │
       │ Intent Classifier│        │                  │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌─────────────────────┐
                    │     ChromaDB        │
                    │  Vector Retrieval   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevant Documents  │
                    │      / Context      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Mistral AI      │
                    │  Response Generator │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Grounded Answer   │
                    └─────────────────────┘
```

---

## ✨ Key Features

### 🔎 Retrieval-Augmented Generation

The assistant retrieves relevant information from enterprise documents before generating an answer.

This helps keep responses grounded in the organization's knowledge base and can reduce hallucinations.

### 🧩 LangGraph Workflow

The application uses **LangGraph** to define the RAG workflow as a graph of processing nodes.

This provides a structured and extensible architecture for routing, retrieval, generation, and future agentic capabilities.

### 🧠 Query Rewriting

User queries can be rewritten before retrieval to improve semantic search quality.

Example:

```text
User Query
    ↓
"What is the leave rule?"
    ↓
Query Rewriter
    ↓
"What is the company's policy regarding employee leave?"
    ↓
Vector Retrieval
```

### 🏢 Department Classification

The system includes department-oriented query classification to help determine which enterprise knowledge area is relevant to a query.

### 📚 Enterprise Knowledge Base

The project includes example enterprise documents covering areas such as:

- HR Leave Policy
- IT Security Policy
- Product FAQ
- Sales Playbook
- Engineering Onboarding

### 🗄️ Vector Search with ChromaDB

Document embeddings are stored in ChromaDB and used for semantic similarity search.

### 🤖 Mistral AI

Mistral models are used for query processing, classification, query rewriting, embeddings, and response generation.

### 🖥️ Streamlit Interface

A Streamlit application provides a simple interface for interacting with the knowledge assistant.

---

# 📂 Project Structure

```text
enterprise-rag-knowledge-assistant/
│
├── agents/
│   ├── __init__.py
│   └── rag_agent.py
│
├── data/
│   ├── engineering_onboarding.md
│   ├── hr_leave_policy.md
│   ├── it_security_policy.md
│   ├── product_faq.md
│   └── sales_playbook.md
│
├── ingestion/
│   ├── chunking.py
│   ├── contextualizer.py
│   ├── embeddings.py
│   ├── loader.py
│   └── metadata.json
│
├── retrieval/
│   ├── __init__.py
│   ├── department_classifier.py
│   ├── query_rewriter.py
│   └── retrieval.py
│
├── .gitignore
├── app.py
├── requirement.txt
└── README.md
```

---

# 🔄 RAG Pipeline

### 1. Document Loading

Enterprise documents are loaded from the `data/` directory.

### 2. Text Chunking

Large documents are divided into smaller chunks so that the retrieval system can locate relevant sections efficiently.

### 3. Embedding Generation

Document chunks are converted into vector embeddings using Mistral embeddings.

### 4. Vector Storage

The embeddings are stored in ChromaDB.

```text
Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
ChromaDB
```

### 5. Query Processing

When the user submits a question, the LangGraph workflow processes the query.

The system can classify the query and rewrite it to improve retrieval.

### 6. Semantic Retrieval

The processed query is used to search the vectors stored in ChromaDB and retrieve the most relevant document chunks.

### 7. Response Generation

The retrieved context is passed to the Mistral model, which generates a response based on the enterprise information.

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangGraph | Agentic workflow orchestration |
| LangChain | LLM/RAG ecosystem integrations |
| Mistral AI | LLM and embeddings |
| ChromaDB | Vector database |
| Streamlit | User interface |
| python-dotenv | Environment variable management |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/rishabh2819/enterprise-rag-knowledge-assistant.git
```

Move into the project:

```bash
cd enterprise-rag-knowledge-assistant
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

For Fish shell:

```fish
source .venv/bin/activate.fish
```

## 3. Install dependencies

```bash
pip install -r requirement.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

Do **not** commit your `.env` file to GitHub.

The `.gitignore` file is configured to prevent environment variables and other local files from being uploaded.

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will start locally and provide a browser-based interface for interacting with the Enterprise RAG Knowledge Assistant.

---

# 💬 Example Queries

### HR

```text
What is the company's leave policy?
```

### IT Security

```text
What are the password requirements?
```

### Product

```text
What features are available in the product?
```

### Sales

```text
What is the recommended sales process?
```

### Engineering

```text
What should a new engineer do during onboarding?
```

---

# 🧠 Why LangGraph?

This project was migrated from a traditional LangChain agent approach to **LangGraph** to provide a more explicit and controllable workflow.

The workflow can be represented as:

```text
START
  │
  ▼
Query Classification
  │
  ▼
Query Rewriting
  │
  ▼
Retrieval
  │
  ▼
Context Processing
  │
  ▼
Response Generation
  │
  ▼
 END
```

LangGraph makes the system easier to extend with additional nodes, conditional routing, tool calls, memory, evaluation, and human-in-the-loop workflows.

---

# 🛡️ Security Considerations

Basic security practices are followed for the project:

### Environment Variables

API keys are stored in `.env` rather than directly inside source code.

### Git Ignore

The repository excludes sensitive and generated/local files such as:

```text
.env
.venv/
venv/
env/
__pycache__/
vectorstore/
chroma_db/
*.log
```

### Private Knowledge Base

The architecture is designed around retrieving information from an organization's internal knowledge base rather than relying exclusively on general-purpose LLM knowledge.

---

# 📈 Future Improvements

- [ ] Conversation memory
- [ ] Source citations in generated answers
- [ ] Retrieval evaluation
- [ ] RAGAS-based evaluation
- [ ] Hybrid search
- [ ] Re-ranking
- [ ] Document upload functionality
- [ ] PDF/DOCX ingestion
- [ ] Authentication and authorization
- [ ] Role-based document access
- [ ] Human-in-the-loop approval
- [ ] LangGraph persistence
- [ ] Production vector database
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] Observability and tracing

---

# 🎯 Learning Objectives

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Vector databases
- Semantic search
- Text chunking
- Embeddings
- Query rewriting
- Agentic workflows
- LangGraph
- Mistral AI
- ChromaDB
- Streamlit
- Environment management
- Git/GitHub project organization

---

# 👨‍💻 Author

**Rishabh Yadav**

Computer Science Engineer | Generative AI | Agentic AI | RAG

---

## ⭐ If you found this project useful

Consider giving the repository a ⭐ on GitHub.
