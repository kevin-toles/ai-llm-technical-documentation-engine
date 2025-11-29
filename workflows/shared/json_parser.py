"""
JSON parsing and validation utilities for LLM responses.

Handles extracting JSON from LLM output with delimiters,
validating checksums, and ensuring required fields are present.
"""

import json
import hashlib
import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ParsedResponse:
    """Parsed and validated LLM JSON response."""
    data: Dict[str, Any]
    raw_json: str
    checksum: Optional[str] = None
    delimiter_found: bool = False


class JSONParseError(Exception):
    """Raised when JSON parsing fails."""
    pass


class JSONValidationError(Exception):
    """Raised when JSON validation fails."""
    pass


def parse_llm_json_response(
    response: str,
    required_fields: Optional[List[str]] = None,
    validate_checksum: bool = True,
    begin_delimiter: str = "BEGIN_JSON",
    end_delimiter: str = "END_JSON",
) -> ParsedResponse:
    """
    Parse and validate JSON from an LLM response.
    
    Handles responses with or without delimiters:
    - With delimiters: Extracts JSON between BEGIN_JSON and END_JSON
    - Without delimiters: Attempts to parse entire response as JSON
    
    Optionally validates SHA256 checksum if present in response.
    
    Args:
        response: Raw LLM response text
        required_fields: List of field names that must be present in the JSON
        validate_checksum: Whether to validate SHA256 checksum if present
        begin_delimiter: Starting delimiter for JSON content
        end_delimiter: Ending delimiter for JSON content
        
    Returns:
        ParsedResponse with validated data
        
    Raises:
        JSONParseError: If JSON cannot be extracted or parsed
        JSONValidationError: If validation fails (missing fields, bad checksum)
        
    Example:
        >>> response = '''
        ... Some preamble text...
        ... 
        ... BEGIN_JSON
        ... {"field1": "value1", "field2": 42}
        ... END_JSON
        ... 
        ... SHA256: abc123...
        ... '''
        >>> result = parse_llm_json_response(response, required_fields=["field1"])
        >>> print(result.data)
        {'field1': 'value1', 'field2': 42}
    """
    # Try to extract JSON with delimiters first
    json_str, delimiter_found = _extract_json_with_delimiters(
        response, begin_delimiter, end_delimiter
    )
    
    # If no delimiters found, try parsing entire response
    if not json_str:
        json_str = response.strip()
        delimiter_found = False
    
    # Parse JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise JSONParseError(
            f"Failed to parse JSON: {e}\n"
            f"Extracted content: {json_str[:200]}..."
        ) from e
    
    if not isinstance(data, dict):
        raise JSONParseError(
            f"Expected JSON object (dict), got {type(data).__name__}"
        )
    
    # Extract checksum if present
    checksum = None
    if validate_checksum:
        checksum = _extract_checksum(response)
        if checksum:
            _validate_checksum(json_str, checksum)
    
    # Validate required fields
    if required_fields:
        _validate_required_fields(data, required_fields)
    
    return ParsedResponse(
        data=data,
        raw_json=json_str,
        checksum=checksum,
        delimiter_found=delimiter_found,
    )


def _extract_json_with_delimiters(
    text: str,
    begin_delimiter: str,
    end_delimiter: str,
) -> tuple[str, bool]:
    """
    Extract JSON content between delimiters.
    
    Returns:
        Tuple of (json_string, delimiter_found)
        Returns ("", False) if delimiters not found
    """
    # Try to find delimiters
    begin_pattern = re.escape(begin_delimiter)
    end_pattern = re.escape(end_delimiter)
    
    pattern = rf"{begin_pattern}\s*(.*?)\s*{end_pattern}"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip(), True
    
    return "", False


def _extract_checksum(text: str) -> Optional[str]:
    """
    Extract SHA256 checksum from response.
    
    Looks for patterns like:
    - SHA256: abc123...
    - Checksum: abc123...
    """
    # Try multiple checksum patterns
    patterns = [
        r"SHA256:\s*([a-fA-F0-9]{64})",
        r"Checksum:\s*([a-fA-F0-9]{64})",
        r"sha256:\s*([a-fA-F0-9]{64})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).lower()
    
    return None


def _validate_checksum(json_str: str, expected_checksum: str) -> None:
    """
    Validate JSON content against SHA256 checksum.
    
    Raises:
        JSONValidationError: If checksum doesn't match
    """
    # Calculate checksum of JSON string (normalized)
    normalized = json.dumps(json.loads(json_str), sort_keys=True, separators=(',', ':'))
    actual_checksum = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    if actual_checksum.lower() != expected_checksum.lower():
        raise JSONValidationError(
            f"Checksum mismatch. Expected: {expected_checksum}, "
            f"Got: {actual_checksum}"
        )


def _validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate that all required fields are present.
    
    Raises:
        JSONValidationError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise JSONValidationError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )


def create_json_response_with_checksum(data: Dict[str, Any]) -> str:
    """
    Create a JSON response with delimiters and checksum.
    
    Useful for testing or creating example responses.
    
    Args:
        data: Dictionary to convert to JSON
        
    Returns:
        Formatted response with BEGIN_JSON, END_JSON, and SHA256 checksum
        
    Example:
        >>> data = {"field1": "value", "field2": 42}
        >>> response = create_json_response_with_checksum(data)
        >>> print(response)
        BEGIN_JSON
        {"field1": "value", "field2": 42}
        END_JSON
        
        SHA256: <checksum>
    """
    json_str = json.dumps(data, indent=2)
    normalized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    checksum = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    return f"""BEGIN_JSON
{json_str}
END_JSON

SHA256: {checksum}"""
