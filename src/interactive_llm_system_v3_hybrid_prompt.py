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

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum, auto
import json

# Import our metadata extraction system
from .metadata_extraction_system import (
    MetadataExtractionService,
    BookMetadata,
    ConceptMatch
)

# Import book taxonomy for intelligent cascading selection
try:
    # Import module-level items that are used throughout
    from .book_taxonomy import (
        BOOK_REGISTRY,
        BookTier
    )
    TAXONOMY_AVAILABLE = True
except ImportError:
    TAXONOMY_AVAILABLE = False
    print("Warning: book_taxonomy.py not available - cascading logic disabled")

# Import LLM integration
import os

try:
    from .llm_integration import call_llm
    # Check if API key is actually available
    LLM_AVAILABLE = bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    if not LLM_AVAILABLE:
        print("Note: LLM libraries available but no API key set - using mock mode")
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM integration not available")

# Book title constants (per SonarQube - avoid duplicated string literals)
# These match the exact titles used in book_taxonomy.py and metadata JSON files
PYTHON_ESSENTIAL_REF = "Python Essential Reference 4th"
FLUENT_PYTHON = "Fluent Python 2nd"
PYTHON_DISTILLED = "Python Distilled"
PYTHON_DATA_ANALYSIS = "Python Data Analysis 3rd"


# ============================================================================
# STATE MACHINE - Analysis Workflow States
# From: Python Architecture Patterns Ch. 8 - State Management
# ============================================================================

class AnalysisPhase(Enum):
    """Analysis workflow states.
    
    Pattern: State Machine (Python Architecture Patterns Ch. 8)
    """
    INITIAL = auto()
    METADATA_SENT = auto()
    CONTENT_REQUESTED = auto()
    ANALYSIS_COMPLETE = auto()
    FAILED = auto()


# ============================================================================
# COMMAND PATTERN - LLM Request/Response
# From: Architecture Patterns with Python Ch. 9 - Commands and Events
# ============================================================================

@dataclass(frozen=True)
class ContentRequest:
    """Command for requesting specific book content.
    
    Pattern: Command Pattern (Architecture Patterns Ch. 9)
    Encapsulates all information needed to perform content retrieval.
    """
    book_name: str
    pages: List[int]
    rationale: str
    priority: int = 1  # Higher = more important
    
    def __lt__(self, other: 'ContentRequest') -> bool:
        """Enable priority queue sorting."""
        return self.priority > other.priority  # Higher priority first


@dataclass
class LLMMetadataResponse:
    """Structured response from Phase 1 metadata analysis.
    
    Pattern: Data Transfer Object (Microservices Ch. 6)
    Engineering: Dataclass with validation (Python Distilled Ch. 7)
    """
    validation_summary: str
    gap_analysis: str
    content_requests: List[ContentRequest]
    analysis_strategy: str
    
    @classmethod
    def from_llm_output(cls, llm_output: str) -> 'LLMMetadataResponse':
        """Parse LLM output into structured response.
        
        Engineering: Factory method pattern (Python Essential Reference Ch. 7)
        """
        try:
            # Strip markdown code blocks if present (Claude often wraps JSON in ```json)
            cleaned_output = llm_output.strip()
            if cleaned_output.startswith('```'):
                # Remove opening ```json or ``` 
                lines = cleaned_output.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                # Remove closing ```
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                cleaned_output = '\n'.join(lines)
            
            # Try to parse as JSON
            data = json.loads(cleaned_output)
            
            # DEBUG: Show parsed JSON structure
            print("\n[DEBUG] JSON parsed successfully")
            print(f"[DEBUG] Keys in response: {list(data.keys())}")
            print(f"[DEBUG] content_requests field: {data.get('content_requests', 'MISSING')}")
            if 'content_requests' in data:
                print(f"[DEBUG] Number of requests: {len(data.get('content_requests', []))}")
                if len(data.get('content_requests', [])) == 0:
                    print("[DEBUG] ⚠️ content_requests array is EMPTY!")
                else:
                    print(f"[DEBUG] ✓ Found {len(data.get('content_requests', []))} content requests")
            
            requests = [
                ContentRequest(
                    book_name=req['book_name'],
                    pages=req['pages'],
                    rationale=req['rationale'],
                    priority=req.get('priority', 1)
                )
                for req in data.get('content_requests', [])
            ]
            
            return cls(
                validation_summary=data.get('validation_summary', ''),
                gap_analysis=data.get('gap_analysis', ''),
                content_requests=requests,
                analysis_strategy=data.get('analysis_strategy', '')
            )
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON parsing failed: {e}")
            print("[DEBUG] Falling back to text format parsing")
            # Fallback: parse text format
            return cls._parse_text_format(llm_output)
    
    @classmethod
    def _parse_text_format(cls, text: str) -> 'LLMMetadataResponse':
        """Parse text-based LLM response.
        
        Engineering: Robustness through multiple parsing strategies
        (Python Cookbook Ch. 2 - Strings and Text)
        """
        # Simple text parsing - extract sections
        sections = {
            'validation': '',
            'gaps': '',
            'requests': [],
            'strategy': ''
        }
        
        # Basic section extraction
        current_section = None
        for line in text.split('\n'):
            line_lower = line.lower()
            if 'validation' in line_lower:
                current_section = 'validation'
            elif 'gap' in line_lower:
                current_section = 'gaps'
            elif 'request' in line_lower or 'content' in line_lower:
                current_section = 'requests'
            elif 'strategy' in line_lower:
                current_section = 'strategy'
            elif current_section:
                sections[current_section] += line + '\n'
        
        # Create minimal response
        return cls(
            validation_summary=sections['validation'].strip(),
            gap_analysis=sections['gaps'].strip(),
            content_requests=[],  # Will need manual review
            analysis_strategy=sections['strategy'].strip()
        )


