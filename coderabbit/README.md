# CodeRabbit Local Analysis Setup

This directory contains CodeRabbit local analysis tools for comprehensive code quality, security, and complexity analysis.

## Quick Start

### 1. Install Analysis Tools

```bash
cd coderabbit
make install-tools
```

This installs:
- **bandit** - Security vulnerability scanner
- **radon** - Complexity and maintainability metrics
- **mypy** - Static type checker
- **ruff** - Fast Python linter
- **flake8** - Style guide enforcement
- **pydocstyle** - Docstring conventions

### 2. Run Analysis

#### Quick Analysis (Fast, Essential Checks)
```bash
cd coderabbit
make coderabbit-quick
```

#### Full Analysis (Comprehensive)
```bash
cd coderabbit
make coderabbit-full
```

#### Security-Focused Analysis
```bash
cd coderabbit
make coderabbit-security
```

### 3. View Results

Results are saved to `reports/coderabbit/`:
- `analysis_results.json` - Structured results
- `analysis_report.md` - Human-readable report
- `CodeRabbit_Audit_YYYYMMDD.md` - Comprehensive audit

## Manual Script Execution

You can also run the analysis script directly:

```bash
cd coderabbit
./scripts/run_coderabbit_analysis.sh quick   # Quick analysis
./scripts/run_coderabbit_analysis.sh full    # Full analysis
./scripts/run_coderabbit_analysis.sh security # Security only
```

Or use Python directly:

```bash
cd coderabbit
python scripts/local_coderabbit.py --path .. --format both
```

## Generate Audit Report

After running analysis, generate a comprehensive audit:

```bash
cd coderabbit
python scripts/coderabbit_audit_generator.py
```

This creates `reports/coderabbit/CodeRabbit_Audit_YYYYMMDD.md` with:
- Issues by component (src/phases/, src/, tests/, etc.)
- Issues by type (security, complexity, quality)
- Issues by severity (critical, high, medium, low)
- Issues by tool (bandit, radon, mypy, ruff, flake8)

## Configuration

Edit `.coderabbit.yaml` to customize:
- File patterns to include/exclude
- Complexity thresholds
- Security rules
- Code quality standards
- Architecture validation rules

## Integration with SonarQube

CodeRabbit analysis complements SonarQube:
- **CodeRabbit**: Fast local analysis, multiple specialized tools
- **SonarQube**: Centralized quality gates, historical trends

Both tools help maintain code quality through different approaches.

## Architecture-Specific Rules

This setup includes custom rules for llm-document-enhancer:
- ✅ Phase separation validation (Phase 1 vs Phase 2)
- ✅ Repository pattern adherence
- ✅ Domain model integrity checks
- ✅ Configuration management validation
- ✅ Dependency injection verification

## Directory Structure

```
coderabbit/
├── README.md                    # This file
├── .coderabbit.yaml            # Configuration
├── Makefile                    # Build commands
├── scripts/
│   ├── local_coderabbit.py            # Main analysis script
│   ├── run_coderabbit_analysis.sh     # Shell wrapper
│   └── coderabbit_audit_generator.py  # Report generator
└── reports/
    └── coderabbit/             # Analysis results (git-ignored)
        ├── analysis_results.json
        ├── analysis_report.md
        └── CodeRabbit_Audit_*.md
```

## Troubleshooting

### Tools Not Installed
```bash
cd coderabbit
make install-tools
```

### Permission Denied on Scripts
```bash
chmod +x coderabbit/scripts/run_coderabbit_analysis.sh
```

### Missing Reports Directory
```bash
mkdir -p coderabbit/reports/coderabbit
```

## Clean Reports

To remove old analysis reports:

```bash
cd coderabbit
make clean-reports
```

## Running from Root Directory

You can also run from the project root:

```bash
# Install tools
make -C coderabbit install-tools

# Run analysis
make -C coderabbit coderabbit-full

# Or use the full path
make -f coderabbit/Makefile coderabbit-full
```
