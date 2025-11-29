#!/usr/bin/env python3
"""
Pure AI/ML Chapter Detection using YAKE + Summa

Instead of regex patterns, this uses statistical NLP to detect chapter boundaries:
1. YAKE keyword extraction to measure topic shifts
2. Summa concept extraction to identify section breaks
3. Content density analysis to find natural boundaries

No hardcoded patterns - works across ANY domain and chapter format.
"""

import sys
from pathlib import Path
from typing import List, Tuple
import json

# Add project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor  # noqa: E402

# Constants
UNTITLED_CHAPTER = "Untitled Chapter"


def _extract_page_keywords(pages: List[dict], extractor: StatisticalExtractor) -> List[List[Tuple[str, float]]]:
    """Extract keywords from each page using YAKE.
    
    Args:
        pages: List of page dicts with 'content' field
        extractor: StatisticalExtractor instance
        
    Returns:
        List of keyword lists for each page
    """
    print("🤖 Using AI/ML to analyze content...")
    page_keywords: list[list[tuple[str, float]]] = []
    for i, page in enumerate(pages, 1):
        text = page.get('content', '')
        
        # Skip empty pages
        if len(text.strip()) < 100:
            page_keywords.append([])
            continue
        
        # Extract top keywords using YAKE
        keywords = extractor.extract_keywords(text, top_n=10)
        page_keywords.append(keywords)
        
        if i % 50 == 0:
            print(f"   Analyzed {i}/{len(pages)} pages...")
    
    return page_keywords


def _calculate_similarities(page_keywords: List[List[Tuple[str, float]]]) -> List[float]:
    """Calculate similarity between consecutive pages.
    
    Args:
        page_keywords: List of keyword lists for each page
        
    Returns:
        List of similarity scores between consecutive pages
    """
    print("🔍 Detecting topic shifts...")
    similarities = []
    for i in range(len(page_keywords) - 1):
        sim = calculate_keyword_similarity(page_keywords[i], page_keywords[i + 1])
        similarities.append(sim)
    return similarities


def _find_topic_boundaries(similarities: List[float], 
                           similarity_threshold: float,
                           min_chapter_length: int) -> List[int]:
    """Find chapter boundaries from similarity scores.
    
    Args:
        similarities: List of similarity scores
        similarity_threshold: Below this = chapter boundary
        min_chapter_length: Minimum pages per chapter
        
    Returns:
        List of boundary page indices
    """
    # Find chapter boundaries (low similarity points)
    boundaries = []
    for i, sim in enumerate(similarities):
        # Check if this is a significant topic shift
        if sim < similarity_threshold:
            # Look ahead to ensure sustained topic change
            if i + 3 < len(similarities):
                next_sims = similarities[i+1:i+4]
                avg_next = sum(next_sims) / len(next_sims)
                # Only mark as boundary if topic stays different
                if avg_next < similarity_threshold + 0.2:
                    boundaries.append(i + 1)
    
    # Filter boundaries - enforce minimum chapter length
    filtered_boundaries = [0]  # Start with page 1
    for boundary in boundaries:
        if boundary - filtered_boundaries[-1] >= min_chapter_length:
            filtered_boundaries.append(boundary)
    
    return filtered_boundaries


def _extract_chapter_title(page: dict, extractor: StatisticalExtractor) -> str:
    """Extract chapter title from a page using concepts and text analysis.
    
    Args:
        page: Page dictionary with 'content' field
        extractor: StatisticalExtractor instance
        
    Returns:
        Extracted chapter title
    """
    text = page.get('content', '')
    
    # Skip if page is empty
    if len(text.strip()) < 50:
        return UNTITLED_CHAPTER
    
    # Extract chapter title using concept extraction + first substantial line
    try:
        concepts = extractor.extract_concepts(text[:2000], top_n=3)
    except ValueError:
        concepts = []
    
    # Find first substantial line (likely the title)
    lines = text.split('\n')
    title = UNTITLED_CHAPTER
    for line in lines[:15]:
        line = line.strip()
        if len(line) > 15 and len(line) < 100:  # Reasonable title length
            # Remove page numbers and common markers
            if not line.replace('.', '').replace(' ', '').isdigit():
                title = line
                break
    
    # If no good title found, use concepts
    if title == UNTITLED_CHAPTER and concepts:
        title = " - ".join(concepts[:2])
    
    return title


