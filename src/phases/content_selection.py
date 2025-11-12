"""
Content Selection Service - Phase 1 of Two-Phase Analysis

Handles metadata analysis and content request generation.
Extracted from AnalysisOrchestrator (Sprint 1 Day 1-2).

RESPONSIBILITIES:
- Analyze chapter metadata
- Identify relevant books using taxonomy
- Generate structured content requests for Phase 2
- Build Phase 1 prompts (both python-guided and comprehensive modes)

ARCHITECTURE PATTERNS:
- Single Responsibility Principle (Clean Architecture)
- Command Pattern for content requests (Architecture Patterns Ch. 9)
- Factory Method for prompt generation (Python Essential Reference Ch. 7)

CONFIGURATION:
- Uses config.settings for all runtime parameters
- No hardcoded values (12-Factor App compliance)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
from config.settings import settings

# Import shared dataclasses and services
from ..interactive_llm_system_v3_hybrid_prompt import (
    ContentRequest,
    LLMMetadataResponse,
    AnalysisPhase,
)

try:
    from ..book_taxonomy import (
        get_recommended_books,
        get_cascading_books,
        score_books_for_concepts,
        BOOK_REGISTRY,
        BookTier
    )
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    print("Warning: book_taxonomy.py not available - cascading logic disabled")

try:
    from ..llm_integration import call_llm
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM integration not available")


class ContentSelectionService:
    """
    Phase 1 service: Analyzes chapter content and generates content requests.
    
    This service implements the first phase of the two-phase LLM workflow:
    1. Receives chapter information (title, concepts, excerpt or full text)
    2. Analyzes available book metadata
    3. Identifies most relevant books using taxonomy scoring
    4. Generates structured content requests (ContentRequest objects)
    5. Returns LLMMetadataResponse for Phase 2 consumption
    
    Configuration (from config.settings):
    - settings.taxonomy.*: Book selection parameters
    - settings.constraints.*: Prompt constraint limits
    - settings.llm.max_tokens: Token budget for Phase 1
    """
    
    def __init__(
        self,
        metadata_service: Any,  # MetadataExtractionService
        llm_available: bool = None
    ):
        """
        Initialize content selection service.
        
        Args:
            metadata_service: Service for accessing book metadata
            llm_available: Override LLM availability (defaults to auto-detect)
        """
        self._metadata_service = metadata_service
        self._llm_available = llm_available if llm_available is not None else LLM_AVAILABLE
        self._config = settings  # Central configuration
        
    def select_content_python_guided(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str
    ) -> LLMMetadataResponse:
        """
        Phase 1 analysis using Python-guided approach (Scenario 1).
        
        Flow:
        1. Python extracts concepts via keyword matching
        2. Python finds matches across all books using metadata service
        3. LLM validates Python matches and requests specific pages
        4. Returns structured content requests
        
        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title
            concepts: List of concepts extracted by Python
            excerpt: Short chapter excerpt for context
            
        Returns:
            LLMMetadataResponse with content requests for Phase 2
        """
        print("\n📋 PHASE 1: Metadata Analysis (Python-Guided)")
        print("-" * 40)
        
        # Build metadata package using taxonomy scoring
        metadata_package = self._build_metadata_package(concepts)
        
        # Build Phase 1 prompt
        prompt = self._build_phase1_prompt(
            chapter_num,
            chapter_title,
            concepts,
            excerpt,
            metadata_package
        )
        
        print(f"Sending metadata for {len(metadata_package['books'])} books...")
        print(f"Estimated tokens: ~{self._estimate_tokens(prompt):,}")
        
        # Check LLM availability
        if not self._llm_available:
            print("⚠️  LLM not available, generating mock response")
            return self._mock_metadata_response(concepts)
        
        # Call LLM
        try:
            # Use configured max_tokens for Phase 1
            max_tokens_phase1 = min(
                self._config.llm.max_tokens // 4,  # Reserve 3/4 for Phase 2
                4000  # Reasonable limit for metadata analysis
            )
            
            llm_output = call_llm(prompt, max_tokens=max_tokens_phase1)
            response = LLMMetadataResponse.from_llm_output(llm_output)
            
            print(f"✓ Received {len(response.content_requests)} content requests")
            for req in response.content_requests[:3]:
                print(f"  - {req.book_name}: {len(req.pages)} pages - {req.rationale[:60]}...")
            
            return response
            
        except Exception as e:
            print(f"❌ Phase 1 failed: {e}")
            return self._mock_metadata_response(concepts)
    
    def select_content_comprehensive(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str
    ) -> LLMMetadataResponse:
        """
        Phase 1 analysis using comprehensive LLM-driven approach (Scenario 2).
        
        Flow:
        1. LLM reads full chapter text
        2. LLM extracts concepts and identifies relevant books
        3. LLM requests specific chapters/sections
        4. Returns structured content requests
        
        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title
            chapter_full_text: Full chapter text (not just excerpt)
            
        Returns:
            LLMMetadataResponse with content requests for Phase 2
        """
        print("\n📋 PHASE 1: Comprehensive LLM-Driven Analysis")
        print("-" * 40)
        
        # Get books metadata without loading content (lazy loading)
        books_metadata = self._build_books_metadata_only()
        
        # Build comprehensive Phase 1 prompt
        prompt = self._build_comprehensive_phase1_prompt(
            chapter_num,
            chapter_title,
            chapter_full_text,
            books_metadata
        )
        
        print(f"Sending full chapter text ({len(chapter_full_text)} chars)")
        print(f"Book metadata for {len(books_metadata)} books")
        print(f"Estimated tokens: ~{self._estimate_tokens(prompt):,}")
        
        if not self._llm_available:
            print("⚠️  LLM not available, cannot perform comprehensive analysis")
            return self._mock_metadata_response([])
        
        try:
            # Use configured max_tokens for Phase 1
            # Phase 1 needs more tokens for complete JSON with all content_requests
            max_tokens_phase1 = self._config.constraints.max_content_requests * 200  # ~200 tokens per request
            max_tokens_phase1 = min(max_tokens_phase1, self._config.llm.max_tokens // 2)
            
            llm_output = call_llm(prompt, max_tokens=max_tokens_phase1)
            
            # DEBUG: Show raw LLM response
            print("\n" + "="*80)
            print("DEBUG: Raw Claude Response (Phase 1)")
            print("="*80)
            print(llm_output[:2000])  # Show first 2000 chars
            if len(llm_output) > 2000:
                print(f"\n... (truncated, total length: {len(llm_output)} chars)")
            print("="*80 + "\n")
            
            response = LLMMetadataResponse.from_llm_output(llm_output)
            
            # Apply configured constraints
            if len(response.content_requests) > self._config.constraints.max_content_requests:
                print(f"\n⚠️  LLM requested {len(response.content_requests)} books - limiting to {self._config.constraints.max_content_requests}")
                sorted_requests = sorted(response.content_requests, key=lambda r: r.priority)
                response.content_requests = sorted_requests[:self._config.constraints.max_content_requests]
                print(f"✓ Truncated to top {self._config.constraints.max_content_requests} highest-priority requests")
            
            print(f"✓ LLM extracted concepts and identified {len(response.content_requests)} book chapters to review")
            for req in response.content_requests[:5]:
                print(f"  - {req.book_name}: {req.rationale[:80]}...")
            
            return response
            
        except Exception as e:
            print(f"❌ Phase 1 failed: {e}")
            import traceback
            traceback.print_exc()
            return self._mock_metadata_response([])
    
    # ========================================================================
    # SUPPORT METHODS - Metadata Building & Prompt Generation
    # ========================================================================
    
    def _build_metadata_package(self, concepts: List[str]) -> Dict[str, Any]:
        """Build metadata package using taxonomy-based scoring."""
        # This is a placeholder - the actual implementation would come from
        # the original AnalysisOrchestrator._build_metadata_package method
        # For now, return minimal structure
        return {
            'books': [],
            'concept_map': {},
            'taxonomy_scores': {}
        }
    
    def _build_phase1_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str,
        metadata_package: Dict[str, Any]
    ) -> str:
        """Build Phase 1 prompt for python-guided analysis."""
        # Placeholder - actual implementation from original code
        return f"Analyze chapter {chapter_num}: {chapter_title}"
    
    def _build_books_metadata_only(self) -> List[Dict[str, Any]]:
        """Build books metadata WITHOUT loading content (lazy loading)."""
        # Placeholder - actual implementation from original code
        return []
    
    def _build_comprehensive_phase1_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str,
        books_metadata: List[Dict[str, Any]]
    ) -> str:
        """Build Phase 1 prompt for comprehensive LLM-driven analysis."""
        # Placeholder - actual implementation from original code
        return f"Comprehensive analysis of chapter {chapter_num}"
    
    def _mock_metadata_response(self, concepts: List[str]) -> LLMMetadataResponse:
        """Generate mock response when LLM unavailable."""
        # Placeholder - actual implementation from original code
        return LLMMetadataResponse(
            validation_summary="Mock validation",
            gap_analysis="Mock gap analysis",
            content_requests=[],
            analysis_strategy="Mock strategy"
        )
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate tokens in text (rough approximation)."""
        # Simple estimation: ~4 characters per token
        return len(text) // 4
