#!/usr/bin/env python3
"""
Universal metadata merger - discovers and merges all metadata files into cache

Guideline Compliance:
- ARCH 5336: Dependency Injection for paths and configuration
- PY 3754: Use pathlib.Path() for all file operations
- PY 32425: Use context managers for file I/O
- PY 21: EAFP exception handling

TDD Refactoring: Extracted hardcoded values, added validation, CLI args, progress indicators
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional


class MetadataMerger:
    """
    Merge metadata files into central cache with validation and progress tracking.
    
    Uses Dependency Injection pattern (ARCH 5336) for flexible configuration.
    """
    
    def __init__(
        self,
        input_dir: Path,
        output_file: Optional[Path] = None,
        book_list: Optional[List[str]] = None
    ):
        """
        Initialize merger with configuration.
        
        Args:
            input_dir: Directory containing *_metadata.json files
            output_file: Path to output cache file (default: input_dir/../output/chapter_metadata_cache.json)
            book_list: Optional list of book names to filter (only merge these books)
        """
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file) if output_file else self.input_dir.parent / "output" / "chapter_metadata_cache.json"
        self.book_list = book_list
    
    def discover_metadata_files(self) -> List[Path]:
        """
        Auto-discover all *_metadata.json files in input directory.
        
        Returns:
            List of Path objects for discovered metadata files
        
        Guideline: PY 3754 - Use pathlib.Path.glob() for file discovery
        """
        metadata_files = list(self.input_dir.glob("*_metadata.json"))
        
        if not metadata_files:
            print(f"⚠️  No metadata files found in {self.input_dir}")
        else:
            print(f"📁 Found {len(metadata_files)} metadata files")
        
        return metadata_files
    
    def validate_metadata_file(self, file_path: Path) -> bool:
        """
        Validate metadata file has required structure.
        
        Args:
            file_path: Path to metadata JSON file
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If metadata structure is invalid
        
        Guideline: PY 32425 - Use context manager for file I/O
        Guideline: PY 21 - EAFP: Try to parse, catch exceptions
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Validate required 'chapters' field exists
            if 'chapters' not in data:
                raise ValueError(f"Missing required field 'chapters' in {file_path.name}")
            
            # Validate 'chapters' is a list
            if not isinstance(data['chapters'], list):
                raise ValueError(f"Field 'chapters' must be a list in {file_path.name}")
            
            return True
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path.name}: {e}")
    
    def detect_duplicate_books(self, files: List[Path]) -> List[str]:
        """
        Detect duplicate book names in discovered files.
        
        Args:
            files: List of metadata file paths
        
        Returns:
            List of book names that appear multiple times
        """
        # Extract book names (remove _metadata.json suffix)
        # Also extract base name (e.g., "book_a" from both "book_a" and "book_a_v2")
        book_names = []
        for f in files:
            # Remove _metadata suffix
            name = f.stem.replace("_metadata", "")
            # Extract base name (remove version suffixes like _v2, _2nd, etc.)
            # Simple approach: split on underscore and take first parts
            base_name = name.split('_v')[0].split('_2nd')[0].split('_ed')[0]
            book_names.append(base_name)
        
        # Find duplicates
        seen = set()
        duplicates = []
        for name in book_names:
            if name in seen and name not in duplicates:
                duplicates.append(name)
            seen.add(name)
        
        if duplicates:
            print(f"⚠️  Duplicate books detected: {', '.join(duplicates)}")
        
        return duplicates
    
    def merge_all(self, dry_run: bool = False) -> Dict[str, List[Dict]]:
        """
        Merge all discovered metadata files into cache.
        
        Args:
            dry_run: If True, show what would be written without creating file
        
        Returns:
            Dictionary mapping book names to chapter lists
        
        Guideline: PY 32425 - Use context manager for file I/O
        """
        files = self.discover_metadata_files()
        
        # Filter by book_list if provided
        if self.book_list:
            files = [
                f for f in files 
                if any(book in f.stem for book in self.book_list)
            ]
            print(f"🔍 Filtered to {len(files)} books from provided list")
        
        # Detect duplicates
        self.detect_duplicate_books(files)
        
        cache = {}
        total_chapters = 0
        
        for idx, file_path in enumerate(files):
            # Show progress
            progress_pct = ((idx + 1) / len(files)) * 100
            print(f"[{progress_pct:.1f}%] Processing {file_path.name}")
            
            # Validate before merging
            try:
                self.validate_metadata_file(file_path)
            except ValueError as e:
                print(f"❌ SKIPPED - {e}")
                continue
            
            # Load metadata
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            chapters = data.get('chapters', [])
            
            # Warn if no chapters
            if not chapters:
                print(f"⚠️  WARNING: {file_path.name} has no chapters")
            
            cache[file_path.name] = chapters
            total_chapters += len(chapters)
        
        # Show merge statistics
        print(f"\n{'='*80}")
        print("📊 MERGE STATISTICS:")
        print(f"   Books: {len(cache)}")
        print(f"   Chapters: {total_chapters}")
        print(f"{'='*80}")
        
        # Save cache (unless dry run)
        if dry_run:
            print(f"\n🔍 DRY RUN MODE - Would write to: {self.output_file}")
            print("   Preview of first book:")
            if cache:
                first_book = list(cache.keys())[0]
                print(f"   {first_book}: {len(cache[first_book])} chapters")
        else:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_file, 'w') as f:
                json.dump(cache, f, indent=2)
            print(f"\n✅ Cache saved to: {self.output_file}")
        
        return cache
    
    def validate_all(self) -> None:
        """
        Validate all metadata files without merging.
        
        Guideline: PY 21 - EAFP: Try to validate, catch exceptions
        """
        files = self.discover_metadata_files()
        
        print(f"\n{'='*80}")
        print("🔍 VALIDATION RESULTS:")
        print(f"{'='*80}")
        
        valid_count = 0
        invalid_count = 0
        
        for file_path in files:
            try:
                self.validate_metadata_file(file_path)
                print(f"✅ {file_path.name}")
                valid_count += 1
            except ValueError as e:
                print(f"❌ {file_path.name} - {e}")
                invalid_count += 1
        
        print(f"\n{'='*80}")
        print(f"📊 SUMMARY: {valid_count} valid, {invalid_count} FAILED")
        print(f"{'='*80}")


