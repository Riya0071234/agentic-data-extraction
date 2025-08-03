import re
from typing import Dict, Any


def is_valid_email(value: str) -> bool:
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value) is not None


def is_valid_date(value: str) -> bool:
    # Supports YYYY-MM-DD or YYYY/MM/DD
    return re.fullmatch(r"\d{4}[-/]\d{2}[-/]\d{2}", value) is not None


def is_numeric(value: str) -> bool:
    return re.fullmatch(r"\d+", value) is not None


def is_boolean(value: str) -> bool:
    return value.strip().lower() in ["true", "false", "yes", "no"]


def compute_confidence(field_name: str, extracted_value: str) -> float:
    """
    Heuristically assign a confidence score based on field name and extracted value content.
    Returns a float between 0.0 and 1.0.
    """
    if not extracted_value or not extracted_value.strip():
        return 0.0

    extracted_value = extracted_value.strip()

    # Check by naming convention
    lower_name = field_name.lower()

    if "email" in lower_name:
        return 1.0 if is_valid_email(extracted_value) else 0.3

    if "date" in lower_name:
        return 1.0 if is_valid_date(extracted_value) else 0.4

    if "id" in lower_name or "number" in lower_name:
        return 1.0 if is_numeric(extracted_value) else 0.5

    if "is_" in lower_name or lower_name.startswith("has_"):
        return 1.0 if is_boolean(extracted_value) else 0.5

    # General fallback: length-based heuristic
    length = len(extracted_value)
    if length > 100:
        return 0.9
    elif length > 50:
        return 0.8
    elif length > 20:
        return 0.7
    elif length > 5:
        return 0.6
    else:
        return 0.4


def score_all_fields(extracted_fields: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute confidence scores for all extracted fields.
    Returns a dict of { field_name: confidence_score }
    """
    scores = {}
    for field, value in extracted_fields.items():
        try:
            scores[field] = compute_confidence(field, str(value))
        except Exception:
            scores[field] = 0.0
    return scores
