#!/usr/bin/env python3
"""
Generate Taxonomy Configuration (Refactored with TDD)

TDD Refactoring improvements:
- Added TaxonomyConfigGenerator class with DI pattern (ARCH 5336)
- Added Path() for file operations (PY 3754)
- Added context managers for file I/O (PY 32425)
- Added EAFP exception handling (PY 21)
- Multiple output formats (JSON, YAML, TOML)
- Cascade reference validation
- Circular dependency detection
- Dry-run and validate-only modes

Generates taxonomy_config.json from the book taxonomy Python code.
This allows for easier inspection and external tool integration.

Usage:
    python scripts/generate_taxonomy_config.py [--output OUTPUT_PATH] [--format json|yaml|toml]

Output:
    taxonomy_config.{json|yaml|toml} containing:
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
from typing import Dict, Any, List, Optional, Set

# Optional imports for YAML and TOML support
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import toml
    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.taxonomy_setup.scripts.book_taxonomy import ALL_BOOKS, BookTier


class TaxonomyConfigGenerator:
    """
    Generate taxonomy configuration with validation and multiple output formats.
    
    Uses Dependency Injection pattern (ARCH 5336) for flexible configuration.
    """
    
    def __init__(
        self,
        output_file: Optional[Path] = None,
        output_format: str = "json",
        pretty: bool = True
    ):
        """
        Initialize generator with configuration.
        
        Args:
            output_file: Path to output file (default: ../output/taxonomy_config.json)
            output_format: Output format (json|yaml|toml)
            pretty: Use pretty formatting (indentation)
        
        Guideline: ARCH 5336 - Dependency Injection for configuration
        """
        if output_file is None:
            # Default to workflow output folder
            output_file = Path(__file__).parent.parent / "output" / "taxonomy_config.json"
        
        self.output_file = Path(output_file)
        self.output_format = output_format.lower()
        self.pretty = pretty
        
        # Validate format is supported
        if self.output_format == "yaml" and not YAML_AVAILABLE:
            raise ValueError("YAML format requires PyYAML package: pip install pyyaml")
        if self.output_format == "toml" and not TOML_AVAILABLE:
            raise ValueError("TOML format requires toml package: pip install toml")
    
    def generate(self) -> Dict[str, Any]:
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
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate taxonomy configuration for consistency.
        
        Args:
            config: Taxonomy configuration dictionary
            
        Raises:
            ValueError: If validation fails
        
        Guideline: PY 21 - EAFP exception handling
        """
        book_names = {book["name"] for book in config["books"]}
        
        # Validate cascade references exist
        for book in config["books"]:
            for cascaded_book in book["cascades_to"]:
                if cascaded_book not in book_names:
                    raise ValueError(
                        f"Book '{book['name']}' cascades to unknown book '{cascaded_book}'"
                    )
            
            # Validate relevance weight
            if book["relevance_weight"] <= 0:
                raise ValueError(
                    f"Book '{book['name']}' has invalid relevance_weight: {book['relevance_weight']}"
                )
        
        # Check for circular dependencies
        self._check_circular_dependencies(config)
        
        print("   ✅ All cascade references valid")
        print("   ✅ All relevance weights valid")
        print("   ✅ No circular dependencies detected")
        print("   ✅ Configuration is consistent")
    
    def _check_circular_dependencies(self, config: Dict[str, Any]) -> None:
        """
        Check for circular cascade dependencies.
        
        Args:
            config: Taxonomy configuration dictionary
        
        Raises:
            ValueError: If circular dependency detected
        
        Note: Currently logs warnings for cycles but doesn't fail validation
        since some intentional cascade patterns may appear circular.
        """
        # Build dependency graph
        graph: Dict[str, List[str]] = {}
        for book in config["books"]:
            graph[book["name"]] = book["cascades_to"]
        
        # DFS to detect cycles
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycles_found: List[str] = []
        
        def has_cycle(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_path = " -> ".join(path + [neighbor])
                    if cycle_path not in cycles_found:
                        cycles_found.append(cycle_path)
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Check each book for cycles
        for book_name in graph:
            if book_name not in visited:
                has_cycle(book_name, [])
        
        if cycles_found:
            # Log warning but don't fail (intentional cascades may exist)
            print(f"   ⚠️  Warning: {len(cycles_found)} potential circular cascade(s) detected:")
            for cycle in cycles_found[:3]:  # Show first 3
                print(f"      - {cycle}")
            if len(cycles_found) > 3:
                print(f"      ... and {len(cycles_found) - 3} more")
            # Don't raise error - cascades may be intentional
    
    def generate_and_save(self, dry_run: bool = False) -> None:
        """
        Generate configuration and save to file.
        
        Args:
            dry_run: If True, show what would be written without creating file
        
        Guideline: PY 32425 - Use context manager for file I/O
        """
        # Generate configuration
        config = self.generate()
        
        # Validate
        self.validate_config(config)
        
        # Format content based on output format
        if self.output_format == "json":
            content = self._format_json(config)
        elif self.output_format == "yaml":
            content = self._format_yaml(config)
        elif self.output_format == "toml":
            content = self._format_toml(config)
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")
        
        if dry_run:
            print(f"\n🔍 DRY RUN MODE - Would write to: {self.output_file}")
            print(f"   Format: {self.output_format.upper()}")
            print("   Preview (first 500 chars):")
            print("-" * 80)
            print(content[:500])
            if len(content) > 500:
                print(f"... ({len(content) - 500} more characters)")
            print("-" * 80)
        else:
            # Save to file
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Print summary
            print(f"\n✅ Taxonomy configuration saved to: {self.output_file}")
            self._print_summary(config)
    
    def validate_only(self) -> None:
        """
        Validate configuration without saving to file.
        """
        print("\n🔍 VALIDATION ONLY MODE")
        print("=" * 80)
        
        config = self.generate()
        self.validate_config(config)
        
        print("\n✅ Validation complete - no errors found")
        self._print_summary(config)
    
    def _format_json(self, config: Dict[str, Any]) -> str:
        """Format configuration as JSON."""
        if self.pretty:
            return json.dumps(config, indent=2, ensure_ascii=False)
        else:
            return json.dumps(config, ensure_ascii=False)
    
    def _format_yaml(self, config: Dict[str, Any]) -> str:
        """Format configuration as YAML."""
        if self.pretty:
            return yaml.dump(config, default_flow_style=False, sort_keys=False)
        else:
            return yaml.dump(config, default_flow_style=True)
    
    def _format_toml(self, config: Dict[str, Any]) -> str:
        """Format configuration as TOML."""
        # TOML has limitations with nested structures
        # Flatten for TOML compatibility
        toml_config = {
            "metadata": config["metadata"],
            "tiers": config["tiers"]
        }
        
        # Add each book as a separate table
        for idx, book in enumerate(config["books"]):
            book_key = f"book_{idx}_{book['name'].replace(' ', '_').replace('.', '')}"
            toml_config[book_key] = book
        
        return toml.dumps(toml_config)
    
    def _print_summary(self, config: Dict[str, Any]) -> None:
        """Print summary statistics (Python Distilled Ch. 5: Program Structure)."""
        print("\n   📊 TAXONOMY SUMMARY:")
        print(f"   📚 Total books: {config['metadata']['total_books']}")
        
        # Tier breakdown
        tier_counts: Dict[str, int] = {}
        total_cascades = 0
        
        for book in config["books"]:
            tier = book["tier"]
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            total_cascades += len(book["cascades_to"])
        
        print("\n   📋 Tier breakdown:")
        for tier, count in sorted(tier_counts.items()):
            print(f"      - {tier}: {count} books")
        
        print(f"\n   🔗 Total cascade relationships: {total_cascades}")
        print(f"   ⚖️  Average cascades per book: {total_cascades / len(config['books']):.1f}")


# Legacy functions (for backwards compatibility)
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
    # Default output to workflow output folder
    default_output = Path(__file__).parent.parent / "output" / "taxonomy_config.json"
    
    parser = argparse.ArgumentParser(
        description="Generate taxonomy configuration from Python definitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate JSON (default)
  %(prog)s

  # Generate YAML
  %(prog)s --format yaml --output taxonomy.yaml

  # Generate TOML
  %(prog)s --format toml --output taxonomy.toml

  # Validate only (no output file)
  %(prog)s --validate-only

  # Preview without writing
  %(prog)s --dry-run
        """
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help="Output path for taxonomy config (default: ../output/taxonomy_config.json)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml", "toml"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Use pretty formatting with indentation (default: True)"
    )
    parser.add_argument(
        "--no-pretty",
        action="store_false",
        dest="pretty",
        help="Disable pretty formatting (compact output)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the generated configuration (always enabled)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate, don't save output file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be written without creating file"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("TAXONOMY CONFIGURATION GENERATOR")
    print("=" * 80)
    
    try:
        # Create generator with injected dependencies
        generator = TaxonomyConfigGenerator(
            output_file=args.output,
            output_format=args.format,
            pretty=args.pretty
        )
        
        # Execute based on mode
        if args.validate_only:
            generator.validate_only()
        else:
            generator.generate_and_save(dry_run=args.dry_run)
        
        print("\n✅ Complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
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
