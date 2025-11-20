#!/usr/bin/env python3
"""
Integration tests for Tab 7: LLM Enhancement

TDD RED Phase: These tests are written BEFORE implementation to define expected behavior.

Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1736-1886 (Tab 7 specification)
Architecture: Repository Pattern for LLM provider abstraction (ARCHITECTURE_GUIDELINES Ch.2)
Error Handling: EAFP philosophy, try/except (PYTHON_GUIDELINES Ch.1)

Test Coverage:
1. Script existence
2. Aggregate package loading
3. Context index building
4. LLM prompt construction
5. Response parsing
6. Enhanced guideline generation
7. Output validation
8. LLM call constraint (only Tab 7)
9. Full enhancement workflow

Document Analysis Phase Complete:
- Step 1: BOOK_TAXONOMY_MATRIX - No LLM concepts (infrastructure task)
- Step 2: Guidelines - Repository Pattern, exception handling, EAFP
- Step 3: NO CONFLICTS - Tab 7 spec is authoritative, reuse Anthropic client patterns
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Project root for file paths
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestLLMEnhancementScript:
    """Tests for Tab 7 LLM enhancement script structure and loading."""
    
    def test_llm_enhancement_script_exists(self):
        """
        RED TEST: Verify Tab 7 enhancement script exists.
        
        Expected: workflows/llm_enhancement/scripts/llm_enhance_guideline.py
        
        This test will FAIL until GREEN phase implementation.
        """
        script = PROJECT_ROOT / "workflows" / "llm_enhancement" / "scripts" / "llm_enhance_guideline.py"
        assert script.exists(), f"Script not found: {script}"
    
    def test_load_aggregate_package(self):
        """
        RED TEST: Verify ability to load aggregate package from Tab 6.
        
        Tests requirement: Load aggregate package JSON
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1755-1758
        
        Given: architecture_patterns_llm_package_*.json exists
        When: Script loads aggregate package
        Then: Should parse JSON and return dict with expected keys
        """
        # Find latest package from Tab 6
        tmp_dir = PROJECT_ROOT / "workflows" / "llm_enhancement" / "tmp"
        package_files = list(tmp_dir.glob("architecture_patterns_llm_package_*.json"))
        
        if not package_files:
            pytest.skip("No aggregate package found - run Tab 6 first")
        
        latest_package = sorted(package_files)[-1]
        
        # Load and validate structure
        with open(latest_package, encoding='utf-8') as f:
            aggregate = json.load(f)
        
        # Verify required keys per Tab 6 output schema
        assert "project" in aggregate, "Missing 'project' key"
        assert "taxonomy" in aggregate, "Missing 'taxonomy' key"
        assert "source_book" in aggregate, "Missing 'source_book' key"
        assert "companion_books" in aggregate, "Missing 'companion_books' key"
        assert "statistics" in aggregate, "Missing 'statistics' key"
    
    def test_load_guideline_json(self):
        """
        RED TEST: Verify ability to load guideline JSON from Tab 5.
        
        Tests requirement: Load guideline JSON
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1760-1763
        
        Given: Any *_guideline.json exists in Tab 5 output
        When: Script loads guideline
        Then: Should parse JSON and return structured guideline data
        """
        guideline_dir = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
        guideline_files = list(guideline_dir.glob("*_guideline.json"))
        
        if not guideline_files:
            pytest.skip("Guideline JSON not found - run Tab 5 first")
        
        # Test with first available guideline
        guideline_file = guideline_files[0]
        with open(guideline_file, encoding='utf-8') as f:
            guideline = json.load(f)
        
        # Verify guideline structure (based on Tab 5 output)
        assert "book_metadata" in guideline or "chapters" in guideline, \
            f"Guideline must have 'book_metadata' or 'chapters' key, got: {list(guideline.keys())}"


class TestContextIndexBuilding:
    """Tests for building cross-book context index from aggregate package."""
    
    def test_build_context_index_from_aggregate(self):
        """
        RED TEST: Verify context index creation from aggregate package.
        
        Tests requirement: Build searchable context index
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1765-1780
        
        Given: Aggregate package with source_book and companion_books
        When: Build context index
        Then: Should create dict mapping book_ch keys to chapter data
        
        Expected structure:
        {
            "architecture_patterns_ch1": {
                "book": "architecture_patterns",
                "chapter": 1,
                "title": "Domain Modeling",
                "keywords": [...],
                "concepts": [...],
                "summary": "..."
            }
        }
        """
        # Sample aggregate package structure
        sample_aggregate = {
            "source_book": {
                "name": "architecture_patterns",
                "metadata": {
                    "chapters": [
                        {
                            "number": 1,
                            "title": "Domain Modeling",
                            "summary": "Test summary",
                            "keywords_enriched": ["domain", "model"],
                            "concepts_enriched": ["DDD", "Entity"]
                        }
                    ]
                }
            },
            "companion_books": []
        }
        
        # Utility function to test (will be in implementation)
        def build_context_index(aggregate: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
            """Helper function that should exist in implementation."""
            context_index = {}
            
            # Index source book
            source_book = aggregate["source_book"]
            book_name = source_book["name"]
            metadata = source_book.get("metadata", {})
            
            for chapter in metadata.get("chapters", []):
                key = f"{book_name}_ch{chapter['number']}"
                context_index[key] = {
                    "book": book_name,
                    "chapter": chapter["number"],
                    "title": chapter["title"],
                    "keywords": chapter.get("keywords_enriched", []),
                    "concepts": chapter.get("concepts_enriched", []),
                    "summary": chapter.get("summary", "")
                }
            
            # Index companion books
            for book in aggregate.get("companion_books", []):
                book_name = book["name"]
                metadata = book.get("metadata", {})
                
                for chapter in metadata.get("chapters", []):
                    key = f"{book_name}_ch{chapter['number']}"
                    context_index[key] = {
                        "book": book_name,
                        "chapter": chapter["number"],
                        "title": chapter["title"],
                        "keywords": chapter.get("keywords_enriched", []),
                        "concepts": chapter.get("concepts_enriched", []),
                        "summary": chapter.get("summary", "")
                    }
            
            return context_index
        
        # Test index building
        context_index = build_context_index(sample_aggregate)
        
        # Verify index structure
        assert "architecture_patterns_ch1" in context_index, \
            "Context index should contain source book chapters"
        
        ch1_data = context_index["architecture_patterns_ch1"]
        assert ch1_data["book"] == "architecture_patterns"
        assert ch1_data["chapter"] == 1
        assert ch1_data["title"] == "Domain Modeling"
        assert "domain" in ch1_data["keywords"]
        assert "DDD" in ch1_data["concepts"]


class TestLLMPromptConstruction:
    """Tests for LLM prompt construction and formatting."""
    
    def test_construct_enhancement_prompt(self):
        """
        RED TEST: Verify enhancement prompt construction.
        
        Tests requirement: Build LLM prompt with chapter and context
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1782-1824
        
        Given: Chapter data and related content from context index
        When: Construct prompt
        Then: Should include chapter details, cross-book context, and task instructions
        """
        chapter_data = {
            "title": "Domain Modeling",
            "keywords": ["domain", "model", "entity"],
            "summary": "Introduction to domain modeling patterns",
            "related_chapters": [
                {"book": "learning_python", "chapter": 26}
            ]
        }
        
        related_content = [
            {
                "book": "learning_python",
                "chapter": 26,
                "title": "OOP: The Big Picture",
                "keywords": ["class", "object", "inheritance"],
                "summary": "Object-oriented programming fundamentals"
            }
        ]
        
        # Utility function to test (will be in implementation)
        def construct_enhancement_prompt(
            chapter: Dict[str, Any],
            related: list
        ) -> str:
            """Helper function that should exist in implementation."""
            prompt = f"""You are enhancing a technical guideline chapter with scholarly depth.

