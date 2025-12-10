#!/bin/bash
# ==============================================================================
# WBS 0.1.2 Validation Script - Environment Configuration
# ==============================================================================
# Purpose: Validate .env.integration file configuration
# Reference: END_TO_END_INTEGRATION_WBS.md WBS 0.1.2
#
# Usage:
#   ./scripts/validate_0.1.2_env.sh
#
# Exit Codes:
#   0 - All validations passed
#   1 - Validation failed
# ==============================================================================

set -e
cd /Users/kevintoles/POC/llm-document-enhancer

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    WBS 0.1.2 VALIDATION SCRIPT                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "1. Checking .env.integration exists..."
test -f .env.integration && echo "   ✓ File exists" || (echo "   ✗ Missing" && exit 1)

echo "2. Checking required variables..."
for VAR in "SEMANTIC_SEARCH_URL=http://localhost:8081" \
           "GATEWAY_URL=http://localhost:8080" \
           "QDRANT_URL=http://localhost:6333" \
           "NEO4J_URI=bolt://localhost:7687"; do
    grep -q "^$VAR" .env.integration && echo "   ✓ Found $VAR" || (echo "   ✗ Missing $VAR" && exit 1)
done

echo "3. Checking for API key..."
grep -qE "^(OPENAI_API_KEY|ANTHROPIC_API_KEY)=.{10,}" .env.integration && echo "   ✓ API key present" || (echo "   ✗ No API key" && exit 1)

echo "4. Testing source..."
source .env.integration
[ "$SEMANTIC_SEARCH_URL" = "http://localhost:8081" ] && echo "   ✓ Variables load correctly" || exit 1

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    WBS 0.1.2 VALIDATION PASSED                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
