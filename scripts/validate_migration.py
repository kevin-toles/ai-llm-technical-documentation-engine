#!/usr/bin/env python3
"""
Migration Validation Script
Validates the workflow reorganization against MIGRATION_PLAN.md

Run from repo root: python3 scripts/validate_migration.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class MigrationStatus:
    """Track migration progress"""
    total_files: int = 0
    moved_files: int = 0
    missing_files: List[str] = field(default_factory=list)
    extra_files: List[str] = field(default_factory=list)
    import_errors: List[Tuple[str, str]] = field(default_factory=list)
    init_files_missing: List[str] = field(default_factory=list)
    symlinks_missing: List[str] = field(default_factory=list)


class MigrationValidator:
    """Validates migration against MIGRATION_PLAN.md"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.status = MigrationStatus()
        
        # Expected file mappings from MIGRATION_PLAN.md
        self.expected_workflow_files = {
            # Workflow 1
            "workflows/01_taxonomy_setup/scripts/book_taxonomy.py": "src/book_taxonomy.py",
            "workflows/01_taxonomy_setup/scripts/generate_taxonomy_config.py": "scripts/generate_taxonomy_config.py",
            
            # Workflow 2
            "workflows/02_pdf_to_json/scripts/convert_pdf_to_json.py": "src/pipeline/convert_pdf_to_json.py",
            
            # Workflow 3
            "workflows/03_metadata_extraction/scripts/generate_metadata_universal.py": "src/pipeline/generate_metadata_universal.py",
            
            # Workflow 4
            "workflows/04_metadata_cache_merge/scripts/merge_metadata_to_cache.py": "src/pipeline/merge_metadata_to_cache.py",
            
            # Workflow 5
            "workflows/05_metadata_enrichment/scripts/generate_chapter_metadata.py": "src/pipeline/generate_chapter_metadata.py",
            "workflows/05_metadata_enrichment/scripts/chapter_metadata_manager.py": "src/chapter_metadata_manager.py",
            
            # Workflow 6
            "workflows/06_base_guideline_generation/scripts/chapter_generator_all_text.py": "src/pipeline/chapter_generator_all_text.py",
            
            # Workflow 7
            "workflows/07_llm_enhancement/scripts/integrate_llm_enhancements.py": "src/integrate_llm_enhancements.py",
            "workflows/07_llm_enhancement/scripts/interactive_llm_system_v3_hybrid_prompt.py": "src/interactive_llm_system_v3_hybrid_prompt.py",
            "workflows/07_llm_enhancement/scripts/metadata_extraction_system.py": "src/metadata_extraction_system.py",
            "workflows/07_llm_enhancement/scripts/compliance_validator_v3.py": "src/pipeline/compliance_validator_v3.py",
            "workflows/07_llm_enhancement/scripts/models/analysis_models.py": "src/models/analysis_models.py",
            "workflows/07_llm_enhancement/scripts/models/__init__.py": "src/models/__init__.py",
            "workflows/07_llm_enhancement/scripts/phases/content_selection_impl.py": "src/phases/content_selection_impl.py",
            "workflows/07_llm_enhancement/scripts/phases/content_selection.py": "src/phases/content_selection.py",
            "workflows/07_llm_enhancement/scripts/phases/__init__.py": "src/phases/__init__.py",
            "workflows/07_llm_enhancement/scripts/builders/metadata_builder.py": "src/builders/metadata_builder.py",
            "workflows/07_llm_enhancement/scripts/builders/__init__.py": "src/builders/__init__.py",
        }
        
        self.expected_shared_files = {
            "shared/cache.py": "src/cache.py",
            "shared/retry.py": "src/retry.py",
            "shared/llm_integration.py": "src/llm_integration.py",
            "shared/json_parser.py": "src/json_parser.py",
            "shared/constants.py": "src/constants.py",
            "shared/providers/base.py": "src/providers/base.py",
            "shared/providers/anthropic_provider.py": "src/providers/anthropic_provider.py",
            "shared/providers/factory.py": "src/providers/factory.py",
            "shared/providers/__init__.py": "src/providers/__init__.py",
            "shared/loaders/content_loaders.py": "src/loaders/content_loaders.py",
            "shared/loaders/__init__.py": "src/loaders/__init__.py",
            "shared/prompts/templates.py": "src/prompts/templates.py",
            "shared/prompts/__init__.py": "src/prompts/__init__.py",
        }
        
        self.expected_init_files = [
            "workflows/__init__.py",
            "workflows/01_taxonomy_setup/__init__.py",
            "workflows/01_taxonomy_setup/scripts/__init__.py",
            "workflows/02_pdf_to_json/__init__.py",
            "workflows/02_pdf_to_json/scripts/__init__.py",
            "workflows/03_metadata_extraction/__init__.py",
            "workflows/03_metadata_extraction/scripts/__init__.py",
            "workflows/04_metadata_cache_merge/__init__.py",
            "workflows/04_metadata_cache_merge/scripts/__init__.py",
            "workflows/05_metadata_enrichment/__init__.py",
            "workflows/05_metadata_enrichment/scripts/__init__.py",
            "workflows/06_base_guideline_generation/__init__.py",
            "workflows/06_base_guideline_generation/scripts/__init__.py",
            "workflows/07_llm_enhancement/__init__.py",
            "workflows/07_llm_enhancement/scripts/__init__.py",
            "workflows/07_llm_enhancement/scripts/builders/__init__.py",
            "workflows/07_llm_enhancement/scripts/models/__init__.py",
            "workflows/07_llm_enhancement/scripts/phases/__init__.py",
            "shared/__init__.py",
            "shared/providers/__init__.py",
            "shared/loaders/__init__.py",
            "shared/prompts/__init__.py",
        ]
        
        self.expected_data_moves = {
            "workflows/02_pdf_to_json/output/textbooks_json": "data/textbooks_json",
            "workflows/03_metadata_extraction/output/metadata": "data/metadata",
            "workflows/04_metadata_cache_merge/output/chapter_metadata_cache.json": "data/chapter_metadata_cache.json",
            "workflows/05_metadata_enrichment/output/chapter_metadata_manual.json": "data/chapter_metadata_manual.json",
            "workflows/06_base_guideline_generation/output/chapter_summaries": "data/chapter_summaries",
        }
    
    def validate_directory_structure(self) -> bool:
        """Validate workflow directories exist"""
        print("\n📁 Validating Directory Structure...")
        
        required_dirs = [
            "workflows/01_taxonomy_setup/scripts",
            "workflows/01_taxonomy_setup/input",
            "workflows/01_taxonomy_setup/output",
            "workflows/02_pdf_to_json/scripts",
            "workflows/02_pdf_to_json/input",
            "workflows/02_pdf_to_json/output",
            "workflows/03_metadata_extraction/scripts",
            "workflows/03_metadata_extraction/input",
            "workflows/03_metadata_extraction/output",
            "workflows/04_metadata_cache_merge/scripts",
            "workflows/04_metadata_cache_merge/input",
            "workflows/04_metadata_cache_merge/output",
            "workflows/05_metadata_enrichment/scripts",
            "workflows/05_metadata_enrichment/input",
            "workflows/05_metadata_enrichment/output",
            "workflows/06_base_guideline_generation/scripts",
            "workflows/06_base_guideline_generation/input",
            "workflows/06_base_guideline_generation/output",
            "workflows/07_llm_enhancement/scripts",
            "workflows/07_llm_enhancement/input",
            "workflows/07_llm_enhancement/output",
            "workflows/07_llm_enhancement/scripts/builders",
            "workflows/07_llm_enhancement/scripts/models",
            "workflows/07_llm_enhancement/scripts/phases",
            "shared",
            "shared/providers",
            "shared/loaders",
            "shared/prompts",
        ]
        
        all_exist = True
        for dir_path in required_dirs:
            full_path = self.repo_root / dir_path
            if full_path.exists():
                print(f"  ✅ {dir_path}")
            else:
                print(f"  ❌ Missing: {dir_path}")
                all_exist = False
        
        return all_exist
    
    def validate_file_moves(self) -> bool:
        """Validate all files moved to correct locations"""
        print("\n📦 Validating File Moves...")
        
        all_files = {**self.expected_workflow_files, **self.expected_shared_files}
        self.status.total_files = len(all_files)
        
        for new_path, old_path in all_files.items():
            full_new_path = self.repo_root / new_path
            full_old_path = self.repo_root / old_path
            
            if full_new_path.exists():
                print(f"  ✅ {new_path}")
                self.status.moved_files += 1
                
                # Check if old file still exists (should be deleted)
                if full_old_path.exists():
                    print(f"  ⚠️  Old file still exists: {old_path}")
            else:
                print(f"  ❌ Missing: {new_path} (from {old_path})")
                self.status.missing_files.append(new_path)
        
        return len(self.status.missing_files) == 0
    
    def validate_init_files(self) -> bool:
        """Validate all __init__.py files exist"""
        print("\n🔧 Validating __init__.py Files...")
        
        all_exist = True
        for init_file in self.expected_init_files:
            full_path = self.repo_root / init_file
            if full_path.exists():
                print(f"  ✅ {init_file}")
            else:
                print(f"  ❌ Missing: {init_file}")
                self.status.init_files_missing.append(init_file)
                all_exist = False
        
        return all_exist
    
    def validate_data_moves(self) -> bool:
        """Validate data files moved to workflow outputs"""
        print("\n📊 Validating Data File Moves...")
        
        all_moved = True
        for new_path, old_path in self.expected_data_moves.items():
            full_new_path = self.repo_root / new_path
            full_old_path = self.repo_root / old_path
            
            if full_new_path.exists():
                print(f"  ✅ {new_path}")
            else:
                print(f"  ❌ Missing: {new_path} (from {old_path})")
                all_moved = False
        
        return all_moved
    
    def validate_old_files_deleted(self) -> bool:
        """Validate old src/ files have been deleted"""
        print("\n🗑️  Validating Old Files Deleted...")
        
        src_path = self.repo_root / "src"
        if not src_path.exists():
            print("  ✅ src/ directory removed")
            return True
        
        # Check if any Python files remain in src/
        remaining_files = list(src_path.rglob("*.py"))
        if remaining_files:
            print(f"  ⚠️  Found {len(remaining_files)} remaining files in src/:")
            for f in remaining_files[:10]:  # Show first 10
                print(f"      - {f.relative_to(self.repo_root)}")
            return False
        
        print("  ✅ No Python files remaining in src/")
        return True
    
    def generate_report(self) -> Dict:
        """Generate validation report"""
        return {
            "total_files": self.status.total_files,
            "moved_files": self.status.moved_files,
            "missing_files": self.status.missing_files,
            "extra_files": self.status.extra_files,
            "init_files_missing": self.status.init_files_missing,
            "symlinks_missing": self.status.symlinks_missing,
            "completion_percentage": (self.status.moved_files / self.status.total_files * 100) if self.status.total_files > 0 else 0,
        }
    
    def run_validation(self) -> bool:
        """Run complete validation"""
        print("=" * 80)
        print("🔍 MIGRATION VALIDATION - Workflow Reorganization")
        print("=" * 80)
        
        results = {
            "directory_structure": self.validate_directory_structure(),
            "file_moves": self.validate_file_moves(),
            "init_files": self.validate_init_files(),
            "data_moves": self.validate_data_moves(),
            "old_files_deleted": self.validate_old_files_deleted(),
        }
        
        # Generate report
        report = self.generate_report()
        
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)
        print(f"Files Moved: {report['moved_files']}/{report['total_files']} ({report['completion_percentage']:.1f}%)")
        print(f"Missing Files: {len(report['missing_files'])}")
        print(f"Missing __init__.py: {len(report['init_files_missing'])}")
        
        all_passed = all(results.values())
        
        if all_passed:
            print("\n✅ ALL VALIDATIONS PASSED - Migration Complete!")
        else:
            print("\n❌ VALIDATION FAILED - See errors above")
            print("\nFailed Checks:")
            for check, passed in results.items():
                if not passed:
                    print(f"  ❌ {check}")
        
        print("=" * 80)
        
        return all_passed


def main():
    """Main entry point"""
    repo_root = Path(__file__).parent.parent
    validator = MigrationValidator(repo_root)
    
    success = validator.run_validation()
    
    # Write report to file
    report = validator.generate_report()
    report_path = repo_root / "migration_validation_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Full report written to: {report_path}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
