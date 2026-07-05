#!/usr/bin/env python3
"""Small JSON Schema validator for PEGO contract smoke tests.

The repository intentionally keeps operation scripts runtime-neutral. This
validator supports the schema features used by PEGO contracts without requiring
an external package in local or CI environments.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Union


Json = Union[dict[str, Any], list[Any], str, int, float, bool, None]


class SchemaValidationError(AssertionError):
    """Raised when an artifact does not match its PEGO JSON Schema."""


def load_json(path: Path) -> Json:
    return json.loads(path.read_text())


def validate_json_file(instance_path: Path, schema_path: Path) -> None:
    validate(load_json(instance_path), load_json(schema_path))


def validate(instance: Json, schema: Json) -> None:
    if not isinstance(schema, dict):
        raise SchemaValidationError("schema root must be an object")
    _validate(instance, schema, schema, "$")


def _validate(instance: Json, schema: dict[str, Any], root: dict[str, Any], path: str) -> None:
    if "$ref" in schema:
        _validate(instance, _resolve_ref(schema["$ref"], root), root, path)
        sibling_schema = {key: value for key, value in schema.items() if key != "$ref"}
        if sibling_schema:
            _validate(instance, sibling_schema, root, path)
        return

    if "anyOf" in schema:
        if not _any_valid(instance, schema["anyOf"], root, path):
            raise SchemaValidationError(f"{path}: value did not match anyOf options")

    if "oneOf" in schema:
        matches = sum(
            1 for option in schema["oneOf"] if _is_valid(instance, option, root, path)
        )
        if matches != 1:
            raise SchemaValidationError(
                f"{path}: value matched {matches} oneOf options, expected exactly 1"
            )

    if "const" in schema and instance != schema["const"]:
        raise SchemaValidationError(
            f"{path}: expected const {schema['const']!r}, got {instance!r}"
        )

    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaValidationError(
            f"{path}: expected one of {schema['enum']!r}, got {instance!r}"
        )

    if "type" in schema:
        _validate_type(instance, schema["type"], path)

    if isinstance(instance, dict):
        _validate_object(instance, schema, root, path)
    elif isinstance(instance, list):
        _validate_array(instance, schema, root, path)
    elif isinstance(instance, str):
        _validate_string(instance, schema, path)
    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        _validate_number(instance, schema, path)


def _resolve_ref(ref: str, root: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise SchemaValidationError(f"unsupported external schema ref: {ref}")

    current: Any = root
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or part not in current:
            raise SchemaValidationError(f"unresolved schema ref: {ref}")
        current = current[part]

    if not isinstance(current, dict):
        raise SchemaValidationError(f"schema ref does not resolve to object: {ref}")
    return current


def _is_valid(instance: Json, schema: Any, root: dict[str, Any], path: str) -> bool:
    if not isinstance(schema, dict):
        return False
    try:
        _validate(instance, schema, root, path)
    except SchemaValidationError:
        return False
    return True


def _any_valid(instance: Json, schemas: Any, root: dict[str, Any], path: str) -> bool:
    if not isinstance(schemas, list) or not schemas:
        raise SchemaValidationError(f"{path}: anyOf must be a non-empty list")
    return any(_is_valid(instance, option, root, path) for option in schemas)


def _validate_type(instance: Json, expected: Any, path: str) -> None:
    expected_types = expected if isinstance(expected, list) else [expected]
    if not any(_matches_type(instance, item) for item in expected_types):
        raise SchemaValidationError(
            f"{path}: expected type {expected!r}, got {type(instance).__name__}"
        )


def _matches_type(instance: Json, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    raise SchemaValidationError(f"unsupported schema type: {expected}")


def _validate_object(
    instance: dict[str, Json],
    schema: dict[str, Any],
    root: dict[str, Any],
    path: str,
) -> None:
    required = schema.get("required", [])
    if not isinstance(required, list):
        raise SchemaValidationError(f"{path}: required must be a list")

    for key in required:
        if key not in instance:
            raise SchemaValidationError(f"{path}: missing required property {key!r}")

    properties = schema.get("properties", {})
    if properties and not isinstance(properties, dict):
        raise SchemaValidationError(f"{path}: properties must be an object")

    for key, value in instance.items():
        if key in properties:
            _validate(value, properties[key], root, f"{path}.{key}")
            continue

        additional = schema.get("additionalProperties", True)
        if additional is False:
            raise SchemaValidationError(f"{path}: unexpected property {key!r}")
        if isinstance(additional, dict):
            _validate(value, additional, root, f"{path}.{key}")


def _validate_array(
    instance: list[Json],
    schema: dict[str, Any],
    root: dict[str, Any],
    path: str,
) -> None:
    if "minItems" in schema and len(instance) < schema["minItems"]:
        raise SchemaValidationError(
            f"{path}: expected at least {schema['minItems']} items, got {len(instance)}"
        )
    if "maxItems" in schema and len(instance) > schema["maxItems"]:
        raise SchemaValidationError(
            f"{path}: expected at most {schema['maxItems']} items, got {len(instance)}"
        )

    items = schema.get("items")
    if isinstance(items, dict):
        for index, value in enumerate(instance):
            _validate(value, items, root, f"{path}[{index}]")


def _validate_string(instance: str, schema: dict[str, Any], path: str) -> None:
    if "minLength" in schema and len(instance) < schema["minLength"]:
        raise SchemaValidationError(
            f"{path}: expected minLength {schema['minLength']}, got {len(instance)}"
        )
    if "maxLength" in schema and len(instance) > schema["maxLength"]:
        raise SchemaValidationError(
            f"{path}: expected maxLength {schema['maxLength']}, got {len(instance)}"
        )
    if "pattern" in schema and re.search(schema["pattern"], instance) is None:
        raise SchemaValidationError(
            f"{path}: value {instance!r} did not match pattern {schema['pattern']!r}"
        )


def _validate_number(
    instance: int | float,
    schema: dict[str, Any],
    path: str,
) -> None:
    if "minimum" in schema and instance < schema["minimum"]:
        raise SchemaValidationError(
            f"{path}: expected minimum {schema['minimum']}, got {instance}"
        )
    if "maximum" in schema and instance > schema["maximum"]:
        raise SchemaValidationError(
            f"{path}: expected maximum {schema['maximum']}, got {instance}"
        )
