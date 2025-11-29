"""
Unit tests for workflows/shared/json_parser.py - Parser Pattern (Python Distilled Ch. 14)

This file tests the Parser pattern implementation with:
- JSON extraction from delimited and non-delimited responses
- SHA256 checksum validation for data integrity
- Required field validation for schema compliance
- Error recovery with custom exceptions
- Type safety with ParsedResponse dataclass

Pattern Compliance: Python Distilled Ch. 14 "Data Encoding"
- Validation before parsing
- Error recovery mechanisms
- Type safety (return typed objects)
- Encoding handling (UTF-8 explicit)

Coverage Target: ≥70% (expect 85%+)
"""

import json
import hashlib
import pytest
from typing import Dict, Any

from workflows.shared.json_parser import (
    parse_llm_json_response,
    create_json_response_with_checksum,
    ParsedResponse,
    JSONParseError,
    JSONValidationError,
    _extract_json_with_delimiters,
    _extract_checksum,
    _validate_checksum,
    _validate_required_fields,
)


# ============================================================================
# Test Class 1: Valid Parsing (Parser Pattern - Success Cases)
# ============================================================================


class TestValidParsing:
    """
    Test successful JSON parsing from various response formats.
    
    Parser Pattern Requirements:
    - Parse simple and complex JSON structures
    - Handle both delimited and non-delimited responses
    - Return typed ParsedResponse objects
    """

    def test_parse_simple_json_with_delimiters(self):
        """Test parsing simple JSON with BEGIN_JSON/END_JSON delimiters."""
        # Arrange
        data = {"name": "Test", "value": 42}
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response, validate_checksum=True)
        
        # Assert - Parser Pattern: Type Safety
        assert isinstance(result, ParsedResponse)
        assert result.data == data
        assert result.delimiter_found is True
        assert result.checksum is not None
        assert len(result.checksum) == 64  # SHA256 is 64 hex chars

    def test_parse_nested_structures(self):
        """Test parsing nested JSON with complex structures."""
        # Arrange - Complex nested structure
        data = {
            "metadata": {
                "title": "Advanced Python",
                "authors": ["Author 1", "Author 2"],
                "chapters": [
                    {"id": 1, "name": "Introduction"},
                    {"id": 2, "name": "Advanced Topics"},
                ]
            },
            "concepts": {
                "primary": ["decorators", "generators"],
                "secondary": {"patterns": ["factory", "singleton"]}
            }
        }
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response)
        
        # Assert - Parser Pattern: Handle Complex Structures
        assert result.data == data
        assert result.data["metadata"]["chapters"][0]["name"] == "Introduction"
        assert "decorators" in result.data["concepts"]["primary"]
        assert result.data["concepts"]["secondary"]["patterns"] == ["factory", "singleton"]

    def test_parse_without_delimiters(self):
        """Test parsing JSON without delimiters (entire response is JSON)."""
        # Arrange - No delimiters, just raw JSON
        data = {"status": "success", "count": 100}
        response = json.dumps(data)
        
        # Act
        result = parse_llm_json_response(response, validate_checksum=False)
        
        # Assert - Parser Pattern: Flexible Parsing
        assert result.data == data
        assert result.delimiter_found is False
        assert result.checksum is None  # No checksum in response

    def test_parse_with_explanatory_text(self):
        """Test parsing JSON with explanatory text around delimiters."""
        # Arrange - LLM response with explanation + delimited JSON
        data = {"extracted": True, "fields": ["title", "author"]}
        json_str = json.dumps(data, indent=2)
        response = f"""
Here's the extracted metadata:

BEGIN_JSON
{json_str}
END_JSON

I hope this helps!
"""
        
        # Act
        result = parse_llm_json_response(response, validate_checksum=False)
        
        # Assert - Parser Pattern: Extract from Unstructured Text
        assert result.data == data
        assert result.delimiter_found is True

    def test_parse_with_custom_delimiters(self):
        """Test parsing with custom delimiter strings."""
        # Arrange
        data = {"custom": "delimiters"}
        json_str = json.dumps(data)
        response = f"START_DATA\n{json_str}\nEND_DATA"
        
        # Act
        result = parse_llm_json_response(
            response,
            begin_delimiter="START_DATA",
            end_delimiter="END_DATA",
            validate_checksum=False
        )
        
        # Assert
        assert result.data == data
        assert result.delimiter_found is True