def main():
    """
    CLI entry point with argument parsing.
    
    Guideline: ARCH 5336 - DI pattern - inject paths from CLI
    """
    parser = argparse.ArgumentParser(
        description="Merge metadata files into central cache",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (auto-discover metadata files)
  %(prog)s

  # Specify custom paths
  %(prog)s --input-dir ../input/metadata --output-file ../output/cache.json

  # Filter specific books
  %(prog)s --book-list "Fluent Python" "Learning Python"

  # Preview without writing
  %(prog)s --dry-run

  # Validate only (no merge)
  %(prog)s --validate-only
        """
    )
    
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path(__file__).parent.parent / "input",
        help='Directory containing *_metadata.json files (default: ../input/)'
    )
    
    parser.add_argument(
        '--output-file',
        type=Path,
        help='Path to output cache file (default: ../output/chapter_metadata_cache.json)'
    )
    
    parser.add_argument(
        '--book-list',
        nargs='+',
        help='Optional list of book names to filter (only merge these books)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be written without creating output file'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate metadata files (do not merge)'
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("UNIVERSAL METADATA MERGER")
    print("="*80)
    
    # Create merger with injected dependencies
    merger = MetadataMerger(
        input_dir=args.input_dir,
        output_file=args.output_file,
        book_list=args.book_list
    )
    
    # Execute based on mode
    if args.validate_only:
        merger.validate_all()
    else:
        merger.merge_all(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
