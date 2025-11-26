#!/usr/bin/env python3
"""
Generate Chapter Metadata: Summaries, Keywords, and Concepts

This script extracts chapter summaries, keywords, and key concepts from 
all 15 book JSON files and updates the chapter_metadata_cache.json file.

For each chapter in each book:
1. Reads the chapter's page content from the JSON
2. Extracts keywords and concepts from the text
3. Generates a brief summary of the chapter's main topics
4. Updates the metadata cache with this information

Usage:
    python3 generate_chapter_metadata.py

Reference: 
- Python Distilled Ch. 7 - Dataclass configuration patterns
- Python Distilled Ch. 9 - pathlib.Path operations  
- Microservices Up and Running Ch. 7 - 12-Factor App configuration
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add project root to path for config access
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configuration management (12-Factor App pattern)
from config.settings import settings  # noqa: E402

# Import StatisticalExtractor for domain-agnostic metadata extraction
# Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.4
from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor  # noqa: E402

# Global extractor instance (initialized once, reused for all chapters)
STATISTICAL_EXTRACTOR = StatisticalExtractor()

# Book locations (simplified - all books now in textbooks_json_dir root)
# Reference: Microservices Ch. 7 - Externalized configuration
BOOK_PATHS = {
    "Fluent Python 2nd.json": "",
    "Python Distilled.json": "",
    "Python Essential Reference 4th.json": "",
    "Python Cookbook 3rd.json": "",
    "Learning Python Ed6.json": "",
    "Python Data Analysis 3rd.json": "",
    "Architecture Patterns with Python.json": "",
    "Python Architecture Patterns.json": "",
    "Building Microservices.json": "",
    "Microservice Architecture.json": "",
    "Microservices Up and Running.json": "",
    "Building Python Microservices with FastAPI.json": "",
    "Microservice APIs Using Python Flask FastAPI.json": "",
    "Python Microservices Development.json": ""
}

# DEPRECATED: Hardcoded keyword list replaced by StatisticalExtractor
# Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.4
# This function is kept for backward compatibility but no longer used
def _get_python_keyword_list() -> List[str]:
    """
    DEPRECATED: Return comprehensive list of Python and programming keywords.
    
    This function has been replaced by StatisticalExtractor's YAKE-based extraction.
    The hardcoded keyword approach only worked for Python/software books.
    
    Use extract_keywords_from_text() instead, which now uses domain-agnostic
    statistical NLP that works across ANY domain (Python, biology, law, etc.).
    """
    return []  # Empty list - no longer used


def extract_keywords_from_text(text: str, max_keywords: int = 15) -> List[str]:
    """
    Extract meaningful keywords from chapter text using statistical NLP.
    
    Replaced hardcoded Python keyword matching with YAKE unsupervised extraction.
    Now works across ANY domain (Python, biology, law, construction, etc.).
    
    Args:
        text: Chapter text content
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords sorted by relevance (YAKE score)
        
    Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.4: Metadata enrichment integration
        - ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for NLP libraries
    """
    keywords_with_scores = STATISTICAL_EXTRACTOR.extract_keywords(text, top_n=max_keywords)
    return [keyword for keyword, score in keywords_with_scores]


# DEPRECATED: Hardcoded concept patterns replaced by StatisticalExtractor
# Per DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.4
# This list is kept for documentation but no longer used
CONCEPT_PATTERNS = []  # Empty list - no longer used


def extract_concepts_from_text(text: str, max_concepts: int = 10) -> List[str]:
    """
    Extract key concepts from chapter text using TextRank.
    
    Replaced 70+ hardcoded regex patterns with Summa statistical extraction.
    Now works across ANY domain without hardcoded domain knowledge.
    
    Args:
        text: Chapter text content
        max_concepts: Maximum number of concepts to return
        
    Returns:
        List of concepts (single-word terms)
        
    Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN Part 1.4: Remove hardcoded patterns
        - ARCHITECTURE_GUIDELINES Ch. 5: Service layer orchestration
    """
    return STATISTICAL_EXTRACTOR.extract_concepts(text, top_n=max_concepts)


def _extract_sample_text(chapter_pages: List[Dict[str, Any]], num_pages: int = 5) -> str:
    """Extract sample text from first N pages for analysis."""
    sample_text = ""
    for page in chapter_pages[:num_pages]:
        sample_text += page.get('content', '') + " "
    return sample_text


def _find_introductory_sentences(sample_text: str, max_sentences: int = 20) -> List[str]:
    """
    Find sentences that introduce chapter topics.
    
    Returns:
        List of meaningful introductory sentences
    """
    sentences = re.split(r'[.!?]+\s+', sample_text)
    meaningful_sentences = []
    
    introductory_markers = [
        'this chapter', 'we will', 'you will learn', 'introduces',
        'covers', 'discusses', 'explores', 'examines', 'provides',
        'focuses on', 'presents', 'demonstrates', 'explains'
    ]
    
    for sent in sentences[:max_sentences]:
        sent = sent.strip()
        if any(marker in sent.lower() for marker in introductory_markers):
            if 30 < len(sent) < 300:  # Reasonable length
                meaningful_sentences.append(sent)
    
    return meaningful_sentences


def _build_concept_summary(concepts: List[str]) -> str:
    """Build summary sentence from top concepts."""
    if not concepts:
        return ""
    
    top_concepts = [c for c in concepts[:3] if len(c) > 3]
    if not top_concepts:
        return ""
    
    concept_str = ', '.join(top_concepts[:2])
    if len(top_concepts) > 2:
        concept_str += f', and {top_concepts[2]}'
    
    return f"Key topics include {concept_str}."


def _categorize_keywords(keywords: List[str]) -> tuple[List[str], List[str]]:
    """
    Categorize keywords into implementation and conceptual.
    
    Returns:
        (implementation_keywords, conceptual_keywords)
    """
    impl_keywords = [k for k in keywords[:10] if k in [
        'class', 'function', 'method', 'decorator', 'generator',
        'iterator', 'lambda', 'comprehension'
    ]]
    concept_keywords = [k for k in keywords[:10] if k in [
        'exception', 'inheritance', 'testing', 'debugging',
        'pattern', 'architecture', 'design', 'api'
    ]]
    
    return impl_keywords, concept_keywords


def _build_keyword_summary(keywords: List[str], max_parts: int) -> str:
    """Build summary sentence from categorized keywords."""
    if not keywords:
        return ""
    
    impl_keywords, concept_keywords = _categorize_keywords(keywords)
    
    keyword_details = []
    if impl_keywords:
        keyword_details.append(', '.join(impl_keywords[:2]))
    if concept_keywords:
        keyword_details.append(', '.join(concept_keywords[:2]))
    
    if keyword_details and max_parts < 3:
        return f"Covers {', '.join(keyword_details)}."
    
    return ""


def _add_technical_context(summary: str, sentences: List[str], sample_text: str) -> str:
    """Add additional technical context if summary is too short."""
    if len(summary) >= 150 or not sample_text:
        return summary
    
    technical_terms = [
        'python', 'code', 'program', 'syntax', 'variable',
        'function', 'class', 'method', 'object', 'data'
    ]
    
    for sent in sentences[1:15]:
        sent = sent.strip()
        if any(tech_word in sent.lower() for tech_word in technical_terms):
            if 40 < len(sent) < 250 and sent not in summary:
                return f"{summary} {sent}."
    
    return summary


def generate_chapter_summary(chapter_pages: List[Dict[str, Any]], 
                            chapter_title: str,
                            keywords: List[str],
                            concepts: List[str]) -> str:
    """
    Generate a concise summary of what the chapter covers.
    
    Creates a 2-3 sentence summary based on:
    - Chapter title
    - Extracted keywords
    - Identified concepts
    - First few pages of content
    """
    # Extract sample text from first pages
    sample_text = _extract_sample_text(chapter_pages, num_pages=5)
    
    # Find introductory sentences
    meaningful_sentences = _find_introductory_sentences(sample_text, max_sentences=20)
    
    # Build summary parts
    summary_parts = []
    
    # Use meaningful sentence if found
    if meaningful_sentences:
        summary_parts.append(meaningful_sentences[0])
    else:
        summary_parts.append(f"This chapter covers {chapter_title.lower()}.")
    
    # Add concept summary
    concept_summary = _build_concept_summary(concepts)
    if concept_summary:
        summary_parts.append(concept_summary)
    
    # Add keyword-based summary if needed
    keyword_summary = _build_keyword_summary(keywords, len(summary_parts))
    if keyword_summary:
        summary_parts.append(keyword_summary)
    
    # Combine summary parts
    summary = ' '.join(summary_parts)
    
    # Add technical context if needed
    sentences = re.split(r'[.!?]+\s+', sample_text)
    summary = _add_technical_context(summary, sentences, sample_text)
    
    return summary[:600]  # Limit to 600 chars for reasonable length


def load_book_json(book_name: str) -> Dict[str, Any]:
    """
    Load a book's JSON file using PathConfig.
    
    Reference: Python Distilled Ch. 9 - Path operations, file I/O
    """
    # Use PathConfig for centralized path management
    json_dir = settings.paths.textbooks_json_dir
    
    # Build path: textbooks_json_dir / subdirectory / book_name
    subdirectory = BOOK_PATHS.get(book_name, "")
    if subdirectory:
        json_path = json_dir / subdirectory / book_name
    else:
        json_path = json_dir / book_name
    
    with open(json_path, 'r') as f:
        return json.load(f)


def process_chapter_metadata(_book_name: str, chapter: Dict[str, Any], 
                            book_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single chapter and extract metadata.
    
    Returns updated chapter dict with summary, keywords, and concepts.
    
    Args:
        _book_name: Book name (reserved for future use)
        chapter: Chapter dictionary with metadata
        book_data: Full book data with pages
    """
    chapter_num = chapter['chapter_number']
    start_page = chapter['start_page']
    end_page = chapter['end_page']
    title = chapter['title']
    
    print(f"  Processing Ch.{chapter_num}: {title} (pp.{start_page}-{end_page})")
    
    # Extract pages for this chapter
    chapter_pages = []
    for page in book_data.get('pages', []):
        page_num = page.get('page_number')
        if page_num and start_page <= page_num <= end_page:
            chapter_pages.append(page)
    
    if not chapter_pages:
        print("    ⚠️  No pages found for this chapter range")
        # Return chapter with empty metadata
        return {
            **chapter,
            'summary': f"Chapter {chapter_num}: {title}",
            'keywords': [],
            'concepts': []
        }
    
    # Combine all chapter text
    chapter_text = "\n".join([p.get('content', '') for p in chapter_pages])
    
    # Extract metadata
    keywords = extract_keywords_from_text(chapter_text)
    concepts = extract_concepts_from_text(chapter_text)
    summary = generate_chapter_summary(chapter_pages, title, keywords, concepts)
    
    print(f"    ✓ Keywords: {len(keywords)}, Concepts: {len(concepts)}")
    
    # Return updated chapter metadata
    return {
        **chapter,
        'summary': summary,
        'keywords': keywords,
        'concepts': concepts
    }


