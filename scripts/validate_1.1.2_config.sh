#!/bin/bash
# =============================================================================
# WBS 1.1.2 Validation Script: Extraction Pipeline Configuration
# Reference: END_TO_END_INTEGRATION_WBS.md
# =============================================================================

set -e

echo "=========================================="
echo "WBS 1.1.2 Validation: Extraction Pipeline Config"
echo "=========================================="

CONFIG_FILE="/Users/kevintoles/POC/llm-document-enhancer/config/pdf_extraction.yaml"
PASSED=0
FAILED=0

# Helper function for test results
check_result() {
    local test_name="$1"
    local condition="$2"
    if [[ "$condition" == "true" ]]; then
        echo "✅ PASS: $test_name"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FAIL: $test_name"
        FAILED=$((FAILED + 1))
    fi
    return 0
}

# -----------------------------------------------------------------------------
# Test 1: Config file exists
# -----------------------------------------------------------------------------
echo ""
echo "Test 1: Config file exists..."
check_result "Config file exists" "$([[ -f "$CONFIG_FILE" ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 2: Has input_pdf configuration
# -----------------------------------------------------------------------------
echo ""
echo "Test 2: Has input_pdf configuration..."
INPUT_PDF_COUNT=$(grep -c "input_pdf:" "$CONFIG_FILE" 2>/dev/null || echo "0")
check_result "Has input_pdf field (count: $INPUT_PDF_COUNT)" "$([[ "$INPUT_PDF_COUNT" -eq 1 ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 3: Has output_json configuration
# -----------------------------------------------------------------------------
echo ""
echo "Test 3: Has output_json configuration..."
OUTPUT_JSON_COUNT=$(grep -c "output_json:" "$CONFIG_FILE" 2>/dev/null || echo "0")
check_result "Has output_json field (count: $OUTPUT_JSON_COUNT)" "$([[ "$OUTPUT_JSON_COUNT" -eq 1 ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 4: YAML is valid
# -----------------------------------------------------------------------------
echo ""
echo "Test 4: YAML syntax is valid..."
YAML_VALID=$(python3 -c "import yaml; yaml.safe_load(open('$CONFIG_FILE')); print('true')" 2>/dev/null || echo 'false')
check_result "Valid YAML syntax" "$YAML_VALID"

# -----------------------------------------------------------------------------
# Test 5: Has chunk_size configuration
# -----------------------------------------------------------------------------
echo ""
echo "Test 5: Has chunk_size configuration..."
CHUNK_SIZE=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print(c.get('chunking', {}).get('chunk_size', 0))" 2>/dev/null || echo "0")
check_result "Has chunk_size: $CHUNK_SIZE" "$([[ "$CHUNK_SIZE" -gt 0 ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 6: Has chunk_overlap configuration
# -----------------------------------------------------------------------------
echo ""
echo "Test 6: Has chunk_overlap configuration..."
CHUNK_OVERLAP=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print(c.get('chunking', {}).get('chunk_overlap', 0))" 2>/dev/null || echo "0")
check_result "Has chunk_overlap: $CHUNK_OVERLAP" "$([[ "$CHUNK_OVERLAP" -gt 0 ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 7: Has chapter_regex configuration
# -----------------------------------------------------------------------------
echo ""
echo "Test 7: Has chapter_regex configuration..."
HAS_REGEX=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print('true' if c.get('chapter_detection', {}).get('chapter_regex') else 'false')" 2>/dev/null || echo 'false')
check_result "Has chapter_regex pattern" "$HAS_REGEX"

# -----------------------------------------------------------------------------
# Test 8: Input PDF path is valid
# -----------------------------------------------------------------------------
echo ""
echo "Test 8: Input PDF path is valid..."
PDF_PATH=$(python3 -c "import yaml; c=yaml.safe_load(open('$CONFIG_FILE')); print(c.get('input', {}).get('input_pdf', ''))" 2>/dev/null || echo "")
check_result "PDF path exists: $PDF_PATH" "$([[ -f "$PDF_PATH" ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=========================================="
echo "WBS 1.1.2 Validation Summary"
echo "=========================================="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo "✅ All WBS 1.1.2 acceptance tests passed!"
    exit 0
else
    echo "❌ Some tests failed. Please review."
    exit 1
fi
