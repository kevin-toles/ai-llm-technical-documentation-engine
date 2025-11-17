"""
Integration tests for complete pipeline: PDF → JSON → Metadata → LLM → Annotations

References:
- Architecture Patterns with Python Ch. 3 (Service Layer Testing) pp. 45-65
- Architecture Patterns with Python Ch. 5 (TDD High Gear) pp. 85-100
- Python Distilled Ch. 14.6 (Integration Testing Patterns) pp. 250-255
- Building Microservices Ch. 7 (Testing) pp. 125-140
- Microservices Up and Running Ch. 8 (Testing Microservices) pp. 145-160

Sprint 4 Day 6: Integration testing to verify all pipeline stages work together.
Testing Philosophy: Mock only external LLM API, use real implementations for owned code.
"""

import json
import pytest
import fitz  # PyMuPDF

from workflows.pdf_to_json.scripts.convert_pdf_to_json import convert_pdf_to_json
from workflows.metadata_enrichment.scripts.generate_chapter_metadata import (
    generate_chapter_summary,
    extract_keywords_from_text,
    extract_concepts_from_text,
)
from shared.providers.base import LLMResponse


# ============================================================================
# Test Infrastructure: Fake LLM Provider
# Reference: Architecture Patterns with Python Ch. 3 pp. 50-55
# ============================================================================


