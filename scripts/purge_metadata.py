#!/usr/bin/env python3
"""
Purge all metadata, taxonomy, and workflow output files except protected directories.

Protected directories (will NOT be deleted):
- /Users/kevintoles/POC/llm-document-enhancer/workflows/pdf_to_json/output/textbooks_json
- /Users/kevintoles/POC/llm-document-enhancer/workflows/llm_enhancement/output
- /Users/kevintoles/POC/llm-document-enhancer/workflows/base_guideline_generation/output
"""

import os
from pathlib import Path
import argparse
from typing import List, Set

# Protected directories - files here will NOT be deleted
PROTECTED_DIRS = {
    "workflows/pdf_to_json/output/textbooks_json",
    "workflows/llm_enhancement/output",
    "workflows/base_guideline_generation/output",
}

# Additional files to keep (configuration, documentation we want to preserve)
KEEP_FILES = {
    "README.md",
    "requirements.txt",
    "sonar-project.properties",
    ".gitignore",
    "config/chapter_patterns.json",
    "config/metadata_keywords.json",
    "config/validation_rules.json",
    "ui/requirements.txt",
    "ui/README.md",
    "coderabbit/README.md",
}


def is_protected(file_path: Path, base_dir: Path) -> bool:
    """Check if a file is in a protected directory."""
    try:
        relative_path = file_path.relative_to(base_dir)
        relative_str = str(relative_path)
        
        # Check if file is in any protected directory
        for protected in PROTECTED_DIRS:
            if relative_str.startswith(protected):
                return True
        
        # Check if it's an explicitly kept file
        if relative_str in KEEP_FILES:
            return True
            
        return False
    except ValueError:
        return False


def find_files_to_delete(base_dir: Path, extensions: Set[str]) -> List[Path]:
    """Find all files with specified extensions that are not in protected directories."""
    files_to_delete = []
    
    for ext in extensions:
        for file_path in base_dir.rglob(f"*{ext}"):
            if file_path.is_file() and not is_protected(file_path, base_dir):
                files_to_delete.append(file_path)
    
    return sorted(files_to_delete)


def get_directory_summary(files: List[Path], base_dir: Path) -> dict:
    """Group files by their parent directory for summary."""
    summary = {}
    for file_path in files:
        try:
            relative_path = file_path.relative_to(base_dir)
            parent = str(relative_path.parent)
            if parent not in summary:
                summary[parent] = []
            summary[parent].append(file_path.name)
        except ValueError:
            continue
    return summary


def print_file_summary(files_to_delete: List[Path], base_dir: Path) -> int:
    """Print summary of files to be deleted. Returns total size in bytes."""
    summary = get_directory_summary(files_to_delete, base_dir)
    print(f"\nFound {len(files_to_delete)} files to delete:")
    print()
    
    total_size = 0
    for directory in sorted(summary.keys()):
        files = summary[directory]
        print(f"\n📁 {directory}/ ({len(files)} files)")
        for filename in sorted(files)[:5]:  # Show first 5 files
            file_path = base_dir / directory / filename
            size = file_path.stat().st_size if file_path.exists() else 0
            total_size += size
            size_kb = size / 1024
            print(f"   • {filename} ({size_kb:.1f} KB)")
        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more files")
    
    return total_size


def print_statistics(files_to_delete: List[Path], total_size: int, summary: dict):
    """Print statistics about files to be deleted."""
    json_count = sum(1 for f in files_to_delete if f.suffix == ".json")
    md_count = sum(1 for f in files_to_delete if f.suffix == ".md")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files: {len(files_to_delete)}")
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
    print(f"Directories affected: {len(summary)}")
    print("\nFile types:")
    print(f"  • JSON files: {json_count}")
    print(f"  • Markdown files: {md_count}")


def execute_deletion(files_to_delete: List[Path], base_dir: Path):
    """Execute the file deletion process."""
    print("\n" + "=" * 80)
    print("EXECUTING DELETION")
    print("=" * 80)
    
    deleted_count = 0
    failed_count = 0
    
    for file_path in files_to_delete:
        try:
            file_path.unlink()
            deleted_count += 1
            print(f"✓ Deleted: {file_path.relative_to(base_dir)}")
        except Exception as e:
            failed_count += 1
            print(f"✗ Failed: {file_path.relative_to(base_dir)} - {e}")
    
    print("\n" + "=" * 80)
    print("DELETION COMPLETE")
    print("=" * 80)
    print(f"Successfully deleted: {deleted_count} files")
    if failed_count > 0:
        print(f"Failed to delete: {failed_count} files")
    print("\n✅ Metadata purge completed. Protected directories remain intact.")


def main():
    parser = argparse.ArgumentParser(
        description="Purge metadata and output files while preserving protected directories"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete files (default is dry-run mode)"
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Base directory of the project"
    )
    
    args = parser.parse_args()
    base_dir = args.base_dir.resolve()
    
    print("=" * 80)
    print("METADATA PURGE TOOL")
    print("=" * 80)
    print(f"\nBase directory: {base_dir}")
    print(f"Mode: {'EXECUTE (files will be deleted)' if args.execute else 'DRY RUN (no files will be deleted)'}")
    print("\nProtected directories:")
    for protected in sorted(PROTECTED_DIRS):
        print(f"  ✓ {protected}")
    
    # Find files to delete
    print("\n" + "=" * 80)
    print("SCANNING FOR FILES TO DELETE")
    print("=" * 80)
    
    extensions_to_delete = {".json", ".md"}
    files_to_delete = find_files_to_delete(base_dir, extensions_to_delete)
    
    if not files_to_delete:
        print("\n✅ No files found to delete. System is clean.")
        return
    
    # Display and get statistics
    total_size = print_file_summary(files_to_delete, base_dir)
    summary = get_directory_summary(files_to_delete, base_dir)
    print_statistics(files_to_delete, total_size, summary)
    
    if not args.execute:
        print("\n" + "=" * 80)
        print("⚠️  DRY RUN MODE - No files were deleted")
        print("=" * 80)
        print("\nTo actually delete these files, run:")
        print(f"  python3 {Path(__file__).name} --execute")
        return
    
    execute_deletion(files_to_delete, base_dir)


if __name__ == "__main__":
    main()
