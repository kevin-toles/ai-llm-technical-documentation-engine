"""
TDD Tests for CSS SonarQube Issues (S4656 - Duplicate Properties)

RED Phase: Tests that verify CSS file does not contain duplicate properties
within the same rule block.

Per CODING_PATTERNS_ANALYSIS.md:
- S4656: Unexpected duplicate property - remove redundant declaration
"""

import re
from pathlib import Path

import pytest


class TestCSSNoDuplicateProperties:
    """Tests for S4656 - No duplicate CSS properties in same rule block."""

    @pytest.fixture
    def css_content(self) -> str:
        """Load the style.css file content."""
        css_path = Path(__file__).parent.parent.parent.parent / "ui" / "static" / "css" / "style.css"
        return css_path.read_text()

    def test_tab_class_has_no_duplicate_border_property(self, css_content: str) -> None:
        """S4656: .tab class should not have duplicate 'border' declarations.
        
        The .tab rule has both:
        - border: none; (line 95)
        - border: 1px solid transparent; (line 101)
        
        Only the latter should remain as it's the intended visual state.
        """
        # Extract .tab rule block
        tab_match = re.search(r'\.tab\s*\{([^}]+)\}', css_content)
        assert tab_match, ".tab class not found in CSS"
        
        tab_content = tab_match.group(1)
        
        # Count 'border:' declarations (not border-radius, border-bottom, etc.)
        border_declarations = re.findall(r'\bborder\s*:', tab_content)
        
        assert len(border_declarations) == 1, (
            f"Expected 1 'border:' declaration in .tab, found {len(border_declarations)}. "
            f"Remove duplicate border declaration per S4656."
        )

    def test_no_duplicate_properties_in_any_rule(self, css_content: str) -> None:
        """S4656: No rule block should have duplicate property declarations.
        
        This is a general check for any duplicate properties within a single rule.
        """
        # Extract all rule blocks
        rule_blocks = re.findall(r'([^{]+)\{([^}]+)\}', css_content)
        
        duplicates_found = []
        for selector, properties in rule_blocks:
            selector = selector.strip()
            # Extract property names (before the colon)
            prop_names = re.findall(r'^\s*([a-z-]+)\s*:', properties, re.MULTILINE)
            
            # Check for duplicates (excluding vendor prefixes like -webkit-)
            seen = {}
            for prop in prop_names:
                if prop.startswith('-'):  # Skip vendor prefixes
                    continue
                if prop in seen:
                    duplicates_found.append(f"{selector}: duplicate '{prop}'")
                seen[prop] = True
        
        assert not duplicates_found, (
            "Found duplicate properties in CSS rules (S4656):\n" +
            "\n".join(duplicates_found)
        )
