import pytest
from pydantic import BaseModel, EmailStr, ValidationError

from hastd.core.models import ExtractionOutput
from src.hastd.core.schema_parser import parse_schema_to_tasks
from src.hastd.core.validator import validate_extraction
from src.hastd.core.github_model import CorrectionAgent, ExtractorAgent
from langchain_core.messages import SystemMessage

# ----- Define a sample test Pydantic model -----
class UserModel(BaseModel):
    name: str
    email: EmailStr
    user_id: int


# ----- Sample JSON Schema (already parsed in real case) -----
sample_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "user_id": {"type": "integer"}
    },
    "required": ["name", "email", "user_id"]
}

sample_text = "The contact is Jane Doe. Her email is jane@example.com and her user ID is 12345."


# ----- Test: Schema Parsing -----
def test_parse_schema_to_tasks():
    tasks = parse_schema_to_tasks(sample_schema)
    assert isinstance(tasks, list)
    assert any("name" in task["field_path"] for task in tasks)


# ----- Test: ExtractorAgent output format -----
def test_extractor_output():
    agent = ExtractorAgent()
    result = agent.run(text=sample_text, field_path="name", schema_fragment={"type": "string"})
    assert isinstance(result, str)
    assert "Jane" in result


# ----- Test: Validation success -----
def test_validator_success():
    output = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "user_id": 12345
    }
    validated, errors = validate_extraction(output, UserModel)
    assert validated == output
    assert errors == {}


# ----- Test: Validation failure -----
def test_validator_failure():
    output = {
        "name": "Jane Doe",
        "email": "not-an-email",
        "user_id": "abc"
    }
    validated, errors = validate_extraction(output, UserModel)
    assert validated is None
    assert "email" in errors
    assert "user_id" in errors


# ----- Test: Correction agent fixes output -----
def test_corrector_agent():
    broken_output = {
        "name": "Jane Doe",
        "email": "not-an-email",
        "user_id": "abc"
    }

    prompt = SystemMessage(content="Fix the invalid fields in the extracted output.")

    agent = CorrectionAgent()
    corrected = agent.run(
        text=sample_text,
        invalid_output=broken_output,
        schema=sample_schema
    )

    # Not checking exact fix but that format now looks usable
    assert isinstance(corrected, dict)
    assert "@" in corrected["email"]
    assert isinstance(corrected["user_id"], int)
