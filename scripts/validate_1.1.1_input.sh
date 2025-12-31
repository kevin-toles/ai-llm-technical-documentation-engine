#!/bin/bash
# =============================================================================
# WBS 1.1.1 Validation Script: Input Preparation
# Reference: END_TO_END_INTEGRATION_WBS.md
# =============================================================================

set -e

# Constants for repeated strings
SEPARATOR="=========================================="

echo "$SEPARATOR"
echo "WBS 1.1.1 Validation: Input Preparation"
echo "$SEPARATOR"

MANIFEST="/Users/kevintoles/POC/textbooks/test_manifest.json"
PDF_DIR="/Users/kevintoles/POC/textbooks/PDF"
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
# Test 1: Checking for PDFs in directory
# -----------------------------------------------------------------------------
echo ""
echo "Test 1: Checking for PDFs in directory..."
PDF_COUNT=$(ls -1 "$PDF_DIR"/*.pdf 2>/dev/null | wc -l | tr -d ' ')
check_result "Found $PDF_COUNT PDF(s) in directory" "$([[ "$PDF_COUNT" -ge 1 ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 2: Checking manifest exists
# -----------------------------------------------------------------------------
echo ""
echo "Test 2: Checking manifest exists..."
check_result "Manifest file exists" "$([[ -f "$MANIFEST" ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 3: Validating manifest JSON
# -----------------------------------------------------------------------------
echo ""
echo "Test 3: Validating manifest JSON..."
JSON_VALID=$(python3 -c "import json; json.load(open('$MANIFEST')); print('true')" 2>/dev/null || echo 'false')
check_result "Valid JSON format" "$JSON_VALID"

# -----------------------------------------------------------------------------
# Test 4: Checking manifest has required fields
# -----------------------------------------------------------------------------
echo ""
echo "Test 4: Checking manifest has required fields..."
PDF_PATH=$(jq -r '.pdf_path' "$MANIFEST" 2>/dev/null)
EXPECTED=$(jq '.expected_chapters' "$MANIFEST" 2>/dev/null)
check_result "PDF path defined: $PDF_PATH" "$([[ -n "$PDF_PATH" && "$PDF_PATH" != "null" ]] && echo 'true' || echo 'false')"
check_result "Expected chapters defined: $EXPECTED" "$([[ -n "$EXPECTED" && "$EXPECTED" != "null" && "$EXPECTED" -gt 0 ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 5: Checking PDF file exists at specified path
# -----------------------------------------------------------------------------
echo ""
echo "Test 5: Checking PDF file exists at specified path..."
check_result "PDF file exists at path" "$([[ -f "$PDF_PATH" ]] && echo 'true' || echo 'false')"

# -----------------------------------------------------------------------------
# Test 6: Testing text extraction
# -----------------------------------------------------------------------------
echo ""
echo "Test 6: Testing text extraction..."
if command -v pdftotext &> /dev/null; then
    CHARS=$(pdftotext -f 1 -l 3 "$PDF_PATH" - 2>/dev/null | wc -c | tr -d ' ')
    check_result "Text extractable ($CHARS chars from pages 1-3)" "$([[ "$CHARS" -gt 100 ]] && echo 'true' || echo 'false')"
else
    echo "⚠️  pdftotext not installed (install with: brew install poppler)"
    FAILED=$((FAILED + 1))
fi

# -----------------------------------------------------------------------------
# Test 7: Checking expected pages
# -----------------------------------------------------------------------------
echo ""
echo "Test 7: Checking expected pages..."
EXPECTED_PAGES=$(jq '.expected_pages' "$MANIFEST" 2>/dev/null)
if command -v pdfinfo &> /dev/null; then
    ACTUAL_PAGES=$(pdfinfo "$PDF_PATH" 2>/dev/null | grep "Pages:" | awk '{print $2}')
    echo "   Expected: $EXPECTED_PAGES, Actual: $ACTUAL_PAGES"
    check_result "Page count matches or close" "$([[ "$ACTUAL_PAGES" -eq "$EXPECTED_PAGES" ]] && echo 'true' || echo 'false')"
else
    echo "⚠️  pdfinfo not installed"
    FAILED=$((FAILED + 1))
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "$SEPARATOR"
echo "WBS 1.1.1 Validation Summary"
echo "$SEPARATOR"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo "✅ All WBS 1.1.1 acceptance tests passed!"
    exit 0
else
    echo "❌ Some tests failed. Please review."
    exit 1
fi
