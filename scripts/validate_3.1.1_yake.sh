#!/bin/bash
# WBS 3.1.1 Validation: YAKE Keyword Extraction
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

echo "=== WBS 3.1.1 Validation: YAKE Keyword Extraction ==="
echo ""

cd /Users/kevintoles/POC/llm-document-enhancer
OUTPUT="workflows/metadata_extraction/output/test_book_metadata.json"

# Test 1: Extractor importable (Acceptance Criteria Row 1)
echo "1. Extractor importable..."
IMPORT_RESULT=$(python3 -c "from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor; print('OK')" 2>&1)
if echo "$IMPORT_RESULT" | grep -q "OK"; then
    pass "Extractor importable"
else
    fail "Extractor import failed"
fi

# Test 2: Extracts keywords >= 5 (Acceptance Criteria Row 2)
echo "2. Extracts keywords (len >= 5)..."
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
" 2>&1)
if [ "$KW_COUNT" -ge 5 ]; then
    pass "Extracts keywords (Found: $KW_COUNT >= 5)"
else
    fail "Too few keywords (Found: $KW_COUNT, Expected: >= 5)"
fi

# Test 3: Keywords are strings (Acceptance Criteria Row 3)
echo "3. Keywords are strings..."
STRINGS_TEST=$(python3 -c "
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
extractor = StatisticalExtractor()
result = extractor.extract_keywords('Test text with keywords and concepts for extraction', top_n=5)
all_strings = all(isinstance(kw, str) for kw, score in result)
print('OK' if all_strings else 'FAIL')
" 2>&1)
if echo "$STRINGS_TEST" | grep -q "OK"; then
    pass "Keywords are strings"
else
    fail "Keywords are not all strings"
fi

# Test 4: No Python-specific hardcoding (Acceptance Criteria Row 4)
# This checks that keywords don't contain actual source code syntax
# Note: "def test" is a legitimate keyword for a Python testing book
echo "4. No Python-specific hardcoding in keywords..."
HARDCODE_COUNT=$(python3 -c "
import json
import re
with open('$OUTPUT') as f:
    data = json.load(f)
# Check keywords for actual code patterns (not legitimate phrases)
# Patterns like 'def func():', 'class Name:', 'import x', 'lambda x:'
code_patterns = [
    r'def \w+\(',          # Function definitions
    r'class \w+[:(]',      # Class definitions  
    r'^import \w+',        # Import statements
    r'lambda \w*:',        # Lambda expressions
    r'^\s*#',              # Comments
]
count = 0
for ch in data.get('chapters', data):
    for kw in ch.get('keywords', []):
        for pattern in code_patterns:
            if re.search(pattern, kw):
                count += 1
print(count)
" 2>&1)
if [ "$HARDCODE_COUNT" = "0" ]; then
    pass "No Python-specific hardcoding in keywords"
else
    fail "Found $HARDCODE_COUNT keywords with code patterns"
fi

# Test 5: Output JSON created (Acceptance Criteria Row 5)
echo "5. Output JSON created..."
if test -f "$OUTPUT"; then
    pass "Output file exists: test_book_metadata.json"
else
    fail "Output file missing"
fi

# Test 6: Each chapter has keywords (Acceptance Criteria Row 6)
echo "6. Each chapter has keywords..."
ALL_HAVE_KW=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
chapters = data.get('chapters', data)
result = all(len(ch.get('keywords', [])) > 0 for ch in chapters)
print('true' if result else 'false')
" 2>&1)
if [ "$ALL_HAVE_KW" = "true" ]; then
    pass "All chapters have keywords"
else
    fail "Not all chapters have keywords"
fi

# Additional tests for completeness

# Test 7: Valid JSON structure
echo "7. Valid JSON structure..."
if python3 -c "import json; json.load(open('$OUTPUT'))" 2>/dev/null; then
    pass "Valid JSON"
else
    fail "Invalid JSON"
fi

# Test 8: Each chapter has concepts
echo "8. Each chapter has concepts..."
ALL_HAVE_CONCEPTS=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
chapters = data.get('chapters', data)
result = all(len(ch.get('concepts', [])) > 0 for ch in chapters)
print('true' if result else 'false')
" 2>&1)
if [ "$ALL_HAVE_CONCEPTS" = "true" ]; then
    pass "All chapters have concepts"
else
    fail "Not all chapters have concepts"
fi

# Test 9: Each chapter has summary
echo "9. Each chapter has summary..."
ALL_HAVE_SUMMARY=$(python3 -c "
import json
with open('$OUTPUT') as f:
    data = json.load(f)
chapters = data.get('chapters', data)
result = all(len(ch.get('summary', '')) > 0 for ch in chapters)
print('true' if result else 'false')
" 2>&1)
if [ "$ALL_HAVE_SUMMARY" = "true" ]; then
    pass "All chapters have summaries"
else
    fail "Not all chapters have summaries"
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
