#!/bin/bash
# WBS 2.2.1 Validation: Guideline Generation
# Validates that the guideline generator produces valid output

echo "=== WBS 2.2.1 Validation: Guideline Generation ==="

cd /Users/kevintoles/POC/llm-document-enhancer
OUTPUT_DIR="workflows/base_guideline_generation/output"

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

# Find any guideline MD file (either GUIDELINES_*.md or *_guideline.md pattern)
# Prefer GUIDELINES_* pattern, then fall back to *_guideline.md
MD_FILE=$(ls -1 "$OUTPUT_DIR"/GUIDELINES_*.md 2>/dev/null | head -1)
if [[ -z "$MD_FILE" ]]; then
    MD_FILE=$(ls -1 "$OUTPUT_DIR"/*_guideline.md 2>/dev/null | head -1)
fi

echo ""
echo "1. Checking output file exists..."
if [[ -n "$MD_FILE" ]] && [[ -f "$MD_FILE" ]]; then
    run_test "MD file exists" "true" "true"
    echo "   Found: $MD_FILE"
else
    run_test "MD file exists" "false" "true"
    echo "ERROR: No guideline MD file found in $OUTPUT_DIR"
    exit 1
fi

echo ""
echo "2. Checking file size..."
SIZE=$(stat -f%z "$MD_FILE" 2>/dev/null || stat --format=%s "$MD_FILE")
if [[ "$SIZE" -gt 10000 ]]; then
    run_test "File size > 10KB" "true" "true"
    echo "   Size: $SIZE bytes"
else
    run_test "File size > 10KB" "$SIZE" ">10000"
fi

echo ""
echo "3. Counting chapter headers..."
CHAPTER_COUNT=$(grep -c "^## Chapter" "$MD_FILE" || echo "0")
if [[ "$CHAPTER_COUNT" -ge 1 ]]; then
    run_test "Has chapter headers" "true" "true"
    echo "   Found: $CHAPTER_COUNT chapter headers"
else
    run_test "Has chapter headers" "$CHAPTER_COUNT" ">=1"
fi

echo ""
echo "4. Checking for Chapter Summary sections..."
SUMMARY_COUNT=$(grep -c "### Chapter Summary" "$MD_FILE" || echo "0")
if [[ "$SUMMARY_COUNT" -ge 1 ]]; then
    run_test "Has Chapter Summary sections" "true" "true"
    echo "   Found: $SUMMARY_COUNT summaries"
else
    run_test "Has Chapter Summary sections" "$SUMMARY_COUNT" ">=1"
fi

echo ""
echo "5. Checking footnote references..."
FOOTNOTE_REFS=$(grep -c "\[\^[0-9]\+\]" "$MD_FILE" || echo "0")
if [[ "$FOOTNOTE_REFS" -ge 1 ]]; then
    run_test "Has footnote references" "true" "true"
    echo "   Found: $FOOTNOTE_REFS footnote references"
else
    run_test "Has footnote references" "$FOOTNOTE_REFS" ">=1"
fi

echo ""
echo "6. Checking footnote definitions..."
FOOTNOTE_DEFS=$(grep -c "^\[\^[0-9]\+\]:" "$MD_FILE" || echo "0")
if [[ "$FOOTNOTE_DEFS" -ge 1 ]]; then
    run_test "Has footnote definitions" "true" "true"
    echo "   Found: $FOOTNOTE_DEFS footnote definitions"
else
    run_test "Has footnote definitions" "$FOOTNOTE_DEFS" ">=1"
fi

echo ""
echo "7. Checking for code annotations..."
ANNOTATION_COUNT=$(grep -ci "annotation:" "$MD_FILE" || echo "0")
if [[ "$ANNOTATION_COUNT" -ge 1 ]]; then
    run_test "Has code annotations" "true" "true"
    echo "   Found: $ANNOTATION_COUNT annotations"
else
    run_test "Has code annotations" "$ANNOTATION_COUNT" ">=1"
fi

echo ""
echo "8. Checking for code blocks..."
CODE_BLOCKS=$(grep -c '^\`\`\`' "$MD_FILE" || echo "0")
if [[ "$CODE_BLOCKS" -ge 2 ]]; then
    run_test "Has code blocks" "true" "true"
    echo "   Found: $((CODE_BLOCKS / 2)) code blocks (approx)"
else
    run_test "Has code blocks" "$CODE_BLOCKS" ">=2"
fi

echo ""
echo "9. Checking for concept breakdowns..."
CONCEPT_COUNT=$(grep -c "#### \*\*" "$MD_FILE" || echo "0")
if [[ "$CONCEPT_COUNT" -ge 1 ]]; then
    run_test "Has concept breakdowns" "true" "true"
    echo "   Found: $CONCEPT_COUNT concepts"
else
    run_test "Has concept breakdowns" "$CONCEPT_COUNT" ">=1"
fi

echo ""
echo "10. Preview first chapter..."
echo "--- Preview (first 30 lines of Chapter 1) ---"
sed -n '/^## Chapter 1/,/^## Chapter 2/p' "$MD_FILE" | head -30
echo "--- End Preview ---"

echo ""
echo "=== Summary ==="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [[ "$TESTS_FAILED" -eq 0 ]]; then
    echo ""
    echo "=== WBS 2.2.1 PASSED ==="
    exit 0
else
    echo ""
    echo "=== WBS 2.2.1 FAILED ==="
    exit 1
fi
