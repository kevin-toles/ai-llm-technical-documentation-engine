#!/bin/bash
# =============================================================================
# WBS 4.1.2 Validation: Configure LLM Gateway Connection
# =============================================================================

set -e

echo "========================================"
echo "WBS 4.1.2 Validation: LLM Gateway Connection"
echo "========================================"
echo ""

PROJECT_ROOT="/Users/kevintoles/POC/llm-document-enhancer"
GATEWAY_URL="http://localhost:8080"

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
# Test 1: Gateway healthy (HTTP 200, status "healthy")
# =============================================================================
HEALTH_STATUS=$(curl -s "$GATEWAY_URL/health" | jq -r '.status' 2>/dev/null || echo "")
if [ "$HEALTH_STATUS" = "healthy" ]; then
    pass "Gateway healthy"
else
    fail "Gateway healthy" "Expected 'healthy', got '$HEALTH_STATUS'"
fi

# =============================================================================
# Test 2: Client importable
# =============================================================================
IMPORT_RESULT=$(python3 -c "from workflows.shared.clients.llm_gateway import LLMGatewayClient; print('OK')" 2>&1)
if [ "$IMPORT_RESULT" = "OK" ]; then
    pass "Client importable"
else
    fail "Client importable" "Import error: $IMPORT_RESULT"
fi

# =============================================================================
# Test 3: GatewayClient class exists with required methods
# =============================================================================
METHODS_RESULT=$(python3 -c "
from workflows.shared.clients.llm_gateway import LLMGatewayClient
client = LLMGatewayClient()
assert hasattr(client, 'chat_completion'), 'Missing chat_completion'
assert hasattr(client, 'health_check'), 'Missing health_check'
print('OK')
" 2>&1)
if [ "$METHODS_RESULT" = "OK" ]; then
    pass "Client has required methods"
else
    fail "Client has required methods" "$METHODS_RESULT"
fi

# =============================================================================
# Test 4: API key is set
# =============================================================================
if [ -n "$OPENAI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ]; then
    pass "API key set"
else
    fail "API key set" "Neither OPENAI_API_KEY nor ANTHROPIC_API_KEY is set"
fi

# =============================================================================
# Test 5: Health check via client
# =============================================================================
HEALTH_RESULT=$(python3 -c "
import asyncio
from workflows.shared.clients.llm_gateway import LLMGatewayClient

async def check():
    async with LLMGatewayClient() as client:
        healthy = await client.health_check()
        print('OK' if healthy else 'FAIL')

asyncio.run(check())
" 2>&1)
if [ "$HEALTH_RESULT" = "OK" ]; then
    pass "Health check via client"
else
    fail "Health check via client" "$HEALTH_RESULT"
fi

# =============================================================================
# Test 6: Simple completion returns response
# =============================================================================
COMPLETION_RESULT=$(python3 -c "
import asyncio
from workflows.shared.clients.llm_gateway import LLMGatewayClient

async def test():
    async with LLMGatewayClient() as client:
        response = await client.chat_completion(
            model='claude-sonnet-4-5-20250929',
            messages=[{'role': 'user', 'content': 'Say hello'}],
            max_tokens=20
        )
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        print('OK' if len(content) > 0 else 'FAIL')

asyncio.run(test())
" 2>&1)
if [ "$COMPLETION_RESULT" = "OK" ]; then
    pass "Simple completion"
else
    fail "Simple completion" "$COMPLETION_RESULT"
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
    echo "✓ All WBS 4.1.2 validation tests passed!"
    exit 0
else
    echo "✗ Some tests failed. Review errors above."
    exit 1
fi