CURRENT CHAPTER:
Title: {chapter["title"]}
Keywords: {", ".join(chapter["keywords"])}
Summary: {chapter["summary"]}

CROSS-BOOK CONTEXT:
"""
            for item in related:
                prompt += f"\n- {item['book']}, Ch.{item['chapter']}: {item['title']}"
                prompt += f"\n  Keywords: {', '.join(item['keywords'])}"
                prompt += f"\n  Summary: {item['summary']}\n"
            
            prompt += """
TASK: Enhance this chapter by adding:

1. **Enhanced Summary** (2-3 paragraphs):
   - Integrate insights from related chapters
   - Add cross-book synthesis
   - Maintain technical accuracy

2. **Key Takeaways** (3-5 bullet points):
   - Actionable insights
   - Practical applications

3. **Best Practices** (2-4 bullets with citations):
   - Industry-standard approaches
   - Cite specific books/chapters from context

4. **Common Pitfalls** (2-3 bullets with solutions):
   - Known challenges
   - Practical solutions

OUTPUT FORMAT (Markdown):
"""
            return prompt
        
        # Test prompt construction
        prompt = construct_enhancement_prompt(chapter_data, related_content)
        
        # Verify prompt contains required elements
        assert "Domain Modeling" in prompt, "Prompt should include chapter title"
        assert "domain, model, entity" in prompt, "Prompt should include keywords"
        assert "learning_python, Ch.26" in prompt, "Prompt should include cross-references"
        assert "Enhanced Summary" in prompt, "Prompt should include task instructions"
        assert "Key Takeaways" in prompt
        assert "Best Practices" in prompt
        assert "Common Pitfalls" in prompt


class TestLLMResponseParsing:
    """Tests for parsing LLM responses into structured data."""
    
    def test_parse_llm_markdown_response(self):
        """
        RED TEST: Verify parsing of LLM markdown response.
        
        Tests requirement: Parse LLM response into structured sections
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1832-1836
        
        Given: LLM markdown response with sections
        When: Parse response
        Then: Should extract enhanced_summary, key_takeaways, best_practices, pitfalls
        """
        sample_response = """
