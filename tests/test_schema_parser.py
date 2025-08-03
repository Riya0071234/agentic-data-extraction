import pytest
from hastd.core.schema_parser import parse_schema_to_tasks


def test_flat_schema_parsing():
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "date": {"type": "string", "format": "date"}
        },
        "required": ["title"]
    }

    tasks = parse_schema_to_tasks(schema)

    assert isinstance(tasks, list)
    assert len(tasks) == 2

    paths = [task['field_path'] for task in tasks]
    assert "title" in paths
    assert "date" in paths


def test_nested_schema_parsing():
    schema = {
        "type": "object",
        "properties": {
            "author": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                },
                "required": ["name"]
            }
        },
        "required": ["author"]
    }

    tasks = parse_schema_to_tasks(schema)

    paths = [task['field_path'] for task in tasks]
    assert "author.name" in paths
    assert "author.email" in paths


def test_array_of_objects_parsing():
    schema = {
        "type": "object",
        "properties": {
            "references": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "year": {"type": "integer"}
                    },
                    "required": ["title"]
                }
            }
        }
    }

    tasks = parse_schema_to_tasks(schema)

    paths = [task['field_path'] for task in tasks]
    assert "references[].title" in paths
    assert "references[].year" in paths


def test_complex_mixed_schema():
    schema = {
        "type": "object",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {
                    "doi": {"type": "string"},
                    "published": {"type": "boolean"}
                }
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }

    tasks = parse_schema_to_tasks(schema)

    paths = [task['field_path'] for task in tasks]
    assert "metadata.doi" in paths
    assert "metadata.published" in paths
    assert "tags[]" in paths