class FakeLLMProvider:
    """
    Deterministic LLM provider for integration testing.
    
    Pattern: Test Double (Architecture Patterns Ch. 3)
    - Implements same interface as real provider
    - Returns deterministic responses
    - Tracks call history for assertions
    """
    
    def __init__(self, responses=None, fail_count=0):
        """
        Args:
            responses: List of response strings (cycled through)
            fail_count: Fail first N calls (for retry testing)
        """
        self.responses = responses or ['{"annotations": ["Sample annotation"]}']
        self.fail_count = fail_count
        self.call_count = 0
        self.call_history = []
    
    def call(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.0,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Return deterministic response or simulate failure."""
        self.call_count += 1
        self.call_history.append({
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system_prompt": system_prompt,
        })
        
        # Simulate failure for retry testing
        if self.call_count <= self.fail_count:
            raise ValueError(f"Simulated LLM failure (attempt {self.call_count})")
        
        # Return deterministic response
        response_index = (self.call_count - self.fail_count - 1) % len(self.responses)
        return LLMResponse(
            content=self.responses[response_index],
            model="fake-gpt-4",
            input_tokens=100,
            output_tokens=200,
            stop_reason="end_turn",
        )
    
    @property
    def model_name(self) -> str:
        """Model identifier for testing."""
        return "fake-gpt-4"
    
    @property
    def provider_name(self) -> str:
        """Provider name for testing."""
        return "fake"


# ============================================================================
# Test Fixtures: Environment Builders
# Reference: Microservices Up and Running Ch. 8 pp. 150-155
# ============================================================================


@pytest.fixture
def sample_pdf_path(tmp_path):
    """
    Create realistic test PDF for integration testing.
    
    Pattern: Fixture Composition (Python Distilled Ch. 14.6)
    - Creates multi-chapter PDF
    - Uses tmp_path for isolation
    - Cleaned up automatically after test
    """
    pdf_path = tmp_path / "integration_test_book.pdf"
    doc = fitz.open()
    
    # Chapter 1: Introduction
    page1 = doc.new_page()
    page1.insert_text((72, 72), "Chapter 1: Introduction to Python Testing")
    page1.insert_text((72, 120), "This chapter covers pytest, fixtures, and mocking.")
    page1.insert_text((72, 150), "Testing is essential for maintaining code quality.")
    
    # Chapter 2: Advanced Topics
    page2 = doc.new_page()
    page2.insert_text((72, 72), "Chapter 2: Advanced Testing Patterns")
    page2.insert_text((72, 120), "Integration testing verifies components work together.")
    page2.insert_text((72, 150), "Mock external dependencies, test real implementations.")
    
    doc.save(str(pdf_path))
    doc.close()
    
    return pdf_path


@pytest.fixture
def integration_environment(tmp_path, sample_pdf_path):
    """
    Complete test environment for integration tests.
    
    Pattern: Test Data Builder (Microservices Up and Running Ch. 8)
    - Provides all resources needed for pipeline
    - Isolated using tmp_path
    - Returns structured environment dict
    """
    return {
        "pdf_path": sample_pdf_path,
        "json_path": tmp_path / "book_data.json",
        "output_dir": tmp_path / "output",
        "cache_dir": tmp_path / "cache",
    }


@pytest.fixture
def fake_llm_provider():
    """Reusable fake LLM provider for integration tests."""
    return FakeLLMProvider(
        responses=[
            '{"annotations": ["Test annotation 1"]}',
            '{"annotations": ["Test annotation 2"]}',
        ]
    )


# ============================================================================
# Test Suite 1: End-to-End Pipeline Tests
# Reference: Architecture Patterns Ch. 5 - TDD in High Gear (pp. 85-100)
# ============================================================================


class TestPipelineEndToEnd:
    """
    Full pipeline integration tests: PDF → JSON → Metadata → LLM → Annotations
    
    Testing Philosophy (Architecture Patterns Ch. 5):
    - "High Gear TDD": Write end-to-end test first
    - Define success criteria from user perspective
    - Mock only external services (LLM API)
    """
    
    def test_complete_pipeline_pdf_to_annotations(self, integration_environment, fake_llm_provider):
        """
        Test complete pipeline flow with all stages integrated.
        
        Reference: Architecture Patterns Ch. 5 p. 85 (High Gear TDD)
        Pattern: End-to-end integration test
        
        Pipeline:
        1. PDF → JSON (convert_pdf_to_json)
        2. JSON → Metadata (generate_chapter_metadata)
        3. Metadata → LLM (fake_llm_provider)
        4. LLM → Annotations
        
        Note: convert_pdf_to_json creates a flat pages structure, not chapters.
        Chapter detection happens in a separate step.
        """
        # Given: A valid PDF
        pdf_path = integration_environment["pdf_path"]
        json_path = integration_environment["json_path"]
        
        # When: Pipeline processes PDF to JSON
        success = convert_pdf_to_json(str(pdf_path), str(json_path))
        
        # Then: JSON created successfully
        assert success is True
        assert json_path.exists()
        
        # When: Load JSON and extract metadata
        with open(json_path) as f:
            book_data = json.load(f)
        
        # Then: JSON has expected structure (flat pages, empty chapters initially)
        assert "pages" in book_data
        assert len(book_data["pages"]) > 0
        
        # When: Generate chapter summary and metadata from pages
        # Simulate treating all pages as one chapter for testing
        all_pages = book_data["pages"]
        chapter_text = " ".join(page["content"] for page in all_pages)
        keywords = extract_keywords_from_text(chapter_text)
        concepts = extract_concepts_from_text(chapter_text)
        summary = generate_chapter_summary(
            all_pages,
            "Test Chapter",
            keywords,
            concepts
        )
        
        # Then: Metadata extracted successfully
        assert len(keywords) > 0
        assert len(concepts) > 0
        assert len(summary) > 0
        
        # When: Call LLM provider with metadata
        prompt = f"Summary: {summary}\nKeywords: {', '.join(keywords)}"
        response = fake_llm_provider.call(prompt, max_tokens=1000)
        
        # Then: LLM response contains annotations
        assert response.content is not None
        assert "annotations" in response.content.lower()
        assert fake_llm_provider.call_count == 1
    
    def test_pipeline_processes_multiple_pages(self, integration_environment, fake_llm_provider):
        """
        Test pipeline handles multi-page PDFs correctly.
        
        Reference: Building Microservices Ch. 7 p. 128 (Integration Testing)
        Pattern: Verify behavior with realistic data
        
        Note: convert_pdf_to_json creates flat pages structure.
        """
        # Given: PDF with multiple pages
        pdf_path = integration_environment["pdf_path"]
        json_path = integration_environment["json_path"]
        
        # When: Convert to JSON
        convert_pdf_to_json(str(pdf_path), str(json_path))
        
        with open(json_path) as f:
            book_data = json.load(f)
        
        # Then: All pages processed
        assert "pages" in book_data
        assert len(book_data["pages"]) == 2  # Our test PDF has 2 pages
        
        # When: Process pages for metadata extraction
        all_text = " ".join(page["content"] for page in book_data["pages"])
        keywords = extract_keywords_from_text(all_text)
        concepts = extract_concepts_from_text(all_text)
        
        # Then: Metadata extracted from all pages
        assert len(keywords) > 0
        assert len(concepts) > 0
    
    def test_pipeline_with_fake_llm_provider_integration(self, integration_environment):
        """
        Test that fake LLM provider integrates correctly with pipeline.
        
        Reference: Architecture Patterns Ch. 3 p. 52 (Service Layer with Fakes)
        Pattern: Integration test with test double
        """
        # Given: Fake LLM with specific responses
        fake_llm = FakeLLMProvider(
            responses=['{"annotations": ["Custom annotation"]}']
        )
        
        # When: Call provider multiple times
        response1 = fake_llm.call("Test prompt 1")
        response2 = fake_llm.call("Test prompt 2")
        
        # Then: Returns deterministic responses
        assert response1.content == '{"annotations": ["Custom annotation"]}'
        assert response2.content == '{"annotations": ["Custom annotation"]}'
        assert fake_llm.call_count == 2
        assert len(fake_llm.call_history) == 2


# ============================================================================
# Test Suite 2: Stage Boundary Integration
# Reference: Building Microservices Ch. 7 - Contract Testing (pp. 130-135)
# ============================================================================


class TestStageBoundaries:
    """
    Verify stage interfaces integrate correctly (contract testing).
    
    Pattern: Consumer-Driven Contracts (Building Microservices Ch. 7)
    - Each stage must produce output compatible with next stage
    - Test the "seams" between components
    """
    
    def test_pdf_json_metadata_integration(self, sample_pdf_path, tmp_path):
        """
        Test PDF → JSON → Metadata integration boundary.
        
        Reference: Building Microservices Ch. 7 p. 130 (Contract Testing)
        Verify: JSON structure from PDF matches metadata input requirements
        
        Note: convert_pdf_to_json creates flat pages structure.
        """
        # Given: PDF converted to JSON
        json_path = tmp_path / "test_book.json"
        convert_pdf_to_json(str(sample_pdf_path), str(json_path))
        
        with open(json_path) as f:
            book_data = json.load(f)
        
        # When: Extract metadata from JSON structure (using pages array)
        pages = book_data["pages"]
        chapter_text = " ".join(page["content"] for page in pages)
        
        # Then: JSON provides required fields for metadata extraction
        assert isinstance(pages, list)
        assert all("content" in page for page in pages)
        assert all("page_number" in page for page in pages)
        
        # Then: Metadata functions accept JSON structure
        keywords = extract_keywords_from_text(chapter_text)
        concepts = extract_concepts_from_text(chapter_text)
        
        assert isinstance(keywords, list)
        assert isinstance(concepts, list)
    
    def test_metadata_llm_integration(self, fake_llm_provider):
        """
        Test Metadata → LLM Provider integration boundary.
        
        Reference: Python Distilled Ch. 14.6 p. 252 (Integration Patterns)
        Verify: Metadata output format compatible with LLM prompt
        """
        # Given: Metadata extracted from text
        sample_text = "Python testing using pytest and fixtures"
        keywords = extract_keywords_from_text(sample_text)
        concepts = extract_concepts_from_text(sample_text)
        
        # When: Construct LLM prompt from metadata
        prompt = f"Keywords: {', '.join(keywords)}\nConcepts: {', '.join(concepts)}"
        
        # Then: Prompt format accepted by LLM provider
        response = fake_llm_provider.call(prompt)
        assert response.content is not None
        assert fake_llm_provider.call_count == 1
    
    def test_json_structure_matches_expected_format(self, sample_pdf_path, tmp_path):
        """
        Test JSON output structure matches expected schema.
        
        Reference: REFACTORING_PLAN.md (Enhanced JSON validation)
        Verify: JSON contains required fields for downstream processing
        
        Note: convert_pdf_to_json creates flat pages structure with empty chapters array.
        """
        # Given: PDF converted to JSON
        json_path = tmp_path / "test_book.json"
        convert_pdf_to_json(str(sample_pdf_path), str(json_path))
        
        # When: Load and validate JSON structure
        with open(json_path) as f:
            book_data = json.load(f)
        
        # Then: JSON has required top-level fields
        assert "metadata" in book_data
        assert "chapters" in book_data  # Empty initially
        assert "pages" in book_data  # Contains actual page data
        
        # Then: Each page has required fields
        for page in book_data["pages"]:
            assert "page_number" in page
            assert "content" in page


# ============================================================================
# Test Suite 3: Error Propagation and Recovery
# Reference: Python Distilled Ch. 14.4 - Exception Testing
# ============================================================================


class TestErrorPropagation:
    """
    Verify error handling across pipeline stages.
    
    Pattern: Exception Testing (Python Distilled Ch. 14.4)
    - Test error cases at each boundary
    - Verify graceful degradation
    """
    
    def test_invalid_pdf_fails_gracefully(self, tmp_path):
        """
        Test pipeline handles invalid PDF without crashing.
        
        Reference: Python Distilled Ch. 14.4 (Exception Testing)
        Pattern: Verify graceful failure
        """
        # Given: Invalid PDF file
        invalid_pdf = tmp_path / "invalid.pdf"
        invalid_pdf.write_bytes(b"Not a real PDF")
        
        json_path = tmp_path / "output.json"
        
        # When: Attempt to convert invalid PDF
        result = convert_pdf_to_json(str(invalid_pdf), str(json_path))
        
        # Then: Returns False (graceful failure)
        assert result is False
    
    def test_llm_failure_can_be_detected(self):
        """
        Test LLM provider failures are detectable.
        
        Reference: Architecture Patterns Ch. 3 p. 55 (Error Handling)
        Pattern: Test exception propagation
        """
        # Given: Fake LLM that always fails
        failing_llm = FakeLLMProvider(fail_count=999)
        
        # When: Call failing LLM
        # Then: Raises exception
        with pytest.raises(Exception, match="Simulated LLM failure"):
            failing_llm.call("Test prompt")
    
    def test_empty_chapter_metadata_extraction_handles_gracefully(self):
        """
        Test metadata extraction with empty chapter.
        
        Reference: Sprint 4 Day 5 edge case testing patterns
        Pattern: Verify edge case handling
        """
        # Given: Empty text
        empty_text = ""
        
        # When: Extract metadata
        keywords = extract_keywords_from_text(empty_text)
        concepts = extract_concepts_from_text(empty_text)
        
        # Then: Returns empty lists (graceful handling)
        assert keywords == []
        assert concepts == []


# ============================================================================
# Test Suite 4: Performance and Baseline
# Reference: Microservices Up and Running Ch. 8 - Performance Testing
# ============================================================================


class TestPerformanceBaseline:
    """
    Establish performance baselines for integration scenarios.
    
    Pattern: Performance Testing (Microservices Up and Running Ch. 8)
    - Measure execution time for baseline comparison
    - Track metrics for future optimization
    """
    
    def test_pipeline_performance_baseline(self, integration_environment, fake_llm_provider):
        """
        Measure baseline performance for complete pipeline.
        
        Reference: Microservices Up and Running Ch. 8 pp. 155-160
        Pattern: Baseline measurement (not strict timing)
        """
        import time
        
        # Given: Complete pipeline environment
        pdf_path = integration_environment["pdf_path"]
        json_path = integration_environment["json_path"]
        
        # When: Measure pipeline execution
        start_time = time.time()
        
        # PDF → JSON
        convert_pdf_to_json(str(pdf_path), str(json_path))
        
        # JSON → Metadata
        with open(json_path) as f:
            book_data = json.load(f)
        
        for chapter in book_data["chapters"]:
            chapter_text = " ".join(page["content"] for page in chapter["pages"])
            extract_keywords_from_text(chapter_text)
            extract_concepts_from_text(chapter_text)
        
        # Metadata → LLM
        fake_llm_provider.call("Test prompt")
        
        elapsed = time.time() - start_time
        
        # Then: Pipeline completes in reasonable time
        # Note: This is a baseline, not a strict requirement
        # Typical values: < 1 second for test PDF
        assert elapsed < 5.0  # Generous upper bound
        
        # Log baseline for future reference
        print(f"\nPipeline baseline: {elapsed:.3f}s")