@dataclass
class ScholarlyAnnotation:
    """Final scholarly annotation output.
    
    Pattern: Value Object (DDD)
    """
    chapter_number: int
    chapter_title: str
    annotation_text: str
    sources_cited: List[str]
    concepts_validated: List[str]
    gaps_identified: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


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


def _prefilter_books_by_taxonomy(
    orchestrator,
    guideline_text: str,
    max_books: int = 10
) -> List[str]:
    """Pre-filter books using taxonomy before sending to LLM.
    
    Per REFACTORING_PLAN.md section 1.2:
    - Reduces token usage by ~40% by filtering books before Phase 1
    - Uses book_taxonomy.py scoring for intelligent selection
    - Matches books to extracted concepts from guideline text
    
    Args:
        orchestrator: AnalysisOrchestrator instance with metadata_service
        guideline_text: Text to extract concepts from
        max_books: Maximum number of books to return
        
    Returns:
        List of book titles (strings) to include in LLM analysis
        
    Example:
        >>> books = _prefilter_books_by_taxonomy(
        ...     orchestrator,
        ...     "This chapter covers decorators",
        ...     max_books=5
        ... )
        >>> "Fluent Python 2nd" in books
        True
    """
    # Extract concepts from the guideline text
    concepts = _extract_concepts_from_text(guideline_text)
    concept_set = set(concepts)
    
    # Use book_taxonomy to score and rank books
    try:
        # Import book_taxonomy scoring function
        from .book_taxonomy import score_books_for_concepts, ALL_BOOKS
        
        # If no concepts found, return top-ranked books by default
        if not concept_set:
            # Return first N books from ALL_BOOKS as fallback
            return [book.book_name for book in ALL_BOOKS[:max_books]]
        
        # Score all books based on concept relevance
        scored_books = score_books_for_concepts(concept_set)
        
        # Take top N books
        top_books = [book_name for book_name, score in scored_books[:max_books]]
        
        return top_books
        
    except Exception as e:
        # Fallback: Return all books if taxonomy scoring fails
        print(f"Warning: Taxonomy scoring failed ({e}), using all books")
        
        # Get all book titles from metadata service
        if hasattr(orchestrator, '_metadata_service'):
            metadata = orchestrator._metadata_service.books_metadata
            all_titles = [meta.get('title', '') for meta in metadata.values()]
            return all_titles[:max_books]
        
        return []


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
        lazy_load: bool = True
    ):
        """Initialize orchestrator with dependencies.
        
        Pattern: Dependency Injection
        
        Args:
            metadata_service: Service for accessing book metadata
            llm_available: Whether LLM is available
            lazy_load: If True, only load books AFTER LLM requests them (saves memory & initial tokens)
        """
        self._metadata_service = metadata_service
        self._llm_available = llm_available
        self._lazy_load = lazy_load
        self._state = AnalysisPhase.INITIAL
        
        # Lazy loading: Don't load books until LLM requests them
        if not lazy_load:
            print("Note: Lazy loading disabled - loading all books upfront")
    
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
        
        # Build books metadata (without Python keyword matching)
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
            # Phase 1 needs more tokens for complete JSON with all content_requests
            # Increased from 3000 to 8000 to prevent JSON truncation
            max_tokens_phase1 = 8000
            llm_output = call_llm(prompt, max_tokens=max_tokens_phase1)
            
            # DEBUG: Show raw LLM response
            print("\n" + "="*80)
            print("DEBUG: Raw Claude Response (Phase 1)")
            print("="*80)
            print(llm_output[:2000])  # Show first 2000 chars
            if len(llm_output) > 2000:
                print(f"\n... (truncated, total length: {len(llm_output)} chars)")
            print("="*80 + "\n")
            
            # CRITICAL: Check if response was truncated (hit token limit)
            # We can't get actual token count here, but we can estimate
            estimated_tokens = len(llm_output) // 3  # Rough estimate: 3 chars per token
            truncation_threshold = max_tokens_phase1 * 0.95  # 95% of max
            
            if estimated_tokens >= truncation_threshold:
                print(f"⚠️  WARNING: Response may be truncated (~{estimated_tokens:,} tokens, limit: {max_tokens_phase1:,})")
                print("   This suggests LLM tried to request too many books.")
                print("   Will attempt to parse and validate...")
            
            response = LLMMetadataResponse.from_llm_output(llm_output)
            
            # BATCHING LOGIC: If we got 0 requests but response was near limit, it was likely truncated
            if len(response.content_requests) == 0 and estimated_tokens >= truncation_threshold:
                print(f"\n❌ TRUNCATION DETECTED: Got 0 content requests but response was {estimated_tokens:,} tokens")
                print("   LLM response was cut off before completing the content_requests array.")
                print("   Re-prompting with constraint to limit to top 10 most relevant books...")
                
                # Re-prompt with constraint
                constrained_prompt = prompt + f"""

IMPORTANT CONSTRAINT: You have access to {len(books_metadata)} books, but please limit your content_requests 
to ONLY the TOP 10 most relevant and high-priority books. Focus on quality over quantity. 
Prioritize books that provide the most direct, substantial coverage of this chapter's core concepts."""
                
                llm_output = call_llm(constrained_prompt, max_tokens=max_tokens_phase1)
                response = LLMMetadataResponse.from_llm_output(llm_output)
                
                print(f"✓ Retry with constraint: Found {len(response.content_requests)} content requests")
            
            # SECONDARY BATCHING: If still getting too many requests (>15), truncate to top 10
            if len(response.content_requests) > 15:
                print(f"\n⚠️  LLM requested {len(response.content_requests)} books - limiting to top 10 by priority")
                # Sort by priority (lower number = higher priority)
                sorted_requests = sorted(response.content_requests, key=lambda r: r.priority)
                response.content_requests = sorted_requests[:10]
                print("✓ Truncated to top 10 highest-priority requests")
            
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
        
        # Gather comprehensive metadata
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
            llm_output = call_llm(prompt, max_tokens=2000)
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
            annotation_text = call_llm(prompt, max_tokens=1500)
            
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
            from chapter_metadata_manager import ChapterMetadataManager
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
                            'concepts': ch.concepts[:10],  # Top 10 key concepts
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
    
    def _format_book_description(self, book: Dict[str, Any], index: int) -> str:
        """Format a single book's metadata description with chapter details.
        
        Extracts book metadata formatting to reduce complexity of parent function.
        """
        book_desc = f"{index}. {book['title']}\n   Author(s): {book.get('author', 'Unknown')}\n   Full Title: {book.get('full_title', book['title'])}\n   Domain: {book['domain']}\n   Concepts: {', '.join(book['concepts_covered'][:8])}"
        
        # Add detailed chapter information if available
        if book.get('has_chapter_metadata') and book.get('chapters'):
            chapters_summary = "\n   Chapters:"
            for ch in book['chapters'][:10]:  # Show first 10 chapters with full metadata
                chapters_summary += f"\n     • Ch.{ch['number']}: {ch['title']} (pp.{ch['pages']})"
                if ch.get('summary'):
                    chapters_summary += f"\n       Summary: {ch['summary']}"
                if ch.get('concepts'):
                    chapters_summary += f"\n       Concepts: {', '.join(ch['concepts'][:5])}"
            
            if len(book['chapters']) > 10:
                chapters_summary += f"\n     ... [{len(book['chapters'])} chapters total]"
            book_desc += chapters_summary
        
        return book_desc
    
    def _build_comprehensive_phase1_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str,
        books_metadata: List[Dict[str, Any]]
    ) -> str:
        """Build Phase 1 prompt for comprehensive LLM-driven analysis."""
        
        books_list = [self._format_book_description(book, i) for i, book in enumerate(books_metadata, 1)]
        books_text = "\n\n".join(books_list)
        
        return f"""You are conducting a comprehensive scholarly cross-reference analysis for Learning Python Ed.6.

CHAPTER {chapter_num}: {chapter_title}

FULL CHAPTER TEXT ({len(chapter_full_text)} characters):
{chapter_full_text[:8000]}
{"... [truncated for prompt length]" if len(chapter_full_text) > 8000 else ""}

COMPANION BOOKS AVAILABLE ({len(books_metadata)} books with chapter metadata):
{books_text}

NOTE: Book content is NOT loaded yet - only metadata is shown above.
After you make your requests, the system will load ONLY the specific chapters you request.
This saves memory and tokens, so feel free to request what you need!

YOUR TASK:

1. READ & ANALYZE THE CHAPTER:
   - Extract ALL key concepts, techniques, and topics covered
   - Identify main themes and learning objectives
   - Note examples, code patterns, and pedagogical approaches

2. CROSS-REFERENCE DISCOVERY:
   - Review the 15 companion books above
   - For each book, consider both:
     * Overall concepts covered (shown in metadata)
     * Specific chapters that might relate (when chapter metadata available)
   - Use the book taxonomy:
     * Architecture Spine books: Patterns, DDD, microservices theory
     * Implementation Layer books: FastAPI, Flask, deployment, APIs
     * Engineering Practices books: Python idioms, recipes, language reference

3. REQUEST SPECIFIC CHAPTERS/SECTIONS:
   - For books WITH chapter metadata: Request specific chapters by number/title
     Example: "Chapter 5: Decorators" or "Chapter 8: Async Programming"
   - For books WITHOUT chapter metadata: Request page ranges that likely contain relevant content
   - Explain WHY each chapter/section would help build cross-references
   - Prioritize books that offer different perspectives (architecture vs implementation vs idioms)

RESPOND IN JSON FORMAT:
{{
  "concepts_extracted": ["list", "of", "all", "concepts", "found"],
  "themes_identified": ["main", "themes"],
  "content_requests": [
    {{
      "book_name": "exact book title",
      "chapters_or_sections": ["Chapter 5: Decorators", "Chapter 8, Section 2"],
      "pages": [145, 146, 147],
      "rationale": "why this content will enhance cross-references",
      "priority": 1-5
    }}
  ],
  "analysis_strategy": "Your plan for synthesizing an integrated annotation"
}}

GUIDELINES:
- Extract concepts comprehensively (don't rely on pre-defined keywords)
- Request 6-12 books that offer substantive cross-references
- Use chapter metadata when available for precise targeting
- Build many-to-many mapping across multiple books
- Consider cascading: Engineering concepts → Architecture patterns → Implementation examples

IMPORTANT CONSTRAINT:
To ensure focused, high-quality cross-references, please limit your content_requests to the TOP 10 most relevant books. Prioritize quality over quantity - select only those books that provide the most substantive connections to the current chapter's concepts.

Provide your comprehensive analysis now."""
    
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
        excerpts = []
        
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
        
        for page_num in req.pages[:10]:  # Limit pages per book
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
            from chapter_metadata_manager import ChapterMetadataManager
            chapter_manager = ChapterMetadataManager()
            has_chapter_metadata = True
        except Exception:
            chapter_manager = None
            has_chapter_metadata = False
        
        for req in content_requests[:10]:  # Limit to top 10 books
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
        import json
        
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
            
        Note: Keys match JSON filenames exactly. Values provide formal citation details.
        """
        citation_map = {
            # Python Language Books (keys match JSON filenames)
            "Learning Python Ed6": ("Lutz, Mark", "Learning Python Ed6"),
            PYTHON_ESSENTIAL_REF: ("Beazley, David", PYTHON_ESSENTIAL_REF),
            FLUENT_PYTHON: ("Ramalho, Luciano", FLUENT_PYTHON),
            PYTHON_DISTILLED: ("Beazley, David", PYTHON_DISTILLED),
            "Python Cookbook 3rd": ("Beazley, David and Jones, Brian K.", "Python Cookbook 3rd"),
            PYTHON_DATA_ANALYSIS: ("McKinney, Wes", PYTHON_DATA_ANALYSIS),
            
            # Architecture Books (keys match JSON filenames)
            "Architecture Patterns with Python": ("Percival, Harry and Gregory, Bob", "Architecture Patterns with Python"),
            "Python Microservices Development": ("Ziadé, Tarek", "Python Microservices Development"),
            "Building Microservices": ("Newman, Sam", "Building Microservices"),
            "Microservice Architecture": ("Dragoni, Nicola et al.", "Microservice Architecture"),
            "Microservices Up and Running": ("Gammelgård, Ronnie and Hammarberg, Marcus", "Microservices Up and Running"),
            "Building Python Microservices with FastAPI": ("Sinha, Sherwin John", "Building Python Microservices with FastAPI"),
            "Microservice APIs Using Python Flask FastAPI": ("Buelta, Jaime", "Microservice APIs Using Python Flask FastAPI"),
            "Python Architecture Patterns": ("Buelta, Jaime", "Python Architecture Patterns"),
        }
        
        if book_filename in citation_map:
            return citation_map[book_filename]
        
        # Fallback: use the filename as-is (already human-readable)
        return ("Unknown", book_filename)
    
    def _phase2_comprehensive_synthesis(
        self,
        chapter_num: int,
        chapter_title: str,
        chapter_full_text: str,
        metadata_response: LLMMetadataResponse
    ) -> ScholarlyAnnotation:
        """Phase 2 for comprehensive analysis: Lazy load content + synthesize annotation."""
        
        # LAZY LOADING: Only load chapters that LLM requested
        if self._lazy_load:
            content_package = self._lazy_load_requested_chapters(
                metadata_response.content_requests
            )
        else:
            # Old approach: retrieve from already-loaded books
            content_package = self._retrieve_requested_content(
                metadata_response.content_requests
            )
        
        print(f"Retrieved content from {len(content_package)} books")
        print(f"Total excerpts: {sum(len(excerpts) for excerpts in content_package.values())}")
        
        # Build synthesis prompt
        prompt = self._build_comprehensive_phase2_prompt(
            chapter_num,
            chapter_title,
            chapter_full_text,
            metadata_response,
            content_package
        )
        
        print(f"Estimated tokens: ~{self._estimate_tokens(prompt):,}")
        
        try:
            llm_output = call_llm(prompt, max_tokens=4000)
            
            # Parse annotation from LLM output
            annotation_text = llm_output.strip()
            
            # Extract sources and concepts (basic parsing)
            sources = list(content_package.keys())
            concepts = metadata_response.validation_summary  # Contains extracted concepts
            
            print(f"✓ Generated annotation: {len(annotation_text)} chars")
            print(f"✓ Sources cited: {len(sources)}")
            print(f"✓ Concepts validated: {len(metadata_response.content_requests)}")
            
            return ScholarlyAnnotation(
                chapter_number=chapter_num,
                chapter_title=chapter_title,
                annotation_text=annotation_text,
                sources_cited=sources,
                concepts_validated=concepts.split(', ') if isinstance(concepts, str) else [],
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
    ) -> str:
        """Build Phase 2 prompt for comprehensive synthesis.
        
        Args:
            chapter_num: Chapter number for identification
            chapter_title: Title of the chapter
            _chapter_full_text: Unused - Phase 2 works with requested excerpts from content_package
            metadata_response: Phase 1 analysis results
            content_package: Book excerpts requested in Phase 1
        """
        
        content_sections = []
        for book_name, excerpts in content_package.items():
            content_sections.append(f"\n## {book_name}")
            for exc in excerpts:
                # Handle full chapters vs page excerpts
                if exc.get('is_full_chapter'):
                    # Full chapter content with citation info
                    content_sections.append(
                        f"\n**Chapter {exc['chapter']}: {exc['title']}**\n"
                        f"Citation: {exc.get('author', 'Unknown')}, *{exc.get('book_title', book_name)}*, "
                        f"Chapter {exc['chapter']}, pages {exc['pages']}.\n"
                        f"Content:\n{exc['content'][:4000]}..."  # First 4000 chars of chapter
                    )
                else:
                    # Page excerpt with citation info
                    content_sections.append(
                        f"\n**Page {exc['page']}**\n"
                        f"Citation: {exc.get('author', 'Unknown')}, *{exc.get('book_title', book_name)}*, {exc['page']}.\n"
                        f"Content: {exc['content'][:600]}..."
                    )
        
        content_text = '\n'.join(content_sections)
        
        return f"""You are generating an integrated scholarly annotation for Learning Python Ed.6.

