#!/bin/bash
# =============================================================================
# WBS 4.2.2 Validation: Verify Enhancement Quality
# =============================================================================

set -e

echo "========================================"
echo "WBS 4.2.2 Validation: Enhancement Quality"
echo "========================================"
echo ""

PROJECT_ROOT="/Users/kevintoles/POC/llm-document-enhancer"
ENHANCED="$PROJECT_ROOT/workflows/llm_enhancement/output/GUIDELINES_Architecture_Patterns_with_Python_ENHANCED.md"
ORIGINAL="$PROJECT_ROOT/workflows/base_guideline_generation/output/GUIDELINES_Architecture_Patterns_with_Python.md"

cd "$PROJECT_ROOT"

PASSED=0
FAILED=0

pass() {
    echo -e "Testing: $1...\t\t\t  \033[32mPASS\033[0m"
    PASSED=$((PASSED + 1))
}

fail() {
    echo -e "Testing: $1...\t\t\t  \033[31mFAIL\033[0m"
    echo "  Error: $2"
    FAILED=$((FAILED + 1))
}

# =============================================================================
# Test 1: Enhanced file exists
# =============================================================================
if [ -f "$ENHANCED" ]; then
    pass "Enhanced file exists"
else
    fail "Enhanced file exists" "File not found: $ENHANCED"
    echo "Cannot continue without enhanced file"
    exit 1
fi

# =============================================================================
# Test 2: Has Cross-References section (≥ 1)
# =============================================================================
CROSS_REF_COUNT=$(grep -ci "cross-reference\|see also\|related" "$ENHANCED" 2>/dev/null || echo 0)
if [ "$CROSS_REF_COUNT" -ge 1 ]; then
    pass "Has Cross-References ($CROSS_REF_COUNT)"
else
    fail "Has Cross-References" "Count: $CROSS_REF_COUNT (expected ≥ 1)"
fi

# =============================================================================
# Test 3: Has Synthesis/Annotations (≥ 1)
# =============================================================================
SYNTHESIS_COUNT=$(grep -ci "synthesis\|annotation\|scholarly\|analysis" "$ENHANCED" 2>/dev/null || echo 0)
if [ "$SYNTHESIS_COUNT" -ge 1 ]; then
    pass "Has Synthesis/Annotations ($SYNTHESIS_COUNT)"
else
    fail "Has Synthesis/Annotations" "Count: $SYNTHESIS_COUNT (expected ≥ 1)"
fi

# =============================================================================
# Test 4: Original content preserved (chapters not removed)
# =============================================================================
ORIG_CHAPTERS=$(grep -c "^## Chapter" "$ORIGINAL" 2>/dev/null || echo 0)
ENHANCED_CHAPTERS=$(grep -c "^## Chapter" "$ENHANCED" 2>/dev/null || echo 0)
if [ "$ENHANCED_CHAPTERS" -ge "$ORIG_CHAPTERS" ]; then
    pass "Original chapters preserved ($ENHANCED_CHAPTERS ≥ $ORIG_CHAPTERS)"
else
    fail "Original chapters preserved" "Enhanced: $ENHANCED_CHAPTERS, Original: $ORIG_CHAPTERS"
fi

# =============================================================================
# Test 5: Footnotes intact (enhanced ≥ original)
# =============================================================================
ORIG_FOOTNOTES=$(grep -oE '\[\^[0-9]+\]' "$ORIGINAL" 2>/dev/null | wc -l | tr -d ' ')
ENHANCED_FOOTNOTES=$(grep -oE '\[\^[0-9]+\]' "$ENHANCED" 2>/dev/null | wc -l | tr -d ' ')
if [ "$ENHANCED_FOOTNOTES" -ge "$ORIG_FOOTNOTES" ]; then
    pass "Footnotes intact ($ENHANCED_FOOTNOTES ≥ $ORIG_FOOTNOTES)"
else
    fail "Footnotes intact" "Enhanced: $ENHANCED_FOOTNOTES, Original: $ORIG_FOOTNOTES"
fi

# =============================================================================
# Test 6: File size increased (content added)
# =============================================================================
ORIG_SIZE=$(wc -c < "$ORIGINAL" | tr -d ' ')
ENHANCED_SIZE=$(wc -c < "$ENHANCED" | tr -d ' ')
if [ "$ENHANCED_SIZE" -gt "$ORIG_SIZE" ]; then
    DIFF=$((ENHANCED_SIZE - ORIG_SIZE))
    pass "Content added (+$DIFF bytes)"
else
    fail "Content added" "Enhanced: $ENHANCED_SIZE, Original: $ORIG_SIZE"
fi

# =============================================================================
# Test 7: No hallucinated book titles (check known patterns)
# Note: This is a basic check - full validation requires citation verification
# =============================================================================
# Check for suspicious patterns like "ISBN:" followed by obviously fake numbers
SUSPICIOUS=$(grep -ci "ISBN: 000\|made-up\|fictional\|hypothetical book" "$ENHANCED" 2>/dev/null | head -1 || echo 0)
SUSPICIOUS=${SUSPICIOUS:-0}
if [ "$SUSPICIOUS" -eq 0 ]; then
    pass "No obvious hallucinations"
else
    fail "No obvious hallucinations" "Found $SUSPICIOUS suspicious patterns"
fi

# =============================================================================
# Test 8: Has chapter summaries (not stripped)
# =============================================================================
SUMMARY_COUNT=$(grep -ci "chapter summary\|### summary" "$ENHANCED" 2>/dev/null || echo 0)
if [ "$SUMMARY_COUNT" -ge 1 ]; then
    pass "Has chapter summaries ($SUMMARY_COUNT)"
else
    fail "Has chapter summaries" "Count: $SUMMARY_COUNT (expected ≥ 1)"
fi

# =============================================================================
# Test 9: Has markdown structure (headers)
# =============================================================================
HEADER_COUNT=$(grep -c "^#" "$ENHANCED" 2>/dev/null || echo 0)
if [ "$HEADER_COUNT" -ge 10 ]; then
    pass "Has markdown structure ($HEADER_COUNT headers)"
else
    fail "Has markdown structure" "Only $HEADER_COUNT headers found"
fi

# =============================================================================
# Test 10: Content is readable (not corrupted - has common words)
# =============================================================================
WORD_COUNT=$(grep -ci "the\|and\|python\|chapter" "$ENHANCED" 2>/dev/null || echo 0)
if [ "$WORD_COUNT" -ge 100 ]; then
    pass "Content readable (has common words)"
else
    fail "Content readable" "Only $WORD_COUNT common words found"
fi

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✓ All WBS 4.2.2 validation tests passed!"
    exit 0
else
    echo "✗ Some tests failed. Review errors above."
    exit 1
fi
