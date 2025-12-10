#!/bin/bash
# WBS 3.1.1 Validation: YAKE Keyword Extraction
# Tests StatisticalExtractor and metadata generation

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

echo "=== WBS 3.1.1 Validation: YAKE Keyword Extraction ==="
echo ""

cd /Users/kevintoles/POC/llm-document-enhancer

# Test 1: StatisticalExtractor importable
echo "1. Testing StatisticalExtractor import..."
IMPORT_RESULT=$(python3 -c "from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor; print('OK')" 2>&1)
if echo "$IMPORT_RESULT" | grep -q "OK"; then
    pass "StatisticalExtractor importable"
else
    fail "StatisticalExtractor import failed"
fi

# Test 2: Extracts keywords (>= 5)
echo "2. Testing keyword extraction..."
KW_COUNT=$(python3 -c "
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
extractor = StatisticalExtractor()
sample = '''
Machine learning pipelines require careful data preprocessing.
Feature engineering transforms raw data into meaningful representations.
Model training involves optimizing parameters through gradient descent.
Evaluation metrics like accuracy and F1 score measure model performance.
'''
result = extractor.extract_keywords(sample, top_n=10)
print(len(result))
" 2>/dev/null)
if [ "$KW_COUNT" -ge 5 ]; then
    pass "Extracts keywords (Found: $KW_COUNT)"
else
    fail "Too few keywords extracted (Found: $KW_COUNT, Expected: >= 5)"
fi

# Test 3: Keywords are strings
echo "3. Testing keywords are strings..."
if python3 -c "
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
extractor = StatisticalExtractor()
result = extractor.extract_keywords('Test text with keywords and concepts', top_n=5)
# Result is list of (keyword, score) tuples
for kw, score in result:
    assert isinstance(kw, str), f'Keyword {kw} is not a string'
print('OK')
" 2>/dev/null | grep -q "OK"; then
    pass "Keywords are strings"
else
    fail "Keywords are not strings"
fi

# Test 4: Extracts concepts
echo "4. Testing concept extraction..."
CONCEPT_COUNT=$(python3 -c "
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
extractor = StatisticalExtractor()
sample = '''
Machine learning pipelines require careful data preprocessing.
Feature engineering transforms raw data into meaningful representations.
Model training involves optimizing parameters through gradient descent.
'''
result = extractor.extract_concepts(sample, top_n=10)
print(len(result))
" 2>/dev/null)
if [ "$CONCEPT_COUNT" -ge 3 ]; then
    pass "Extracts concepts (Found: $CONCEPT_COUNT)"
else
    fail "Too few concepts extracted (Found: $CONCEPT_COUNT, Expected: >= 3)"
fi

# Test 5: Output JSON exists
echo "5. Checking output file exists..."
OUTPUT="workflows/metadata_extraction/output/test_book_metadata.json"
if [ -f "$OUTPUT" ]; then
    pass "Output file exists: test_book_metadata.json"
else
    fail "Output file missing (run extraction first)"
fi

# Test 6: Valid JSON
echo "6. Validating JSON syntax..."
if python3 -c "import json; json.load(open('$OUTPUT'))" 2>/dev/null; then
    pass "Valid JSON"
else
    fail "Invalid JSON"
fi

# Test 7: Each chapter has keywords
echo "7. Checking all chapters have keywords..."
CHAPTERS_WITH_KW=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
count = sum(1 for ch in data if len(ch.get('keywords', [])) > 0)
print(count)
" 2>/dev/null)
TOTAL_CHAPTERS=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
print(len(data))
" 2>/dev/null)
if [ "$CHAPTERS_WITH_KW" -eq "$TOTAL_CHAPTERS" ]; then
    pass "All chapters have keywords ($CHAPTERS_WITH_KW/$TOTAL_CHAPTERS)"
else
    fail "Not all chapters have keywords ($CHAPTERS_WITH_KW/$TOTAL_CHAPTERS)"
fi

# Test 8: Each chapter has concepts
echo "8. Checking all chapters have concepts..."
CHAPTERS_WITH_CONCEPTS=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
count = sum(1 for ch in data if len(ch.get('concepts', [])) > 0)
print(count)
" 2>/dev/null)
if [ "$CHAPTERS_WITH_CONCEPTS" -eq "$TOTAL_CHAPTERS" ]; then
    pass "All chapters have concepts ($CHAPTERS_WITH_CONCEPTS/$TOTAL_CHAPTERS)"
else
    fail "Not all chapters have concepts ($CHAPTERS_WITH_CONCEPTS/$TOTAL_CHAPTERS)"
fi

# Test 9: Each chapter has summary
echo "9. Checking all chapters have summaries..."
CHAPTERS_WITH_SUMMARY=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
count = sum(1 for ch in data if len(ch.get('summary', '')) > 0)
print(count)
" 2>/dev/null)
if [ "$CHAPTERS_WITH_SUMMARY" -eq "$TOTAL_CHAPTERS" ]; then
    pass "All chapters have summaries ($CHAPTERS_WITH_SUMMARY/$TOTAL_CHAPTERS)"
else
    fail "Not all chapters have summaries ($CHAPTERS_WITH_SUMMARY/$TOTAL_CHAPTERS)"
fi

# Summary
echo ""
echo "=== Summary ==="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo "=== WBS 3.1.1 PASSED ==="
    exit 0
else
    echo ""
    echo "=== WBS 3.1.1 FAILED ==="
    exit 1
fi
