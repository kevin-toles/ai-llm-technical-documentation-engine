#!/usr/bin/env python3
"""
Interactive Metadata-First LLM Analysis System - V3 Hybrid Prompt

VERSION 3 CHANGES (Hybrid Prompt Quality Enforcement):
- Restored original strict quality standards for Phase 2 output
- Forces honest validation of each excerpt BEFORE writing analysis
- Explicit IF/THEN logic: genuine technical content vs. keyword-match artifacts
- Strict rules against generic filler ("complements", "broadens", "enhances")
- Tighter output constraints: 5-7 sentences (10 max) vs. previous 5-10
- Tier organization is now OPTIONAL (only when multiple genuine sources exist)
- Maintains Phase 1 context (validation summary, gaps, strategy) from V2

KEY DIFFERENCE FROM ORIGINAL:
- V2: Verbose tier-based organization, loose quality standards
- V3: Validation-first approach, strict honesty requirements, concrete citations only

ARCHITECTURE (from companion books):
- Two-Phase Request/Response Pattern (Microservice APIs Ch. 6)
- Command Pattern for LLM requests (Architecture Patterns with Python Ch. 9)
- Event-Driven orchestration (Building Microservices Ch. 4)
- State Machine for analysis workflow (Python Architecture Patterns Ch. 8)

ENGINEERING PRACTICES:
- Protocol-oriented design (Fluent Python Ch. 13)
- Async/await for concurrent operations (Fluent Python Ch. 21)
- Dataclass validation (Python Distilled Ch. 7)
- Functional composition (Fluent Python Ch. 7)
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
import json

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import our metadata extraction system
from workflows.llm_enhancement.scripts.metadata_extraction_system import (  # noqa: E402
    MetadataExtractionService
)

# Import LLM integration
import os  # noqa: E402

try:
    from workflows.shared.llm_integration import call_llm  # noqa: E402
    # Check if API key is actually available
    LLM_AVAILABLE = bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    if not LLM_AVAILABLE:
        print("Note: LLM libraries available but no API key set - using mock mode")
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM integration not available")

# Sprint 3.3: Import centralized constants (eliminates duplication)
# Per Quality Assessment: Fix 4 duplicate constants issue
# Reference: REFACTORING_PLAN.md Sprint 3.3 - Constants extraction
from workflows.shared.constants import BookTitles  # noqa: E402

# Sprint 3.4: Import metadata builder (extract builder pattern)
# Per BOOK_TAXONOMY_MATRIX.md: Architecture Patterns with Python (Tier 1)
# Reference: REFACTORING_PLAN.md Sprint 3.4 - Builder extraction
from workflows.llm_enhancement.scripts.builders.metadata_builder import MetadataBuilder  # noqa: E402


# ============================================================================
# DATA MODELS - Sprint 3.1 Architecture Refactoring
# Extracted to src/models/analysis_models.py for better organization
# Following: REFACTORING_PLAN.md Sprint 3, ARCHITECTURE_GUIDELINES Ch. 1
# ============================================================================

# Import data models from new models module (Sprint 3.1)
# Maintains backward compatibility - existing code continues to work
from workflows.llm_enhancement.scripts.models.analysis_models import (  # noqa: E402
    AnalysisPhase,
    ContentRequest,
    LLMMetadataResponse,
    ScholarlyAnnotation
)


# ============================================================================
# SPRINT 1: TAXONOMY PRE-FILTERING FUNCTIONS
# Per REFACTORING_PLAN.md section 1.2
# ============================================================================

def _extract_concepts_from_text(text: str) -> List[str]:
    """Extract key programming concepts from chapter text.
    
    Per REFACTORING_PLAN.md section 1.2:
    - Identifies Python-specific terms (decorators, generators, etc.)
    - Extracts design patterns mentioned
    - Captures architecture concepts
    - Extracts capitalized terms (proper nouns/concepts)
    
    Args:
        text: Chapter or guideline text to analyze
        
    Returns:
        List of extracted concept strings
        
    Example:
        >>> text = "This chapter covers decorators and generators."
        >>> _extract_concepts_from_text(text)
        ['decorator', 'decorators', 'generator', 'generators']
    """
    if not text:
        return []
    
    import re
    
    # Keyword-based concept extraction
    concept_keywords = [
        # Python-specific
        "decorator", "generator", "context manager", "metaclass",
        "async", "await", "coroutine", "iterator", "comprehension",
        "lambda", "closure", "descriptor", "property", "classmethod",
        "staticmethod", "abstract", "protocol", "generic", "type hint",
        
        # Design patterns
        "factory", "singleton", "observer", "strategy", "adapter",
        "decorator pattern", "facade", "proxy", "builder", "prototype",
        "command", "iterator", "template", "state", "visitor",
        
        # Architecture
        "microservice", "api", "rest", "graphql", "gateway",
        "repository", "service", "domain", "entity", "aggregate",
        "event", "message", "queue", "cache", "ddd",
        "architecture", "pattern", "solid", "dry", "testing",
        
        # Data structures & algorithms
        "list", "dict", "set", "tuple", "array", "hash", "tree",
        "graph", "algorithm", "data structure"
    ]
    
    text_lower = text.lower()
    found_concepts = [kw for kw in concept_keywords if kw in text_lower]
    
    # Also extract capitalized terms (likely proper nouns/concepts)
    # Match: Single capitalized word or multiple capitalized words (e.g., "Domain Driven Design")
    capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    
    # Limit capitalized terms to avoid noise (max 10 per plan)
    return found_concepts + capitalized[:10]


# ============================================================================
# ORCHESTRATOR - Two-Phase Analysis Workflow
# From: Microservice APIs Ch. 6 - Request/Response Patterns
#       Building Microservices Ch. 4 - Orchestration
# ============================================================================

class AnalysisOrchestrator:
    """Orchestrates two-phase LLM analysis workflow.
    
    Pattern: Orchestration Pattern (Building Microservices Ch. 4)
    Coordinates metadata analysis → content requests → deep analysis
    """
    
    def __init__(
        self,
        metadata_service: MetadataExtractionService,
        llm_available: bool = LLM_AVAILABLE,
        lazy_load: bool = True,
        aggregate_data: Optional[Dict[str, Any]] = None
    ):
        """Initialize orchestrator with dependencies.
        
        Pattern: Dependency Injection
        
        Args:
            metadata_service: Service for accessing book metadata
            llm_available: Whether LLM is available
            lazy_load: If True, only load books AFTER LLM requests them (saves memory & initial tokens)
            aggregate_data: Aggregate package data containing taxonomy, companion books, source book
        """
        self._metadata_service = metadata_service
        self._llm_available = llm_available
        self._lazy_load = lazy_load
        self._state = AnalysisPhase.INITIAL
        self._current_chapter_num = 0  # Tracking for cache keys
        self._aggregate_data = aggregate_data or {}
        
        # Extract source book and companion books from aggregate for dynamic use
        self._source_book_name = self._extract_source_book_name()
        self._companion_book_titles = self._extract_companion_book_titles()
        self._citation_map = self._build_citation_map()
        
        # Sprint 3.4: Initialize metadata builder (Builder pattern)
        self._metadata_builder = MetadataBuilder(metadata_service)
        
        # Lazy loading: Don't load books until LLM requests them
        if not lazy_load:
            print("Note: Lazy loading disabled - loading all books upfront")
    
    def _extract_source_book_name(self) -> str:
        """Extract source book name from aggregate data."""
        source_book = self._aggregate_data.get("source_book", {})
        name = source_book.get("name", "")
        # Remove profile suffix if present (e.g., "AI Engineering Building Applications_BASELINE")
        for suffix in ["_BASELINE", "_CURRENT", "_MODERATE", "_AGGRESSIVE"]:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
        return name or "Unknown Book"
    
    def _extract_companion_book_titles(self) -> List[str]:
        """Extract companion book titles from aggregate data.
        
        Dynamically builds the list from the aggregate package instead of hardcoding.
        """
        titles = []
        companion_books = self._aggregate_data.get("companion_books", [])
        
        for book in companion_books:
            name = book.get("name", "")
            if name:
                titles.append(name)
                # Also add common variations
                if "2nd" not in name and "3rd" not in name and "4th" not in name:
                    # Add variations with edition markers for fuzzy matching
                    titles.append(f"{name} 2nd")
                    titles.append(f"{name} 3rd")
        
        # Also include source book
        if self._source_book_name:
            titles.append(self._source_book_name)
        
        # Deduplicate
        return list(dict.fromkeys(titles))
    
    def _build_citation_map(self) -> Dict[str, tuple]:
        """Build citation map from aggregate data.
        
        Creates (author, title) tuples for each book.
        Falls back to ("Unknown", title) if author not available.
        """
        citation_map = {}
        
        # Source book
        source_book = self._aggregate_data.get("source_book", {})
        source_name = source_book.get("name", "")
        source_author = source_book.get("metadata", {}).get("author", "Unknown")
        if source_name:
            citation_map[source_name] = (source_author, source_name)
        
        # Companion books
        for book in self._aggregate_data.get("companion_books", []):
            name = book.get("name", "")
            # Try to get author from metadata (structure varies)
            author = "Unknown"
            metadata = book.get("metadata", {})
            if isinstance(metadata, dict):
                author = metadata.get("author", "Unknown")
            
            if name:
                citation_map[name] = (author, name)
        
        # Add centralized constants as fallback (known authors)
        citation_map.update({
            BookTitles.PYTHON_ESSENTIAL_REF: ("Beazley, David", BookTitles.PYTHON_ESSENTIAL_REF),
            BookTitles.FLUENT_PYTHON: ("Ramalho, Luciano", BookTitles.FLUENT_PYTHON),
            BookTitles.PYTHON_DISTILLED: ("Beazley, David", BookTitles.PYTHON_DISTILLED),
            BookTitles.PYTHON_DATA_ANALYSIS: ("McKinney, Wes", BookTitles.PYTHON_DATA_ANALYSIS),
            BookTitles.ARCH_PATTERNS_PYTHON: ("Percival, Harry and Gregory, Bob", BookTitles.ARCH_PATTERNS_PYTHON),
            BookTitles.BUILDING_MICROSERVICES: ("Newman, Sam", BookTitles.BUILDING_MICROSERVICES),
            BookTitles.PYTHON_COOKBOOK: ("Beazley, David and Jones, Brian K.", BookTitles.PYTHON_COOKBOOK),
        })
        
        return citation_map
    
    def _execute_phase1_with_retry(
        self,
        prompt: str,
        max_tokens: int,
        books_count: int
    ) -> LLMMetadataResponse:
        """
        Execute Phase 1 LLM call with truncation detection and retry logic.
        
        Extracted from analyze_chapter_comprehensive to reduce complexity.
        
        Args:
            prompt: The prompt to send to LLM
            max_tokens: Maximum tokens for response
            books_count: Number of books in metadata (for constraint message)
            
        Returns:
            LLMMetadataResponse with content requests
            
        Raises:
            Exception if both initial and retry attempts fail
            
        Reference:
            - Fluent Python Ch. 7: Extract Method pattern for complexity reduction
            - Architecture Patterns Ch. 3: Error handling separation
        """
        # Pass phase="phase1" and chapter_num for caching
        llm_output = call_llm(prompt, max_tokens=max_tokens, phase="phase1", chapter_num=self._current_chapter_num)
        
        # DEBUG: Show raw LLM response
        print("\n" + "="*80)
        print("DEBUG: Raw Claude Response (Phase 1)")
        print("="*80)
        print(llm_output[:2000])  # Show first 2000 chars
        if len(llm_output) > 2000:
            print(f"\n... (truncated, total length: {len(llm_output)} chars)")
        print("="*80 + "\n")
        
        # Check if response was truncated
        estimated_tokens = len(llm_output) // 3
        truncation_threshold = max_tokens * 0.95
        
        if estimated_tokens >= truncation_threshold:
            print(f"⚠️  WARNING: Response may be truncated (~{estimated_tokens:,} tokens, limit: {max_tokens:,})")
            print("   This suggests LLM tried to request too many books.")
            print("   Will attempt to parse and validate...")
        
        response = LLMMetadataResponse.from_llm_output(llm_output)
        
        # If truncated (0 requests but near token limit), retry with constraint
        if len(response.content_requests) == 0 and estimated_tokens >= truncation_threshold:
            print(f"\n❌ TRUNCATION DETECTED: Got 0 content requests but response was {estimated_tokens:,} tokens")
            print("   Re-prompting with constraint to limit to top 10 most relevant books...")
            
            constrained_prompt = prompt + f"""

