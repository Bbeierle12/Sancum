import argparse
import sys
from typing import List, Optional

import yaml
from pydantic import BaseModel, ValidationError, field_validator

class Pivot(BaseModel):
    type: Optional[str] = None
    center: Optional[str] = None
    elements: Optional[List[str]] = []

class Verse(BaseModel):
    verse_id: str
    text: str
    covenant_tags: List[str]
    emotion_codes: List[str]
    pivot: Optional[Pivot] = None
    notes: Optional[str] = ""

    @field_validator('verse_id')
    def verse_id_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('verse_id must not be empty')
        return v

    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('text must not be empty')
        return v

def validate_schema(file_path: str):
    """
    Loads a YAML file and validates its contents against the Sanctum schema.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Use safe_load_all for multi-document YAML files, but we expect one list
            data = yaml.safe_load(f)
            if not data:
                print("?  Warning: YAML file is empty.")
                return

        error_found = False
        for i, item in enumerate(data):
            try:
                Verse.model_validate(item)
            except ValidationError as e:
                print(f"?? Error in object at index {i} (verse_id: {item.get('verse_id', 'N/A')}):")
                print(e)
                error_found = True
        
        if error_found:
            sys.exit(1)

        print("? All good. Schema validation passed.")

    except FileNotFoundError:
        print(f"?? Error: File not found at '{file_path}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"?? Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"?? An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a Sanctum YAML data file against the defined schema.")
    parser.add_argument("file_path", type=str, help="The path to the YAML file to validate.")
    args = parser.parse_args()
    validate_schema(args.file_path)
