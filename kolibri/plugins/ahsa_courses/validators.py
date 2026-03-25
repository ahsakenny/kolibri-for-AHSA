"""
Course Blueprint Validator
==========================

Validates course blueprint JSON/YAML files before importing.
"""
from jsonschema import Draft7Validator
from jsonschema import ValidationError

# JSON Schema for course blueprint validation
COURSE_BLUEPRINT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": [
        "course_id",
        "title",
        "grade_level",
        "subject",
        "credit_value",
        "total_weeks",
    ],
    "properties": {
        "course_id": {"type": "string", "minLength": 1, "maxLength": 50},
        "title": {"type": "string", "minLength": 1, "maxLength": 200},
        "description": {"type": "string"},
        "grade_band": {"type": "string", "enum": ["middle", "high"]},
        "grade_level": {"type": "integer", "minimum": 6, "maximum": 12},
        "subject": {
            "type": "string",
            "enum": [
                "ela",
                "math",
                "science",
                "social_studies",
                "world_language",
                "elective",
            ],
        },
        "florida_standard_set": {"type": "string"},
        "ncaa_core_area": {
            "type": "string",
            "enum": [
                "english",
                "mathematics",
                "natural_science",
                "social_science",
                "additional",
                "none",
            ],
        },
        "is_ncaa_approved": {"type": "boolean"},
        "duration": {
            "type": "string",
            "enum": ["full_year", "semester", "quarter"],
        },
        "credit_value": {"type": "number", "minimum": 0, "maximum": 2},
        "total_weeks": {"type": "integer", "minimum": 1},
        "weekly_minutes": {"type": "integer", "minimum": 0},
        "is_honors": {"type": "boolean"},
        "is_ap": {"type": "boolean"},
        "requires_lab": {"type": "boolean"},
        "syllabus": {"type": "string"},
        "pacing_guide": {"type": "string"},
        "required_materials": {"type": "array"},
        "teacher_notes": {"type": "string"},
        "teacher_led": {"type": "boolean"},
        "academic_integrity_policy": {"type": "string"},
        "version": {"type": "string"},
        "semesters": {"type": "array", "items": {"type": "object"}},
        "weeks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["week_number", "title"],
                "properties": {
                    "week_number": {"type": "integer", "minimum": 1},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "objectives": {"type": "array", "items": {"type": "string"}},
                    "standards_alignment": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "estimated_minutes": {"type": "integer"},
                    "requires_teacher_interaction": {"type": "boolean"},
                    "teacher_interaction_notes": {"type": "string"},
                    "lesson_plans": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["lesson_number", "title"],
                        },
                    },
                    "assessments": {"type": "array", "items": {"type": "object"}},
                },
            },
        },
        "grade_categories": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "weight"],
                "properties": {
                    "name": {"type": "string"},
                    "weight": {"type": "number", "minimum": 0, "maximum": 100},
                    "drop_lowest": {"type": "integer", "minimum": 0},
                },
            },
        },
    },
}


def validate_blueprint(blueprint_data):
    """
    Validate a course blueprint against the schema.

    Args:
        blueprint_data (dict): The blueprint data to validate

    Returns:
        tuple: (is_valid, errors_list)

    Raises:
        ValidationError: If validation fails
    """
    validator = Draft7Validator(COURSE_BLUEPRINT_SCHEMA)
    errors = list(validator.iter_errors(blueprint_data))

    if errors:
        error_messages = [f"{error.path}: {error.message}" for error in errors]
        return False, error_messages

    return True, []


def validate_blueprint_file(file_path):
    """
    Validate a blueprint file (JSON or YAML).

    Args:
        file_path (str): Path to the blueprint file

    Returns:
        tuple: (is_valid, errors_list, data)
    """
    import json
    import os

    try:
        with open(file_path, "r") as f:
            if file_path.endswith(".json"):
                data = json.load(f)
            elif file_path.endswith((".yaml", ".yml")):
                import yaml

                data = yaml.safe_load(f)
            else:
                return False, ["Unsupported file format. Use .json or .yaml"], None

        is_valid, errors = validate_blueprint(data)
        return is_valid, errors, data

    except FileNotFoundError:
        return False, [f"File not found: {file_path}"], None
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {str(e)}"], None
    except Exception as e:
        return False, [f"Error reading file: {str(e)}"], None
