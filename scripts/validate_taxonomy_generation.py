#!/usr/bin/env python3
"""
Tab 3 Taxonomy Validation Script

Validates that taxonomy generation (Tab 3) produces correct output structure.

Validates:
1. Taxonomy JSON structure (required 'tiers' key, tier structure)
2. Tier categorization (3 tiers: architecture, implementation, practices)
3. Priority ordering (architecture=1, implementation=2, practices=3)
4. Concept deduplication (no duplicates within same tier)

Usage:
    python scripts/validate_taxonomy_generation.py --taxonomy path/to/taxonomy.json
    python scripts/validate_taxonomy_generation.py  # Auto-find taxonomy in output dir

References:
    - MASTER_IMPLEMENTATION_GUIDE Task 2.1
    - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
    - PYTHON_GUIDELINES Ch.8: Classes and OOP
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.taxonomy_validation_services import TaxonomyValidationOrchestrator


def find_taxonomy_file() -> Optional[Path]:
    """
    Auto-find taxonomy JSON file in output directory.
    
    Returns:
        Path to taxonomy file, or None if not found
    """
    output_dir = Path("workflows/taxonomy_setup/output")
    
    if not output_dir.exists():
        return None
    
    # Look for *_taxonomy.json files
    taxonomy_files = list(output_dir.glob("*_taxonomy.json"))
    
    if not taxonomy_files:
        return None
    
    # Return most recent file
    return max(taxonomy_files, key=lambda p: p.stat().st_mtime)


def validate_taxonomy(taxonomy_path: Path) -> bool:
    """
    Validate taxonomy JSON file.
    
    Args:
        taxonomy_path: Path to taxonomy JSON file
        
    Returns:
        True if validation passed, False otherwise
    """
    print(f"\n📁 Loading taxonomy: {taxonomy_path}")
    
    # Load taxonomy JSON
    try:
        with open(taxonomy_path, 'r', encoding='utf-8') as f:
            taxonomy = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Taxonomy file not found: {taxonomy_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading taxonomy: {e}")
        return False
    
    # Run validation
    orchestrator = TaxonomyValidationOrchestrator(taxonomy)
    return orchestrator.validate_all()


def main() -> int:
    """
    Main entry point for taxonomy validation.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description='Validate Tab 3 taxonomy generation output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate specific taxonomy file
  python scripts/validate_taxonomy_generation.py --taxonomy workflows/taxonomy_setup/output/python_taxonomy.json
  
  # Auto-find and validate most recent taxonomy
  python scripts/validate_taxonomy_generation.py
        """
    )
    parser.add_argument(
        '--taxonomy',
        type=str,
        help='Path to taxonomy JSON file (auto-detects if not provided)'
    )
    
    args = parser.parse_args()
    
    # Determine taxonomy file
    if args.taxonomy:
        taxonomy_path = Path(args.taxonomy)
    else:
        print("🔍 Auto-detecting taxonomy file...")
        found_path = find_taxonomy_file()
        
        if found_path is None:
            print("❌ Error: No taxonomy files found in workflows/taxonomy_setup/output/")
            print("   Run generate_concept_taxonomy.py first to create taxonomy.")
            return 1
        
        taxonomy_path = found_path
        print(f"✓ Found: {taxonomy_path}")
    
    # Validate
    success = validate_taxonomy(taxonomy_path)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
