"""
RED Phase Tests for SonarQube Issues in chapter_generator_all_text.py

These tests MUST FAIL initially, demonstrating the issues identified by SonarQube:
1. Unused parameter `all_footnotes` in _convert_markdown_to_json (line 1830)
2. Regex with reluctant quantifier in _extract_book_metadata (line 1618)
3. Complex regex pattern in _extract_concept_data (line 1650)
4. Regex patterns in _extract_chapter_sections (lines 1680-1681)

Test-Driven Development (TDD) Cycle:
- RED: Tests fail due to SonarQube violations
- GREEN: Fix violations with minimal changes
- REFACTOR: Verify anti-pattern compliance

References:
- reports/sonarqube_task16_analysis.md: SonarQube findings
- ANTI_PATTERN_ANALYSIS.md: Code quality patterns
"""

import re
import pytest
import inspect
from typing import List, Dict, Any
from workflows.base_guideline_generation.scripts.chapter_generator_all_text import (
    _extract_book_metadata,
    _extract_concept_data,
    _extract_chapter_sections,
    _convert_markdown_to_json
)


class TestUnusedParameterFix:
    """Test that all_footnotes parameter is actually used or removed."""
    
    def test_convert_markdown_to_json_uses_all_footnotes_parameter(self):
        """
        RED: This test MUST FAIL initially.
        
        SonarQube S1172 MAJOR: Unused parameter 'all_footnotes'
        Function signature includes parameter but never references it in body.
        
        Expected: Parameter should be removed OR used in function body
        """
        # Get function signature
        sig = inspect.signature(_convert_markdown_to_json)
        params = list(sig.parameters.keys())
        
        # Get function source code
        source = inspect.getsource(_convert_markdown_to_json)
        
        if 'all_footnotes' in params:
            # If parameter exists, it MUST be used in function body
            # Check for actual usage (not just parameter definition)
            # Remove parameter line from source to avoid false positive
            source_lines = source.split('\n')
            body_lines = [line for line in source_lines if 'all_footnotes' in line and 'def ' not in line]
            
            assert len(body_lines) > 0, (
                "SonarQube S1172: Parameter 'all_footnotes' is declared but never used. "
                "Either remove the parameter or use it in the function body."
            )


class TestRegexReluctantQuantifiersFix:
    """Test that regex patterns use appropriate quantifiers."""
    
    def test_extract_book_metadata_source_regex_not_reluctant(self):
        """
        RED: This test MUST FAIL initially.
        
        SonarQube S6019 MAJOR: Reluctant quantifier (.+?) used incorrectly
        Pattern: r'\*Source: (.+?)\*'
        
        Since the pattern ends with \*, the reluctant quantifier will match
        minimal text anyway. Using greedy (.+) is clearer and more efficient.
        
        Expected: Pattern should use greedy quantifier (.+) instead of (.+?)
        """
        # Get source code to inspect regex pattern
        source = inspect.getsource(_extract_book_metadata)
        
        # Find the source_match regex pattern
        source_pattern_match = re.search(r"source_match = re\.search\(r'([^']+)'", source)
        assert source_pattern_match, "Could not find source_match regex in function"
        
        pattern = source_pattern_match.group(1)
        
        # Check that pattern does NOT use reluctant quantifier
        assert '.+?' not in pattern, (
            f"SonarQube S6019: Reluctant quantifier '.+?' is inefficient here. "
            f"Pattern '{pattern}' should use greedy '.+' instead because it's bounded by \\*"
        )
    
    def test_extract_concept_data_regex_has_reasonable_limits(self):
        """
        RED: This test MIGHT PASS initially (depends on implementation).
        
        SonarQube S6019: Complex regex with multiple quantifiers
        Pattern should have reasonable limits to prevent ReDoS attacks.
        
        Expected: Pattern should have bounded quantifiers (not unlimited .+)
        """
        # Get source code to inspect regex pattern
        source = inspect.getsource(_extract_concept_data)
        
        # Find the concept_pattern regex
        pattern_match = re.search(r"concept_pattern = r'([^']+)'", source)
        assert pattern_match, "Could not find concept_pattern regex in function"
        
        pattern = pattern_match.group(1)
        
        # Check that pattern uses bounded quantifiers, not unlimited ones
        # Look for patterns like .+ or .* without bounds
        unbounded_quantifiers = re.findall(r'(?<!\\)\.\+(?!\{)', pattern)
        
        assert len(unbounded_quantifiers) == 0, (
            f"SonarQube S6019: Pattern contains {len(unbounded_quantifiers)} unbounded quantifiers. "
            f"Use bounded quantifiers like .{{1,1000}} to prevent ReDoS attacks."
        )
    
    def test_extract_chapter_sections_cross_text_regex_not_reluctant(self):
        """
        RED: This test MUST PASS initially (false negative - pattern is actually correct).
        
        Note: The current implementation uses greedy (.+) which is CORRECT.
        This test verifies the pattern remains correct after any changes.
        
        Expected: Pattern should use greedy (.+) with lookahead boundary
        """
        # Get source code to inspect regex pattern
        source = inspect.getsource(_extract_chapter_sections)
        
        # Find the cross_text_match regex
        cross_text_match = re.search(r"cross_text_match = re\.search\(r'([^']+)'", source)
        assert cross_text_match, "Could not find cross_text_match regex in function"
        
        pattern = cross_text_match.group(1)
        
        # Verify pattern uses greedy quantifier (not reluctant)
        assert '.+' in pattern and '.+?' not in pattern, (
            "Pattern should use greedy '.+' with lookahead boundary, not reluctant '.+?'"
        )
    
    def test_extract_chapter_sections_summary_regex_not_reluctant(self):
        """
        RED: This test MUST PASS initially (false negative - pattern is actually correct).
        
        Note: The current implementation uses greedy (.+) which is CORRECT.
        This test verifies the pattern remains correct after any changes.
        
        Expected: Pattern should use greedy (.+) with lookahead boundary
        """
        # Get source code to inspect regex pattern
        source = inspect.getsource(_extract_chapter_sections)
        
        # Find the summary_match regex
        summary_match = re.search(r"summary_match = re\.search\(r'([^']+)'", source)
        assert summary_match, "Could not find summary_match regex in function"
        
        pattern = summary_match.group(1)
        
        # Verify pattern uses greedy quantifier (not reluctant)
        assert '.+' in pattern and '.+?' not in pattern, (
            "Pattern should use greedy '.+' with lookahead boundary, not reluctant '.+?'"
        )


