"""
Chapter Metadata Manager

Combines auto-detected chapter metadata with manual corrections.
Provides clean API for LLM system to access chapter structure.

Usage:
    manager = ChapterMetadataManager()
    chapters = manager.get_chapters("Fluent_Python_2nd_Content.json")
    chapter_summary = manager.get_chapter_summary("Fluent_Python_2nd_Content.json")
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ChapterInfo:
    """Clean chapter information for LLM consumption"""
    chapter_number: int
    title: str
    start_page: int
    end_page: int
    page_count: int
    keywords: List[str]
    summary: str = ""  # 2-3 sentence chapter summary
    concepts: List[str] = None  # Key concepts covered in chapter
    
    def __post_init__(self):
        """Ensure concepts is always a list"""
        if self.concepts is None:
            self.concepts = []
    
    def __str__(self) -> str:
        return f"Ch. {self.chapter_number}: {self.title} (pp. {self.start_page}-{self.end_page})"
    
    def to_compact_string(self) -> str:
        """One-line summary for LLM prompts"""
        return f"{self.chapter_number}. {self.title} (pp.{self.start_page}-{self.end_page})"


class ChapterMetadataManager:
    """
    Manages chapter metadata from multiple sources:
    1. Auto-detected chapters (chapter_metadata_cache.json)
    2. Manual corrections (chapter_metadata_manual.json)
    3. Existing JSON metadata (chapters field in book JSONs)
    """
    
    def __init__(self, scripts_dir: Optional[str] = None):
        if scripts_dir is None:
            scripts_dir = Path(__file__).parent
        else:
            scripts_dir = Path(scripts_dir)
        
        self.cache_file = scripts_dir / "chapter_metadata_cache.json"
        self.manual_file = scripts_dir / "chapter_metadata_manual.json"
        
        # Load all metadata sources
        self.auto_detected = self._load_auto_detected()
        self.manual_metadata = self._load_manual()
        self.override_files = self._load_override_list()
    
    def _load_auto_detected(self) -> Dict:
        """Load auto-detected chapter metadata"""
        if not self.cache_file.exists():
            return {}
        
        with open(self.cache_file, 'r') as f:
            return json.load(f)
    
    def _load_manual(self) -> Dict:
        """Load manual chapter metadata"""
        if not self.manual_file.exists():
            return {}
        
        with open(self.manual_file, 'r') as f:
            data = json.load(f)
        
        # Remove metadata fields
        return {k: v for k, v in data.items() if not k.startswith('_')}
    
    def _load_override_list(self) -> List[str]:
        """Load list of files where manual metadata overrides auto-detection"""
        if not self.manual_file.exists():
            return []
        
        with open(self.manual_file, 'r') as f:
            data = json.load(f)
        
        return data.get('_override_auto_detection', {}).get('files', [])
    
    def get_chapters(self, filename: str) -> List[ChapterInfo]:
        """
        Get chapter metadata for a book.
        Priority: Manual (if in override list) > Auto-detected
        """
        chapters_data = None
        
        # Check if manual override
        if filename in self.override_files and filename in self.manual_metadata:
            chapters_data = self.manual_metadata[filename].get('chapters', [])
        # Otherwise use auto-detected
        elif filename in self.auto_detected:
            chapters_data = self.auto_detected[filename]
        # Finally check manual (even if not in override)
        elif filename in self.manual_metadata:
            chapters_data = self.manual_metadata[filename].get('chapters', [])
        
        if not chapters_data:
            return []
        
        # Convert to ChapterInfo objects
        chapters = []
        for ch_data in chapters_data:
            try:
                chapter = ChapterInfo(
                    chapter_number=ch_data.get('chapter_number', 0),
                    title=ch_data.get('title', 'Unknown'),
                    start_page=ch_data.get('start_page', 0),
                    end_page=ch_data.get('end_page', 0),
                    page_count=ch_data.get('page_count', 
                                          ch_data.get('end_page', 0) - ch_data.get('start_page', 0) + 1),
                    keywords=ch_data.get('keywords', []),
                    summary=ch_data.get('summary', ''),  # Add summary field
                    concepts=ch_data.get('concepts', [])  # Add concepts field
                )
                chapters.append(chapter)
            except Exception as e:
                print(f"Warning: Error parsing chapter data: {e}")
                continue
        
        # Sort by chapter number
        chapters.sort(key=lambda x: x.chapter_number)
        
        return chapters
    
    def get_chapter_summary(self, filename: str, max_chapters: int = 20) -> str:
        """
        Get a compact summary of chapters for including in LLM prompts.
        
        Returns string like:
        "15 chapters: 1. Data Structures (pp.1-60), 2. Strings (pp.61-120), ..."
        """
        chapters = self.get_chapters(filename)
        
        if not chapters:
            return "No chapter metadata available"
        
        # Create compact list
        chapter_strs = [ch.to_compact_string() for ch in chapters[:max_chapters]]
        
        total_count = len(chapters)
        summary = f"{total_count} chapters: " + ", ".join(chapter_strs)
        
        if total_count > max_chapters:
            summary += f", ... and {total_count - max_chapters} more"
        
        return summary
    
    def get_chapter_by_number(self, filename: str, chapter_num: int) -> Optional[ChapterInfo]:
        """Get a specific chapter by number"""
        chapters = self.get_chapters(filename)
        
        for ch in chapters:
            if ch.chapter_number == chapter_num:
                return ch
        
        return None
    
    def find_chapters_by_keyword(self, filename: str, keyword: str) -> List[ChapterInfo]:
        """Find chapters that match a keyword"""
        chapters = self.get_chapters(filename)
        keyword_lower = keyword.lower()
        
        matches = []
        for ch in chapters:
            # Check in title
            if keyword_lower in ch.title.lower():
                matches.append(ch)
                continue
            
            # Check in keywords
            for kw in ch.keywords:
                if keyword_lower in kw.lower():
                    matches.append(ch)
                    break
        
        return matches
    
    def get_all_books_with_chapters(self) -> List[str]:
        """Get list of all book filenames that have chapter metadata"""
        all_books = set()
        
        all_books.update(self.auto_detected.keys())
        all_books.update(self.manual_metadata.keys())
        
        return sorted(list(all_books))
    
    def format_for_llm_prompt(self, filename: str, include_keywords: bool = False) -> str:
        """
        Format chapter metadata for LLM Phase 1 prompt.
        
        Returns formatted text like:
        ```
        Book: Fluent Python 2nd Ed.
        Chapters:
          1. The Python Data Model (pp.3-20) [data model, protocols, dunder]
          2. An Array of Sequences (pp.21-45) [sequences, lists, tuples]
          ...
        ```
        """
        chapters = self.get_chapters(filename)
        
        if not chapters:
            return f"Book: {filename}\nNo chapter structure available"
        
        # Get book display name (remove _Content.json suffix)
        book_name = filename.replace('_Content.json', '').replace('_', ' ')
        
        lines = [f"Book: {book_name}"]
        lines.append(f"Total Chapters: {len(chapters)}")
        lines.append("Structure:")
        
        for ch in chapters:
            if include_keywords and ch.keywords:
                kw_str = f" [{', '.join(ch.keywords[:5])}]"
            else:
                kw_str = ""
            
            lines.append(f"  {ch.chapter_number}. {ch.title} (pp.{ch.start_page}-{ch.end_page}){kw_str}")
        
        return "\n".join(lines)
    
    def generate_book_toc_summary(self) -> str:
        """Generate summary of all books and their chapter counts"""
        books = self.get_all_books_with_chapters()
        
        lines = ["="*80]
        lines.append("CHAPTER METADATA SUMMARY - ALL BOOKS")
        lines.append("="*80)
        
        for filename in books:
            chapters = self.get_chapters(filename)
            book_name = filename.replace('_Content.json', '').replace('_', ' ')
            
            if chapters:
                lines.append(f"\n📖 {book_name}")
                lines.append(f"   {len(chapters)} chapters (pages {chapters[0].start_page}-{chapters[-1].end_page})")
                
                # Show first 3 chapters
                for ch in chapters[:3]:
                    lines.append(f"   {ch}")
                
                if len(chapters) > 3:
                    lines.append(f"   ... and {len(chapters) - 3} more")
        
        lines.append("\n" + "="*80)
        return "\n".join(lines)


if __name__ == "__main__":
    # Test the manager
    manager = ChapterMetadataManager()
    
    print("="*80)
    print("CHAPTER METADATA MANAGER TEST")
    print("="*80)
    
    # Show all books
    print(manager.generate_book_toc_summary())
    
    # Test specific book
    print("\n" + "="*80)
    print("EXAMPLE: Fluent Python Chapter Metadata for LLM")
    print("="*80)
    print(manager.format_for_llm_prompt("Fluent_Python_2nd_Content.json", include_keywords=True))
    
    # Test keyword search
    print("\n" + "="*80)
    print("EXAMPLE: Find chapters about 'decorator'")
    print("="*80)
    
    for filename in ["Fluent_Python_2nd_Content.json", "Python_Cookbook_3rd_Content.json"]:
        matches = manager.find_chapters_by_keyword(filename, "decorator")
        if matches:
            print(f"\n{filename}:")
            for ch in matches:
                print(f"  {ch}")