# ============================================================================
# Test Class 2: Error Handling (Parser Pattern - Error Recovery)
# ============================================================================


class TestErrorHandling:
    """
    Test error handling for malformed JSON and invalid responses.
    
    Parser Pattern Requirements:
    - Graceful error recovery
    - Clear error messages with JSONParseError
    - Distinguish parse errors from validation errors
    """

    def test_malformed_json_syntax_error(self):
        """Test handling of malformed JSON syntax."""
        # Arrange - Invalid JSON (missing closing brace)
        response = 'BEGIN_JSON\n{"name": "Test", "value": 42\nEND_JSON'
        
        # Act & Assert - Parser Pattern: Error Recovery
        with pytest.raises(JSONParseError) as exc_info:
            parse_llm_json_response(response, validate_checksum=False)
        
        assert "Failed to parse JSON" in str(exc_info.value)

    def test_non_dict_json_rejected(self):
        """Test rejection of non-dict JSON (arrays, primitives)."""
        # Arrange - Valid JSON but not a dict
        test_cases = [
            ('["array", "of", "strings"]', 'list'),  # Array
            ('42', 'int'),  # Number
            ('"just a string"', 'str'),  # String
            ('true', 'bool'),  # Boolean
            ('null', 'NoneType'),  # Null
        ]
        
        # Act & Assert - Parser Pattern: Type Safety
        for json_str, expected_type in test_cases:
            response = f"BEGIN_JSON\n{json_str}\nEND_JSON"
            with pytest.raises(JSONParseError) as exc_info:
                parse_llm_json_response(response, validate_checksum=False)
            
            # Error message format: "Expected JSON object (dict), got <type>"
            assert "Expected JSON object (dict)" in str(exc_info.value)

    def test_empty_response_error(self):
        """Test handling of empty or whitespace-only response."""
        # Arrange
        test_cases = ["", "   ", "\n\n", "\t\t"]
        
        # Act & Assert - Parser Pattern: Input Validation
        for response in test_cases:
            with pytest.raises(JSONParseError):
                parse_llm_json_response(response, validate_checksum=False)

    def test_incomplete_json_with_delimiters(self):
        """Test handling of response with only one delimiter."""
        # Arrange - Missing END_JSON
        response = "BEGIN_JSON\n{\"name\": \"Test\"}"
        
        # Act - Should fall back to parsing entire response
        with pytest.raises(JSONParseError):
            # Will try to parse entire response as JSON, which includes BEGIN_JSON
            parse_llm_json_response(response, validate_checksum=False)


# ============================================================================
# Test Class 3: Checksum Validation (Data Integrity)
# ============================================================================


class TestChecksumValidation:
    """
    Test SHA256 checksum validation for data integrity.
    
    Parser Pattern Requirements:
    - Verify data integrity with checksums
    - Detect tampering or corruption
    - Handle normalized JSON (sorted keys, compact separators)
    """

    def test_valid_checksum_passes(self):
        """Test that valid checksum passes validation."""
        # Arrange - Use helper to create valid response with checksum
        data = {"title": "Book", "author": "Author", "year": 2024}
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response, validate_checksum=True)
        
        # Assert - Parser Pattern: Data Integrity
        assert result.data == data
        assert result.checksum is not None
        assert len(result.checksum) == 64

    def test_invalid_checksum_raises_validation_error(self):
        """Test that invalid checksum raises JSONValidationError."""
        # Arrange - Create response with wrong checksum
        data = {"field": "value"}
        json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        wrong_checksum = "a" * 64  # Invalid checksum
        response = f"BEGIN_JSON\n{json_str}\nEND_JSON\nSHA256: {wrong_checksum}"
        
        # Act & Assert - Parser Pattern: Validation
        with pytest.raises(JSONValidationError) as exc_info:
            parse_llm_json_response(response, validate_checksum=True)
        
        assert "Checksum mismatch" in str(exc_info.value)

    def test_checksum_validation_can_be_disabled(self):
        """Test that checksum validation can be skipped."""
        # Arrange - Response with wrong checksum
        data = {"field": "value"}
        json_str = json.dumps(data)
        response = f"BEGIN_JSON\n{json_str}\nEND_JSON\nSHA256: {'a' * 64}"
        
        # Act - Disable checksum validation
        result = parse_llm_json_response(response, validate_checksum=False)
        
        # Assert - Should succeed without validation
        assert result.data == data

    def test_checksum_normalization(self):
        """Test that checksum uses normalized JSON (sorted keys, compact)."""
        # Arrange - JSON with different formatting but same content
        data = {"z": 3, "a": 1, "m": 2}  # Unsorted keys
        
        # Normalized form: {"a":1,"m":2,"z":3}
        normalized = json.dumps(data, sort_keys=True, separators=(',', ':'))
        expected_checksum = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
        
        # Create response with correct normalized checksum
        json_str = json.dumps(data, indent=2)  # Pretty printed
        response = f"BEGIN_JSON\n{json_str}\nEND_JSON\nChecksum: {expected_checksum}"
        
        # Act
        result = parse_llm_json_response(response, validate_checksum=True)
        
        # Assert - Parser Pattern: Normalization for Consistency
        assert result.data == data
        assert result.checksum == expected_checksum

    def test_missing_checksum_when_validation_enabled(self):
        """Test behavior when checksum validation enabled but no checksum in response."""
        # Arrange - No checksum in response
        data = {"field": "value"}
        response = f"BEGIN_JSON\n{json.dumps(data)}\nEND_JSON"
        
        # Act - Validation enabled but checksum missing
        result = parse_llm_json_response(response, validate_checksum=True)
        
        # Assert - Should succeed (checksum is optional)
        assert result.data == data
        assert result.checksum is None


