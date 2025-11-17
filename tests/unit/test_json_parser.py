"""
Tests for JSON parsing and validation utilities.
"""

import pytest
import json
import hashlib

from shared.json_parser import (
    parse_llm_json_response,
    create_json_response_with_checksum,
    ParsedResponse,
    JSONParseError,
    JSONValidationError,
)


class TestParseBasicJSON:
    """Tests for basic JSON parsing."""
    
    def test_parse_simple_json(self):
        """Test parsing simple JSON without delimiters."""
        response = '{"field1": "value1", "field2": 42}'
        result = parse_llm_json_response(response, validate_checksum=False)
        
        assert result.data == {"field1": "value1", "field2": 42}
        assert result.delimiter_found is False
        assert result.checksum is None
    
    def test_parse_json_with_whitespace(self):
        """Test parsing JSON with surrounding whitespace."""
        response = '''
        
        {"field1": "value1"}
        
        '''
        result = parse_llm_json_response(response, validate_checksum=False)
        
        assert result.data == {"field1": "value1"}
    
    def test_parse_invalid_json(self):
        """Test that invalid JSON raises JSONParseError."""
        response = '{"invalid": json}'
        
        with pytest.raises(JSONParseError, match="Failed to parse JSON"):
            parse_llm_json_response(response)
    
    def test_parse_non_dict_json(self):
        """Test that non-dictionary JSON raises error."""
        response = '["array", "not", "dict"]'
        
        with pytest.raises(JSONParseError, match="Expected JSON object"):
            parse_llm_json_response(response)


class TestParseWithDelimiters:
    """Tests for JSON parsing with BEGIN_JSON/END_JSON delimiters."""
    
    def test_parse_with_standard_delimiters(self):
        """Test parsing JSON with BEGIN_JSON and END_JSON."""
        response = '''
        Some preamble text that should be ignored.
        
        BEGIN_JSON
        {"field1": "value1", "field2": 42}
        END_JSON
        
        Some trailing text.
        '''
        
        result = parse_llm_json_response(response, validate_checksum=False)
        
        assert result.data == {"field1": "value1", "field2": 42}
        assert result.delimiter_found is True
    
    def test_parse_with_custom_delimiters(self):
        """Test parsing with custom delimiters."""
        response = '''
        START_DATA
        {"custom": "delimiters"}
        END_DATA
        '''
        
        result = parse_llm_json_response(
            response,
            begin_delimiter="START_DATA",
            end_delimiter="END_DATA",
            validate_checksum=False,
        )
        
        assert result.data == {"custom": "delimiters"}
        assert result.delimiter_found is True
    
    def test_parse_case_insensitive_delimiters(self):
        """Test that delimiter matching is case-insensitive."""
        response = '''
        begin_json
        {"field": "value"}
        end_json
        '''
        
        result = parse_llm_json_response(response, validate_checksum=False)
        
        assert result.data == {"field": "value"}
        assert result.delimiter_found is True
    
    def test_parse_multiline_json_in_delimiters(self):
        """Test parsing multi-line formatted JSON."""
        response = '''
        BEGIN_JSON
        {
            "field1": "value1",
            "field2": {
                "nested": "value"
            },
            "field3": [1, 2, 3]
        }
        END_JSON
        '''
        
        result = parse_llm_json_response(response, validate_checksum=False)
        
        assert result.data["field1"] == "value1"
        assert result.data["field2"]["nested"] == "value"
        assert result.data["field3"] == [1, 2, 3]


