# Smart Knowledge Base (Enterprise RAG API Architecture)
A high-performance, production-ready REST API for a Retrieval-Augmented Generation (RAG) Knowledge Base System. Built entirely using native Python patterns, this platform allows users to securely ingest private documentation, process text into high-density semantic vector embeddings locally, and expose a stateless conversational interface powered by advanced LLMs.
Unlike generic boilerplate AI applications that rely heavily on restrictive orchestration frameworks (like LangChain or LlamaIndex), this core engine was engineered from the ground up using core design patterns to maximize data privacy, maintain strict type safety, ensure database contract isolation, and optimize LLM context window longevity.

## System Architecture & Tech Stack
The architecture is explicitly split into an isolated local data-ingestion pipeline and a fast cloud-generation layer:
* **API Framework:** FastAPI (Python 3.10+, Asynchronous ASGI backend)
* **Data Validation Layer:** Pydantic V2 (Strict runtime type-checking)
* **Database & Vector Storage:** PostgreSQL with the `pgvector` extension
* **Embedding Generation Engine:** Local HuggingFace `all-MiniLM-L6-v2` (Sentence-Transformers executing locally on CPU)
* **LLM Orchestration:** Google Gemini 2.5 Flash API (Leveraging custom safety threshold bypasses for compliance document parsing)

## ✨ Core Engineering Features

* **Data Privacy-Centric Indexing:** Uses a local embedding model to vectorize private PDFs before sending mathematical coordinate distances to PostgreSQL. Sensitive corporate texts are never sent to third-party providers for embedding generation.
* **Stateless Memory Synchronization:** The FastAPI backend remains completely stateless. The conversation history is managed dynamically via incoming client payloads, keeping database overhead low and allowing seamless horizontal scaling.
* **Token-Window Optimization:** Features an automatic background conversation summarization mechanism utilizing Gemini 2.5 Flash to condense long running histories and prevent token-window overflow or latency degradation.
* **Database Contract Isolation:** Employs strict Pydantic V2 data schemas mapped to SQLAlchemy aliases, completely decoupling the client-facing REST API contracts from underlying relational database schemas.
* **Production Security Operations:** Configured with robust Cross-Origin Resource Sharing (CORS) middleware policies and automated pipeline secret protection layouts via pattern-matched `.gitignore` environments.

## 🚀 Local Deployment Instructions

### Prerequisites
* Python 3.10 or higher
* PostgreSQL instance running locally with the `pgvector` extension initialized.

### 1. Project Initialization & Dependency Installation
Clone the repository and initialize a localized virtual environment within your terminal environment:
```bash
# Navigate to the API workspace directory
cd smart-knowledge-api

# Initialize the Python virtual environment
python -m venv .venv

# Activate the environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install frozen production requirements
pip install --upgrade pip
pip install -r requirements.txt
