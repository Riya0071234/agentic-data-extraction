Of course. This is a great final step. A README that reflects the current working POC and lays out the ambitious future vision is the perfect way to frame your submission.

Here is the entire, final `README.md` code. Replace the old code in your file with this.

-----

# The HASTD Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-proof--of--concept-orange.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A Hierarchical Agentic approach for high-fidelity structured data extraction from complex, unstructured documents.

The **Hierarchical Agentic Schema-Task Decomposition (HASTD)** framework represents a paradigm shift from monolithic prompting to a structured, resilient, and scalable agentic architecture for data extraction. It excels where traditional LLM pipelines fail, especially with large documents and complex JSON schemas.

---

## ✨ Key Features

* **⚙️ Schema-to-DAG Engine:** Programmatically converts complex JSON schemas into a Directed Acyclic Graph (DAG) of discrete, manageable extraction tasks.
* **🤖 Hierarchical Multi-Agent System (HMAS):** Employs a team of specialized AI agents—a high-level Orchestrator, fine-tuned Extractor SLMs, and dedicated Validation/Correction agents—to execute the task graph efficiently.
* **🔄 Resilient Self-Correction Loop:** Uses LangGraph to create a stateful, cyclical workflow that programmatically validates every extracted piece of data and automatically attempts to correct errors.
* **🎯 Heterogeneous Model Strategy:** Leverages powerful frontier models for complex reasoning and cost-effective, fine-tuned Small Language Models for high-throughput extraction.
* **📈 Calibrated Confidence Scoring:** Generates a reliable, multi-faceted confidence score for each field, enabling dependable downstream automation and efficient HITL workflows.

---

## 🏛️ Architecture

The HASTD framework deconstructs a complex extraction problem into a manageable, multi-stage workflow orchestrated by a team of specialized AI agents.

![HASTD Architecture Diagram](https://drive.google.com/file/d/1W-Y5EA3HkRcmFOumqLblAwJ0_snQc7dw/view?usp=sharing)

---

## 🛠️ Technology Stack

* **Orchestration:** LangGraph
* **Agent Communication:** LangChain
* **Schema Validation:** Pydantic
* **Vector Storage:** ChromaDB, Milvus, Pinecone
* **LLMs:** Claude 3 Family, GPT-4o, Llama 3
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
    git clone [https://github.com/Riya0071234/agentic-data-extraction.git](https://github.com/Riya0071234/agentic-data-extraction.git)
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
    * Open the `.env` file and add your API keys.

---

## ⚡ Proof-of-Concept: Running the Demo

The current version of this repository contains a functional proof-of-concept (`run_poc.py`). This script executes the core, DAG-driven, self-correcting agentic loop for a sample document and schema.

**To run the proof-of-concept:**

1.  Make sure your `.env` file is configured with your API keys.
2.  Run the script from the root of the project directory:

    ```bash
    python run_poc.py
    ```

You will see the step-by-step output in your terminal as the agents work to extract, validate, and correct each field from the schema.

---

## 🗺️ Roadmap and Future Goals

This proof-of-concept demonstrates the core, self-correcting agentic loop. The long-term vision for the HASTD framework is to build it into a full-featured, production-ready extraction platform. Key future steps are detailed in the project report and include:

### 1. Full Production API and Library
* **Develop the FastAPI Server:** Build out the `api/main.py` file to provide a robust, production-ready REST API for the extraction service.
* **Create an Installable Package:** Package the `src/hastd` directory so it can be installed via `pip` and used as a library in other applications.

### 2. Performance and Scalability Enhancements
* **Parallel Execution:** Implement parallel execution for independent branches of the task DAG to dramatically reduce latency on complex schemas.
* **Full-Scale Fine-Tuning:** Build out the `Draft-Refine-Critique` synthetic data pipeline outlined in the report to create highly specialized, cost-effective SLM-based Extractor Agents.

### 3. Advanced Agentic Capabilities
* **Dynamic Schema Adaptation:** Train an agent that can autonomously detect and adapt to minor changes in document formats without requiring redeployment.
* **Advanced Self-Healing:** Develop a "Root Cause Analysis Agent" that analyzes patterns of failure to identify and suggest fixes for systemic issues.
* **Cost-Based Dynamic Model Selection:** Evolve the Orchestrator to make real-time, cost-aware decisions, choosing between fast/cheap and slow/powerful models on a per-task basis.

### 4. Human-in-the-Loop (HITL) Interface
* Develop a dedicated web interface for human reviewers. The key feature will be **visual grounding**, where clicking an extracted data field instantly highlights the source text in the original document, enabling rapid verification and correction.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and open a pull request with your changes.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
````
