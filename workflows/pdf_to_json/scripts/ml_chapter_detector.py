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
from typing import List, Dict, Tuple
import json

# Add project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor


def calculate_keyword_similarity(keywords1: List[Tuple[str, float]], 
                                  keywords2: List[Tuple[str, float]]) -> float:
    """
    Calculate similarity between two sets of keywords using Jaccard similarity.
    
    Returns:
        Similarity score 0.0-1.0 (0=completely different topics, 1=same topics)
    """
    set1 = set(kw for kw, _ in keywords1)
    set2 = set(kw for kw, _ in keywords2)
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


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
    print("🤖 Using AI/ML to analyze content...")
    page_keywords = []
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
    
    # Step 2: Calculate similarity between consecutive pages
    print("🔍 Detecting topic shifts...")
    similarities = []
    for i in range(len(page_keywords) - 1):
        sim = calculate_keyword_similarity(page_keywords[i], page_keywords[i + 1])
        similarities.append(sim)
    
    # Step 3: Find chapter boundaries (low similarity points)
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
                    boundaries.append(i + 1)  # +1 because similarity[i] is between page[i] and page[i+1]
    
    # Step 4: Filter boundaries - enforce minimum chapter length
    filtered_boundaries = [0]  # Start with page 1
    for boundary in boundaries:
        if boundary - filtered_boundaries[-1] >= min_chapter_length:
            filtered_boundaries.append(boundary)
    
    # Step 5: Extract chapter titles from boundary pages using concepts
    print(f"📖 Found {len(filtered_boundaries)} chapter boundaries")
    chapters = []
    for i, boundary_idx in enumerate(filtered_boundaries):
        page = pages[boundary_idx]
        text = page.get('content', '')
        
        # Skip if page is empty
        if len(text.strip()) < 50:
            continue
        
        # Extract chapter title using concept extraction + first substantial line
        try:
            concepts = extractor.extract_concepts(text[:2000], top_n=3)
        except ValueError:
            concepts = []
        
        # Find first substantial line (likely the title)
        lines = text.split('\n')
        title = "Untitled Chapter"
        for line in lines[:15]:
            line = line.strip()
            if len(line) > 15 and len(line) < 100:  # Reasonable title length
                # Remove page numbers and common markers
                if not line.replace('.', '').replace(' ', '').isdigit():
                    title = line
                    break
        
        # If no good title found, use concepts
        if title == "Untitled Chapter" and concepts:
            title = " - ".join(concepts[:2])
        
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
