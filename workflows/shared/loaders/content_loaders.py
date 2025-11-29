"""
Content loading utilities for two-phase LLM workflow.

Sprint 3.2 - TDD GREEN: Extract content loading methods from interactive_llm_system_v3_hybrid_prompt.py

Following Document Hierarchy:
- REFACTORING_PLAN.md: Sprint 3.2 - Extract content loaders
- docs/BOOK_TAXONOMY_MATRIX.md: Engineering Practices tier - File I/O, Python fundamentals
- ARCHITECTURE_GUIDELINES: Repository Pattern (Ch. 4), Strategy Pattern (Ch. 5)
  * Repository abstracts data access from business logic
  * Strategy pattern for different loading approaches
  * Single Responsibility Principle
- PYTHON_GUIDELINES: File I/O (Ch. 9), Path handling (Ch. 10), Type hints (Ch. 7)
  * Pathlib for file operations
  * Type hints for all parameters and returns
  * Exception handling for file operations

Architectural Patterns Applied:
- Repository Pattern (Architecture Patterns Ch. 4): BookContentRepository
- Strategy Pattern (Architecture Patterns Ch. 5): ChapterContentLoader
- Lazy Loading: Load content only when requested

TDD GREEN Phase:
- Extracted from lines 682-936 of interactive_llm_system_v3_hybrid_prompt.py
- Preserves all functionality exactly
- Enables 9 failing tests to pass
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

# Sprint 3.3: Import centralized constants (eliminates duplication)
# Per Quality Assessment: Fix 4 duplicate constants issue
# Reference: REFACTORING_PLAN.md Sprint 3.3 - Constants extraction
from workflows.shared.constants import BookTitles

# Module-level logger
logger = logging.getLogger(__name__)


class BookContentRepository:
    """
    Repository for loading book JSON content.
    
    Pattern: Repository Pattern (Architecture Patterns Ch. 4)
    
    Abstracts file system access for loading book content. Provides a clean
    interface for the rest of the application to retrieve book data without
    knowing about file paths, JSON parsing, or error handling.
    
    Responsibilities:
    - Load book JSON files by name
    - Provide citation information (author, title)
    - Handle file system errors gracefully
    - Return None for missing books (fail-safe)
    
    References:
        - ARCHITECTURE_GUIDELINES Ch. 4: Repository Pattern
        - PYTHON_GUIDELINES Ch. 9: File I/O operations
        - PYTHON_GUIDELINES Ch. 10: Path handling with pathlib
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 844-936
    """
    
    # Class constant: Citation map for Chicago-style citations
    # Per PYTHON_GUIDELINES Ch. 6: Class constants for immutable data
    # Sprint 3.3: Using centralized BookTitles constants (no duplication)
    CITATION_MAP = {
        # Python Language Books (keys match JSON filenames)
        "Learning Python Ed6": ("Lutz, Mark", "Learning Python Ed6"),
        BookTitles.PYTHON_ESSENTIAL_REF: ("Beazley, David", BookTitles.PYTHON_ESSENTIAL_REF),
        BookTitles.FLUENT_PYTHON: ("Ramalho, Luciano", BookTitles.FLUENT_PYTHON),
        BookTitles.PYTHON_DISTILLED: ("Beazley, David", BookTitles.PYTHON_DISTILLED),
        "Python Cookbook 3rd": ("Beazley, David and Jones, Brian K.", "Python Cookbook 3rd"),
        BookTitles.PYTHON_DATA_ANALYSIS: ("McKinney, Wes", BookTitles.PYTHON_DATA_ANALYSIS),
        
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
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize repository with data directory.
        
        Args:
            data_dir: Optional path to data directory. If None, uses default
                     location relative to this file.
        """
        if data_dir is None:
            # Default: ../data/textbooks_json relative to this file
            self.data_dir = Path(__file__).parent.parent.parent / "data" / "textbooks_json"
        else:
            self.data_dir = data_dir
    
    def load_book_json(self, book_name: str) -> Optional[Dict]:
        """
        Load a single book's JSON file by its human-readable name.
        
        This is the lazy loading implementation - only called when needed.
        
        Args:
            book_name: Human-readable book name (e.g., "Fluent Python 2nd")
            
        Returns:
            Dict with book content (pages indexed by page number), or None if not found
            
        References:
            - PYTHON_GUIDELINES Ch. 9: File I/O with context managers
            - PYTHON_GUIDELINES Ch. 10: Pathlib for file operations
        """
        # Filename is just book_name + .json (e.g., "Fluent Python 2nd.json")
        target_filename = f"{book_name}.json"
        
        # Check if directory exists
        if not self.data_dir.exists():
            logger.warning(f"JSON directory not found: {self.data_dir}")
            return None
        
        json_file = self.data_dir / target_filename
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
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
                logger.error(f"Error loading {json_file}: {e}")
                return None
        
        # If not found, log helpful debug info
        logger.warning(f"Could not find file '{target_filename}' in JSON directory")
        return None
    
    def get_citation_info(self, book_name: str) -> tuple[str, str]:
        """
        Get author and full title for Chicago-style citations.
        
        Args:
            book_name: Human-readable book name matching JSON filename
                      (e.g., "Fluent Python 2nd")
            
        Returns:
            Tuple of (author, full_title) for citation formatting
            
        Note:
            Keys match JSON filenames exactly. Values provide formal citation details.
            Uses class constant CITATION_MAP for better encapsulation.
            
        References:
            - PYTHON_GUIDELINES Ch. 6: Class constants for immutable data
            - Source: interactive_llm_system_v3_hybrid_prompt.py lines 897-929
        """
        if book_name in self.CITATION_MAP:
            return self.CITATION_MAP[book_name]
        
        # Fallback: use the filename as-is (already human-readable)
        return ("Unknown", book_name)


