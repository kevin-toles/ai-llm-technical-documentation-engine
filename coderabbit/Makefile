# CodeRabbit Manual Analysis Makefile - LLM Document Enhancer
.PHONY: help install-tools coderabbit-quick coderabbit-full coderabbit-security coderabbit-setup clean-reports

# Default target
help:
	@echo "CodeRabbit Manual Analysis Commands (LLM Document Enhancer):"
	@echo "  make install-tools        - Install all required analysis tools"
	@echo "  make coderabbit-setup     - Set up CodeRabbit configuration and tools"
	@echo "  make coderabbit-quick     - Run quick CodeRabbit analysis (manual)"
	@echo "  make coderabbit-full      - Run comprehensive CodeRabbit analysis (manual)"
	@echo "  make coderabbit-security  - Run security-focused analysis (manual)"
	@echo "  make coderabbit-manual    - Run manual analysis via script"
	@echo "  make coderabbit-workflows - Scan workflows/ directory only"
	@echo "  make clean-reports        - Clean analysis reports"
	@echo ""
	@echo "🎯 Manual Trigger Design: CodeRabbit runs only when explicitly requested"
	@echo "🔧 Use: ./scripts/run_coderabbit_analysis.sh [quick|full|security]"

# Install analysis tools
install-tools:
	@echo "🔧 Installing CodeRabbit analysis tools..."
	pip3 install --upgrade pip
	pip3 install bandit flake8 mypy radon ruff safety pydocstyle
	pip3 install pre-commit
	@echo "✅ Tools installed successfully"

# Set up CodeRabbit
coderabbit-setup: install-tools
	@echo "🚀 Setting up CodeRabbit manual analysis..."
	mkdir -p reports/coderabbit
	chmod +x scripts/run_coderabbit_analysis.sh
	@echo "✅ CodeRabbit manual setup complete"
	@echo "🔧 Use: ./scripts/run_coderabbit_analysis.sh or make commands"

# Manual analysis via script
coderabbit-manual:
	@echo "🎯 Running manual CodeRabbit analysis via script..."
	bash scripts/run_coderabbit_analysis.sh full

# Quick analysis (essential checks only)
coderabbit-quick:
	@echo "⚡ Running quick CodeRabbit analysis (manual trigger)..."
	bash scripts/run_coderabbit_analysis.sh quick

# Full comprehensive analysis
coderabbit-full:
	@echo "🔍 Running comprehensive CodeRabbit analysis (manual trigger)..."
	bash scripts/run_coderabbit_analysis.sh full

# Security-focused analysis
coderabbit-security:
	@echo "🔒 Running security-focused analysis (manual trigger)..."
	bash scripts/run_coderabbit_analysis.sh security

# PR-ready analysis (what would run in CI)
coderabbit-pr: clean-reports
	@echo "🔍 Running PR-ready CodeRabbit analysis..."
	mkdir -p reports/coderabbit
	python scripts/local_coderabbit.py --path .. --format both
	@echo ""
	@echo "📋 PR Analysis Summary:"
	@if [ -f "reports/coderabbit/analysis_results.json" ]; then \
		python -c "import json; data=json.load(open('reports/coderabbit/analysis_results.json')); print(f\"🚨 Critical: {data['summary']['by_severity'].get('critical', 0)}\"); print(f\"🔴 High: {data['summary']['by_severity'].get('high', 0)}\"); print(f\"🟡 Medium: {data['summary']['by_severity'].get('medium', 0)}\"); print(f\"📊 Total: {data['summary']['total_issues']}\")"; \
	fi
	@echo "✅ PR analysis complete"

# Run pre-commit hooks
coderabbit-precommit:
	@echo "🔧 Running pre-commit CodeRabbit checks..."
	pre-commit run --all-files

# Directed scans for specific directories
coderabbit-workflows:
	@echo "🔍 Running CodeRabbit analysis on workflows/ directory..."
	python scripts/local_coderabbit.py --path ../workflows --format both
	@echo "✅ Workflows analysis complete"
	@echo "📋 Check reports/coderabbit/ for results"

# Clean reports
clean-reports:
	@echo "🧹 Cleaning analysis reports..."
	rm -rf reports/coderabbit/*
	@echo "✅ Reports cleaned"

# Integration with SonarQube
coderabbit-with-sonar: coderabbit-full
	@echo "🔗 Running CodeRabbit + SonarQube analysis..."
	@echo "⚠️  SonarQube integration requires separate configuration"

# Watch mode for development
coderabbit-watch:
	@echo "👁️  Starting CodeRabbit watch mode..."
	@echo "🔄 Run 'make coderabbit-quick' in another terminal to analyze changes"
	@while true; do \
		inotifywait -r -e modify,create,delete --include='.*\.py$$' .. 2>/dev/null && \
		echo "📝 Python files changed - run 'make coderabbit-quick' to analyze"; \
	done

# Generate project health report
coderabbit-health: coderabbit-full
	@echo "🏥 Generating project health report..."
	@if [ -f "reports/coderabbit/analysis_results.json" ]; then \
		python3 -c 'import json; data=json.load(open("reports/coderabbit/analysis_results.json")); total=data["summary"]["total_issues"]; critical=data["summary"]["by_severity"].get("critical", 0); high=data["summary"]["by_severity"].get("high", 0); medium=data["summary"]["by_severity"].get("medium", 0); score=max(0, 100-(critical*10)-(high*3)-medium); print(f"📊 Health Score: {score}/100"); print(f"Total: {total}, Critical: {critical}, High: {high}, Medium: {medium}")'; \
	else \
		echo "⚠️  No analysis results found - run coderabbit-full first"; \
	fi