# ============================================================================
# Test Class 4: Required Fields Validation (Schema Validation)
# ============================================================================


class TestRequiredFieldsValidation:
    """
    Test required field validation for schema compliance.
    
    Parser Pattern Requirements:
    - Enforce schema requirements
    - Validate required fields are present
    - Clear error messages listing missing fields
    """

    def test_required_fields_present_passes(self):
        """Test that all required fields present passes validation."""
        # Arrange
        data = {"title": "Book", "author": "Author", "year": 2024}
        response = create_json_response_with_checksum(data)
        required = ["title", "author"]
        
        # Act
        result = parse_llm_json_response(response, required_fields=required)
        
        # Assert - Parser Pattern: Schema Validation
        assert result.data == data
        assert "title" in result.data
        assert "author" in result.data

    def test_missing_required_fields_raises_validation_error(self):
        """Test that missing required fields raises JSONValidationError."""
        # Arrange
        data = {"title": "Book"}  # Missing 'author'
        response = create_json_response_with_checksum(data)
        required = ["title", "author", "year"]
        
        # Act & Assert - Parser Pattern: Validation
        with pytest.raises(JSONValidationError) as exc_info:
            parse_llm_json_response(response, required_fields=required)
        
        error_msg = str(exc_info.value)
        assert "Missing required fields" in error_msg
        assert "author" in error_msg
        assert "year" in error_msg
        assert "title" not in error_msg  # Title is present

    def test_no_required_fields_validation_optional(self):
        """Test that required field validation is optional."""
        # Arrange
        data = {"any": "field"}
        response = create_json_response_with_checksum(data)
        
        # Act - No required fields specified
        result = parse_llm_json_response(response, required_fields=None)
        
        # Assert - Should succeed without validation
        assert result.data == data

    def test_empty_required_fields_list(self):
        """Test that empty required fields list means no validation."""
        # Arrange
        data = {"field": "value"}
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response, required_fields=[])
        
        # Assert
        assert result.data == data


# ============================================================================
# Test Class 5: Edge Cases & Special Scenarios
# ============================================================================


