# The HASTD Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A Hierarchical Agentic approach for high-fidelity structured data extraction from complex, unstructured documents.

The **Hierarchical Agentic Schema-Task Decomposition (HASTD)** framework represents a paradigm shift from monolithic prompting to a structured, resilient, and scalable agentic architecture for data extraction. It excels where traditional LLM pipelines fail, especially with large documents and complex JSON schemas.

---

## ✨ Key Features

* **⚙️ Schema-to-DAG Engine:** Programmatically converts complex JSON schemas into a Directed Acyclic Graph (DAG) of discrete, manageable extraction tasks.
* **🤖 Hierarchical Multi-Agent System (HMAS):** Employs a team of specialized AI agents—a high-level Orchestrator, fine-tuned Extractor SLMs, and dedicated Validation/Correction agents—to execute the task graph efficiently.
* **🔄 Resilient Self-Correction Loop:** Uses LangGraph to create a stateful, cyclical workflow that programmatically validates every extracted piece of data and automatically attempts to correct errors.
* **🎯 Heterogeneous Model Strategy:** Leverages powerful frontier models (e.g., Claude 3 Opus) for complex reasoning and cost-effective, fine-tuned Small Language Models (e.g., Llama 3 8B) for high-throughput extraction.
* **📈 Calibrated Confidence Scoring:** Generates a reliable, multi-faceted confidence score for each field, enabling dependable downstream automation and efficient human-in-the-loop (HITL) workflows.

---

## 🏛️ Architecture

The HASTD framework deconstructs a complex extraction problem into a manageable, multi-stage workflow orchestrated by a team of specialized AI agents.

![HASTD Architecture Diagram](./docs/assets/architecture.png)

---

## 🛠️ Technology Stack

* **Orchestration:** LangGraph
* **Agent Communication:** LangChain
* **Schema Validation:** Pydantic
* **Vector Storage:** ChromaDB (for local prototyping), Milvus / Pinecone (for production)
* **LLMs:**
    * **Orchestrator/Corrector:** Claude 3 Opus/Sonnet, GPT-4o
    * **Extractors (Fine-tuned):** Llama 3 8B, ReaderLM-v2
* **API:** FastAPI
* **Observability:** LangSmith

---

## 🚀 Getting Started

Follow these instructions to set up and run the HASTD framework on your local machine.

### 1. Prerequisites

* Python 3.10+
* An OpenAI or Anthropic API key

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/hastd-extraction.git](https://github.com/your-username/hastd-extraction.git)
    cd hastd-extraction
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    * Create a file named `.env` by copying the example file:
        ```bash
        cp .env.example .env
        ```
    * Open the `.env` file and add your API keys:
        ```env
        OPENAI_API_KEY="sk-..."
        ANTHROPIC_API_KEY="sk-..."
        LANGCHAIN_API_KEY="..." # For LangSmith tracing
        ```

---

## ⚡ Quick Start: Usage

The HASTD framework can be run as a library or through its FastAPI server.

### As a Library

Import the `HASTDExtractor` class, initialize it, and call the `.extract()` method.

```python
from hastd import HASTDExtractor
import json

# 1. Initialize the extractor
extractor = HASTDExtractor()

# 2. Define your inputs
with open("data/samples/document_1.txt", "r") as f:
    unstructured_text = f.read()

with open("data/samples/schema_1.json", "r") as f:
    json_schema = json.load(f)

# 3. Run the extraction process
result = extractor.extract(
    document_content=unstructured_text,
    json_schema=json_schema
)

# 4. Print the results
print(json.dumps(result, indent=2))
