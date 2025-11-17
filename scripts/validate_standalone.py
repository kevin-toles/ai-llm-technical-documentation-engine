#!/usr/bin/env python3
"""
Standalone repo validation script - verify everything works.
Run from repo root: python3 scripts/validate_standalone.py
"""

import sys
from pathlib import Path

# Add repo root to path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

def validate_structure():
    """Validate directory structure and required files."""
    print("Validating directory structure...")
    errors = []
    
    required_dirs = [
        "src",
        "data/textbooks_json",
        "data/metadata",
        "guidelines",
        "logs",
        "outputs"
    ]
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            errors.append(f"Missing directory: {dir_path}")
        else:
            print(f"  ✅ {dir_path}")
    
    return errors

def validate_python_files():
    """Validate all Python files present."""
    print("\nValidating Python files...")
    errors = []
    
    required_py = [
        "src/__init__.py",
        "src/integrate_llm_enhancements.py",
        "src/interactive_llm_system_v3_hybrid_prompt.py",
        "src/llm_integration.py",
        "src/metadata_extraction_system.py",
        "src/book_taxonomy.py",
        "src/chapter_metadata_manager.py"
    ]
    
    for py_file in required_py:
        if not Path(py_file).exists():
            errors.append(f"Missing Python file: {py_file}")
        else:
            print(f"  ✅ {py_file}")
    
    return errors

def validate_data_files():
    """Validate data files."""
    print("\nValidating data files...")
    errors = []
    
    json_count = len(list(Path("data/textbooks_json").glob("*.json")))
    if json_count != 14:
        errors.append(f"Expected 14 book JSONs, found {json_count}")
    else:
        print("  ✅ 14 book JSONs found")
    
    metadata_count = len(list(Path("data/metadata").glob("*.json")))
    if metadata_count != 14:
        errors.append(f"Expected 14 metadata JSONs, found {metadata_count}")
    else:
        print("  ✅ 14 metadata JSONs found")
    
    if not Path("data/chapter_metadata_cache.json").exists():
        errors.append("Missing chapter_metadata_cache.json")
    else:
        print("  ✅ chapter_metadata_cache.json")
    
    return errors

def validate_config():
    """Validate configuration files."""
    print("\nValidating configuration files...")
    errors = []
    
    required_config = [
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md"
    ]
    
    for config_file in required_config:
        if not Path(config_file).exists():
            errors.append(f"Missing config file: {config_file}")
        else:
            print(f"  ✅ {config_file}")
    
    # Check for .env (optional but recommended)
    if not Path(".env").exists():
        print("  ⚠️  .env file not found (create from .env.example)")
    else:
        print("  ✅ .env")
    
    return errors

def validate_imports():
    """Test that imports work."""
    print("\nValidating imports...")
    errors = []
    
    try:
        from workflows.w07_llm_enhancement.scripts.metadata_extraction_system import MetadataServiceFactory  # noqa: F401
        print("  ✅ metadata_extraction_system")
    except ImportError as e:
        errors.append(f"Import failed: metadata_extraction_system - {e}")
    
    try:
        from shared.llm_integration import call_llm  # noqa: F401
        print("  ✅ llm_integration")
    except ImportError as e:
        errors.append(f"Import failed: llm_integration - {e}")
    
    try:
        from workflows.w01_taxonomy_setup.scripts.book_taxonomy import BOOK_REGISTRY  # noqa: F401
        print("  ✅ book_taxonomy")
    except ImportError as e:
        errors.append(f"Import failed: book_taxonomy - {e}")
    
    try:
        from workflows.w07_llm_enhancement.scripts.interactive_llm_system_v3_hybrid_prompt import AnalysisOrchestrator  # noqa: F401
        print("  ✅ interactive_llm_system_v3_hybrid_prompt")
    except ImportError as e:
        errors.append(f"Import failed: interactive_llm_system_v3_hybrid_prompt - {e}")
    
    return errors

def main():
    print("=" * 60)
    print("LLM Document Enhancer - Standalone Validation")
    print("=" * 60)
    
    all_errors = []
    
    all_errors.extend(validate_structure())
    all_errors.extend(validate_python_files())
    all_errors.extend(validate_data_files())
    all_errors.extend(validate_config())
    all_errors.extend(validate_imports())
    
    print("\n" + "=" * 60)
    if all_errors:
        print("❌ VALIDATION FAILED")
        print("=" * 60)
        for error in all_errors:
            print(f"  - {error}")
        return 1
    else:
        print("✅ ALL VALIDATION PASSED")
        print("=" * 60)
        print("\nStandalone repo is ready!")
        print("\nNext steps:")
        print("  1. Ensure .env file has ANTHROPIC_API_KEY")
        print("  2. Run: python3 -m src.integrate_llm_enhancements")
        print("  3. Initialize git: git init")
        print("  4. Push to GitHub")
        return 0

if __name__ == "__main__":
    sys.exit(main())