IMPORTANT CONSTRAINT: You have access to {books_count} books, but please limit your content_requests 
to ONLY the TOP 10 most relevant and high-priority books. Focus on quality over quantity. 
Prioritize books that provide the most direct, substantial coverage of this chapter's core concepts."""
            
            # Note: Different prompt = different cache key (won't hit previous cache)
            llm_output = call_llm(constrained_prompt, max_tokens=max_tokens, phase="phase1", chapter_num=self._current_chapter_num)
            response = LLMMetadataResponse.from_llm_output(llm_output)
            print(f"✓ Retry with constraint: Found {len(response.content_requests)} content requests")
        
        return response
    
    def _limit_content_requests(self, response: LLMMetadataResponse, max_requests: int = 10) -> LLMMetadataResponse:
        """
        Limit content requests to top N by priority.
        
        Extracted from analyze_chapter_comprehensive to reduce complexity.
        
        Args:
            response: LLMMetadataResponse with content requests
            max_requests: Maximum number of requests to keep (default 10)
            
        Returns:
            Modified LLMMetadataResponse with limited requests
            
        Reference:
            - Python Distilled Ch. 5: Function organization best practices
        """
        if len(response.content_requests) > max_requests + 5:  # Allow some buffer
            print(f"\n⚠️  LLM requested {len(response.content_requests)} books - limiting to top {max_requests} by priority")
            sorted_requests = sorted(response.content_requests, key=lambda r: r.priority)
            response.content_requests = sorted_requests[:max_requests]
            print(f"✓ Truncated to top {max_requests} highest-priority requests")
        
        return response
    
    def analyze_chapter_comprehensive(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str
    ) -> ScholarlyAnnotation:
        """SCENARIO 2: LLM-driven comprehensive analysis.
        
        Flow:
        1. LLM reads FULL chapter text (not excerpt)
        2. LLM extracts ALL concepts from chapter
        3. LLM reviews metadata for all 15 books
        4. LLM identifies relevant books and requests specific chapters/sections
        5. LLM receives requested content
        6. LLM synthesizes integrated academic annotation bridging concepts
        
        This approach lets LLM discover concepts Python might miss and request
        coherent chapter-level content instead of scattered pages.
        """
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE LLM ANALYSIS: Chapter {chapter_num} - {chapter_title}")
        print(f"{'='*80}")
        
        # Track current chapter for cache key generation
        self._current_chapter_num = chapter_num
        
        # Build books metadata (all books - using data-driven concept taxonomy)
        books_metadata = self._build_books_metadata_only()
        
        # Phase 1: LLM reads chapter, extracts concepts, identifies relevant books
        print("\n📋 PHASE 1: Concept Extraction & Book Identification")
        print("-" * 40)
        
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
            return self._fallback_analysis(chapter_num, chapter_title, [])
        
        try:
            # Phase 1: Execute with retry logic (extracted to helper)
            max_tokens_phase1 = 8000
            response = self._execute_phase1_with_retry(prompt, max_tokens_phase1, len(books_metadata))
            
            # LLM self-limits - no hard cap on books
            # (removed max_requests=10 to let LLM decide what's relevant)
            
            print(f"✓ LLM extracted concepts and identified {len(response.content_requests)} book chapters to review")
            for req in response.content_requests[:5]:
                print(f"  - {req.book_name}: {req.rationale[:80]}...")
            
        except Exception as e:
            print(f"❌ Phase 1 failed: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_analysis(chapter_num, chapter_title, [])
        
        # Phase 2: Retrieve requested chapters and synthesize
        print("\n📖 PHASE 2: Chapter Retrieval & Synthesis")
        print("-" * 40)
        
        annotation = self._phase2_comprehensive_synthesis(
            chapter_num,
            chapter_title,
            chapter_full_text,
            response
        )
        
        self._state = AnalysisPhase.ANALYSIS_COMPLETE
        return annotation
    
    def analyze_chapter(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_concepts: List[str],
        chapter_excerpt: str
    ) -> ScholarlyAnnotation:
        """SCENARIO 1: Python-guided analysis (current approach).
        
        Flow:
        1. Python extracts concepts via keyword matching
        2. Python finds matches across all books
        3. LLM validates Python matches and requests specific pages
        4. LLM receives requested content
        5. LLM generates annotation
        
        Engineering: Template Method Pattern (Python Essential Reference Ch. 7)
        Defines skeleton of analysis algorithm.
        """
        print(f"\n{'='*80}")
        print(f"PYTHON-GUIDED ANALYSIS: Chapter {chapter_num} - {chapter_title}")
        print(f"{'='*80}")
        
        # Phase 1: Metadata Analysis
        metadata_response = self._phase1_metadata_analysis(
            chapter_num,
            chapter_title,
            chapter_concepts,
            chapter_excerpt
        )
        
        if not metadata_response.content_requests:
            print("⚠️  No content requests from LLM, using fallback strategy")
            return self._fallback_analysis(chapter_num, chapter_title, chapter_concepts)
        
        # Phase 2: Targeted Content Analysis
        annotation = self._phase2_content_analysis(
            chapter_num,
            chapter_title,
            chapter_concepts,
            chapter_excerpt,
            metadata_response
        )
        
        self._state = AnalysisPhase.ANALYSIS_COMPLETE
        return annotation
    
    def _phase1_metadata_analysis(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str
    ) -> LLMMetadataResponse:
        """Phase 1: Send metadata, receive content requests.
        
        Pattern: Request/Response (Microservice APIs Ch. 6)
        Engineering: Method chaining for fluent interface (Fluent Python Ch. 11)
        """
        print("\n📋 PHASE 1: Metadata Analysis")
        print("-" * 40)
        
        self._state = AnalysisPhase.METADATA_SENT
        
        # Gather comprehensive metadata (Sprint 3.4: delegated to MetadataBuilder)
        metadata_package = self._metadata_builder.build_metadata_package(concepts)
        
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
        
        # Check LLM availability BEFORE calling
        if not self._llm_available:
            print("⚠️  LLM not available, generating intelligent mock response based on concepts")
            mock_response = self._mock_metadata_response(concepts)
            print(f"✓ Generated {len(mock_response.content_requests)} mock content requests")
            for req in mock_response.content_requests[:3]:
                print(f"  - {req.book_name}: {len(req.pages)} pages - {req.rationale[:60]}...")
            self._state = AnalysisPhase.CONTENT_REQUESTED
            return mock_response
        
        # Call LLM
        try:
            llm_output = call_llm(prompt, max_tokens=2000, phase="phase1", chapter_num=chapter_num)
            response = LLMMetadataResponse.from_llm_output(llm_output)
            
            print(f"✓ Received {len(response.content_requests)} content requests")
            for req in response.content_requests[:3]:
                print(f"  - {req.book_name}: {len(req.pages)} pages - {req.rationale[:60]}...")
            
            self._state = AnalysisPhase.CONTENT_REQUESTED
            return response
            
        except Exception as e:
            print(f"❌ Phase 1 failed: {e}")
            self._state = AnalysisPhase.FAILED
            return self._mock_metadata_response(concepts)
    
    def _phase2_content_analysis(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str,
        metadata_response: LLMMetadataResponse
    ) -> ScholarlyAnnotation:
        """Phase 2: Send requested content, receive scholarly annotation.
        
        Pattern: Content Negotiation (Microservice APIs Ch. 7)
        Engineering: Builder pattern for complex object construction
        """
        print("\n📖 PHASE 2: Deep Content Analysis")
        print("-" * 40)
        
        # Retrieve requested content
        content_package = self._retrieve_requested_content(
            metadata_response.content_requests
        )
        
        print(f"Retrieved content from {len(content_package)} books")
        print(f"Total excerpts: {sum(len(excerpts) for excerpts in content_package.values())}")
        
        # Build Phase 2 prompt
        prompt = self._build_phase2_prompt(
            chapter_num,
            chapter_title,
            concepts,
            excerpt,
            metadata_response,
            content_package
        )
        
        print(f"Estimated tokens: ~{self._estimate_tokens(prompt):,}")
        
        if not self._llm_available:
            return self._mock_annotation(chapter_num, chapter_title, concepts)
        
        # Call LLM for final analysis
        try:
            annotation_text = call_llm(prompt, max_tokens=1500, phase="phase2", chapter_num=chapter_num)
            
            # Parse sources and concepts from annotation
            sources = self._extract_sources(annotation_text)
            validated_concepts = [c for c in concepts if c.lower() in annotation_text.lower()]
            
            annotation = ScholarlyAnnotation(
                chapter_number=chapter_num,
                chapter_title=chapter_title,
                annotation_text=annotation_text,
                sources_cited=sources,
                concepts_validated=validated_concepts,
                gaps_identified=self._extract_gaps(metadata_response.gap_analysis),
                metadata={
                    'phase1_requests': len(metadata_response.content_requests),
                    'content_sources': len(content_package),
                    'analysis_strategy': metadata_response.analysis_strategy
                }
            )
            
            print(f"✓ Generated annotation: {len(annotation_text)} chars")
            print(f"✓ Sources cited: {len(sources)}")
            print(f"✓ Concepts validated: {len(validated_concepts)}")
            
            return annotation
            
        except Exception as e:
            print(f"❌ Phase 2 failed: {e}")
            return self._mock_annotation(chapter_num, chapter_title, concepts)
    
    # ========================================================================
    # SCENARIO 2 METHODS: LLM-Driven Comprehensive Analysis
    # ========================================================================
    
    def _build_books_metadata_only(self) -> List[Dict[str, Any]]:
        """Build books metadata WITHOUT loading any book content.
        
        For Scenario 2 with lazy loading:
        - Send ONLY metadata (titles, chapters, concepts)
        - LLM reviews and requests specific chapters
        - System loads ONLY requested chapters (saves memory and tokens)
        
        This is much more efficient than loading all 9,180 pages upfront!
        """
        all_books = self._metadata_service._repo.get_all()
        
        # Try to load chapter metadata manager
        try:
            from workflows.metadata_enrichment.scripts.chapter_metadata_manager import ChapterMetadataManager
            chapter_manager = ChapterMetadataManager()
            has_chapter_metadata = True
        except Exception:
            chapter_manager = None
            has_chapter_metadata = False
            print("  Note: Chapter metadata not available, using basic book metadata only")
        
        books_metadata = []
        for book in all_books:
            # Get citation info
            author, full_title = self._get_citation_info(book.file_name)
            
            # Build basic metadata (NO CONTENT LOADED)
            book_meta = {
                'title': book.title,
                'file_name': book.file_name,  # For lazy loading later
                'domain': book.domain,
                'total_pages': book.total_pages,
                'description': f"{book.domain} - covers {', '.join(sorted(book.concepts_covered)[:10])}",
                'concepts_covered': sorted(book.concepts_covered)[:20],  # Top 20 concepts
                # Citation metadata for Chicago-style references
                'author': author,
                'full_title': full_title
            }
            
            # Add chapter information if available (still no content)
            if has_chapter_metadata and chapter_manager:
                # Chapter cache expects filename with .json extension
                chapters = chapter_manager.get_chapters(book.file_name + '.json')
                if chapters:
                    book_meta['chapters'] = [
                        {
                            'number': ch.chapter_number,
                            'title': ch.title,
                            'pages': f"{ch.start_page}-{ch.end_page}",
                            'summary': ch.summary,  # Full 2-3 sentence summary
                            'concepts': (ch.concepts[:10] if ch.concepts else []),  # Top 10 key concepts
                            'keywords': ch.keywords[:10]  # Top 10 keywords (increased from 5)
                        }
                        for ch in chapters[:15]  # First 15 chapters
                    ]
                    book_meta['has_chapter_metadata'] = True
                else:
                    book_meta['has_chapter_metadata'] = False
            else:
                book_meta['has_chapter_metadata'] = False
            
            books_metadata.append(book_meta)
        
        return books_metadata
    
    def _build_comprehensive_phase1_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str,
        books_metadata: List[Dict[str, Any]]
    ) -> str:
        """
        Build Phase 1 prompt for comprehensive LLM-driven analysis.
        
        REFACTORED: Now uses template system from src/prompts/
        
        References:
            - Template: src/prompts/comprehensive_phase1.txt
            - Formatter: src/prompts/templates.format_comprehensive_phase1_prompt
            - Sprint 2.11: TDD REFACTOR - Integrate Phase1
        """
        from workflows.shared.prompts.templates import format_comprehensive_phase1_prompt
        
        return format_comprehensive_phase1_prompt(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            chapter_full_text=chapter_full_text,
            books_metadata=books_metadata,
            source_book_name=self._source_book_name
        )
    
    def _extract_chapter_numbers_from_rationale(self, rationale: str) -> List[int]:
        """Extract chapter numbers from rationale text.
        
        Args:
            rationale: Rationale text that may contain chapter references like "Chapter 5: Decorators"
            
        Returns:
            List of unique chapter numbers found
        """
        import re
        chapter_pattern = r'Chapter\s+(\d+)'
        chapter_matches = re.findall(chapter_pattern, rationale, re.IGNORECASE)
        return [int(num) for num in set(chapter_matches)]
    
    def _load_full_chapter_content(
        self,
        chapter_num: int,
        chapter_info,
        book_content: Dict,
        book_name: str
    ) -> Optional[Dict[str, Any]]:
        """Load all pages for a specific chapter.
        
        Args:
            chapter_num: Chapter number to load
            chapter_info: Chapter metadata object with start_page, end_page, title
            book_content: Full book JSON content dict
            book_name: Human-readable book name for citation
            
        Returns:
            Dict with chapter content and metadata, or None if no content found
        """
        chapter_content = []
        for page_num in range(chapter_info.start_page, chapter_info.end_page + 1):
            if str(page_num) in book_content:
                page_text = book_content[str(page_num)].get('content', '')
                chapter_content.append(page_text)
        
        if not chapter_content:
            return None
        
        author, full_title = self._get_citation_info(book_name)
        
        print(f"    ✓ Loaded Chapter {chapter_num} from {book_name} ({len(chapter_content)} pages)")
        
        return {
            'chapter': chapter_num,
            'title': chapter_info.title,
            'pages': f"{chapter_info.start_page}-{chapter_info.end_page}",
            'content': '\n'.join(chapter_content),
            'is_full_chapter': True,
            'author': author,
            'book_title': full_title,
            'book_filename': book_name
        }
    
    def _load_chapters_for_request(
        self,
        req: ContentRequest,
        book_content: Dict,
        chapter_manager
    ) -> List[Dict[str, Any]]:
        """Load full chapters based on request rationale.
        
        Args:
            req: Content request with book name and rationale
            book_content: Full book JSON content
            chapter_manager: ChapterMetadataManager instance
            
        Returns:
            List of chapter excerpt dicts with content and metadata
        """
        excerpts: list[dict[str, Any]] = []
        
        chapter_nums = self._extract_chapter_numbers_from_rationale(req.rationale)
        if not chapter_nums:
            return excerpts
        
        chapters = chapter_manager.get_chapters(req.book_name.replace(' ', '_') + '_Content.json')
        
        for chapter_num in chapter_nums:
            chapter_info = next((ch for ch in chapters if ch.chapter_number == chapter_num), None)
            if chapter_info:
                chapter_data = self._load_full_chapter_content(
                    chapter_num, chapter_info, book_content, req.book_name
                )
                if chapter_data:
                    excerpts.append(chapter_data)
        
        return excerpts
    
    def _load_page_excerpts_for_request(
        self,
        req: ContentRequest,
        book_content: Dict
    ) -> List[Dict[str, Any]]:
        """Load individual pages for a content request (fallback behavior).
        
        Args:
            req: Content request with book name and pages
            book_content: Full book JSON content
            
        Returns:
            List of page excerpt dicts with content and metadata
        """
        excerpts = []
        author, full_title = self._get_citation_info(req.book_name)
        
        for page_num in req.pages:  # Process all LLM-requested pages
            if str(page_num) in book_content:
                excerpts.append({
                    'page': page_num,
                    'content': book_content[str(page_num)].get('content', '')[:1000],
                    'is_full_chapter': False,
                    'author': author,
                    'book_title': full_title,
                    'book_filename': req.book_name
                })
        
        return excerpts
    
    def _lazy_load_requested_chapters(
        self,
        content_requests: List[ContentRequest]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Lazy load ONLY the chapters/pages that LLM requested.
        
        This is called AFTER Phase 1, so we only load what we need.
        Saves memory and initial token cost.
        
        Supports TWO modes:
        1. Chapter-level: If request includes chapter info, load entire chapter
        2. Page-level: If only pages, load those specific pages
        
        Returns:
            Dict mapping book_name -> list of chapter/page content
        """
        print(f"  Lazy loading content from {len(content_requests)} requests...")
        
        content_package = {}
        
        # Try to load chapter metadata manager for chapter-level retrieval
        try:
            from workflows.metadata_enrichment.scripts.chapter_metadata_manager import ChapterMetadataManager
            chapter_manager = ChapterMetadataManager()
            has_chapter_metadata = True
        except Exception:
            chapter_manager = None
            has_chapter_metadata = False
        
        for req in content_requests:  # Process all LLM-requested books
            try:
                book_content = self._load_book_json_by_name(req.book_name)
                if not book_content:
                    continue
                
                excerpts = []
                
                # Try chapter-level loading if metadata available
                if has_chapter_metadata and chapter_manager:
                    excerpts = self._load_chapters_for_request(req, book_content, chapter_manager)
                    if excerpts:
                        content_package[req.book_name] = excerpts
                        continue
                
                # Fallback: Load individual pages
                excerpts = self._load_page_excerpts_for_request(req, book_content)
                if excerpts:
                    content_package[req.book_name] = excerpts
                    
            except Exception as e:
                print(f"  Warning: Could not load {req.book_name}: {e}")
                continue
        
        return content_package
    
    def _load_book_json_by_name(self, book_name: str) -> Optional[Dict]:
        """Load a single book's JSON file by its human-readable name.
        
        This is the lazy loading implementation - only called when needed.
        
        Args:
            book_name: Human-readable book name (e.g., "Fluent Python 2nd")
        """
        from pathlib import Path
        
        # Load from Textbooks_JSON directory (updated to use actual data location)
        json_dir = Path(__file__).parent.parent / "data" / "textbooks_json"
        
        # Filename is just book_name + .json (e.g., "Fluent Python 2nd.json")
        target_filename = f"{book_name}.json"
        
        
        # Check if directory exists
        if not json_dir.exists():
            print(f"  Warning: JSON directory not found: {json_dir}")
            return None
            
        json_file = json_dir / target_filename
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    # Return pages dict
                    if isinstance(data, dict) and 'pages' in data:
                        # Convert pages list to dict indexed by page number
                        pages_dict = {}
                        for page in data['pages']:
                            page_num = page.get('page_number')
                            if page_num:
                                pages_dict[str(page_num)] = page
                        return pages_dict
                    return data
            except Exception as e:
                print(f"  Error loading {json_file}: {e}")
                return None
        
        # If not found, log helpful debug info
        print(f"  Warning: Could not find file '{target_filename}' in JSON directory")
        return None
    
    def _get_citation_info(self, book_filename: str) -> tuple[str, str]:
        """Get author and full title for Chicago-style citations.
        
        Args:
            book_filename: Human-readable book name matching JSON filename (e.g., "Fluent Python 2nd")
            
        Returns:
            Tuple of (author, full_title) for citation formatting
            
        Note: Uses dynamic citation_map built from aggregate data at init time.
        Falls back to known authors for core books if aggregate doesn't have author info.
        """
        # Use dynamically built citation map from aggregate data
        if book_filename in self._citation_map:
            return self._citation_map[book_filename]
        
        # Fallback: use the filename as-is (already human-readable)
        return ("Unknown", book_filename)
    
    def _extract_concepts_from_requests(
        self,
        content_requests: List[Any]
    ) -> List[str]:
        """
        Extract key concepts from content request rationales.
        
        Extracted from _phase2_comprehensive_synthesis() to reduce complexity (S3776).
        
        Args:
            content_requests: List of content request objects with rationale fields.
            
        Returns:
            List of extracted concept keywords.
        """
        concepts = []
        for req in content_requests:
            for word in req.rationale.lower().split():
                clean_word = word.strip()
                if len(clean_word) > 4 and clean_word.isalpha():
                    concepts.append(clean_word)
        return concepts
    
    def _extract_and_merge_concepts(
        self,
        content_requests: List[Any],
        annotation_text: str
    ) -> List[str]:
        """
        Extract and merge concepts from requests and annotation text.
        
        Extracted from _phase2_comprehensive_synthesis() to reduce complexity (S3776).
        
        Args:
            content_requests: Content request objects.
            annotation_text: Generated annotation text.
            
        Returns:
            Deduplicated list of concept keywords (max 20).
        """
        concepts_validated = self._extract_concepts_from_requests(content_requests)
        
        # Extract concepts from annotation text
        annotation_concepts = _extract_concepts_from_text(annotation_text)
        for concept in annotation_concepts:
            clean = concept.strip().lower()
            if clean.isalpha() and len(clean) > 3 and '\n' not in concept:
                concepts_validated.append(clean)
        
        # Deduplicate and limit to top 20
        return list(dict.fromkeys(concepts_validated))[:20]
    
    def _phase2_comprehensive_synthesis(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str,
        metadata_response: LLMMetadataResponse
    ) -> ScholarlyAnnotation:
        """Phase 2 for comprehensive analysis: Lazy load content + synthesize annotation."""
        
        # Load content based on mode
        content_package = (
            self._lazy_load_requested_chapters(metadata_response.content_requests)
            if self._lazy_load
            else self._retrieve_requested_content(metadata_response.content_requests)
        )
        
        print(f"Retrieved content from {len(content_package)} books")
        print(f"Total excerpts: {sum(len(excerpts) for excerpts in content_package.values())}")
        
        # Build synthesis prompt
        system_prompt, user_prompt = self._build_comprehensive_phase2_prompt(
            chapter_num, chapter_title, chapter_full_text,
            metadata_response, content_package
        )
        
        print(f"Estimated tokens: ~{self._estimate_tokens(user_prompt):,}")
        
        try:
            llm_output = call_llm(
                user_prompt, system_prompt=system_prompt, 
                max_tokens=4000, phase="phase2", chapter_num=chapter_num
            )
            
            annotation_text = llm_output.strip()
            
            # Extract sources from annotation + content package
            sources = self._extract_sources(annotation_text)
            for book_name in content_package.keys():
                if book_name not in sources:
                    sources.append(book_name)
            
            # Extract and merge concepts using helper
            concepts_validated = self._extract_and_merge_concepts(
                metadata_response.content_requests, annotation_text
            )
            
            print(f"✓ Generated annotation: {len(annotation_text)} chars")
            print(f"✓ Sources cited: {len(sources)}")
            print(f"✓ Concepts validated: {len(concepts_validated)}")
            
            return ScholarlyAnnotation(
                chapter_number=chapter_num,
                chapter_title=chapter_title,
                annotation_text=annotation_text,
                sources_cited=sources,
                concepts_validated=concepts_validated,
                gaps_identified=[],
                metadata={'status': 'comprehensive_synthesis', 'method': 'scenario_2'}
            )
            
        except Exception as e:
            print(f"❌ Phase 2 synthesis failed: {e}")
            return self._mock_annotation(chapter_num, chapter_title, [])
    
    def _build_comprehensive_phase2_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        _chapter_full_text: str,
        metadata_response: LLMMetadataResponse,
        content_package: Dict[str, List[Dict]]
    ) -> tuple:
        """
        Build Phase 2 prompt for comprehensive synthesis.
        
        REFACTORED: Now uses template system from src/prompts/
        Returns both system prompt and user prompt for proper separation.
        
        Args:
            chapter_num: Chapter number for identification
            chapter_title: Title of the chapter
            _chapter_full_text: Unused - Phase 2 works with requested excerpts from content_package
            metadata_response: Phase 1 analysis results
            content_package: Book excerpts requested in Phase 1
            
        Returns:
            Tuple of (system_prompt, user_prompt) ready for LLM
            
        References:
            - Template: src/prompts/comprehensive_phase2.txt
            - System: src/prompts/comprehensive_phase2_system.txt
            - Formatter: src/prompts/templates.format_comprehensive_phase2_prompt
            - Sprint 2.12: TDD REFACTOR - Integrate Phase2
        """
        from workflows.shared.prompts.templates import format_comprehensive_phase2_prompt
        
        # Extract taxonomy from aggregate data
        taxonomy_data = self._aggregate_data.get('taxonomy') if self._aggregate_data else None
        
        return format_comprehensive_phase2_prompt(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            metadata_response=metadata_response,
            content_package=content_package,
            source_book_name=self._source_book_name,
            taxonomy_data=taxonomy_data
        )
    
    # ========================================================================
    # SCENARIO 1 METHODS: Python-Guided Analysis (Original)
    # ========================================================================
    # Sprint 3.4: Metadata building methods extracted to MetadataBuilder
    # See: src/builders/metadata_builder.py
    
    def _build_phase1_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str,
        metadata_package: Dict[str, Any]
    ) -> str:
        """
        Build Phase 1 prompt for metadata analysis.
        
        REFACTORED: Now uses template system from src/prompts/
        
        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title
            concepts: List of key concepts from chapter
            excerpt: Chapter text excerpt
            metadata_package: Dict containing concept_mapping, total_books, total_pages, books
            
        Returns:
            Formatted prompt string ready for LLM
            
        References:
            - Template: src/prompts/phase1.txt
            - Formatter: src/prompts/templates.format_phase1_prompt
            - Sprint 2.13: TDD REFACTOR - Integrate Phase1
            - BOOK_TAXONOMY_MATRIX.md: Taxonomy embedded in template
            - PYTHON_GUIDELINES: String formatting, template composition
        """
        from workflows.shared.prompts.templates import format_phase1_prompt
        
        return format_phase1_prompt(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            concepts=concepts,
            excerpt=excerpt,
            metadata_package=metadata_package
        )
    
    def _build_phase2_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str,
        metadata_response: LLMMetadataResponse,
        content_package: Dict[str, List[Dict]]
    ) -> str:
        """
        Build Phase 2 prompt for deep scholarly analysis.
        
        REFACTORED: Now uses template system from src/prompts/
        
        Args:
            chapter_num: Chapter number
            chapter_title: Chapter title
            concepts: List of key concepts from chapter
            excerpt: Chapter text excerpt
            metadata_response: Phase 1 analysis results with:
                - validation_summary: Python keyword match validation
                - gap_analysis: Identified gaps
                - analysis_strategy: Planned approach
            content_package: Retrieved book excerpts (dict of book_name -> excerpts list)
            
        Returns:
            Formatted prompt string ready for LLM
            
        References:
            - Template: src/prompts/phase2.txt
            - Formatter: src/prompts/templates.format_phase2_prompt
            - Sprint 2.14: TDD REFACTOR - Integrate Phase2 (FINAL)
            - ARCHITECTURE_GUIDELINES: Separation of concerns principle
        """
        from workflows.shared.prompts.templates import format_phase2_prompt
        
        return format_phase2_prompt(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            concepts=concepts,
            excerpt=excerpt,
            metadata_response=metadata_response,
            content_package=content_package
        )
    
    def _retrieve_requested_content(
        self,
        requests: List[ContentRequest]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Retrieve content for all requests.
        
        Engineering: List comprehension and dictionary construction
        (Python Cookbook Ch. 1 - Data Structures and Algorithms)
        """
        content_package = {}
        
        # Sort by priority
        sorted_requests = sorted(requests)
        
        for request in sorted_requests:  # Process all LLM-requested books
            # Clean book name for lookup
            clean_name = request.book_name.replace(' ', '_').replace('_Content', '')
            
            excerpts = []
            for page_num in request.pages:  # Process all LLM-requested pages
                page = self._metadata_service._repo.get_page(clean_name, page_num)
                if page:
                    excerpts.append({
                        'page': page.page_number,
                        'chapter': page.chapter,
                        'content': page.content[:1000],  # Limit content length
                        'rationale': request.rationale
                    })
            
            if excerpts:
                content_package[request.book_name] = excerpts
        
        return content_package
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text.
        
        Engineering: Simple heuristic (can be enhanced with tiktoken)
        """
        return len(text) // 4
    
    def _extract_sources(self, annotation: str) -> List[str]:
        """Extract cited sources from annotation text.
        
        Uses the companion book titles from aggregate data (dynamically loaded).
        Matches book titles mentioned in the annotation text.
        """
        sources = []
        
        # Use dynamically extracted companion book titles from aggregate
        # (populated in __init__ from aggregate_data)
        known_books = self._companion_book_titles if self._companion_book_titles else []
        
        # Fallback: add some core known titles if aggregate didn't provide any
        if not known_books:
            known_books = [
                BookTitles.FLUENT_PYTHON,
                BookTitles.PYTHON_ESSENTIAL_REF,
                BookTitles.PYTHON_DISTILLED,
                BookTitles.PYTHON_DATA_ANALYSIS,
                BookTitles.ARCH_PATTERNS_PYTHON,
                BookTitles.BUILDING_MICROSERVICES,
            ]
        
        annotation_lower = annotation.lower()
        
        for book_title in known_books:
            # Check for exact match (case-insensitive)
            if book_title.lower() in annotation_lower:
                # Add book title directly (dedup happens below)
                sources.append(book_title)
        
        # Deduplicate while preserving order
        seen = set()
        unique_sources = []
        for s in sources:
            if s not in seen:
                seen.add(s)
                unique_sources.append(s)
        
        return unique_sources
    
    def _extract_gaps(self, gap_text: str) -> List[str]:
        """Extract identified gaps from gap analysis text."""
        # Simple extraction - split by common delimiters
        gaps = []
        for line in gap_text.split('\n'):
            line = line.strip()
            if line and len(line) > 10:
                # Remove bullet points and numbers
                clean = line.lstrip('- •123456789.').strip()
                if clean:
                    gaps.append(clean)
        return gaps[:5]  # Top 5 gaps
    
    def _fallback_analysis(
        self,
        chapter_num: int,
        chapter_title: str,
        _concepts: List[str]
    ) -> ScholarlyAnnotation:
        """Fallback when LLM requests fail.
        
        Args:
            chapter_num: Chapter number for identification
            chapter_title: Title of the chapter
            _concepts: Unused - fallback provides minimal response without concept analysis
        """
        return ScholarlyAnnotation(
            chapter_number=chapter_num,
            chapter_title=chapter_title,
            annotation_text="Analysis unavailable - LLM integration failed",
            sources_cited=[],
            concepts_validated=[],
            gaps_identified=[],
            metadata={'status': 'fallback'}
        )
    
    def _get_recommended_books_from_taxonomy(
        self,
        concepts: List[str],
        concept_mapping: Dict
    ) -> List[str]:
        """Get recommended books from concept mapping.
        
        Note: Previously used hardcoded book_taxonomy.py. Now uses data-driven
        concept mapping from generate_concept_taxonomy.py (new system).
        
        Args:
            concepts: List of concepts to match (for backward compatibility)
            concept_mapping: Dict mapping concepts to matched books/pages
            
        Returns:
            List of recommended book names from concept mapping
        """
        # Use all books from concept_mapping (data-driven approach)
        return list(concept_mapping.keys())[:12]
    
    def _calculate_request_priority(
        self,
        matched_concepts: set,
        total_concepts: int
    ) -> int:
        """Calculate priority for a content request.
        
        Args:
            matched_concepts: Set of concepts matched in this book
            total_concepts: Total number of concepts being searched
            
        Returns:
            Priority score (1-5) based on match strength
        """
        match_strength = len(matched_concepts) / max(total_concepts, 1)
        base_priority = min(5, int(match_strength * 5) + 1)
        
        # Priority is purely based on concept match strength (data-driven)
        # No hardcoded tier adjustments
        
        return base_priority
    
    def _build_content_request_from_matches(
        self,
        book_name: str,
        matches: Dict,
        concepts: List[str]
    ) -> Optional[ContentRequest]:
        """Build content request from concept matches for a book.
        
        Args:
            book_name: Name of the book
            matches: Dict mapping pages to matched concepts
            concepts: Full list of concepts being searched
            
        Returns:
            ContentRequest or None if no valid matches
        """
        if not matches:
            return None
        
        # Get top matching pages (sorted by relevance)
        sorted_matches = sorted(
            matches.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        # Take top 5-8 pages with matches
        top_pages = [int(page) for page, _ in sorted_matches[:8]]
        if not top_pages:
            return None
        
        # Build rationale from matched concepts
        all_matched_concepts = set()
        for _, matched_concepts in sorted_matches[:8]:
            all_matched_concepts.update(matched_concepts)
        
        priority = self._calculate_request_priority(all_matched_concepts, len(concepts))
        
        rationale = f"Python keyword matches found for: {', '.join(list(all_matched_concepts)[:5])}"
        if len(all_matched_concepts) > 5:
            rationale += f" (and {len(all_matched_concepts) - 5} more)"
        
        return ContentRequest(
            book_name=book_name,
            pages=top_pages,
            rationale=rationale,
            priority=priority
        )
    
    def _mock_metadata_response(self, concepts: List[str]) -> LLMMetadataResponse:
        """Mock response for testing without LLM - uses ACTUAL Python keyword matching.
        
        This fallback now produces real annotations instead of 'Analysis unavailable'
        by leveraging the metadata_package concept_mapping results.
        Refactored to reduce cognitive complexity.
        """
        requests = []
        metadata_package = getattr(self, '_last_metadata_package', None)
        
        if metadata_package and 'concept_mapping' in metadata_package:
            concept_mapping = metadata_package['concept_mapping']
            recommended_books = self._get_recommended_books_from_taxonomy(concepts, concept_mapping)
            
            # Build content requests from actual keyword matches
            for book_name in recommended_books:
                if book_name not in concept_mapping:
                    continue
                
                request = self._build_content_request_from_matches(
                    book_name,
                    concept_mapping[book_name],
                    concepts
                )
                if request:
                    requests.append(request)
        
        # If no requests from metadata, provide minimal fallback
        if not requests:
            requests.append(ContentRequest(
                book_name=BookTitles.PYTHON_DISTILLED,
                pages=[1, 2, 3],
                rationale="General Python concepts reference",
                priority=3
            ))
        
        return LLMMetadataResponse(
            validation_summary=f"Python keyword matching identified {len(requests)} books with relevant content across {sum(len(r.pages) for r in requests)} pages.",
            gap_analysis="Using actual Python keyword matching results. Gaps will be identified during Phase 2 analysis based on retrieved content.",
            content_requests=requests,
            analysis_strategy=f"Synthesize cross-references from {len(requests)} books using verified Python keyword matches. Organize by tier: Architecture patterns → Implementation examples → Engineering practices."
        )
    
    def _mock_annotation(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str]
    ) -> ScholarlyAnnotation:
        """Mock annotation for testing."""
        source_book = self._source_book_name or "the source book"
        annotation_text = f"""The {chapter_title} chapter introduces Python's numeric type system, which receives sophisticated treatment in several companion texts. Python Essential Reference 4th (Ch. 3, pp. 145-148) provides comprehensive implementation details for integer, float, and Decimal types, emphasizing precision control through decimal.Context managers—a critical topic absent from {source_book}'s introductory coverage. Fluent Python 2nd (Ch. 12, pp. 89-91) demonstrates advanced numeric protocols through operator overloading examples, showing how custom classes can integrate seamlessly with Python's numeric tower using __add__, __mul__, and other special methods. The gap analysis reveals that while {source_book} establishes foundational concepts like type coercion and basic arithmetic, it defers complex number applications and NumPy integration patterns that appear extensively in Python Data Analysis 3rd. Python Distilled (pp. 45-46) offers a concise middle ground, covering numeric best practices including integer division nuances and floating-point comparison pitfalls that intermediate learners should understand."""
        
        return ScholarlyAnnotation(
            chapter_number=chapter_num,
            chapter_title=chapter_title,
            annotation_text=annotation_text,
            sources_cited=[BookTitles.PYTHON_ESSENTIAL_REF, BookTitles.FLUENT_PYTHON, BookTitles.PYTHON_DATA_ANALYSIS, BookTitles.PYTHON_DISTILLED],
            concepts_validated=concepts,
            gaps_identified=[
                "Decimal context management for precision control",
                "Complex number practical applications",
                "NumPy integration patterns",
                "Performance considerations for numeric computations"
            ],
            metadata={
                'status': 'mock',
                'demonstrates': 'full_workflow'
            }
        )


# ============================================================================
# DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("INTERACTIVE METADATA-FIRST LLM ANALYSIS SYSTEM - TEST STUB")
    print("NOTE: This is a standalone test. Use integrate_llm_enhancements.py for production workflow.")
    print("="*80)
    print("\n⚠️  This test stub is for development/debugging only.")
    print("⚠️  To process actual chapters, run: integrate_llm_enhancements.py")
    print("\nExiting...")
    exit(0)
    
    # DISABLED: Old test code (kept for reference)
    # metadata_service = MetadataServiceFactory.create_default()
    # orchestrator = AnalysisOrchestrator(metadata_service, llm_available=LLM_AVAILABLE)
    # annotation = orchestrator.analyze_chapter(chapter_num=5, ...)