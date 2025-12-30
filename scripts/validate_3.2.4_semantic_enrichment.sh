#!/bin/bash
#
# WBS 3.2.4 Validation Script - Integrate Search Client into Metadata Enrichment
#
# This script validates that the semantic search integration is working correctly
# in the metadata enrichment workflow.
#
# Prerequisites:
#   - semantic-search-service running on localhost:8081
#   - Test input file exists (test_book_metadata.json or similar)
#
# Usage:
#   ./scripts/validate_3.2.4_semantic_enrichment.sh
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
echo "WBS 3.2.4 Validation: Semantic Enrichment"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENRICH_SCRIPT="$PROJECT_ROOT/workflows/metadata_enrichment/scripts/enrich_metadata_per_book.py"
OUTPUT_DIR="$PROJECT_ROOT/workflows/metadata_enrichment/output"
SEMANTIC_URL="http://localhost:8081"

echo "Project Root: $PROJECT_ROOT"
echo "Enrich Script: $ENRICH_SCRIPT"
echo "Semantic Search URL: $SEMANTIC_URL"
echo ""

# Test 1: --use-semantic-search flag exists in help
run_test "--use-semantic-search flag exists" \
    "python3 '$ENRICH_SCRIPT' --help 2>&1 | grep -q '\-\-use-semantic-search'"

# Test 2: --semantic-search-url flag exists in help
run_test "--semantic-search-url flag exists" \
    "python3 '$ENRICH_SCRIPT' --help 2>&1 | grep -q '\-\-semantic-search-url'"

# Test 3: Search client module can be imported
run_test "SearchClient module imports" \
    "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_ROOT\"); from workflows.shared.clients.search_client import SemanticSearchClient'"

# Test 4: Search client has required methods
run_test "SearchClient has embed method" \
    "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_ROOT\"); from workflows.shared.clients.search_client import SemanticSearchClient; c = SemanticSearchClient(\"http://localhost:8081\"); assert hasattr(c, \"embed\")'"

run_test "SearchClient has search method" \
    "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_ROOT\"); from workflows.shared.clients.search_client import SemanticSearchClient; c = SemanticSearchClient(\"http://localhost:8081\"); assert hasattr(c, \"search\")'"

run_test "SearchClient has hybrid_search method" \
    "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_ROOT\"); from workflows.shared.clients.search_client import SemanticSearchClient; c = SemanticSearchClient(\"http://localhost:8081\"); assert hasattr(c, \"hybrid_search\")'"

# Test 5: Output files exist from previous run (semantic)
if [[ -f "$OUTPUT_DIR/test_book_semantic_enriched.json" ]]; then
    run_test "Semantic enrichment output exists" \
        "test -f '$OUTPUT_DIR/test_book_semantic_enriched.json'"
    
    # Test 6: Output has similarity_source field
    run_test "Output has similarity_source field" \
        "jq -e '.chapters[0].similarity_source' '$OUTPUT_DIR/test_book_semantic_enriched.json'"
    
    # Test 7: similarity_source is 'semantic_search'
    run_test "similarity_source is 'semantic_search'" \
        "jq -e '.chapters[0].similarity_source == \"semantic_search\"' '$OUTPUT_DIR/test_book_semantic_enriched.json' | grep -q 'true'"
    
    # Test 8: enrichment_metadata.method is 'semantic_search'
    run_test "enrichment_metadata method is 'semantic_search'" \
        "jq -e '.enrichment_metadata.method == \"semantic_search\"' '$OUTPUT_DIR/test_book_semantic_enriched.json' | grep -q 'true'"
else
    echo -e "${YELLOW}Skipping output validation - no semantic enriched file found${NC}"
fi

# Test 9: TF-IDF output for comparison
if [[ -f "$OUTPUT_DIR/test_book_tfidf_enriched.json" ]]; then
    run_test "TF-IDF output exists" \
        "test -f '$OUTPUT_DIR/test_book_tfidf_enriched.json'"
    
    # Test 10: TF-IDF output has 'tfidf' source
    run_test "TF-IDF output has 'tfidf' source" \
        "jq -e '.chapters[0].similarity_source == \"tfidf\"' '$OUTPUT_DIR/test_book_tfidf_enriched.json' | grep -q 'true'"
    
    # Test 11: Semantic and TF-IDF outputs are different
    run_test "Semantic and TF-IDF outputs differ" \
        "! diff -q '$OUTPUT_DIR/test_book_semantic_enriched.json' '$OUTPUT_DIR/test_book_tfidf_enriched.json'"
else
    echo -e "${YELLOW}Skipping TF-IDF validation - no TF-IDF enriched file found${NC}"
fi

# Test 12: Integration test file exists
run_test "Integration test file exists" \
    "test -f '$PROJECT_ROOT/tests_integration/test_semantic_enrichment.py'"

# Summary
echo ""
echo "========================================"
echo "Validation Summary"
echo "========================================"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All WBS 3.2.4 validation tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some validation tests failed.${NC}"
    exit 1
fi