class TestChecksumValidation:
    """Tests for SHA256 checksum validation."""
    
    def test_valid_checksum(self):
        """Test that valid checksum passes validation."""
        data = {"field1": "value1", "field2": 42}
        response = create_json_response_with_checksum(data)
        
        result = parse_llm_json_response(response, validate_checksum=True)
        
        assert result.data == data
        assert result.checksum is not None
        assert len(result.checksum) == 64  # SHA256 hex length
    
    def test_invalid_checksum(self):
        """Test that invalid checksum raises error."""
        response = '''
        BEGIN_JSON
        {"field": "value"}
        END_JSON
        
        SHA256: 0000000000000000000000000000000000000000000000000000000000000000
        '''
        
        with pytest.raises(JSONValidationError, match="Checksum mismatch"):
            parse_llm_json_response(response, validate_checksum=True)
    
    def test_checksum_case_insensitive(self):
        """Test that checksum validation is case-insensitive."""
        data = {"test": "data"}
        json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        checksum = hashlib.sha256(json_str.encode()).hexdigest().upper()
        
        response = f'''
        BEGIN_JSON
        {json.dumps(data)}
        END_JSON
        
        SHA256: {checksum}
        '''
        
        result = parse_llm_json_response(response, validate_checksum=True)
        assert result.data == data
    
    def test_no_checksum_with_validation_enabled(self):
        """Test that missing checksum is OK when validation enabled."""
        response = '''
        BEGIN_JSON
        {"field": "value"}
        END_JSON
        '''
        
        # Should not raise - checksum is optional
        result = parse_llm_json_response(response, validate_checksum=True)
        assert result.checksum is None
    
    def test_checksum_extraction_patterns(self):
        """Test various checksum format patterns."""
        data = {"test": "data"}
        json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        checksum = hashlib.sha256(json_str.encode()).hexdigest()
        
        patterns = [
            f"SHA256: {checksum}",
            f"Checksum: {checksum}",
            f"sha256: {checksum}",
        ]
        
        for pattern in patterns:
            response = f'''
            BEGIN_JSON
            {json.dumps(data)}
            END_JSON
            
            {pattern}
            '''
            
            result = parse_llm_json_response(response, validate_checksum=True)
            assert result.checksum == checksum.lower()


class TestRequiredFields:
    """Tests for required field validation."""
    
    def test_all_required_fields_present(self):
        """Test validation passes when all fields present."""
        response = '{"field1": "value1", "field2": 42, "field3": true}'
        
        result = parse_llm_json_response(
            response,
            required_fields=["field1", "field2"],
            validate_checksum=False,
        )
        
        assert "field1" in result.data
        assert "field2" in result.data
    
    def test_missing_required_field(self):
        """Test validation fails when required field missing."""
        response = '{"field1": "value1"}'
        
        with pytest.raises(JSONValidationError, match="Missing required fields: field2"):
            parse_llm_json_response(
                response,
                required_fields=["field1", "field2"],
                validate_checksum=False,
            )
    
    def test_multiple_missing_fields(self):
        """Test error message includes all missing fields."""
        response = '{"field1": "value1"}'
        
        with pytest.raises(JSONValidationError, match="field2.*field3"):
            parse_llm_json_response(
                response,
                required_fields=["field1", "field2", "field3"],
                validate_checksum=False,
            )
    
    def test_no_required_fields(self):
        """Test validation passes when no fields required."""
        response = '{"any": "field"}'
        
        result = parse_llm_json_response(
            response,
            required_fields=None,
            validate_checksum=False,
        )
        
        assert result.data == {"any": "field"}


class TestCreateJSONResponseWithChecksum:
    """Tests for creating JSON responses with checksums."""
    
    def test_create_response(self):
        """Test creating a response with checksum."""
        data = {"field1": "value1", "field2": 42}
        response = create_json_response_with_checksum(data)
        
        assert "BEGIN_JSON" in response
        assert "END_JSON" in response
        assert "SHA256:" in response
        assert '"field1": "value1"' in response
    
    def test_created_response_is_parseable(self):
        """Test that created response can be parsed back."""
        data = {"field1": "value1", "field2": 42}
        response = create_json_response_with_checksum(data)
        
        result = parse_llm_json_response(response, validate_checksum=True)
        
        assert result.data == data
        assert result.delimiter_found is True
        assert result.checksum is not None
    
    def test_roundtrip(self):
        """Test creating and parsing complex data."""
        data = {
            "string": "value",
            "number": 123,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "object": {"nested": "data"},
        }
        
        response = create_json_response_with_checksum(data)
        result = parse_llm_json_response(response, validate_checksum=True)
        
        assert result.data == data


class TestParsedResponse:
    """Tests for ParsedResponse dataclass."""
    
    def test_parsed_response_structure(self):
        """Test ParsedResponse contains expected fields."""
        response = create_json_response_with_checksum({"test": "data"})
        result = parse_llm_json_response(response)
        
        assert isinstance(result, ParsedResponse)
        assert isinstance(result.data, dict)
        assert isinstance(result.raw_json, str)
        assert isinstance(result.delimiter_found, bool)
        # checksum can be None or str
        assert result.checksum is None or isinstance(result.checksum, str)
