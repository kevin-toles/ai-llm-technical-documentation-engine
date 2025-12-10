#!/bin/bash
# =============================================================================
# WBS 4.3.1 Validation: Measure and Compare Token Usage
# =============================================================================

set -e

echo "========================================"
echo "WBS 4.3.1 Validation: Token Usage Analysis"
echo "========================================"
echo ""

PROJECT_ROOT="/Users/kevintoles/POC/llm-document-enhancer"
API_LOG_DIR="$PROJECT_ROOT/logs/llm_api"

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
# Extract token counts from most recent API logs
# =============================================================================
echo "Extracting token counts from API logs..."
echo ""

# Find the 5 most recent API call logs (from the Chapter 1 run)
LATEST_LOGS=$(ls -t "$API_LOG_DIR"/*.json 2>/dev/null | head -5)

if [ -z "$LATEST_LOGS" ]; then
    echo "ERROR: No API logs found in $API_LOG_DIR"
    exit 1
fi

# Calculate totals
TOTAL_INPUT=0
TOTAL_OUTPUT=0
PHASE1_TOKENS=0
PHASE2_TOKENS=0

for log in $LATEST_LOGS; do
    INPUT=$(jq -r '.response.input_tokens // 0' "$log" 2>/dev/null)
    OUTPUT=$(jq -r '.response.output_tokens // 0' "$log" 2>/dev/null)
    TOTAL=$((INPUT + OUTPUT))
    
    # Identify phase by call number or content
    CALL_NUM=$(jq -r '.call_number // 0' "$log" 2>/dev/null)
    
    # Phase 1 calls typically have higher input (full chapter text)
    # Phase 2 calls have targeted content
    if [ "$INPUT" -gt 2500 ]; then
        PHASE1_TOKENS=$((PHASE1_TOKENS + TOTAL))
    else
        PHASE2_TOKENS=$((PHASE2_TOKENS + TOTAL))
    fi
    
    TOTAL_INPUT=$((TOTAL_INPUT + INPUT))
    TOTAL_OUTPUT=$((TOTAL_OUTPUT + OUTPUT))
done

TOTAL_TOKENS=$((TOTAL_INPUT + TOTAL_OUTPUT))

echo "=== Token Usage Summary ==="
echo "Phase 1 (metadata analysis): ~$PHASE1_TOKENS tokens"
echo "Phase 2 (targeted content):  ~$PHASE2_TOKENS tokens"
echo "Total tokens used:           $TOTAL_TOKENS tokens"
echo ""

# =============================================================================
# Test 1: Phase 1 tokens < 15,000
# =============================================================================
if [ "$PHASE1_TOKENS" -lt 15000 ]; then
    pass "Phase 1 < 15,000 ($PHASE1_TOKENS)"
else
    fail "Phase 1 < 15,000" "Actual: $PHASE1_TOKENS"
fi

# =============================================================================
# Test 2: Phase 2 tokens < 60,000
# =============================================================================
if [ "$PHASE2_TOKENS" -lt 60000 ]; then
    pass "Phase 2 < 60,000 ($PHASE2_TOKENS)"
else
    fail "Phase 2 < 60,000" "Actual: $PHASE2_TOKENS"
fi

# =============================================================================
# Test 3: Total tokens < 75,000 per chapter
# =============================================================================
if [ "$TOTAL_TOKENS" -lt 75000 ]; then
    pass "Total < 75,000 ($TOTAL_TOKENS)"
else
    fail "Total < 75,000" "Actual: $TOTAL_TOKENS"
fi

# =============================================================================
# Test 4: > 50% reduction vs comprehensive approach
# =============================================================================
# Comprehensive approach estimate: 150,000 tokens (full chapter + all companion context)
COMPREHENSIVE_ESTIMATE=150000
SAVINGS=$(( (COMPREHENSIVE_ESTIMATE - TOTAL_TOKENS) * 100 / COMPREHENSIVE_ESTIMATE ))

echo ""
echo "=== Savings Analysis ==="
echo "Comprehensive approach (theoretical): ~$COMPREHENSIVE_ESTIMATE tokens"
echo "Two-phase approach (actual):          $TOTAL_TOKENS tokens"
echo "Reduction:                            ${SAVINGS}%"
echo ""

if [ "$SAVINGS" -gt 50 ]; then
    pass ">50% reduction (${SAVINGS}%)"
else
    fail ">50% reduction" "Only ${SAVINGS}% savings"
fi

# =============================================================================
# Test 5: API logs exist and have token data
# =============================================================================
LOG_COUNT=$(ls "$API_LOG_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$LOG_COUNT" -gt 0 ]; then
    pass "API logs exist ($LOG_COUNT files)"
else
    fail "API logs exist" "No log files found"
fi

# =============================================================================
# Test 6: Token counts are reasonable (not zero, not astronomical)
# =============================================================================
if [ "$TOTAL_TOKENS" -gt 100 ] && [ "$TOTAL_TOKENS" -lt 1000000 ]; then
    pass "Token counts reasonable"
else
    fail "Token counts reasonable" "Total: $TOTAL_TOKENS"
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
    echo "✓ All WBS 4.3.1 validation tests passed!"
    echo ""
    echo "Token Efficiency Summary:"
    echo "  - Phase 1: $PHASE1_TOKENS tokens (target < 15,000)"
    echo "  - Phase 2: $PHASE2_TOKENS tokens (target < 60,000)"
    echo "  - Total:   $TOTAL_TOKENS tokens (target < 75,000)"
    echo "  - Savings: ${SAVINGS}% vs comprehensive approach"
    exit 0
else
    echo "✗ Some tests failed. Review errors above."
    exit 1
fi