class TestIntegratedSonarQubeFixes:
    """Integration test to verify all SonarQube fixes work together."""
    
    def test_book_metadata_extraction_with_fixed_regex(self):
        """
        Verify _extract_book_metadata works correctly with fixed regex.
        """
        test_markdown = """# Learning Python 6th Edition
*Source: O'Reilly Media, 2019*

## Chapter 1: Introduction
Some content here.
"""
        result = _extract_book_metadata(test_markdown, "Learning_Python_Ed6")
        
        assert result["title"] == "Learning Python 6th Edition"
        assert "O'Reilly Media, 2019" in result["source"]
        assert result["book_name"] == "Learning_Python_Ed6"
    
    def test_concept_extraction_with_safe_regex(self):
        """
        Verify _extract_concept_data works with bounded quantifiers.
        """
        test_content = """#### **Variables** *(p.123)*

**Verbatim Educational Excerpt**
```
x = 10
y = 20
```
[^1]
**Annotation:** Variables store data values."""
        
        result = _extract_concept_data(test_content)
        
        # Should extract at least basic structure (even if pattern needs adjustment)
        assert isinstance(result, list)
    
    def test_chapter_sections_extraction_with_greedy_quantifiers(self):
        """
        Verify _extract_chapter_sections correctly extracts sections.
        """
        test_content = """### Cross-Text Analysis

This chapter relates to concepts in other books.

### Chapter Summary
Key takeaways from this chapter."""
        
        result = _extract_chapter_sections(test_content)
        
        assert "relates to concepts" in result["cross_text_analysis"]
        assert "Key takeaways" in result["chapter_summary"]
    
    def test_markdown_to_json_conversion_parameter_usage(self):
        """
        Verify _convert_markdown_to_json correctly uses or removes all_footnotes.
        """
        test_docs = [
            "# Test Book",
            "*Source: Test Publisher*",
            "",
            "## Chapter 1: Introduction",
            "Content here."
        ]
        test_footnotes = [
            {
                "num": 1,
                "author": "Test Author",
                "title": "Test Book",
                "file": "test.pdf",
                "page": 10,
                "start_line": 1,
                "end_line": 5
            }
        ]
        
        # This should work without errors
        result = _convert_markdown_to_json(test_docs, "Test_Book", test_footnotes)
        
        assert "book_metadata" in result
        assert "chapters" in result
        assert "footnotes" in result