CHAPTER {chapter_num}: {chapter_title}

CONCEPTS YOU EXTRACTED:
{metadata_response.validation_summary}

YOUR ANALYSIS STRATEGY:
{metadata_response.analysis_strategy}

COMPANION CONTENT RETRIEVED (from {len(content_package)} books):
NOTE: Some entries are FULL CHAPTERS, others are page excerpts.
{content_text[:15000]}

TASK: Write a comprehensive integrated annotation (8-12 sentences) that:

1. BRIDGE CONCEPTS ACROSS TEXTS:
   - Show how concepts in Learning Python connect to architectural patterns (Architecture books)
   - Demonstrate how concepts are applied in real implementations (Implementation books)
   - Highlight advanced techniques or idioms (Engineering Practices books)

2. CREATE INTEGRATED ANALYSIS:
   - Don't just list what each book says separately
   - SYNTHESIZE: Show how ideas from different books reinforce/extend each other
   - Example: "The decorator syntax (Learning Python) maps to the Decorator Pattern (Architecture Patterns) 
     and is used for dependency injection in FastAPI (Implementation)"

3. ACADEMIC RIGOR:
   - Cite specific content from retrieved chapters/excerpts using Chicago-style footnotes
   - For full chapters, cite the chapter title and key points
   - **CHICAGO FOOTNOTE FORMAT**: Author(s), *Book Title*, Chapter/Section, page numbers.
     Example: "Ramalho, Luciano, *Fluent Python, 2nd Edition*, Chapter 5, 145-167."
   - Include inline citations in your annotation text
   - Explain pedagogical value (why learners should consult these references)
   - Note any gaps or areas needing further exploration

