#!/usr/bin/env python3
"""
Tab 4 Metadata Enrichment Validation Script

Validates that metadata enrichment (Tab 4) produces correct output structure.

Validates:
1. Enriched metadata JSON structure (book, enrichment_metadata, chapters)
2. Enrichment metadata fields (method, libraries, corpus_size, etc.)
3. Statistical method compliance (no LLM, required libraries)
4. Chapter enrichment fields (related_chapters, keywords_enriched, concepts_enriched)
5. Similarity score validity (0.0-1.0 range)

Usage:
    python scripts/validate_metadata_enrichment.py --enriched path/to/enriched.json
    python scripts/validate_metadata_enrichment.py  # Auto-find enriched files

References:
    - MASTER_IMPLEMENTATION_GUIDE Task 2.2
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

from scripts.metadata_enrichment_validation_services import EnrichmentValidationOrchestrator


def find_enriched_file() -> Optional[Path]:
    """
    Auto-find enriched metadata JSON file in output directory.
    
    Returns:
        Path to enriched file, or None if not found
    """
    output_dir = Path("workflows/metadata_enrichment/output")
    
    if not output_dir.exists():
        return None
    
    # Look for *_metadata_enriched.json files
    enriched_files = list(output_dir.glob("*_metadata_enriched.json"))
    
    if not enriched_files:
        return None
    
    # Return first file found
    return enriched_files[0]


def validate_enriched_metadata(enriched_path: Path) -> int:
    """
    Validate enriched metadata file.
    
    Args:
        enriched_path: Path to enriched metadata JSON file
        
    Returns:
        Exit code: 0 for success, 1 for failure
    """
    print(f"Validating: {enriched_path}")
    print(f"File size: {enriched_path.stat().st_size / 1024:.1f} KB")
    
    # Load enriched metadata
    try:
        with open(enriched_path, encoding='utf-8') as f:
            enriched_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n❌ Invalid JSON: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error loading file: {e}")
        return 1
    
    # Run validation orchestrator
    orchestrator = EnrichmentValidationOrchestrator(enriched_data)
    success = orchestrator.validate_all()
    
    return 0 if success else 1


def main():
    """
    Command-line interface for enriched metadata validation.
    
    Example:
        python scripts/validate_metadata_enrichment.py
        python scripts/validate_metadata_enrichment.py --enriched path/to/file.json
    """
    parser = argparse.ArgumentParser(
        description="Validate Tab 4 enriched metadata output"
    )
    parser.add_argument(
        "--enriched",
        type=Path,
        help="Path to enriched metadata JSON file"
    )
    
    args = parser.parse_args()
    
    # Determine enriched file path
    if args.enriched:
        enriched_path = args.enriched
        if not enriched_path.exists():
            print(f"❌ Error: File not found: {enriched_path}")
            sys.exit(1)
    else:
        # Auto-find enriched file
        found_path = find_enriched_file()
        if found_path is None:
            print("❌ Error: No enriched metadata files found")
            print("   Expected location: workflows/metadata_enrichment/output/*_metadata_enriched.json")
            sys.exit(1)
        enriched_path = found_path
        print(f"Auto-detected: {enriched_path.name}")
    
    # Run validation
    exit_code = validate_enriched_metadata(enriched_path)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