def main():
    """Main processing function."""
    print("="*80)
    print("GENERATING CHAPTER METADATA FOR ALL 15 BOOKS")
    print("="*80)
    
    # Load current metadata cache from configured metadata directory
    # Reference: Python Distilled Ch. 9 p. 228 - mkdir(parents=True, exist_ok=True)
    cache_path = settings.paths.metadata_dir / "chapter_metadata_cache.json"
    
    # Create metadata directory if it doesn't exist (12-Factor App - idempotent operations)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load cache if exists, otherwise start with empty dict
    if cache_path.exists():
        with open(cache_path, 'r') as f:
            cache = json.load(f)
    else:
        print(f"No existing cache found at {cache_path}, starting fresh")
        cache = {}
    
    print(f"\nLoaded cache with {len(cache)} books\n")
    
    # Process each book
    books_processed = 0
    chapters_processed = 0
    
    for book_name in BOOK_PATHS.keys():
        if book_name not in cache:
            print(f"⚠️  {book_name} not in cache, skipping...")
            continue
        
        print(f"\n{'='*80}")
        print(f"Processing: {book_name}")
        print(f"{'='*80}")
        
        try:
            # Load book JSON
            book_data = load_book_json(book_name)
            
            # Process each chapter
            updated_chapters = []
            for chapter in cache[book_name]:
                updated_chapter = process_chapter_metadata(book_name, chapter, book_data)
                updated_chapters.append(updated_chapter)
                chapters_processed += 1
            
            # Update cache
            cache[book_name] = updated_chapters
            books_processed += 1
            
            print(f"✓ Completed {book_name}: {len(updated_chapters)} chapters")
            
        except FileNotFoundError as e:
            print(f"❌ Error loading {book_name}: {e}")
            continue
        except Exception as e:
            print(f"❌ Error processing {book_name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save updated cache
    print(f"\n{'='*80}")
    print("SAVING UPDATED METADATA")
    print(f"{'='*80}")
    
    with open(cache_path, 'w') as f:
        json.dump(cache, f, indent=2)
    
    print("\n✅ SUCCESS!")
    print(f"   Processed {books_processed} books")
    print(f"   Updated {chapters_processed} chapters")
    print(f"   Saved to: {cache_path}")
    print("\nAll chapters now have:")
    print("  - summary (2-3 sentence overview)")
    print("  - keywords (technical terms, max 15)")
    print("  - concepts (key topics discussed, max 10)")


if __name__ == "__main__":
    main()
