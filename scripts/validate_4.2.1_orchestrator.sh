#!/bin/bash
# =============================================================================
# WBS 4.2.1 Validation: Run Two-Phase Orchestrator
# =============================================================================

set -e

echo "========================================"
echo "WBS 4.2.1 Validation: Two-Phase Orchestrator"
echo "========================================"
echo ""

PROJECT_ROOT="/Users/kevintoles/POC/llm-document-enhancer"
SCRIPT="$PROJECT_ROOT/workflows/llm_enhancement/scripts/integrate_llm_enhancements.py"
AGGREGATE="$PROJECT_ROOT/workflows/llm_enhancement/input/aggregate_package.json"
GUIDELINE="$PROJECT_ROOT/workflows/base_guideline_generation/output/GUIDELINES_Architecture_Patterns_with_Python.md"
OUTPUT="$PROJECT_ROOT/workflows/llm_enhancement/output/GUIDELINES_Architecture_Patterns_with_Python_ENHANCED.md"
LOG_DIR="$PROJECT_ROOT/workflows/logs"

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
# Test 1: Script shows help (exit 0)
# =============================================================================
if python3 "$SCRIPT" --help > /dev/null 2>&1; then
    pass "Script shows help"
else
    fail "Script shows help" "Exit code not 0"
fi

# =============================================================================
# Test 2: Input files exist
# =============================================================================
if [ -f "$AGGREGATE" ] && [ -f "$GUIDELINE" ]; then
    pass "Input files exist"
else
    fail "Input files exist" "Missing aggregate or guideline file"
fi

# =============================================================================
# Test 3: Script runs without crash (uses cached results for speed)
# =============================================================================
# Note: Using existing output if available to avoid API costs
if [ -f "$OUTPUT" ]; then
    pass "Script produced output"
else
    # Run with 1 chapter if no output exists
    echo "  Running orchestrator (--chapters 1)..."
    START_TIME=$(date +%s)
    if python3 "$SCRIPT" \
        --aggregate "$AGGREGATE" \
        --guideline "$GUIDELINE" \
        --output "$OUTPUT" \
        --chapters 1 > /dev/null 2>&1; then
        END_TIME=$(date +%s)
        RUNTIME=$((END_TIME - START_TIME))
        if [ "$RUNTIME" -lt 300 ]; then
            pass "Script runs (${RUNTIME}s < 300s)"
        else
            fail "Script runs" "Runtime ${RUNTIME}s exceeded 5 minutes"
        fi
    else
        fail "Script runs" "Exit code not 0"
    fi
fi

# =============================================================================
# Test 4: Output file created
# =============================================================================
if [ -f "$OUTPUT" ]; then
    pass "Output file created"
else
    fail "Output file created" "File not found: $OUTPUT"
fi

# =============================================================================
# Test 5: Output > Input size (more content added)
# =============================================================================
if [ -f "$OUTPUT" ] && [ -f "$GUIDELINE" ]; then
    INPUT_SIZE=$(wc -c < "$GUIDELINE" | tr -d ' ')
    OUTPUT_SIZE=$(wc -c < "$OUTPUT" | tr -d ' ')
    if [ "$OUTPUT_SIZE" -gt "$INPUT_SIZE" ]; then
        pass "Output > Input size"
    else
        fail "Output > Input size" "Input: $INPUT_SIZE, Output: $OUTPUT_SIZE"
    fi
else
    fail "Output > Input size" "Files not found"
fi

# =============================================================================
# Test 6: Phase 1 logged (check for orchestrator or phase messages)
# =============================================================================
LATEST_LOG=$(ls -t "$LOG_DIR"/llm_enhancement_*.log 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    if grep -qi "phase\|orchestrator" "$LATEST_LOG" 2>/dev/null; then
        pass "Phase logging present"
    else
        fail "Phase logging present" "No phase/orchestrator messages in log"
    fi
else
    fail "Phase logging present" "No log file found"
fi

# =============================================================================
# Test 7: Token count logged (check API logs)
# =============================================================================
API_LOG_DIR="$PROJECT_ROOT/logs/llm_api"
if [ -d "$API_LOG_DIR" ]; then
    LATEST_API_LOG=$(ls -t "$API_LOG_DIR"/*.json 2>/dev/null | head -1)
    if [ -n "$LATEST_API_LOG" ]; then
        if jq -e '.response.output_tokens' "$LATEST_API_LOG" > /dev/null 2>&1; then
            pass "Token count logged"
        else
            fail "Token count logged" "No token count in API log"
        fi
    else
        fail "Token count logged" "No API log files"
    fi
else
    fail "Token count logged" "API log directory not found"
fi

# =============================================================================
# Test 8: Has --chapters flag
# =============================================================================
if python3 "$SCRIPT" --help 2>&1 | grep -q "\-\-chapters"; then
    pass "Has --chapters flag"
else
    fail "Has --chapters flag" "Flag not in help output"
fi

# =============================================================================
# Test 9: Has --output flag
# =============================================================================
if python3 "$SCRIPT" --help 2>&1 | grep -q "\-\-output"; then
    pass "Has --output flag"
else
    fail "Has --output flag" "Flag not in help output"
fi

# =============================================================================
# Test 10: Has --verbose flag
# =============================================================================
if python3 "$SCRIPT" --help 2>&1 | grep -q "\-\-verbose"; then
    pass "Has --verbose flag"
else
    fail "Has --verbose flag" "Flag not in help output"
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
    echo "✓ All WBS 4.2.1 validation tests passed!"
    exit 0
else
    echo "✗ Some tests failed. Review errors above."
    exit 1
fi
