from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

import os
import json
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledGraph
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

from hastd.core.schema_parser import parse_schema_into_tasks
from hastd.core.models import DynamicPydanticFactory
from hastd.core.confidence import score_all_fields

# --------------------------
# 🔐 Load API keys
# --------------------------
load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --------------------------
# 🧠 LangGraph Setup
# --------------------------
class GraphState(dict):
    schema: dict
    document: str
    tasks: list
    extracted_data: dict
    errors: str | None
    corrected_data: dict | None
    confidence: dict | None


def extractor_agent(state: GraphState) -> GraphState:
    prompt = (
        f"Extract the following fields from the document:\n"
        f"{[task['field_path'] for task in state['tasks']]}\n\n"
        f"Document:\n{state['document']}"
    )
    result = llm.invoke(prompt)
    try:
        output = json.loads(result.content)
    except json.JSONDecodeError:
        output = {"error": "Invalid JSON"}
    return {**state, "extracted_data": output}


def validation_agent(state: GraphState) -> GraphState:
    schema = state["schema"]
    data = state.get("extracted_data", {})
    try:
        model = DynamicPydanticFactory.create_model_from_schema(schema)
        model(**data)
        return {**state, "errors": None}
    except Exception as e:
        return {**state, "errors": str(e)}


def correction_agent(state: GraphState) -> GraphState:
    prompt = (
        f"Correct the following extracted data based on errors and original text.\n\n"
        f"Document:\n{state['document']}\n\n"
        f"Extracted:\n{json.dumps(state['extracted_data'], indent=2)}\n\n"
        f"Errors:\n{state['errors']}"
    )
    result = llm.invoke(prompt)
    try:
        corrected = json.loads(result.content)
    except json.JSONDecodeError:
        corrected = {}
    return {**state, "extracted_data": corrected, "corrected_data": corrected}


def confidence_agent(state: GraphState) -> GraphState:
    return {**state, "confidence": score_all_fields(state["extracted_data"])}


def has_errors(state: GraphState):
    return "correct" if state.get("errors") else "no_errors"


def build_agent_graph() -> CompiledGraph:
    builder = StateGraph(GraphState)

    builder.add_node("extract", extractor_agent)
    builder.add_node("validate", validation_agent)
    builder.add_node("correct", correction_agent)
    builder.add_node("score", confidence_agent)

    builder.set_entry_point("extract")
    builder.add_edge("extract", "validate")
    builder.add_conditional_edges("validate", has_errors, {
        "correct": "correct",
        "no_errors": "score"
    })
    builder.add_edge("correct", "validate")
    builder.add_edge("score", END)

    return builder.compile()


agent_graph = build_agent_graph()

# --------------------------
# 🚀 FastAPI App
# --------------------------
app = FastAPI(title="HASTD Agentic Extraction API")


class ExtractionRequest(BaseModel):
    document_text: str
    json_schema: Dict[str, Any]


@app.post("/extract")
def extract_data(req: ExtractionRequest):
    try:
        task_list = parse_schema_into_tasks(req.json_schema)
        inputs = {
            "schema": req.json_schema,
            "document": req.document_text,
            "tasks": task_list,
        }

        final_state = agent_graph.invoke(inputs, config=RunnableConfig())

        return {
            "extracted_data": final_state["extracted_data"],
            "corrected_data": final_state.get("corrected_data"),
            "confidence_scores": final_state.get("confidence"),
            "errors": final_state.get("errors"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