class TestEdgeCases:
    """
    Test edge cases and special scenarios.
    
    Parser Pattern Requirements:
    - Handle empty JSON objects/arrays
    - Handle null/None values
    - Case-insensitive delimiter matching
    - Unicode and special characters
    """

    def test_empty_json_object(self):
        """Test parsing empty JSON object {}."""
        # Arrange
        data = {}
        response = f"BEGIN_JSON\n{json.dumps(data)}\nEND_JSON"
        
        # Act
        result = parse_llm_json_response(response, validate_checksum=False)
        
        # Assert - Parser Pattern: Handle Edge Cases
        assert result.data == {}
        assert isinstance(result.data, dict)

    def test_null_values_in_data(self):
        """Test handling of null/None values in JSON."""
        # Arrange
        data = {"field1": None, "field2": "value", "field3": None}
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response)
        
        # Assert - Parser Pattern: Preserve Null Values
        assert result.data["field1"] is None
        assert result.data["field2"] == "value"
        assert result.data["field3"] is None

    def test_case_insensitive_delimiters(self):
        """Test that delimiter matching is case-insensitive."""
        # Arrange - Mixed case delimiters
        data = {"test": "case"}
        json_str = json.dumps(data)
        test_cases = [
            (f"begin_json\n{json_str}\nend_json", True),  # lowercase
            (f"BEGIN_JSON\n{json_str}\nEND_JSON", True),  # uppercase
            (f"Begin_Json\n{json_str}\nEnd_Json", True),  # mixed case
        ]
        
        # Act & Assert - Parser Pattern: Flexible Input
        for response, expected_delimiter_found in test_cases:
            result = parse_llm_json_response(response, validate_checksum=False)
            assert result.data == data
            assert result.delimiter_found == expected_delimiter_found

    def test_unicode_and_special_characters(self):
        """Test handling of Unicode and special characters in JSON."""
        # Arrange - Unicode characters
        data = {
            "title": "Pythön Programming 🐍",
            "author": "José García",
            "symbols": "αβγδ ∑∏∫",
            "emoji": "😀🎉🚀"
        }
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response)
        
        # Assert - Parser Pattern: Encoding Handling
        assert result.data == data
        assert result.data["title"] == "Pythön Programming 🐍"
        assert "🐍" in result.data["title"]

    def test_large_json_response(self):
        """Test handling of large JSON responses (>1000 items)."""
        # Arrange - Large nested structure
        data = {
            "items": [{"id": i, "name": f"Item {i}", "value": i * 10} for i in range(1000)],
            "metadata": {"count": 1000, "type": "large_dataset"}
        }
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response)
        
        # Assert - Parser Pattern: Performance
        assert len(result.data["items"]) == 1000
        assert result.data["items"][500]["id"] == 500
        assert result.data["metadata"]["count"] == 1000


# ============================================================================
# Test Class 6: Helper Functions (Internal API)
# ============================================================================


class TestHelperFunctions:
    """
    Test internal helper functions for delimiter extraction and validation.
    
    Note: These are tested implicitly through parse_llm_json_response(),
    but explicit tests ensure correct behavior at each layer.
    """

    def test_extract_json_with_delimiters_success(self):
        """Test _extract_json_with_delimiters() finds JSON correctly."""
        # Arrange
        json_str = '{"key": "value"}'
        text = f"Some text\nBEGIN_JSON\n{json_str}\nEND_JSON\nMore text"
        
        # Act
        extracted, found = _extract_json_with_delimiters(text, "BEGIN_JSON", "END_JSON")
        
        # Assert
        assert found is True
        assert extracted.strip() == json_str

    def test_extract_json_no_delimiters(self):
        """Test _extract_json_with_delimiters() when delimiters absent."""
        # Arrange
        text = '{"no": "delimiters"}'
        
        # Act
        extracted, found = _extract_json_with_delimiters(text, "BEGIN_JSON", "END_JSON")
        
        # Assert - When delimiters not found, returns empty string
        assert found is False
        assert extracted == ""  # Implementation returns empty string when delimiters not found

    def test_extract_checksum_various_patterns(self):
        """Test _extract_checksum() finds checksums in different formats."""
        # Arrange
        valid_checksum = "a" * 64
        test_cases = [
            f"SHA256: {valid_checksum}",
            f"Checksum: {valid_checksum}",
            f"sha256: {valid_checksum}",
            f"Some text\nSHA256: {valid_checksum}\nMore text",
        ]
        
        # Act & Assert
        for text in test_cases:
            checksum = _extract_checksum(text)
            assert checksum == valid_checksum

    def test_extract_checksum_not_found(self):
        """Test _extract_checksum() returns None when no checksum present."""
        # Arrange
        text = "No checksum here"
        
        # Act
        checksum = _extract_checksum(text)
        
        # Assert
        assert checksum is None

    def test_validate_checksum_success(self):
        """Test _validate_checksum() passes for valid checksum."""
        # Arrange
        json_str = '{"test":"data"}'
        normalized = json.dumps(json.loads(json_str), sort_keys=True, separators=(',', ':'))
        expected = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
        
        # Act - Should not raise
        _validate_checksum(json_str, expected)

    def test_validate_checksum_mismatch(self):
        """Test _validate_checksum() raises error for invalid checksum."""
        # Arrange
        json_str = '{"test":"data"}'
        wrong_checksum = "b" * 64
        
        # Act & Assert
        with pytest.raises(JSONValidationError) as exc_info:
            _validate_checksum(json_str, wrong_checksum)
        
        assert "Checksum mismatch" in str(exc_info.value)

    def test_validate_required_fields_success(self):
        """Test _validate_required_fields() passes when all present."""
        # Arrange
        data = {"field1": "a", "field2": "b", "field3": "c"}
        required = ["field1", "field3"]
        
        # Act - Should not raise
        _validate_required_fields(data, required)

    def test_validate_required_fields_missing(self):
        """Test _validate_required_fields() raises error for missing fields."""
        # Arrange
        data = {"field1": "a"}
        required = ["field1", "field2", "field3"]
        
        # Act & Assert
        with pytest.raises(JSONValidationError) as exc_info:
            _validate_required_fields(data, required)
        
        error_msg = str(exc_info.value)
        assert "field2" in error_msg
        assert "field3" in error_msg


