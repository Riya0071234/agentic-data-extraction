from typing import Dict, Any
from pydantic import create_model, BaseModel, EmailStr

# A mapping from JSON schema types to Python/Pydantic types
TYPE_MAPPING = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}

class DynamicPydanticFactory:
    """
    A factory for creating Pydantic models on-the-fly from a JSON schema.
    This is the core of the dynamic validation system, making a static
    model registry unnecessary.
    """
    @staticmethod
    def create_model_from_schema(
        schema: Dict[str, Any], 
        model_name: str = "DynamicValidationModel"
    ) -> BaseModel:
        """
        Dynamically creates a Pydantic model from a JSON schema's properties.

        Args:
            schema: The JSON schema dictionary (or a sub-schema).
            model_name: The name for the new Pydantic model class.

        Returns:
            A Pydantic BaseModel class generated from the schema.
        """
        fields = {}
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])
        
        for name, props in properties.items():
            field_type = TYPE_MAPPING.get(props.get("type"), Any)
            
            # For specific string formats like email, use Pydantic's special types
            if props.get("format") == "email":
                field_type = EmailStr

            # Use '...' for required fields, or a default value (None) for optional fields
            if name in required_fields:
                default_value = ...
            else:
                default_value = None
            
            fields[name] = (field_type, default_value)
            
        return create_model(model_name, **fields)