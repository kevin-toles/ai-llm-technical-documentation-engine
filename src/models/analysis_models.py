"""
Analysis data models for two-phase LLM workflow.

Sprint 3.1 - TDD GREEN: Extract data models from interactive_llm_system_v3_hybrid_prompt.py

Following Document Hierarchy:
- REFACTORING_PLAN.md: Sprint 3 - Extract classes to separate modules
- ARCHITECTURE_GUIDELINES: Single Responsibility Principle (Ch. 1)
  * Each class has ONE clear responsibility
  * Models are immutable value objects (where appropriate)
- PYTHON_GUIDELINES: Dataclasses, type hints, validation (Ch. 7, Ch. 14)
  * Use @dataclass for clean data structures
  * frozen=True for immutability where appropriate
  * Type hints for all fields
- BOOK_TAXONOMY_MATRIX: Engineering Practices tier
  * Python language fundamentals
  * Dataclass patterns from Python Distilled

Architectural Patterns Applied:
- State Machine (Python Architecture Patterns Ch. 8): AnalysisPhase enum
- Command Pattern (Architecture Patterns Ch. 9): ContentRequest
- Data Transfer Object (Microservices Ch. 6): LLMMetadataResponse
- Value Object (DDD): ScholarlyAnnotation

TDD GREEN Phase:
- Extracted from lines 83-236 of interactive_llm_system_v3_hybrid_prompt.py
- Preserves all functionality exactly
- Enables 6 failing tests to pass
"""

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List


class AnalysisPhase(Enum):
    """Analysis workflow states.
    
    Pattern: State Machine (Python Architecture Patterns Ch. 8)
    
    Represents different stages in the two-phase analysis workflow:
    - INITIAL: Starting state before any analysis
    - METADATA_SENT: Phase 1 metadata request sent to LLM
    - CONTENT_REQUESTED: Phase 2 content request sent to LLM
    - ANALYSIS_COMPLETE: Both phases completed successfully
    - FAILED: Analysis failed at some stage
    
    References:
        - ARCHITECTURE_GUIDELINES: State management patterns
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 83-92
    """
    INITIAL = auto()
    METADATA_SENT = auto()
    CONTENT_REQUESTED = auto()
    ANALYSIS_COMPLETE = auto()
    FAILED = auto()


@dataclass(frozen=True)
class ContentRequest:
    """Command for requesting specific book content.
    
    Pattern: Command Pattern (Architecture Patterns Ch. 9)
    
    Encapsulates all information needed to perform content retrieval from
    companion books. Immutable (frozen=True) to prevent modification after
    creation, following functional programming principles.
    
    Attributes:
        book_name: Title of the companion book to retrieve from
        pages: List of page numbers to retrieve
        rationale: Reason why this content is needed (from LLM)
        priority: Priority level (higher = more important, default=1)
    
    References:
        - ARCHITECTURE_GUIDELINES: Command pattern encapsulation
        - PYTHON_GUIDELINES: frozen dataclass for immutability
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 101-116
    """
    book_name: str
    pages: List[int]
    rationale: str
    priority: int = 1  # Higher = more important
    
    def __lt__(self, other: 'ContentRequest') -> bool:
        """Enable priority queue sorting.
        
        Returns True if self has HIGHER priority (reverse sort).
        This allows using heapq or sorted() with highest priority first.
        
        References:
            - PYTHON_GUIDELINES Ch. 4: Special methods for ordering
        """
        return self.priority > other.priority  # Higher priority first


@dataclass
class LLMMetadataResponse:
    """Structured response from Phase 1 metadata analysis.
    
    Pattern: Data Transfer Object (Microservices Ch. 6)
    
    Parses and validates LLM Phase 1 output into structured data.
    Supports both JSON and text-based formats for robustness.
    
    Attributes:
        validation_summary: LLM's validation of Python keyword matches
        gap_analysis: Identified gaps in keyword matching
        content_requests: List of ContentRequest objects for Phase 2
        analysis_strategy: Planned approach for content retrieval
    
    References:
        - ARCHITECTURE_GUIDELINES: DTO pattern for service boundaries
        - PYTHON_GUIDELINES Ch. 7: Dataclass with validation
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 118-218
    """
    validation_summary: str
    gap_analysis: str
    content_requests: List[ContentRequest]
    analysis_strategy: str
    
    @classmethod
    def from_llm_output(cls, llm_output: str) -> 'LLMMetadataResponse':
        """Parse LLM output into structured response.
        
        Factory method that handles multiple output formats:
        1. JSON format (preferred)
        2. Markdown-wrapped JSON (```json ... ```)
        3. Text format (fallback)
        
        Args:
            llm_output: Raw string output from LLM
            
        Returns:
            LLMMetadataResponse instance with parsed data
            
        References:
            - PYTHON_GUIDELINES Ch. 7: Factory method pattern
            - PYTHON_GUIDELINES Ch. 2: Robust string parsing
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
        
        Fallback parser for when LLM doesn't return valid JSON.
        Extracts sections based on keywords.
        
        Args:
            text: Raw text output from LLM
            
        Returns:
            LLMMetadataResponse with extracted sections
            
        References:
            - PYTHON_GUIDELINES Ch. 2: String parsing robustness
            - Pattern: Multiple parsing strategies for resilience
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
    
    Pattern: Value Object (Domain-Driven Design)
    
    Represents a complete scholarly annotation for a chapter, including
    the annotation text, sources cited, validated concepts, and identified gaps.
    
    Attributes:
        chapter_number: Chapter number (e.g., 1, 2, 3)
        chapter_title: Chapter title
        annotation_text: Complete scholarly annotation content
        sources_cited: List of cited sources (books, chapters, pages)
        concepts_validated: Concepts that were successfully cross-referenced
        gaps_identified: Concepts where cross-references couldn't be found
        metadata: Additional metadata (flexible dict for future extensions)
    
    References:
        - ARCHITECTURE_GUIDELINES: Value object pattern
        - PYTHON_GUIDELINES Ch. 7: Dataclass with default_factory
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 224-236
    """
    chapter_number: int
    chapter_title: str
    annotation_text: str
    sources_cited: List[str]
    concepts_validated: List[str]
    gaps_identified: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