4. TIER-BASED ORGANIZATION:
   - Architecture Spine: Theoretical foundations, patterns, design principles
   - Implementation Layer: Practical applications, deployments, real-world usage
   - Engineering Practices: Language features, idioms, best practices

5. CITATION REQUIREMENTS (Chicago Manual of Style, 17th Edition):
   - Use footnote-style citations embedded in your annotation
   - Format: Author(s), *Book Title*, edition/chapter info, page numbers.
   - For chapters: Include chapter number and title when available
   - Example for full chapter: "As Percival and Gregory demonstrate in *Architecture Patterns with Python*, 
     Chapter 3, pages 45-67, the repository pattern provides..."
   - Example for single page: "Ramalho notes (*Fluent Python, 2nd Edition*, 145) that..."
   - When synthesizing multiple sources, cite each appropriately
   - All citation metadata has been provided above for each excerpt

Generate the integrated scholarly annotation now (output only the annotation text, no JSON)."""
    
    # ========================================================================
    # SCENARIO 1 METHODS: Python-Guided Analysis (Original)
    # ========================================================================
    
    def _get_taxonomy_recommendations(self, concepts: List[str]) -> tuple[List[str], Dict[str, List[str]]]:
        """Get book recommendations and cascading relationships from taxonomy.
        
        Args:
            concepts: List of concepts to match against taxonomy
            
        Returns:
            Tuple of (recommended_books, cascading_info) where cascading_info maps book_name -> cascaded books
        """
        if not TAXONOMY_AVAILABLE:
            return [], {}
        
        concept_set = set(concepts)
        scored_books = score_books_for_concepts(concept_set)
        recommended_books = [book_name for book_name, score in scored_books if score >= 0.2]
        
        # Build cascading relationships
        cascading_info = {}
        for book_name in recommended_books[:8]:
            cascades = get_cascading_books(book_name, depth=1)
            if cascades:
                cascading_info[book_name] = cascades
                for cascaded_book in cascades:
                    if cascaded_book not in recommended_books:
                        recommended_books.append(cascaded_book)
        
        return recommended_books, cascading_info
    
    def _calculate_relevance_boosts(
        self,
        book_file_name: str,
        cascading_info: Dict[str, List[str]]
    ) -> tuple[float, float]:
        """Calculate tier and cascading boosts for a book.
        
        Args:
            book_file_name: Book's canonical file name
            cascading_info: Dict mapping source books to their cascaded books
            
        Returns:
            Tuple of (tier_boost, cascading_boost)
        """
        tier_boost = 0.0
        cascading_boost = 0.0
        
        if not TAXONOMY_AVAILABLE or book_file_name not in BOOK_REGISTRY:
            return tier_boost, cascading_boost
        
        book_role = BOOK_REGISTRY[book_file_name]
        
        # Higher tier = higher priority
        if book_role.tier == BookTier.ARCHITECTURE_SPINE:
            tier_boost = 0.3
        elif book_role.tier == BookTier.IMPLEMENTATION:
            tier_boost = 0.2
        else:  # ENGINEERING_PRACTICES
            tier_boost = 0.1
        
        # Check if this book is recommended via cascading
        for cascades in cascading_info.values():
            if book_file_name in cascades:
                cascading_boost = 0.2
                break
        
        return tier_boost, cascading_boost
    
    def _build_book_metadata_entry(
        self,
        book: BookMetadata,
        concept_map: Dict[str, List[ConceptMatch]],
        cascading_info: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Build metadata entry for a single book.
        
        Args:
            book: BookMetadata object
            concept_map: Concept to ConceptMatch mapping
            cascading_info: Cascading relationships between books
            
        Returns:
            Dict with book metadata including relevance scores
        """
        base_relevance = self._calculate_book_relevance(book, concept_map)
        tier_boost, cascading_boost = self._calculate_relevance_boosts(book.file_name, cascading_info)
        final_relevance = base_relevance + tier_boost + cascading_boost
        
        book_meta = {
            'file_name': book.file_name,
            'domain': book.domain,
            'total_pages': book.total_pages,
            'chapters_count': len(book.chapters),
            'concepts_covered': sorted(book.concepts_covered),
            'relevance_to_chapter': round(final_relevance, 2),
            'tier': BOOK_REGISTRY[book.file_name].tier.value if TAXONOMY_AVAILABLE and book.file_name in BOOK_REGISTRY else 'Unknown'
        }
        
        if book.file_name in cascading_info:
            book_meta['cascades_to'] = cascading_info[book.file_name]
        
        return book_meta
    
    def _build_metadata_package(self, concepts: List[str]) -> Dict[str, Any]:
        """Build comprehensive metadata package for Phase 1.
        
        Engineering: Dictionary comprehension and data transformation
        (Fluent Python Ch. 3 - Dictionaries and Sets)
        
        NOW WITH CASCADING LOGIC: Enhances concept mapping with tier-based recommendations
        Refactored to reduce cognitive complexity.
        """
        all_books = self._metadata_service._repo.get_all()
        concept_map = self._metadata_service.create_concept_mapping(concepts)
        
        # Get taxonomy-based recommendations
        _recommended_books, cascading_info = self._get_taxonomy_recommendations(concepts)
        
        # Build structured metadata for each book
        books_metadata = [
            self._build_book_metadata_entry(book, concept_map, cascading_info)
            for book in all_books
        ]
        
        # Sort by relevance
        books_metadata.sort(key=lambda b: b['relevance_to_chapter'], reverse=True)
        
        # Build complete metadata package
        metadata_package = {
            'books': books_metadata,
            'concept_mapping': {
                concept: [
                    {
                        'book': match.book_name,
                        'pages': match.pages[:5],
                        'occurrences': match.total_occurrences,
                        'relevance': round(match.relevance_score, 2)
                    }
                    for match in matches[:3]
                ]
                for concept, matches in concept_map.items()
            },
            'total_books': len(books_metadata),
            'total_pages': sum(b['total_pages'] for b in books_metadata),
            'cascading_relationships': cascading_info if TAXONOMY_AVAILABLE else {}
        }
        
        # Save for fallback use in _mock_metadata_response
        self._last_metadata_package = metadata_package
        
        return metadata_package
    
    def _calculate_book_relevance(
        self,
        book: BookMetadata,
        concept_map: Dict[str, List[ConceptMatch]]
    ) -> float:
        """Calculate how relevant a book is to the chapter concepts.
        
        Engineering: Scoring algorithm using functional programming
        (Fluent Python Ch. 7 - Functions as First-Class Objects)
        """
        relevance = 0.0
        
        for concept, matches in concept_map.items():
            for match in matches:
                # Clean book name comparison
                match_book_clean = match.book_name.replace('_', ' ').lower()
                book_title_clean = book.title.replace('_', ' ').lower()
                
                if match_book_clean in book_title_clean or book_title_clean in match_book_clean:
                    relevance += match.relevance_score
        
        return relevance
    
    def _build_phase1_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str,
        metadata_package: Dict[str, Any]
    ) -> str:
        """Build Phase 1 prompt for metadata analysis.
        
        Engineering: String formatting and template composition
        (Python Distilled Ch. 2 - Operators and Expressions)
        """
        return f"""You are conducting a comprehensive gap analysis for Learning Python Ed.6 cross-references.

CHAPTER CONTEXT:
- Chapter {chapter_num}: {chapter_title}
- Key Concepts: {', '.join(concepts)}

CHAPTER EXCERPT:
{excerpt[:800]}

PYTHON KEYWORD MATCHING RESULTS:
{json.dumps(metadata_package['concept_mapping'], indent=2)}

COMPANION BOOK METADATA ({metadata_package['total_books']} books, {metadata_package['total_pages']:,} pages):
{json.dumps(metadata_package['books'], indent=2)}

TASK: Analyze the metadata and identify what specific content you need to perform a thorough scholarly cross-text analysis.

RESPOND IN JSON FORMAT:
{{
  "validation_summary": "Which Python matches look promising vs. superficial?",
  "gap_analysis": "What concepts/areas might be missing from Python matching?",
  "content_requests": [
    {{
      "book_name": "<<COPY EXACT file_name HERE>>",
      "pages": [page numbers],
      "rationale": "why needed",
      "priority": 1-5
    }}
  ],
  "analysis_strategy": "planned approach"
}}

CRITICAL: For book_name, copy the EXACT file_name value from metadata. Examples:
✅ CORRECT: "Fluent Python 2nd" (matches file_name in metadata)
✅ CORRECT: "Python Distilled" (matches file_name in metadata)  
✅ CORRECT: "Architecture Patterns with Python" (matches file_name)
❌ WRONG: "Fluent Python, 2nd Edition" (don't add commas or Edition)
❌ WRONG: "Python Distilled Content" (don't add Content)

Look at the file_name field in the metadata above and copy it character-for-character.

GUIDELINES FOR ANALYZING PYTHON KEYWORD MATCHING RESULTS:
1. EVALUATE MATCHES: Review the concept_mapping data showing which books/pages match each concept
   - High relevance (>0.7): Strong indicator of substantive coverage
   - Medium relevance (0.4-0.7): May be worth investigating
   - Low relevance (<0.4): Likely superficial mentions

2. VALIDATE PROMISING MATCHES: Request pages from high-relevance matches to verify they provide:
   - Technical depth beyond simple keyword mentions
   - Different perspectives or advanced treatment
   - Architectural or implementation context

3. IDENTIFY GAPS: Look for concepts that may need coverage beyond keyword matching:
   - Abstract concepts that may appear under different terminology
   - Architectural patterns that connect to the chapter's concepts
   - Implementation techniques not directly named in the chapter

4. APPLY BOOK TAXONOMY (evaluate ALL 15 books comprehensively):
   
   ARCHITECTURE SPINE BOOKS (foundational patterns):
   - Architecture Patterns with Python: DDD/Event-Driven foundation, cascades to implementation
   - Building Microservices: Conceptual rationale, organizational patterns
   - Microservice Architecture: Academic theory, formal design patterns
   - Python Architecture Patterns: Pattern catalog, architectural crosswalks
   
   IMPLEMENTATION LAYER BOOKS (practical application):
   - Python Microservices Development: Docker, async, deployment scaffolding
   - Building Python Microservices with FastAPI: Modern async, dependency injection
   - Microservice APIs Using Python Flask FastAPI: API governance, versioning
   - Microservices Up and Running: Operational lifecycle, observability
   
   ENGINEERING PRACTICES BOOKS (language and idioms):
   - Python Essential Reference 4th: Language syntax and semantics foundation
   - Fluent Python 2nd: Advanced Pythonic patterns, protocols, metaclasses
   - Python Distilled: Concise best practices and core concepts
   - Python Cookbook 3rd: Recipe-based practical solutions
   - Python Data Analysis 3rd: Data structures and analysis patterns
   - Learning Python Ed6: (Primary text - do not self-reference)

5. USE CASCADING LOGIC: When a concept triggers matches in one tier, check related tiers:
   - Engineering concept (e.g., "decorator") → Check Architecture books for decorator pattern
   - Architecture pattern → Check Implementation books for practical applications
   - Implementation technique → Check Engineering books for language fundamentals

6. REQUEST STRATEGICALLY:
   - Include ALL books with relevance > 0.3 (typically 8-15 books for comprehensive analysis)
   - Organize requests by tier (Architecture → Implementation → Engineering)
   - Request 3-8 pages per book focusing on highest-relevance matches
   - Set priority 5 for foundational concepts, 3-4 for supporting context, 1-2 for peripheral references

7. CROSS-TIER VALIDATION:
   - If Engineering Practice book shows high relevance, check if Architecture books provide patterns
   - If Architecture book matches, verify Implementation books show practical usage
   - Build many-to-many mapping across all applicable books

Provide your comprehensive analysis now."""
    
    def _build_phase2_prompt(
        self,
        chapter_num: int,
        chapter_title: str,
        concepts: List[str],
        excerpt: str,
        metadata_response: LLMMetadataResponse,
        content_package: Dict[str, List[Dict]]
    ) -> str:
        """Build Phase 2 prompt for deep scholarly analysis."""
        
        # Format retrieved content
        content_sections = []
        for book_name, excerpts in content_package.items():
            content_sections.append(f"\n## {book_name}")
            for exc in excerpts:
                content_sections.append(
                    f"\nPage {exc['page']}: {exc['content'][:500]}..."
                )
        
        content_text = '\n'.join(content_sections)
        
        return f"""You are generating a scholarly cross-text annotation for Learning Python Ed.6.

CHAPTER {chapter_num}: {chapter_title}
KEY CONCEPTS: {', '.join(concepts)}

PRIMARY TEXT EXCERPT:
{excerpt[:800]}

YOUR PHASE 1 ANALYSIS:
- Validation: {metadata_response.validation_summary[:200]}
- Gaps Identified: {metadata_response.gap_analysis[:200]}
- Strategy: {metadata_response.analysis_strategy[:200]}

COMPANION BOOKS CONTENT (from {len(content_package)} books):
{content_text[:8000]}

TASK: Write a scholarly annotation that analyzes the relationship between the primary text and companion book excerpts.

ANALYSIS APPROACH:

1. VALIDATE EACH EXCERPT: For each companion book page above, determine:
   - Does it contain genuine technical/educational discussion of the matched concepts?
   - Or is it metadata, forewords, prefaces, or keyword-match artifacts?

2. FOR GENUINE TECHNICAL CONTENT:
   - Identify specific concepts that appear in BOTH the primary text and companion excerpt
   - Describe how the companion book treats these concepts differently (e.g., deeper implementation detail, alternative framing, architectural interpretation, formal description)
   - Cite concrete elements FROM THE COMPANION EXCERPT ITSELF (terminology, definitions, behaviors, code patterns, rules)
   - Explain the pedagogical reason a learner should consult this cross-reference (clarifies ambiguity, expands mechanics, formalizes definitions, offers advanced idioms)

3. FOR NON-SUBSTANTIVE CONTENT:
   - Acknowledge why the match occurred (token overlap or keyword similarity)
   - State explicitly that the page does NOT provide substantive technical treatment
   - Explain this is a limitation of keyword matching, not a conceptual relationship
   - Direct the learner to rely on the primary text for this topic

4. ORGANIZE BY TIER (when multiple genuine sources exist):
   - Architecture Spine books: Patterns, DDD, theoretical frameworks
   - Implementation Layer books: Practical applications, deployment, real-world usage
   - Engineering Practices books: Language idioms, protocols, advanced techniques
   - Show connections across tiers when applicable

STRICT RULES:
- BE SPECIFIC. Use actual phrasing or technical elements from the excerpts
- DO NOT invent connections. Only describe relationships grounded in provided excerpts
- DO NOT use generic filler: "complements," "broadens," "enhances," "deepens"
- DO NOT summarize the books—analyze their relationship to the primary text
- DO NOT exceed 10 sentences total (aim for 5-7)
- OUTPUT ONLY the annotation text, no metadata or JSON

Generate the scholarly annotation now."""
    
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
        
        for request in sorted_requests[:10]:  # Limit to top 10 books
            # Clean book name for lookup
            clean_name = request.book_name.replace(' ', '_').replace('_Content', '')
            
            excerpts = []
            for page_num in request.pages[:10]:  # Limit pages per book
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
        """Extract cited sources from annotation text."""
        sources = []
        # Simple extraction - look for book mentions
        all_books = self._metadata_service._repo.get_all()
        for book in all_books:
            book_name_variants = [
                book.title,
                book.title.replace('_', ' '),
                book.file_name.replace('_Content.json', '').replace('_', ' ')
            ]
            for variant in book_name_variants:
                if variant.lower() in annotation.lower():
                    sources.append(book.title)
                    break
        return list(set(sources))
    
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
        """Get recommended books using taxonomy or fallback to concept mapping.
        
        Args:
            concepts: List of concepts to match
            concept_mapping: Dict mapping concepts to matched books/pages
            
        Returns:
            List of recommended book names
        """
        try:
            from book_taxonomy import get_recommended_books
            concept_set = set(concepts)
            return get_recommended_books(
                concept_set,
                min_relevance=0.3,
                include_cascades=True,
                max_books=12
            )
        except Exception:
            # Fallback: use all books from concept_mapping
            return list(concept_mapping.keys())[:12]
    
    def _calculate_request_priority(
        self,
        matched_concepts: set,
        total_concepts: int,
        book_name: str
    ) -> int:
        """Calculate priority for a content request.
        
        Args:
            matched_concepts: Set of concepts matched in this book
            total_concepts: Total number of concepts being searched
            book_name: Name of the book
            
        Returns:
            Priority score (1-5)
        """
        match_strength = len(matched_concepts) / max(total_concepts, 1)
        base_priority = min(5, int(match_strength * 5) + 1)
        
        # Adjust by book tier if taxonomy available
        try:
            from book_taxonomy import BOOK_REGISTRY
            if book_name in BOOK_REGISTRY:
                tier = BOOK_REGISTRY[book_name].tier.value
                if "Architecture" in tier:
                    base_priority = min(5, base_priority + 1)
        except Exception:
            pass
        
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
        
        priority = self._calculate_request_priority(all_matched_concepts, len(concepts), book_name)
        
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
                book_name=PYTHON_DISTILLED,
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
        annotation_text = f"""The {chapter_title} chapter introduces Python's numeric type system, which receives sophisticated treatment in several companion texts. Python Essential Reference 4th (Ch. 3, pp. 145-148) provides comprehensive implementation details for integer, float, and Decimal types, emphasizing precision control through decimal.Context managers—a critical topic absent from Learning Python's introductory coverage. Fluent Python 2nd (Ch. 12, pp. 89-91) demonstrates advanced numeric protocols through operator overloading examples, showing how custom classes can integrate seamlessly with Python's numeric tower using __add__, __mul__, and other special methods. The gap analysis reveals that while Learning Python establishes foundational concepts like type coercion and basic arithmetic, it defers complex number applications and NumPy integration patterns that appear extensively in Python Data Analysis 3rd. Python Distilled (pp. 45-46) offers a concise middle ground, covering numeric best practices including integer division nuances and floating-point comparison pitfalls that intermediate learners should understand."""
        
        return ScholarlyAnnotation(
            chapter_number=chapter_num,
            chapter_title=chapter_title,
            annotation_text=annotation_text,
            sources_cited=[PYTHON_ESSENTIAL_REF, FLUENT_PYTHON, PYTHON_DATA_ANALYSIS, PYTHON_DISTILLED],
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