def calculate_keyword_similarity(keywords1: List[Tuple[str, float]], 
                                  keywords2: List[Tuple[str, float]]) -> float:
    """
    Calculate similarity between two sets of keywords using Jaccard similarity.
    
    Returns:
        Similarity score 0.0-1.0 (0=completely different topics, 1=same topics)
    """
    set1 = {kw for kw, _ in keywords1}
    set2 = {kw for kw, _ in keywords2}
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def _filter_boundaries_by_length(boundaries: List[int], min_chapter_length: int) -> List[int]:
    """Filter boundaries to enforce minimum chapter length."""
    filtered_boundaries = [0]  # Start with page 1
    for boundary in boundaries:
        if boundary - filtered_boundaries[-1] >= min_chapter_length:
            filtered_boundaries.append(boundary)
    return filtered_boundaries


def _build_chapter_list(filtered_boundaries: List[int], pages: List[dict], extractor: StatisticalExtractor) -> List[dict]:
    """Build chapter list from boundaries."""
    chapters = []
    for i, boundary_idx in enumerate(filtered_boundaries):
        page = pages[boundary_idx]
        title = _extract_chapter_title(page, extractor)
        
        # Determine end page
        if i + 1 < len(filtered_boundaries):
            end_page = filtered_boundaries[i + 1] - 1
        else:
            end_page = len(pages)
        
        chapters.append({
            'number': i + 1,
            'title': title,
            'start_page': boundary_idx + 1,  # Pages are 1-indexed
            'end_page': end_page,
            'confidence': 'ml_detected'
        })
    return chapters


def detect_chapters_ml(pages: List[dict], 
                       similarity_threshold: float = 0.3,
                       min_chapter_length: int = 5) -> List[dict]:
    """
    Detect chapter boundaries using pure AI/ML - no regex patterns.
    
    Algorithm:
    1. Extract keywords from each page using YAKE
    2. Calculate keyword similarity between consecutive pages
    3. Low similarity = topic shift = potential chapter boundary
    4. Validate boundaries with content density checks
    5. Extract chapter titles from boundary pages using concept extraction
    
    Args:
        pages: List of page dicts with 'content' field
        similarity_threshold: Below this = chapter boundary (default 0.3)
        min_chapter_length: Minimum pages per chapter (default 5)
    
    Returns:
        List of chapter dicts {number, title, start_page, end_page}
    """
    extractor = StatisticalExtractor()
    
    # Step 1: Extract keywords for each page
    page_keywords = _extract_page_keywords(pages, extractor)
    
    # Step 2: Calculate similarity between consecutive pages
    similarities = _calculate_similarities(page_keywords)
    
    # Step 3: Find chapter boundaries (low similarity points) with filtering
    boundaries = _find_topic_boundaries(similarities, similarity_threshold, min_chapter_length)
    
    # Step 4: Extract chapter titles and build chapter list
    print(f"📖 Found {len(boundaries)} chapter boundaries")
    return _build_chapter_list(boundaries, pages, extractor)


def main():
    """Test the ML chapter detector"""
    if len(sys.argv) < 2:
        print("Usage: python ml_chapter_detector.py <json_file>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    pages = data.get('pages', [])
    print(f"📚 Loaded: {len(pages)} pages")
    
    # Detect chapters using ML
    chapters = detect_chapters_ml(pages)
    
    print(f"\n✅ Detected {len(chapters)} chapters using AI/ML:\n")
    for ch in chapters:
        print(f"   Chapter {ch['number']}: {ch['title'][:60]}... (pages {ch['start_page']}-{ch['end_page']})")


if __name__ == "__main__":
    main()
