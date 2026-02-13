import json
import jsonschema
from jsonschema import validate
from .logger import logger

class Validator:
    @staticmethod
    def validate_schema(data: dict, schema: dict):
        """
        Validates the data against the given JSON schema.
        """
        try:
            validate(instance=data, schema=schema)
            logger.info("Schema validation passed.")
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            raise AssertionError(f"Schema validation failed: {e.message}")
