#!/bin/bash
# WBS 2.1.1 Validation: Setup Input Data for Guideline Generator
# Validates that input data is properly configured for Phase 2

echo "=== WBS 2.1.1 Validation: Setup Input Data ==="

cd /Users/kevintoles/POC/llm-document-enhancer
INPUT_DIR="workflows/base_guideline_generation/input"
JSON_FILE="$INPUT_DIR/test_book.json"
MANIFEST="$INPUT_DIR/book_manifest.json"

# Constants for repeated values
EXPECTED_NON_EMPTY=$EXPECTED_NON_EMPTY

TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    local expected="$3"
    
    if [[ "$result" == "$expected" ]]; then
        echo "✓ $name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "✗ $name (expected: $expected, got: $result)" >&2
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    return 0
}

echo ""
echo "1. Checking input JSON accessible..."
if [[ -f "$JSON_FILE" ]] || [[ -L "$JSON_FILE" ]]; then
    # Verify symlink target exists
    if [[ -r "$JSON_FILE" ]]; then
        run_test "Input JSON accessible" "true" "true"
    else
        run_test "Input JSON accessible (broken symlink)" "false" "true"
    fi
else
    run_test "Input JSON exists" "false" "true"
fi

echo ""
echo "2. Checking book manifest exists..."
if [[ -f "$MANIFEST" ]]; then
    run_test "Book manifest exists" "true" "true"
else
    run_test "Book manifest exists" "false" "true"
fi

echo ""
echo "3. Validating manifest JSON syntax..."
if python3 -c "import json; json.load(open('$MANIFEST'))" 2>/dev/null; then
    run_test "Valid JSON syntax" "true" "true"
else
    run_test "Valid JSON syntax" "false" "true"
fi

echo ""
echo "4. Checking manifest has author..."
AUTHOR=$(jq -r '.author // empty' "$MANIFEST" 2>/dev/null)
if [[ -n "$AUTHOR" ]]; then
    run_test "Manifest has author" "true" "true"
    echo "   Author: $AUTHOR"
else
    run_test "Manifest has author" "empty" $EXPECTED_NON_EMPTY
fi

echo ""
echo "5. Checking manifest has title..."
TITLE=$(jq -r '.title // empty' "$MANIFEST" 2>/dev/null)
if [[ -n "$TITLE" ]]; then
    run_test "Manifest has title" "true" "true"
    echo "   Title: $TITLE"
else
    run_test "Manifest has title" "empty" $EXPECTED_NON_EMPTY
fi

echo ""
echo "6. Checking manifest has tier..."
TIER=$(jq -r '.tier // empty' "$MANIFEST" 2>/dev/null)
if [[ -n "$TIER" ]]; then
    run_test "Manifest has tier" "true" "true"
    echo "   Tier: $TIER"
else
    run_test "Manifest has tier" "empty" $EXPECTED_NON_EMPTY
fi

echo ""
echo "7. Checking json_source reference..."
JSON_SOURCE=$(jq -r '.json_source // empty' "$MANIFEST" 2>/dev/null)
if [[ -n "$JSON_SOURCE" ]]; then
    run_test "Manifest has json_source" "true" "true"
    echo "   JSON Source: $JSON_SOURCE"
    
    # Verify json_source file exists
    if [[ -f "$INPUT_DIR/$JSON_SOURCE" ]] || [[ -L "$INPUT_DIR/$JSON_SOURCE" ]]; then
        run_test "JSON source file exists" "true" "true"
    else
        run_test "JSON source file exists" "false" "true"
    fi
else
    run_test "Manifest has json_source" "empty" $EXPECTED_NON_EMPTY
fi

echo ""
echo "8. Verifying input JSON has chapters..."
CHAPTER_COUNT=$(jq '.chapters | length' "$JSON_FILE" 2>/dev/null || echo "0")
if [[ "$CHAPTER_COUNT" -ge 1 ]]; then
    run_test "Input JSON has chapters" "true" "true"
    echo "   Chapters in JSON: $CHAPTER_COUNT"
else
    run_test "Input JSON has chapters" "$CHAPTER_COUNT" ">=1"
fi

echo ""
echo "=== Summary ==="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [[ "$TESTS_FAILED" -eq 0 ]]; then
    echo ""
    echo "=== WBS 2.1.1 PASSED ==="
    exit 0
else
    echo ""
    echo "=== WBS 2.1.1 FAILED ==="
    exit 1
fi
