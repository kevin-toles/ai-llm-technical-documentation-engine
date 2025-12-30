#!/bin/bash
# WBS 1.2.1 Validation: PDF to JSON Extraction
# Validates that PDF extraction produces correct chapter structure

echo "=== WBS 1.2.1 Validation: PDF to JSON ==="

cd /Users/kevintoles/POC/llm-document-enhancer
OUTPUT="workflows/pdf_to_json/output/test_book.json"
MANIFEST="/Users/kevintoles/POC/textbooks/test_manifest.json"

TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    local expected="$3"
    
    if [[ "$result" = "$expected" ]]; then
        echo "✓ $name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "✗ $name (expected: $expected, got: $result)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    return 0
}

echo ""
echo "1. Checking output file exists..."
if [[ -f "$OUTPUT" ]]; then
    run_test "Output file exists" "true" "true"
else
    run_test "Output file exists" "false" "true"
    echo "ERROR: Output missing - run extraction first"
    exit 1
fi

echo ""
echo "2. Validating JSON syntax..."
if python3 -c "import json; json.load(open('$OUTPUT'))" 2>/dev/null; then
    run_test "Valid JSON syntax" "true" "true"
else
    run_test "Valid JSON syntax" "false" "true"
    exit 1
fi

echo ""
echo "3. Checking chapters array exists..."
HAS_CHAPTERS=$(jq 'has("chapters")' "$OUTPUT")
run_test "Has chapters key" "$HAS_CHAPTERS" "true"

echo ""
echo "4. Counting chapters..."
CHAPTER_COUNT=$(jq '.chapters | length' "$OUTPUT")
EXPECTED=$(jq '.expected_chapters' "$MANIFEST" 2>/dev/null || echo "13")
echo "   Found: $CHAPTER_COUNT chapters (expected: $EXPECTED)"

DIFF=$((CHAPTER_COUNT - EXPECTED))
DIFF=${DIFF#-}  # Absolute value
if [[ "$DIFF" -le 2 ]]; then
    run_test "Chapter count within tolerance (±2)" "true" "true"
else
    run_test "Chapter count within tolerance (±2)" "off by $DIFF" "within 2"
fi

echo ""
echo "5. Validating chapter structure..."
ALL_HAVE_TITLE=$(jq '[.chapters[] | has("title")] | all' "$OUTPUT")
ALL_HAVE_CONTENT=$(jq '[.chapters[] | has("content")] | all' "$OUTPUT")
run_test "All chapters have title" "$ALL_HAVE_TITLE" "true"
run_test "All chapters have content" "$ALL_HAVE_CONTENT" "true"

echo ""
echo "6. Checking content length..."
MIN_CONTENT=$(jq '[.chapters[] | .content | length] | min' "$OUTPUT")
AVG_CONTENT=$(jq '[.chapters[] | .content | length] | add / length | floor' "$OUTPUT")
echo "   Min content: $MIN_CONTENT chars"
echo "   Average content: $AVG_CONTENT chars"

if [[ "$MIN_CONTENT" -gt 100 ]]; then
    run_test "Min content > 100 chars" "true" "true"
else
    run_test "Min content > 100 chars" "$MIN_CONTENT" ">100"
fi

echo ""
echo "7. Checking chapter numbering..."
CHAPTER_NUMBERS=$(jq '[.chapters[].number] | sort | unique' "$OUTPUT")
FIRST_CHAPTER=$(jq '.chapters[0].number' "$OUTPUT")
LAST_CHAPTER=$(jq '.chapters[-1].number' "$OUTPUT")
echo "   Chapter range: $FIRST_CHAPTER to $LAST_CHAPTER"

if [[ "$FIRST_CHAPTER" -eq 1 ]]; then
    run_test "First chapter is 1" "true" "true"
else
    run_test "First chapter is 1" "$FIRST_CHAPTER" "1"
fi

echo ""
echo "8. Checking page ranges..."
FIRST_PAGE=$(jq '.chapters[0].start_page' "$OUTPUT")
LAST_PAGE=$(jq '.chapters[-1].end_page' "$OUTPUT")
echo "   Page range: $FIRST_PAGE to $LAST_PAGE"

HAS_OVERLAPS=$(jq '
    [.chapters | sort_by(.start_page)] | 
    . as $chapters | 
    [range(1; length)] | 
    map($chapters[.].start_page <= $chapters[.-1].end_page) | 
    any
' "$OUTPUT")
if [[ "$HAS_OVERLAPS" = "false" ]]; then
    run_test "No overlapping page ranges" "true" "true"
else
    run_test "No overlapping page ranges" "overlap found" "no overlap"
fi

echo ""
echo "9. Listing chapter titles..."
jq -r '.chapters[] | "   Ch \(.number): \(.title)"' "$OUTPUT"

echo ""
echo "=== Summary ==="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [[ "$TESTS_FAILED" -eq 0 ]]; then
    echo ""
    echo "=== WBS 1.2.1 PASSED ==="
    exit 0
else
    echo ""
    echo "=== WBS 1.2.1 FAILED ==="
    exit 1
fi