class ChapterContentLoader:
    """
    Strategy for loading chapter content from books.
    
    Pattern: Strategy Pattern (Architecture Patterns Ch. 5)
    
    Encapsulates different strategies for loading content:
    1. Full chapter loading (all pages in a chapter)
    2. Chapter-based loading (load specific chapters from request)
    3. Page excerpt loading (fallback - individual pages)
    
    Works with BookContentRepository to retrieve book data, then applies
    specific loading strategies based on the request.
    
    Responsibilities:
    - Load full chapter content with metadata
    - Load chapters based on ContentRequest objects
    - Load individual page excerpts (fallback)
    - Format content with proper citations
    
    References:
        - ARCHITECTURE_GUIDELINES Ch. 5: Strategy Pattern
        - PYTHON_GUIDELINES Ch. 7: Dataclass integration
        - Source: interactive_llm_system_v3_hybrid_prompt.py lines 682-787
    """
    
    def __init__(self, repository: Optional[BookContentRepository] = None):
        """
        Initialize loader with repository.
        
        Args:
            repository: Optional BookContentRepository. If None, creates default.
        """
        self.repository = repository or BookContentRepository()
    
    def load_full_chapter(
        self,
        chapter_num: int,
        chapter_info,
        book_content: Dict,
        book_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load all pages for a specific chapter.
        
        Args:
            chapter_num: Chapter number to load
            chapter_info: Chapter metadata object with start_page, end_page, title
            book_content: Full book JSON content dict
            book_name: Human-readable book name for citation
            
        Returns:
            Dict with chapter content and metadata, or None if no content found
            
        References:
            - Source: interactive_llm_system_v3_hybrid_prompt.py lines 682-721
        """
        chapter_content = []
        for page_num in range(chapter_info.start_page, chapter_info.end_page + 1):
            if str(page_num) in book_content:
                page_text = book_content[str(page_num)].get('content', '')
                chapter_content.append(page_text)
        
        if not chapter_content:
            return None
        
        author, full_title = self.repository.get_citation_info(book_name)
        
        logger.info(f"Loaded Chapter {chapter_num} from {book_name} ({len(chapter_content)} pages)")
        
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
    
    def load_chapters_for_request(
        self,
        req,  # ContentRequest from models
        book_content: Dict,
        chapter_manager,
        extract_chapter_numbers_func
    ) -> List[Dict[str, Any]]:
        """
        Load full chapters based on request rationale.
        
        Args:
            req: ContentRequest with book name and rationale
            book_content: Full book JSON content
            chapter_manager: ChapterMetadataManager instance
            extract_chapter_numbers_func: Function to extract chapter numbers from rationale
            
        Returns:
            List of chapter excerpt dicts with content and metadata
            
        References:
            - Source: interactive_llm_system_v3_hybrid_prompt.py lines 724-756
        """
        excerpts: list[dict[str, Any]] = []
        
        chapter_nums = extract_chapter_numbers_func(req.rationale)
        if not chapter_nums:
            return excerpts
        
        chapters = chapter_manager.get_chapters(req.book_name.replace(' ', '_') + '_Content.json')
        
        for chapter_num in chapter_nums:
            chapter_info = next((ch for ch in chapters if ch.chapter_number == chapter_num), None)
            if chapter_info:
                chapter_data = self.load_full_chapter(
                    chapter_num, chapter_info, book_content, req.book_name
                )
                if chapter_data:
                    excerpts.append(chapter_data)
        
        return excerpts
    
    def load_page_excerpts(
        self,
        req,  # ContentRequest from models
        book_content: Dict
    ) -> List[Dict[str, Any]]:
        """
        Load individual pages for a content request (fallback behavior).
        
        Args:
            req: ContentRequest with book name and pages
            book_content: Full book JSON content
            
        Returns:
            List of page excerpt dicts with content and metadata
            
        References:
            - Source: interactive_llm_system_v3_hybrid_prompt.py lines 759-787
        """
        excerpts = []
        author, full_title = self.repository.get_citation_info(req.book_name)
        
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
