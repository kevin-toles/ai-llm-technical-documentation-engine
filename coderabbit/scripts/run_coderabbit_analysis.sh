#!/bin/bash
# Manual CodeRabbit Analysis Script
# Usage: ./scripts/run_coderabbit_analysis.sh [quick|full|security|audit]
# Two-Tier Analysis: quick (filtered) vs audit (comprehensive)

set -e

ANALYSIS_TYPE=${1:-full}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "🤖 Starting Manual CodeRabbit Analysis"
echo "📅 Timestamp: $TIMESTAMP"
echo "🔍 Analysis Type: $ANALYSIS_TYPE"
echo "📁 Working Directory: $(pwd)"

# Check for emergency disable flag
if [ "$DISABLE_FILTERING" = "true" ]; then
    echo "🚨 EMERGENCY MODE: All filtering disabled"
    ANALYSIS_TYPE="audit-emergency"
fi

echo "==========================================="

# Ensure we're in the coderabbit directory or parent
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CODERABBIT_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$CODERABBIT_DIR")"

echo "📂 Script location: $SCRIPT_DIR"
echo "📂 CodeRabbit directory: $CODERABBIT_DIR"
echo "� Project root: $PROJECT_ROOT"

# Check if required tools are installed
echo "🔧 Checking dependencies..."
python3 -c "import bandit, radon, mypy" 2>/dev/null || {
    echo "⚠️  Installing missing dependencies..."
    pip install bandit flake8 mypy radon ruff safety pydocstyle
}

# Create reports directory
mkdir -p "$CODERABBIT_DIR/reports/coderabbit"
mkdir -p "$CODERABBIT_DIR/reports/filtering"

# Define exclusion patterns based on analysis type
case "$ANALYSIS_TYPE" in
    "quick")
        echo "⚡ Running Quick Analysis (Tier 1: Daily Developer)"
        echo "📋 Applied Filters: Safe directories + venv + verified false positives"
        EXCLUSIONS="__pycache__,.git,venv,env,.venv,.pytest_cache,.mypy_cache,docker_volumes,cache_storage,logs,backups,build,dist,reports"
        python3 "$SCRIPT_DIR/local_coderabbit.py" --path "$PROJECT_ROOT" --format both
        ;;
    "security")
        echo "🔒 Running Security-Only Analysis (Filtered)"
        echo "📋 Applied Filters: Safe directories only"
        EXCLUSIONS="__pycache__,.git,.pytest_cache,.mypy_cache,docker_volumes,cache_storage,logs,backups,build,dist,reports"
        cd "$PROJECT_ROOT"
        bandit -r . -f json -o "$CODERABBIT_DIR/reports/coderabbit/security_manual_$TIMESTAMP.json" \
            --exclude $EXCLUSIONS \
            --quiet || true
        echo "✅ Security analysis complete"
        echo "📄 Report: $CODERABBIT_DIR/reports/coderabbit/security_manual_$TIMESTAMP.json"
        ;;
    "audit"|"audit-emergency")
        echo "🔒 Running Comprehensive Security Audit (Tier 2: Weekly)"
        echo "📋 Applied Filters: Ultra-safe directories ONLY"
        if [ "$ANALYSIS_TYPE" = "audit-emergency" ]; then
            echo "🚨 EMERGENCY: NO FILTERING APPLIED"
            EXCLUSIONS=""
        else
            EXCLUSIONS="__pycache__,.git,.pytest_cache,.mypy_cache,docker_volumes,cache_storage,logs,backups,build,dist,reports"
        fi
        python3 "$SCRIPT_DIR/local_coderabbit.py" --path "$PROJECT_ROOT" --format both
        echo "⚠️  Manual review required for dependency warnings"
        ;;
    "full"|*)
        echo "🔍 Running Comprehensive Analysis (Tier 1: Filtered)"
        echo "📋 Applied Filters: Safe directories + venv + verified false positives" 
        EXCLUSIONS="__pycache__,.git,venv,env,.venv,.pytest_cache,.mypy_cache,docker_volumes,cache_storage,logs,backups,build,dist,reports"
        python3 "$SCRIPT_DIR/local_coderabbit.py" --path "$PROJECT_ROOT" --format both
        
        # Generate audit report
        if [ -f "$SCRIPT_DIR/coderabbit_audit_generator.py" ]; then
            echo "📋 Generating comprehensive audit report..."
            python3 "$SCRIPT_DIR/coderabbit_audit_generator.py"
        fi
        ;;
esac

# Show results summary
echo "==========================================="
echo "📊 Analysis Complete!"

if [ -f "$CODERABBIT_DIR/reports/coderabbit/analysis_results.json" ]; then
    echo "📋 Results Summary:"
    python3 -c "
import json
import os
results_file = '$CODERABBIT_DIR/reports/coderabbit/analysis_results.json'
if os.path.exists(results_file):
    with open(results_file) as f:
        data = json.load(f)
    print(f'🚨 Critical: {data[\"summary\"][\"by_severity\"].get(\"critical\", 0)}')
    print(f'🔴 High: {data[\"summary\"][\"by_severity\"].get(\"high\", 0)}')
    print(f'🟡 Medium: {data[\"summary\"][\"by_severity\"].get(\"medium\", 0)}')
    print(f'🔵 Low: {data[\"summary\"][\"by_severity\"].get(\"low\", 0)}')
    print(f'📊 Total: {data[\"summary\"][\"total_issues\"]}')
else:
    print('No detailed results available')
"
fi

echo ""
echo "📂 Reports Location: $CODERABBIT_DIR/reports/coderabbit/"
echo "📄 Available Reports:"
ls -la "$CODERABBIT_DIR/reports/coderabbit/" 2>/dev/null | grep -E '\.(md|json)$' | while read -r line; do
    echo "   $line"
done

echo ""
echo "🔗 Next Steps:"
echo "   • Review reports in coderabbit/reports/coderabbit/"
echo "   • Run 'cd coderabbit && make coderabbit-health' for health score"
echo "   • Use GitHub Actions for team-wide analysis"
echo ""
echo "📊 Analysis Types Available:"
echo "   • quick     - Tier 1: Daily developer analysis (filtered)"
echo "   • full      - Tier 1: Comprehensive analysis (filtered)" 
echo "   • audit     - Tier 2: Weekly security audit (minimal filtering)"
echo "   • security  - Security-only scan (filtered)"
echo ""
echo "🚨 Emergency: DISABLE_FILTERING=true bash coderabbit/scripts/run_coderabbit_analysis.sh audit"
echo ""
echo "✅ Manual CodeRabbit analysis complete!"