# ============================================================================
# Test Class 7: Parser Pattern Compliance (PRIMARY VALIDATION)
# ============================================================================


class TestParserPatternCompliance:
    """
    Validate Parser Pattern implementation against Python Distilled Ch. 14.
    
    PRIMARY PATTERN VALIDATION TESTS
    These tests explicitly verify architecture pattern requirements.
    """

    def test_validation_before_parsing(self):
        """
        Parser Pattern: Validation before processing.
        
        Ensures input validation occurs before attempting to parse.
        """
        # Arrange - Empty input
        response = ""
        
        # Act & Assert - Should fail validation immediately
        with pytest.raises(JSONParseError):
            parse_llm_json_response(response, validate_checksum=False)

    def test_error_recovery_with_custom_exceptions(self):
        """
        Parser Pattern: Error recovery with clear exception types.
        
        Distinguishes between parse errors and validation errors.
        """
        # Test 1: Parse error (malformed JSON)
        with pytest.raises(JSONParseError):
            parse_llm_json_response('BEGIN_JSON\n{invalid}\nEND_JSON', validate_checksum=False)
        
        # Test 2: Validation error (missing required fields)
        data = {"field": "value"}
        response = create_json_response_with_checksum(data)
        with pytest.raises(JSONValidationError):
            parse_llm_json_response(response, required_fields=["missing_field"])

    def test_type_safety_returns_dataclass(self):
        """
        Parser Pattern: Type safety with typed return values.
        
        Returns ParsedResponse dataclass, not raw dict.
        """
        # Arrange
        data = {"test": "data"}
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response)
        
        # Assert - Type safety enforced
        assert isinstance(result, ParsedResponse)
        assert hasattr(result, 'data')
        assert hasattr(result, 'raw_json')
        assert hasattr(result, 'checksum')
        assert hasattr(result, 'delimiter_found')

    def test_encoding_handling_utf8(self):
        """
        Parser Pattern: Explicit encoding handling (UTF-8).
        
        Handles Unicode characters correctly.
        """
        # Arrange - Unicode content
        data = {"text": "Tëst UTF-8: €£¥"}
        response = create_json_response_with_checksum(data)
        
        # Act
        result = parse_llm_json_response(response)
        
        # Assert - Encoding preserved
        assert result.data["text"] == "Tëst UTF-8: €£¥"

    def test_performance_large_file_handling(self):
        """
        Parser Pattern: Efficient parsing for large files.
        
        Note: json.loads() is used which loads entire content.
        For very large files (>100MB), streaming parser would be needed.
        """
        # Arrange - Moderately large JSON (1MB+)
        data = {"records": [{"id": i, "data": "x" * 1000} for i in range(1000)]}
        response = create_json_response_with_checksum(data)
        
        # Act
        import time
        start = time.time()
        result = parse_llm_json_response(response)
        duration = time.time() - start
        
        # Assert - Should parse reasonably fast (<1 second)
        assert result.data == data
        assert duration < 1.0  # Performance threshold
