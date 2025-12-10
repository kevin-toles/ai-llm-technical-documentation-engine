#!/bin/bash
# WBS 3.1.2 Validation: TF-IDF Similarity (Local Mode)
# Tests per acceptance criteria table in END_TO_END_INTEGRATION_WBS.md

TESTS_PASSED=0
TESTS_FAILED=0

pass() {
    echo "✓ $1"
    ((TESTS_PASSED++))
}

fail() {
    echo "✗ $1"
    ((TESTS_FAILED++))
}

echo "=== WBS 3.1.2 Validation: TF-IDF Similarity ==="
echo ""

cd /Users/kevintoles/POC/llm-document-enhancer
INPUT="workflows/metadata_extraction/output/test_book_metadata.json"
OUTPUT="workflows/metadata_enrichment/output/test_book_enriched.json"

# Test 1: Script runs (Acceptance Criteria Row 1)
echo "1. Script runs without errors..."
SCRIPT_OUTPUT=$(python3 workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py \
  --input "$INPUT" \
  --output "$OUTPUT" 2>&1)
SCRIPT_EXIT=$?
if [ $SCRIPT_EXIT -eq 0 ]; then
    pass "Script runs (exit code: $SCRIPT_EXIT)"
else
    fail "Script crashed (exit code: $SCRIPT_EXIT)"
    echo "Output: $SCRIPT_OUTPUT"
fi

# Test 2: Output created (Acceptance Criteria Row 2)
echo "2. Output file created..."
if test -f "$OUTPUT"; then
    pass "Output file exists: test_book_enriched.json"
else
    fail "Output file missing"
fi

# Test 3: Has similarity scores (Acceptance Criteria Row 3)
echo "3. Has tfidf_similar field..."
HAS_TFIDF=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
has_field = 'tfidf_similar' in data['chapters'][0]
print('true' if has_field else 'false')
" 2>&1)
if [ "$HAS_TFIDF" = "true" ]; then
    pass "Has tfidf_similar field"
else
    fail "Missing tfidf_similar field"
fi

# Test 4: Scores in range [0, 1] (Acceptance Criteria Row 4)
echo "4. Scores in valid range [0, 1]..."
SCORES_VALID=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
all_valid = True
for ch in data['chapters']:
    for sim in ch.get('tfidf_similar', []):
        score = sim.get('score', 0)
        if not (0 <= score <= 1):
            all_valid = False
            break
print('true' if all_valid else 'false')
" 2>&1)
if [ "$SCORES_VALID" = "true" ]; then
    pass "All scores in [0, 1]"
else
    fail "Some scores outside [0, 1]"
fi

# Test 5: Top-5 populated (Acceptance Criteria Row 5)
echo "5. Top-5 similar chapters (at most 5)..."
TOP5_COUNT=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
count = len(data['chapters'][0].get('tfidf_similar', []))
print(count)
" 2>&1)
if [ "$TOP5_COUNT" -le 5 ]; then
    pass "Top-5 populated (count: $TOP5_COUNT <= 5)"
else
    fail "Too many similar chapters (count: $TOP5_COUNT > 5)"
fi

# Test 6: Self not in similar (Acceptance Criteria Row 6)
echo "6. No self-reference in similar chapters..."
NO_SELF=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
no_self_ref = True
for ch in data['chapters']:
    ch_id = ch.get('chapter_number')
    for sim in ch.get('tfidf_similar', []):
        if sim.get('chapter_id') == ch_id:
            no_self_ref = False
            break
print('true' if no_self_ref else 'false')
" 2>&1)
if [ "$NO_SELF" = "true" ]; then
    pass "No self-references"
else
    fail "Self-reference found in similar chapters"
fi

# Test 7: Valid JSON structure
echo "7. Valid JSON structure..."
if python3 -c "import json; json.load(open('$OUTPUT'))" 2>/dev/null; then
    pass "Valid JSON"
else
    fail "Invalid JSON"
fi

# Test 8: All chapters have tfidf_similar
echo "8. All chapters have similarity data..."
ALL_HAVE_SIMILAR=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
all_have = all('tfidf_similar' in ch for ch in data['chapters'])
print('true' if all_have else 'false')
" 2>&1)
if [ "$ALL_HAVE_SIMILAR" = "true" ]; then
    pass "All chapters have tfidf_similar"
else
    fail "Some chapters missing tfidf_similar"
fi

# Summary
echo ""
echo "=== Summary ==="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

# Show sample output
echo ""
echo "=== Sample Output ==="
python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
for i, ch in enumerate(data['chapters'][:3]):
    print(f\"Chapter {ch.get('chapter_number')}: {ch.get('title')}\")
    for sim in ch.get('tfidf_similar', [])[:2]:
        print(f\"  -> Ch {sim['chapter_id']}: {sim['title']} (score: {sim['score']})\")
"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo "=== WBS 3.1.2 PASSED ==="
    exit 0
else
    echo ""
    echo "=== WBS 3.1.2 FAILED ==="
    exit 1
fi
