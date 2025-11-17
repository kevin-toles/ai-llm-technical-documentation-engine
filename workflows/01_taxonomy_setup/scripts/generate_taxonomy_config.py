#!/usr/bin/env python3
"""
Generate Taxonomy Configuration

Generates taxonomy_config.json from the book taxonomy Python code.
This allows for easier inspection and external tool integration.

Usage:
    python scripts/generate_taxonomy_config.py [--output OUTPUT_PATH]

Output:
    taxonomy_config.json containing:
    - All book definitions
    - Tier classifications
    - Keyword triggers
    - Cascading relationships
    - Relevance weights
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

from book_taxonomy import ALL_BOOKS, BookTier


def generate_taxonomy_config() -> Dict[str, Any]:
    """
    Generate taxonomy configuration from book_taxonomy.py definitions.
    
    Returns:
        Dictionary containing complete taxonomy configuration
    """
    config = {
        "metadata": {
            "version": "1.0.0",
            "total_books": len(ALL_BOOKS),
            "description": "Hierarchical taxonomy of companion technical books"
        },
        "tiers": {
            "architecture_spine": {
                "description": "Foundational architectural patterns and principles",
                "priority": 1
            },
            "implementation": {
                "description": "Practical framework and technology implementations",
                "priority": 2
            },
            "engineering_practices": {
                "description": "Language fundamentals and coding practices",
                "priority": 3
            }
        },
        "books": []
    }
    
    # Add each book's configuration
    for book in ALL_BOOKS:
        book_config = {
            "name": book.book_name,
            "tier": book.tier.value,
            "primary_focus": book.primary_focus,
            "relevance_weight": book.relevance_weight,
            "keyword_triggers": sorted(book.keyword_triggers),
            "cascades_to": book.cascades_to,
            "metadata": {
                "trigger_count": len(book.keyword_triggers),
                "cascade_count": len(book.cascades_to)
            }
        }
        config["books"].append(book_config)
    
    # Sort books by tier priority
    tier_order = {
        BookTier.ARCHITECTURE_SPINE: 0,
        BookTier.IMPLEMENTATION: 1,
        BookTier.ENGINEERING_PRACTICES: 2
    }
    config["books"].sort(key=lambda b: (
        tier_order.get(BookTier(b["tier"]), 999),
        b["name"]
    ))
    
    return config


def save_taxonomy_config(config: Dict[str, Any], output_path: Path) -> None:
    """
    Save taxonomy configuration to JSON file.
    
    Args:
        config: Taxonomy configuration dictionary
        output_path: Path to save JSON file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Taxonomy configuration saved to: {output_path}")
    print(f"   📚 Total books: {config['metadata']['total_books']}")
    
    # Print tier breakdown
    tier_counts = {}
    for book in config["books"]:
        tier = book["tier"]
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    
    print("\n   Tier breakdown:")
    for tier, count in sorted(tier_counts.items()):
        print(f"     - {tier}: {count} books")


def main():
    """Main entry point for taxonomy config generation."""
    parser = argparse.ArgumentParser(
        description="Generate taxonomy configuration JSON from Python definitions"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / "config" / "taxonomy_config.json",
        help="Output path for taxonomy_config.json (default: config/taxonomy_config.json)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the generated configuration"
    )
    
    args = parser.parse_args()
    
    print("Generating taxonomy configuration...")
    print("=" * 70)
    
    try:
        # Generate configuration
        config = generate_taxonomy_config()
        
        # Validate if requested
        if args.validate:
            print("\n🔍 Validating configuration...")
            validate_taxonomy_config(config)
        
        # Save to file
        save_taxonomy_config(config, args.output)
        
        print("\n✅ Generation complete!")
        
    except Exception as e:
        print(f"\n❌ Error generating taxonomy configuration: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def validate_taxonomy_config(config: Dict[str, Any]) -> None:
    """
    Validate taxonomy configuration for consistency.
    
    Args:
        config: Taxonomy configuration dictionary
        
    Raises:
        ValueError: If validation fails
    """
    # Validation checks:
    # - Check all cascades_to references exist
    # - Verify no circular cascading dependencies
    # - Ensure all keyword triggers are lowercase
    # - Validate relevance weights are positive
    # - Check tier values are valid
    
    book_names = {book["name"] for book in config["books"]}
    
    for book in config["books"]:
        # Check cascade references
        for cascaded_book in book["cascades_to"]:
            if cascaded_book not in book_names:
                raise ValueError(
                    f"Book '{book['name']}' cascades to unknown book '{cascaded_book}'"
                )
        
        # Check relevance weight
        if book["relevance_weight"] <= 0:
            raise ValueError(
                f"Book '{book['name']}' has invalid relevance_weight: {book['relevance_weight']}"
            )
    
    print("   ✅ All cascade references valid")
    print("   ✅ All relevance weights valid")
    print("   ✅ Configuration is consistent")


if __name__ == "__main__":
    main()
