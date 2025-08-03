import json
from typing import Any, Dict, List, Optional
from pathlib import Path

class ExtractionTask:
    def __init__(
        self,
        field_path: str,
        field_type: str,
        required: bool = False,
        enum: Optional[List[Any]] = None,
        description: Optional[str] = None,
    ):
        self.field_path = field_path
        self.field_type = field_type
        self.required = required
        self.enum = enum
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_path": self.field_path,
            "field_type": self.field_type,
            "required": self.required,
            "enum": self.enum,
            "description": self.description,
        }

    def __repr__(self):
        return f"<Task: {self.field_path} ({self.field_type}){' [required]' if self.required else ''}>"

def parse_json_schema(
    schema: Dict[str, Any],
    path_prefix: str = "",
    required_fields: Optional[List[str]] = None,
) -> List[ExtractionTask]:
    tasks = []

    if required_fields is None:
        required_fields = schema.get("required", [])

    properties = schema.get("properties", {})

    for field_name, field_schema in properties.items():
        full_path = f"{path_prefix}.{field_name}" if path_prefix else field_name
        field_type = field_schema.get("type", "object")
        enum_values = field_schema.get("enum")
        description = field_schema.get("description", "")
        is_required = field_name in required_fields

        if field_type == "object":
            # Recurse into nested object
            child_required = field_schema.get("required", [])
            tasks.extend(parse_json_schema(field_schema, full_path, child_required))
        elif field_type == "array":
            # Recurse into array items if they are objects
            item_schema = field_schema.get("items", {})
            item_type = item_schema.get("type", "object")
            if item_type == "object":
                child_required = item_schema.get("required", [])
                tasks.extend(parse_json_schema(item_schema, full_path + "[]", child_required))
            else:
                tasks.append(
                    ExtractionTask(
                        field_path=full_path + "[]",
                        field_type=item_type,
                        required=is_required,
                        enum=enum_values,
                        description=description,
                    )
                )
        else:
            tasks.append(
                ExtractionTask(
                    field_path=full_path,
                    field_type=field_type,
                    required=is_required,
                    enum=enum_values,
                    description=description,
                )
            )

    return tasks

# --- Example CLI runner for quick testing ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python schema_parser.py path_to_schema.json")
        sys.exit(1)

    schema_path = Path(sys.argv[1])
    if not schema_path.exists():
        print(f"Schema file {schema_path} not found.")
        sys.exit(1)

    with open(schema_path, "r") as f:
        schema = json.load(f)

    tasks = parse_json_schema(schema)
    for task in tasks:
        print(task.to_dict())
