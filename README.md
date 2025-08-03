# The HASTD Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A Hierarchical Agentic approach for high-fidelity structured data extraction from complex, unstructured documents.

The **Hierarchical Agentic Schema-Task Decomposition (HASTD)** framework represents a paradigm shift from monolithic prompting to a structured, resilient, and scalable agentic architecture for data extraction. It excels where traditional LLM pipelines fail, especially with large documents and complex JSON schemas.

Status: ✅ Minimal Working POC Complete (Self-Correcting Agentic Loop)
Next Milestone: Modular Agent Framework, RAG Integration

---

# 📌 Overview

The HASTD Framework offers a scalable and fault-tolerant system for high-fidelity structured extraction from unstructured data using a modular, agentic approach powered by LangGraph.

---

# ✨ Highlights So Far

✅ LangGraph Agentic Loop: Implemented a self-correcting multi-agent cycle (Extractor → Validator → Corrector).

✅ Pydantic Schema Validation: Validates outputs against real-world schemas (e.g. GitHub Actions).

✅ Schema Parser: Parses JSON schemas into field-level extraction tasks (early DAG generation logic).

✅ Modular Codebase: Organized under src/hastd/core, future-ready for multi-agent orchestration.

---
## 🚀 How to Run the POC
```bash

# Step 1: Clone the repository
git clone https://github.com/Riya0071234/agentic-data-extraction.git
cd agentic-data-extraction

# Step 2: Set up the environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Step 3: Set your OpenAI key
echo OPENAI_API_KEY="sk-..." > .env

# Step 4: Run the proof of concept script
python run_poc.py
```
---

# 💡 Example: What This Script Does

Given an unstructured text file like:
```kotlin
The contact is Jane Doe. Her email is jane@example.com and her user ID is 12345.
```
And a JSON schema that expects name, email, and user_id, it will:

1. Extract the fields using GPT-4o

2. Validate them using Pydantic

3. If invalid (e.g., wrong type or format), automatically attempt to fix them via the correction agent

4. Return structured JSON output + confidence report

---
# 🧭 Current Structure
```bash
├── run_poc.py               # Main entry point: Proof-of-concept agentic loop
└── src/
    └── hastd/
        ├── core/
        │   ├── models.py              # Model registry + test schemas
        │   ├── schema_parser.py       # Task decomposition from schema
        │   └── github_model.py        # Pydantic model matching github_actions_schema.json

```

---
# 🔮 Next Milestones
Goal	Description
📁 Agent Modularization	Move extractor, validator, corrector agents into src/hastd/agents/
📚 RAG Integration	Chunk large documents, store in Vector DB (Chroma), route relevant chunks to extractors
🧠 Fine-tuning	Add SLM extractors (e.g., Llama 3 8B) for cost-efficient large-scale inference
🔄 DAG Execution	Transform schema → DAG of extraction tasks → graph traversal
🧑‍💻 FastAPI Server	Serve extraction as a clean endpoint (/extract)
🧪 Confidence Scores	Implement field-level isotonic regression confidence calibration
🧰 HITL UI (Stretch)	Flag low-confidence fields in a frontend for human review

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

![HASTD Architecture Diagram](https://drive.google.com/file/d/1W-Y5EA3HkRcmFOumqLblAwJ0_snQc7dw/view?usp=drive_link)

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
    git clone (https://github.com/Riya0071234/agentic-data-extraction.git)
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

## 🤝 Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch (git checkout -b feature/your-feature-name).

3. Make your changes.

4. Commit your changes (git commit -m 'Add some amazing feature').

5. Push to the branch (git push origin feature/your-feature-name).

6. Open a Pull Request.

---

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