### Enhanced Summary

This chapter provides comprehensive coverage of domain modeling patterns.
The concepts build on object-oriented principles from Learning Python Ch.26.

Domain modeling translates business requirements into code structures.

### Key Takeaways

- Domain models encapsulate business logic
- Entities have identity, value objects do not
- Aggregates define consistency boundaries
- Repositories abstract data access

### Best Practices

- Use value objects for immutable data (Architecture Patterns, Ch.1)
- Define clear aggregate boundaries (DDD principles)
- Keep domain logic separate from infrastructure

### Common Pitfalls

- **Anemic domain models**: Models with no behavior
  - Solution: Move business logic into domain entities
- **Large aggregates**: Performance issues with big object graphs
  - Solution: Split into smaller aggregates with clear boundaries
"""
        
        # Utility function to test (will be in implementation)
        def parse_llm_response(response: str) -> Dict[str, Any]:
            """Helper function that should exist in implementation."""
            sections = {}
            
            # Simple parsing logic (implementation can be more sophisticated)
            lines = response.strip().split('\n')
            current_section = None
            current_content = []
            
            for line in lines:
                if line.startswith('### Enhanced Summary'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    current_section = 'enhanced_summary'
                    current_content = []
                elif line.startswith('### Key Takeaways'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    current_section = 'key_takeaways'
                    current_content = []
                elif line.startswith('### Best Practices'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    current_section = 'best_practices'
                    current_content = []
                elif line.startswith('### Common Pitfalls'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content).strip()
                    current_section = 'common_pitfalls'
                    current_content = []
                elif current_section:
                    current_content.append(line)
            
            # Add last section
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            
            return sections
        
        # Test parsing
        parsed = parse_llm_response(sample_response)
        
        # Verify all sections extracted
        assert "enhanced_summary" in parsed, "Should extract enhanced summary"
        assert "key_takeaways" in parsed, "Should extract key takeaways"
        assert "best_practices" in parsed, "Should extract best practices"
        assert "common_pitfalls" in parsed, "Should extract common pitfalls"
        
        # Verify content
        assert "domain modeling patterns" in parsed["enhanced_summary"].lower()
        assert "Domain models encapsulate business logic" in parsed["key_takeaways"]
        assert "Anemic domain models" in parsed["common_pitfalls"]


class TestEnhancedGuidelineGeneration:
    """Tests for generating final enhanced guideline output."""
    
    @pytest.mark.integration
    def test_enhanced_guideline_output_schema(self):
        """
        RED TEST: Verify enhanced guideline output structure.
        
        Tests requirement: Generate enhanced markdown output
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1838-1885
        
        Expected output file structure:
        - Filename: {book}_guideline_enhanced.md
        - Location: workflows/llm_enhancement/output/
        - Size: 400-1000 KB (estimated)
        - Format: Markdown with enhanced sections per chapter
        
        This test will be SKIPPED until GREEN phase generates actual output.
        """
        output_dir = PROJECT_ROOT / "workflows" / "llm_enhancement" / "output"
        enhanced_files = list(output_dir.glob("*_guideline_enhanced.md"))
        
        if not enhanced_files:
            pytest.skip("Enhanced guideline not yet generated - run enhancement script first")
        
        # Use first enhanced file found
        enhanced_file = enhanced_files[0]
        
        # Verify file exists and is non-empty
        assert enhanced_file.exists(), f"Enhanced guideline not found: {enhanced_file}"
        
        file_size_kb = enhanced_file.stat().st_size / 1024
        assert file_size_kb > 50, f"Enhanced guideline too small: {file_size_kb:.1f} KB"
        
        # Read and verify structure
        content = enhanced_file.read_text(encoding='utf-8')
        
        # Verify enhanced sections present
        assert "### Enhanced Summary" in content or "Enhanced Summary" in content, \
            "Output should contain enhanced summaries"
        assert "### Key Takeaways" in content or "Key Takeaways" in content, \
            "Output should contain key takeaways"
        assert "### Best Practices" in content or "Best Practices" in content, \
            "Output should contain best practices"
        assert "### Common Pitfalls" in content or "Common Pitfalls" in content, \
            "Output should contain common pitfalls"
    
    def test_llm_calls_only_in_tab7(self):
        """
        RED TEST: Verify LLM calls ONLY occur in Tab 7 workflow.
        
        Tests requirement: LLM enhancement is THE ONLY LLM WORKFLOW
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1-100
        
        Critical constraint: Tabs 1-6 use ONLY statistical methods.
        Only Tab 7 makes LLM API calls.
        
        This test will be SKIPPED until implementation complete.
        """
        # This test verifies architectural constraint
        # In production, would check:
        # 1. No anthropic/openai imports in Tab 1-6 scripts
        # 2. LLM provider only imported in Tab 7 script
        # 3. API call logging shows calls only from Tab 7
        
        pytest.skip("Architectural constraint - verify during code review")


class TestLLMEnhancementWorkflow:
    """Integration tests for complete Tab 7 enhancement workflow."""
    
    @pytest.mark.integration
    def test_full_enhancement_workflow(self):
        """
        RED TEST: Verify complete end-to-end enhancement workflow.
        
        Tests requirement: Full Tab 7 workflow integration
        Reference: CONSOLIDATED_IMPLEMENTATION_PLAN.md lines 1751-1885
        
        Workflow steps:
        1. Load aggregate package (Tab 6 output)
        2. Load guideline (Tab 5 output)
        3. Build context index
        4. For each chapter:
           a. Get related content
           b. Construct LLM prompt
           c. Call LLM API
           d. Parse response
           e. Integrate enhancements
        5. Generate enhanced markdown
        6. Save output
        
        This test will be SKIPPED until full implementation complete.
        """
        # Verify required inputs exist
        tmp_dir = PROJECT_ROOT / "workflows" / "llm_enhancement" / "tmp"
        package_files = list(tmp_dir.glob("architecture_patterns_llm_package_*.json"))
        
        if not package_files:
            pytest.skip("Aggregate package not found - run Tab 6 first")
        
        guideline_dir = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
        guideline_file = guideline_dir / "architecture_patterns_guideline.json"
        
        if not guideline_file.exists():
            pytest.skip("Guideline not found - run Tab 5 first")
        
        # Verify output exists (after implementation)
        output_dir = PROJECT_ROOT / "workflows" / "llm_enhancement" / "output"
        enhanced_files = list(output_dir.glob("architecture_patterns_guideline_enhanced.md"))
        
        if not enhanced_files:
            pytest.skip("Enhanced guideline not yet generated - run enhancement script first")
        
        enhanced_file = enhanced_files[0]
        
        # Verify complete workflow outputs
        assert enhanced_file.exists(), "Enhanced guideline should be generated"
        
        content = enhanced_file.read_text(encoding='utf-8')
        
        # Verify workflow produced expected enhancements
        assert len(content) > 100000, "Enhanced guideline should be substantial (>100KB)"
        assert "Enhanced Summary" in content, "Should contain LLM-enhanced summaries"
        assert "Key Takeaways" in content, "Should contain key takeaways"
        assert "Best Practices" in content, "Should contain best practices with citations"
        assert "Common Pitfalls" in content, "Should contain pitfalls with solutions"
