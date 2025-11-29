#!/usr/bin/env python3
"""
Tab 5 Implementation Validation Script
Validates that all CONSOLIDATED_IMPLEMENTATION_PLAN.md Tab 5 requirements are met.

Refactored using Service Layer Pattern and Strategy Pattern.
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.tab5_validation_services import Tab5ValidationOrchestrator


def validate_tab5_implementation(md_file: str = None, json_file: str = None):
    """
    Validate Tab 5 implementation (refactored: CC 34 → 1).
    
    Delegates to Tab5ValidationOrchestrator service layer.
    
    Args:
        md_file: Optional path to MD file (default: workflow output)
        json_file: Optional path to JSON file (default: workflow output)
    """
    from pathlib import Path
    md_path = Path(md_file) if md_file else None
    json_path = Path(json_file) if json_file else None
    orchestrator = Tab5ValidationOrchestrator(md_path, json_path)
    return orchestrator.validate_all()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Validate Tab 5 implementation')
    parser.add_argument('--md', help='Path to MD file', default=None)
    parser.add_argument('--json', help='Path to JSON file', default=None)
    args = parser.parse_args()
    
    success = validate_tab5_implementation(args.md, args.json)
    sys.exit(0 if success else 1)
