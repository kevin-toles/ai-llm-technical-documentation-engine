#!/bin/bash
#
# WBS 4.1.1 Validation Script - Create Aggregate Package
#
# This script validates that the aggregate package creation is working correctly.
#
# Usage:
#   ./scripts/validate_4.1.1_aggregate_package.sh
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    printf "%-50s" "Testing: $test_name..."
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

echo "========================================"
echo "WBS 4.1.1 Validation: Create Aggregate Package"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CREATE_SCRIPT="$PROJECT_ROOT/workflows/llm_enhancement/scripts/create_aggregate_package.py"
ENRICHED_FILE="$PROJECT_ROOT/workflows/metadata_enrichment/output/test_book_enriched.json"
OUTPUT_FILE="$PROJECT_ROOT/workflows/llm_enhancement/input/aggregate_package.json"

echo "Project Root: $PROJECT_ROOT"
echo "Create Script: $CREATE_SCRIPT"
echo "Enriched File: $ENRICHED_FILE"
echo "Output File: $OUTPUT_FILE"
echo ""

# Test 1: Script exists
run_test "Script exists" "test -f '$CREATE_SCRIPT'"

# Test 2: Enriched input exists
run_test "Enriched metadata exists" "test -f '$ENRICHED_FILE'"

# Test 3: Script runs without error
run_test "Script runs (exit 0)" \
    "python3 '$CREATE_SCRIPT' --enriched '$ENRICHED_FILE' --output '$OUTPUT_FILE'"

# Test 4: Output created
run_test "Output file created" "test -f '$OUTPUT_FILE'"

# Test 5: Valid JSON
run_test "Valid JSON" \
    "python3 -c \"import json; json.load(open('$OUTPUT_FILE'))\""

# Test 6: Has source_book
run_test "Has source_book key" \
    "jq -e 'has(\"source_book\")' '$OUTPUT_FILE'"

# Test 7: Has chapters
run_test "Has chapters array" \
    "jq -e '.source_book.chapters' '$OUTPUT_FILE'"

# Test 8: Has at least 1 chapter
run_test "Has ≥ 1 chapter" \
    "test \$(jq '.source_book.chapters | length' '$OUTPUT_FILE') -ge 1"

# Test 9: First chapter has keywords (enriched metadata)
run_test "Has enriched metadata (keywords)" \
    "jq -e '.source_book.chapters[0] | has(\"keywords\")' '$OUTPUT_FILE' | grep -q true"

# Test 10: Has similar_chapters (from enrichment)
run_test "Has similar_chapters" \
    "jq -e '.source_book.chapters[0] | has(\"similar_chapters\")' '$OUTPUT_FILE' | grep -q true"

# Test 11: Has package_info
run_test "Has package_info" \
    "jq -e 'has(\"package_info\")' '$OUTPUT_FILE'"

# Test 12: Has statistics
run_test "Has statistics" \
    "jq -e 'has(\"statistics\")' '$OUTPUT_FILE'"

# Summary
echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All WBS 4.1.1 validation tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some validation tests failed.${NC}"
    exit 1
fi
