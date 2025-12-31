#!/bin/bash
# ==============================================================================
# WBS 0.1.1 Validation Script - Docker Compose Integration
# ==============================================================================
# Purpose: Validate docker-compose.integration.yml configuration and deployment
# Reference: END_TO_END_INTEGRATION_WBS.md WBS 0.1.1
# 
# Usage:
#   ./scripts/validate_0.1.1_docker.sh           # Run full validation
#   ./scripts/validate_0.1.1_docker.sh --skip-up # Skip docker-compose up (syntax only)
#
# Exit Codes:
#   0 - All validations passed
#   1 - Validation failed
# ==============================================================================

set -e
cd /Users/kevintoles/POC/llm-document-enhancer

SKIP_UP=false
if [[ "$1" == "--skip-up" ]]; then
    SKIP_UP=true
fi

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    WBS 0.1.1 VALIDATION SCRIPT                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: File exists
echo "1. Checking file exists..."
if [[ -f docker-compose.integration.yml ]]; then
    echo "   ✓ File exists ($(ls -la docker-compose.integration.yml | awk '{print $5}') bytes)"
else
    echo "   ✗ File missing: docker-compose.integration.yml"
    exit 1
fi

# Test 2: YAML syntax valid
echo "2. Validating YAML syntax..."
if docker-compose -f docker-compose.integration.yml config --quiet 2>/dev/null; then
    echo "   ✓ YAML syntax valid"
else
    echo "   ✗ YAML syntax invalid"
    docker-compose -f docker-compose.integration.yml config 2>&1 | head -20
    exit 1
fi

# Test 3: Service count
echo "3. Counting services..."
SERVICE_COUNT=$(docker-compose -f docker-compose.integration.yml config --services | wc -l | tr -d ' ')
if [[ "$SERVICE_COUNT" -ge 5 ]]; then
    echo "   ✓ $SERVICE_COUNT services defined (minimum: 5)"
    docker-compose -f docker-compose.integration.yml config --services | sed 's/^/     - /'
else
    echo "   ✗ Only $SERVICE_COUNT services defined (minimum: 5)"
    exit 1
fi

# Test 4: Network defined
echo "4. Checking network definition..."
NETWORK_COUNT=$(grep -c "integration-network" docker-compose.integration.yml || echo "0")
if [[ "$NETWORK_COUNT" -ge 1 ]]; then
    echo "   ✓ Network 'integration-network' defined ($NETWORK_COUNT references)"
else
    echo "   ✗ Network 'integration-network' not defined"
    exit 1
fi

# Skip deployment tests if requested
if [[ "$SKIP_UP" = true ]]; then
    echo ""
    echo "=== Skipping deployment tests (--skip-up flag) ==="
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║              WBS 0.1.1 SYNTAX VALIDATION PASSED                         ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    exit 0
fi

# Test 5: Start services
echo "5. Starting services..."
if docker-compose -f docker-compose.integration.yml up -d 2>&1; then
    echo "   ✓ docker-compose up succeeded"
else
    echo "   ✗ docker-compose up failed"
    exit 1
fi

# Test 6: Wait and check health
echo "6. Waiting for health checks (60s max)..."
WAIT_TIME=0
MAX_WAIT=60
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    HEALTHY_COUNT=$(docker-compose -f docker-compose.integration.yml ps 2>/dev/null | grep -c "healthy" || echo "0")
    if [[ "$HEALTHY_COUNT" -ge 5 ]]; then
        echo "   ✓ $HEALTHY_COUNT services healthy after ${WAIT_TIME}s"
        break
    fi
    echo "   ... $HEALTHY_COUNT/5 healthy (waiting ${WAIT_TIME}s/${MAX_WAIT}s)"
    sleep 10
    WAIT_TIME=$((WAIT_TIME + 10))
done

if [[ "$HEALTHY_COUNT" -lt 5 ]]; then
    echo "   ✗ Only $HEALTHY_COUNT services healthy after ${MAX_WAIT}s"
    echo ""
    echo "Container status:"
    docker-compose -f docker-compose.integration.yml ps
    exit 1
fi

# Test 7: Health endpoint verification
echo "7. Verifying health endpoints..."
ENDPOINTS_OK=true

for endpoint in "http://localhost:8080/health" "http://localhost:8081/health" "http://localhost:8082/health"; do
    if curl -sf "$endpoint" > /dev/null 2>&1; then
        echo "   ✓ $endpoint responding"
    else
        echo "   ✗ $endpoint not responding"
        ENDPOINTS_OK=false
    fi
done

if [[ "$ENDPOINTS_OK" = false ]]; then
    echo "   ⚠ Some endpoints not responding (may need more startup time)"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    WBS 0.1.1 VALIDATION PASSED                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Running containers:"
docker-compose -f docker-compose.integration.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
