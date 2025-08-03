import os
import json
from typing import Literal, Optional, TypedDict, Dict, Any, List
import dpath.util

from dotenv import load_dotenv
from pydantic import ValidationError
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# Correctly named imports from your project files
from hastd.core.schema_parser import parse_schema_into_tasks
from hastd.core.models import DynamicPydanticFactory
from hastd.core.task_dag import TaskDAGBuilder

# -----------------------------
# 🔐 Load API keys from .env
# -----------------------------
load_dotenv()
# Note: Using a cheaper/faster model like "gpt-4o-mini" or "claude-3-haiku-20240307" is ideal for development
llm = ChatOpenAI(model="gpt-4o", temperature=0)


# -----------------------------
# 🧠 Define LangGraph State for a SINGLE task
# -----------------------------
class AgentState(TypedDict):
    document: str
    task: Dict[str, Any]
    final_json: Dict[str, Any]  # The master JSON being built
    extracted_data: Optional[Dict[str, Any]]
    errors: Optional[str]
    max_attempts: int
    current_attempt: int


# -----------------------------
# 🤖 Agent: Extractor (focused on a single task)
# -----------------------------
def extractor_agent(state: AgentState) -> Dict[str, Any]:
    print(f"---  extractor_agent: Extracting '{state['task']['field_path']}' ---")
    task = state['task']
    field_name = task['field_path'].split('.')[-1].replace('[]', '')

    prompt = f"""
    From the following document, extract the single field '{task['field_path']}'.
    Pay close attention to the field description: "{task['description']}".

    DOCUMENT:
    ---
    {state['document']}
    ---

    Return ONLY a single JSON object with the key "{field_name}". Do not include any other text or explanations.
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        parsed_output = json.loads(result.content)
    except json.JSONDecodeError:
        parsed_output = {"error": "LLM returned malformed JSON."}

    return {"extracted_data": parsed_output, "current_attempt": state["current_attempt"] + 1}


# -----------------------------
# ✅ Agent: Validator (focused on a single task)
# -----------------------------
def validation_agent(state: AgentState) -> Dict[str, Any]:
    print("--- validation_agent: Validating output ---")
    task = state["task"]
    data = state.get("extracted_data", {})

    # Create a simple schema for just this one field
    field_name = task['field_path'].split('.')[-1].replace('[]', '')
    single_field_schema = {
        "properties": {
            field_name: {
                "type": task["field_type"],
                "description": task["description"]
            }
        }
    }

    try:
        # Use the dynamic factory to create a Pydantic model for this one field
        model = DynamicPydanticFactory.create_model_from_schema(single_field_schema)
        model(**data)
        print("✅ Validation PASSED")
        return {"errors": None}
    except ValidationError as e:
        print(f"❌ Validation FAILED: {str(e)}")
        return {"errors": str(e)}


# -----------------------------
# 🔁 Agent: Correction (focused on a single task)
# -----------------------------
def correction_agent(state: AgentState) -> Dict[str, Any]:
    print("--- correction_agent: Attempting to correct ---")
    task = state['task']
    field_name = task['field_path'].split('.')[-1].replace('[]', '')

    prompt = f"""
    A previous attempt to extract a field from a document failed. Please correct it.

    DOCUMENT:
    ---
    {state['document']}
    ---
    FIELD TO EXTRACT: {task['field_path']}
    DESCRIPTION: {task['description']}

    PREVIOUS (INCORRECT) OUTPUT:
    {json.dumps(state['extracted_data'], indent=2)}

    VALIDATION ERRORS:
    {state['errors']}

    Return ONLY a corrected JSON object with the key "{field_name}".
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        corrected = json.loads(result.content)
    except json.JSONDecodeError:
        corrected = {"error": "Corrector LLM returned malformed JSON."}

    return {"extracted_data": corrected}


# -----------------------------
# 🔀 Condition: Should correct or give up?
# -----------------------------
def should_correct(state: AgentState) -> Literal["correct", "__end__"]:
    if state.get("errors") and state["current_attempt"] < state["max_attempts"]:
        return "correct"
    return "__end__"


# -----------------------------
# 🧠 Build LangGraph
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("extract", extractor_agent)
builder.add_node("validate", validation_agent)
builder.add_node("correct", correction_agent)

builder.set_entry_point("extract")
builder.add_edge("extract", "validate")
builder.add_conditional_edges("validate", should_correct, {
    "correct": "correct",
    "__end__": END
})
builder.add_edge("correct", "extract")  # Loop back to extractor for a fresh attempt

agentic_loop = builder.compile()

# -----------------------------
# 🚀 Main Orchestration Logic
# -----------------------------
if __name__ == "__main__":
    # 1. Load sample document and schema
    with open("data/samples/document_1.txt", "r") as f:
        document_text = f.read()

    with open("data/samples/schema_1.json", "r") as f:
        json_schema = json.load(f)

    # 2. Use Schema Parser and DAG Builder to get execution order
    tasks = parse_schema_into_tasks(json_schema)
    dag_builder = TaskDAGBuilder(tasks)
    execution_order = dag_builder.get_execution_order()

    # Create a quick lookup for task details
    tasks_by_path = {task.field_path: task.to_dict() for task in tasks}

    # 3. Iterate through the DAG and run the agentic loop for each task
    final_json_output = {}

    print("🚀 STARTING HASTD ORCHESTRATION\n" + "=" * 40)

    for field_path in execution_order:
        if field_path not in tasks_by_path:
            # This is a parent object path, not an extraction task itself
            continue

        current_task = tasks_by_path[field_path]

        initial_state = {
            "document": document_text,
            "task": current_task,
            "final_json": final_json_output,  # Provide context of what's already extracted
            "max_attempts": 3,
            "current_attempt": 0,
        }

        # Invoke the agentic loop for this single task
        final_task_state = agentic_loop.invoke(initial_state)

        # 4. Merge the successful result into the final JSON
        if not final_task_state.get("errors") and final_task_state.get("extracted_data"):
            # Use dpath to safely set nested dictionary values
            # e.g., for path "author.name", this creates {'author': {'name': ...}}
            try:
                # The LLM returns a dict like {'name': 'Jane'}, we need the value
                value_to_set = list(final_task_state["extracted_data"].values())[0]
                dpath.util.new(final_json_output, current_task['field_path'], value_to_set)
                print(f"✅ Successfully extracted and merged '{current_task['field_path']}'")
            except Exception as e:
                print(f"🔥 Error merging data for '{current_task['field_path']}': {e}")
        else:
            print(
                f"❌ Failed to extract '{current_task['field_path']}' after {final_task_state['current_attempt']} attempts.")
        print("-" * 40)

    # 5. Print the final combined result
    print("\n\n✅ FINAL COMBINED JSON OUTPUT\n" + "=" * 40)
    print(json.dumps(final_json_output, indent=2))