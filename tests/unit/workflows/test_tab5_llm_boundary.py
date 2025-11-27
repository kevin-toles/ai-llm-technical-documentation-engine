"""
RED Phase Tests for Task 1.1: Verify LLM Disabled in Tab 5

Test-Driven Development (TDD) Cycle:
- RED: These tests MUST FAIL initially (no USE_LLM_SEMANTIC_ANALYSIS constant exists)
- GREEN: Add constant and enforce architecture boundary
- REFACTOR: Verify anti-pattern compliance

Architecture Requirement:
- Tab 5 (Guideline Generation): Statistical methods ONLY (YAKE, Summa, TF-IDF)
- Tab 7 (LLM Enhancement): LLM calls ONLY (Claude, GPT)
- Clear separation of concerns per ARCHITECTURE_GUIDELINES

References:
- MASTER_IMPLEMENTATION_GUIDE.md: Task 1.1 (lines 2722-2726)
- ANTI_PATTERN_ANALYSIS.md: §9.1 (Stale configuration references)
- ARCHITECTURE_GUIDELINES: Separation of concerns, module boundaries
"""

import pytest
import re
from pathlib import Path
from typing import List


class TestTab5ArchitectureBoundary:
    """Verify Tab 5 has NO LLM calls - architecture boundary enforcement."""
    
    def test_use_llm_semantic_analysis_constant_exists(self):
        """
        RED: This test MUST FAIL initially.
        
        Requirement: chapter_generator_all_text.py must have explicit constant
        USE_LLM_SEMANTIC_ANALYSIS = False to document architecture boundary.
        
        Reference: MASTER_IMPLEMENTATION_GUIDE.md Task 1.1
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Check for constant definition (with or without type annotation)
        pattern = r'USE_LLM_SEMANTIC_ANALYSIS\s*(?::\s*bool)?\s*=\s*(True|False)'
        match = re.search(pattern, content)
        
        assert match is not None, (
            "USE_LLM_SEMANTIC_ANALYSIS constant not found. "
            "Tab 5 must have explicit constant documenting LLM is disabled."
        )
    
    def test_use_llm_semantic_analysis_is_false(self):
        """
        RED: This test MUST FAIL initially.
        
        Requirement: USE_LLM_SEMANTIC_ANALYSIS must be False (not True).
        LLM calls belong in Tab 7 only.
        
        Reference: Architecture boundary - Tab 5 uses statistical methods only
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Find constant value (with or without type annotation)
        pattern = r'USE_LLM_SEMANTIC_ANALYSIS\s*(?::\s*bool)?\s*=\s*(True|False)'
        match = re.search(pattern, content)
        
        if match:
            value = match.group(1)
            assert value == "False", (
                f"USE_LLM_SEMANTIC_ANALYSIS is {value}, must be False. "
                "Tab 5 must NOT make LLM calls (architecture boundary violation)."
            )
        else:
            pytest.fail("USE_LLM_SEMANTIC_ANALYSIS constant not found")
    
    def test_no_anthropic_imports_in_tab5(self):
        """
        RED: This test SHOULD PASS initially (no imports found).
        
        Verify Tab 5 does not import Anthropic or LLM providers.
        LLM imports belong in Tab 7 only.
        
        Reference: ARCHITECTURE_GUIDELINES - Dependency boundaries
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Check for LLM provider imports
        forbidden_imports = [
            r'from\s+anthropic\s+import',
            r'import\s+anthropic',
            r'from\s+openai\s+import',
            r'import\s+openai',
            r'from\s+.*AnthropicProvider',
            r'from\s+.*LLMProvider'
        ]
        
        violations: List[str] = []
        for pattern in forbidden_imports:
            matches = re.findall(pattern, content)
            if matches:
                violations.extend(matches)
        
        assert len(violations) == 0, (
            f"Found {len(violations)} LLM provider imports in Tab 5: {violations}. "
            "Tab 5 must NOT import LLM providers (architecture boundary violation)."
        )
    
    def test_no_llm_api_calls_in_tab5(self):
        """
        RED: This test SHOULD PASS initially (calls removed).
        
        Verify Tab 5 does not make LLM API calls (client.messages.create, etc.).
        
        Reference: Architecture boundary - statistical methods only
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Check for LLM API call patterns
        forbidden_patterns = [
            r'client\.messages\.create',
            r'openai\.ChatCompletion',
            r'anthropic\.Anthropic',
            r'\.complete\(',
            r'\.generate\(',
        ]
        
        violations: List[str] = []
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content)
            if matches:
                violations.append(f"{pattern}: {len(matches)} occurrences")
        
        assert len(violations) == 0, (
            f"Found LLM API calls in Tab 5: {violations}. "
            "Tab 5 must use statistical methods only (YAKE, Summa, TF-IDF)."
        )
    
    def test_architecture_boundary_comment_present(self):
        """
        RED: This test SHOULD PASS initially (comment exists).
        
        Verify architecture boundary is documented in comments.
        Ensures developers understand the separation.
        
        Reference: ANTI_PATTERN_ANALYSIS §9.2 (Documentation drift)
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Check for architecture boundary documentation
        required_keywords = [
            r'Architecture Boundary',
            r'NO LLM',
            r'Tab 5'
        ]
        
        found_count = 0
        for keyword in required_keywords:
            if re.search(keyword, content, re.IGNORECASE):
                found_count += 1
        
        assert found_count >= 2, (
            f"Found {found_count}/3 architecture boundary keywords. "
            "Tab 5 must document 'Architecture Boundary: NO LLM calls' in comments."
        )


class TestTab5OutputJSONValidation:
    """Verify Tab 5 output JSONs have llm_enabled: false."""
    
    def test_guideline_jsons_have_llm_disabled(self):
        """
        RED: This test MAY FAIL (one JSON has llm_enabled: true).
        
        All guideline JSONs generated by Tab 5 must have "llm_enabled": false
        since Tab 5 uses statistical methods only.
        
        Reference: Grep search found Architecture Patterns JSON has llm_enabled: true
        """
        output_dir = Path("workflows/base_guideline_generation/output")
        json_files = list(output_dir.glob("*_guideline.json"))
        
        assert len(json_files) > 0, "No guideline JSON files found in output directory"
        
        violations: List[str] = []
        for json_file in json_files:
            content = json_file.read_text()
            
            # Check for "llm_enabled": true
            if re.search(r'"llm_enabled"\s*:\s*true', content, re.IGNORECASE):
                violations.append(json_file.name)
        
        assert len(violations) == 0, (
            f"Found {len(violations)} guideline JSONs with llm_enabled: true: {violations}. "
            "Tab 5 output must have llm_enabled: false (statistical methods only)."
        )


class TestLegacyLLMCodeRemoval:
    """Verify legacy LLM helper functions are fully removed or commented."""
    
    def test_no_llm_function_definitions(self):
        """
        RED: This test SHOULD PASS (functions removed, comments remain).
        
        Verify _try_llm_annotation and _try_llm_summary are removed.
        Comments about removal are acceptable.
        
        Reference: Lines 610, 743 have comments about removed functions
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Check for function definitions (not comments)
        forbidden_functions = [
            r'^def _try_llm_annotation\(',
            r'^def _try_llm_summary\(',
            r'^def.*llm.*annotation\(',
            r'^def.*llm.*summary\('
        ]
        
        violations: List[str] = []
        for pattern in forbidden_functions:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                violations.extend(matches)
        
        assert len(violations) == 0, (
            f"Found {len(violations)} LLM function definitions: {violations}. "
            "Legacy LLM functions must be removed from Tab 5."
        )
    
    def test_removal_comments_present(self):
        """
        RED: This test SHOULD PASS (comments exist).
        
        Verify removal is documented so developers know functions existed
        and were intentionally removed (not accidentally deleted).
        
        Reference: ANTI_PATTERN_ANALYSIS §9.11 (TODO comments → issue references)
        """
        file_path = Path("workflows/base_guideline_generation/scripts/chapter_generator_all_text.py")
        content = file_path.read_text()
        
        # Check for removal documentation
        removal_patterns = [
            r'_try_llm_annotation removed',
            r'_try_llm_summary removed',
            r'removed.*LLM',
            r'Tab 7.*LLM'
        ]
        
        found_count = 0
        for pattern in removal_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_count += 1
        
        assert found_count >= 2, (
            f"Found {found_count}/4 removal documentation patterns. "
            "LLM function removal must be documented to prevent accidental re-introduction."
        )
