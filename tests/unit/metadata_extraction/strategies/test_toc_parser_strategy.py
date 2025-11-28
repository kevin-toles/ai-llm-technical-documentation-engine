#!/usr/bin/env python3
"""
TDD Tests for TOCParserStrategy - Parse Table of Contents for Chapter Detection

RED Phase: These tests define expected behavior for TOC parsing.
The implementation should:
1. Locate the Table of Contents page
2. Extract chapter title → page number mappings
3. Handle page offset issues (logical vs physical pages)
4. Fall back to YAKE validation when TOC parsing fails

Test Fixtures:
- Sample TOC pages from Python Microservices Development
- Edge cases: missing TOC, malformed entries, offset calculations

References:
- Architecture Patterns with Python Ch. 13 (Strategy Pattern)
- Python Distilled Ch. 5 (Regular Expressions)
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md (YAKE integration)
"""

import pytest
from pathlib import Path
from typing import List, Dict, Tuple


# Sample TOC content from Python Microservices Development (page 10)
SAMPLE_TOC_CONTENT = """Table of Contents
Preface
1
Chapter 1: Understanding Microservices
8
Origins of Service-Oriented Architecture
9
The monolithic approach
10
The microservice approach
14
Microservice benefits
16
Separation of concerns
16
Smaller projects
16
Scaling and deployment
17
Microservices pitfalls
18
Illogical splitting
18
More network interactions
19
Data storing and sharing
19
Compatibility issues
20
Testing
20
Implementing microservices with Python
21
The WSGI standard
22
Greenlet and Gevent
23
Twisted and Tornado
25
asyncio
26
Language performances
29
Summary
31
Chapter 2: Discovering Flask
33
Which Python?
35
How Flask handles requests
35
Routing
39
"""

# Alternative TOC format (inline page numbers)
INLINE_TOC_CONTENT = """Table of Contents

Chapter 1: Introduction to Python .......................... 1
Chapter 2: Variables and Data Types ...................... 25
Chapter 3: Control Flow ...................................... 55
Chapter 4: Functions ......................................... 89
"""

# TOC with section numbers like "1 Title" (no "Chapter" prefix)
NUMERIC_PREFIX_TOC = """Contents

1 Understanding Microservices                                8
2 Discovering Flask                                         33
3 Coding, Testing, and Documenting                         67
4 Designing Runnerly                                       105
"""

# Sample page data for testing
def create_sample_pages() -> List[Dict]:
    """Create sample pages simulating Python Microservices Development structure."""
    pages = []
    
    # Pages 1-9: Front matter
    for i in range(1, 10):
        pages.append({
            'page_number': i,
            'content': f'Front matter page {i}\n' * 10
        })
    
    # Page 10: Table of Contents
    pages.append({
        'page_number': 10,
        'content': SAMPLE_TOC_CONTENT
    })
    
    # Pages 11-21: More front matter and preface
    for i in range(11, 22):
        pages.append({
            'page_number': i,
            'content': f'Preface and introduction content {i}\n' * 10
        })
    
    # Page 22: Actual Chapter 1 start
    pages.append({
        'page_number': 22,
        'content': """1
Understanding Microservices
We're always trying to improve the way we build software. Over the years, we have changed
the way we organize projects. We've learned that having small teams working on small
projects is more efficient than a hundred of developers working on one big product. And if
all those small projects interact together and form a consistent product, we get the best of
both worlds.
In the same way, instead of building our apps as big monolithic programs, we can split
them into self-contained services. Each service is a small, lightweight application that is
independent of the others.
This chapter covers microservices and their benefits. It also explains why Python is a
great choice for building microservices. In particular, we will cover:
• Origins of service-oriented architecture
• The microservice approach
• Benefits and pitfalls of microservices
• The Python landscape for microservices
"""
    })
    
    # Pages 23-47: More Chapter 1 content
    for i in range(23, 48):
        pages.append({
            'page_number': i,
            'content': f'Understanding Microservices\nChapter 1 content page {i}\n' * 5
        })
    
    # Page 48: Actual Chapter 2 start
    pages.append({
        'page_number': 48,
        'content': """2
Discovering Flask
Flask is a microframework for Python, written by Armin Ronacher. By microframework, we
mean that Flask is a lightweight framework that provides the essential components to
build web applications. It doesn't include a database abstraction layer, form validation,
or authentication mechanisms by default. But all those features can be added via extensions.
In this chapter, we'll learn how to build a simple Flask application. We'll cover:
• How Flask handles requests
• Routing and URL converters
• Request and Response objects
• Flask built-in features
"""
    })
    
    return pages


class TestTOCParserStrategyDetection:
    """Test TOC page detection capability."""
    
    def test_detect_toc_page_by_header(self):
        """Should find page containing 'Table of Contents' header."""
        # Import will fail until implementation exists
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = create_sample_pages()
        strategy = TOCParserStrategy()
        
        toc_page = strategy.find_toc_page(pages)
        
        assert toc_page is not None, "Should find TOC page"
        assert toc_page['page_number'] == 10, "TOC should be on page 10"
        assert 'Table of Contents' in toc_page['content']
    
    def test_detect_toc_page_alternative_headers(self):
        """Should find TOC with 'Contents' header (without 'Table of')."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = [
            {'page_number': 1, 'content': 'Title page'},
            {'page_number': 2, 'content': 'Contents\n\nChapter 1: Intro ... 1\nChapter 2: Basics ... 15'},
        ]
        strategy = TOCParserStrategy()
        
        toc_page = strategy.find_toc_page(pages)
        
        assert toc_page is not None
        assert toc_page['page_number'] == 2
    
    def test_no_toc_found_returns_none(self):
        """Should return None when no TOC page exists."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = [
            {'page_number': 1, 'content': 'Just regular content without TOC'},
            {'page_number': 2, 'content': 'More regular content here'},
        ]
        strategy = TOCParserStrategy()
        
        toc_page = strategy.find_toc_page(pages)
        
        assert toc_page is None


class TestTOCParserStrategyExtraction:
    """Test chapter entry extraction from TOC."""
    
    def test_extract_chapters_with_separate_line_numbers(self):
        """Should extract chapter→page mappings when page numbers are on separate lines."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        strategy = TOCParserStrategy()
        entries = strategy.parse_toc_entries(SAMPLE_TOC_CONTENT)
        
        assert len(entries) >= 2, f"Should extract at least 2 chapters, got {len(entries)}"
        
        # Check first chapter
        ch1 = entries[0]
        assert ch1['chapter_number'] == 1, f"First chapter should be 1, got {ch1.get('chapter_number')}"
        assert 'Understanding Microservices' in ch1['title']
        assert ch1['toc_page_number'] == 8, f"TOC says Chapter 1 is on page 8, got {ch1.get('toc_page_number')}"
        
        # Check second chapter
        ch2 = entries[1]
        assert ch2['chapter_number'] == 2
        assert 'Discovering Flask' in ch2['title']
        assert ch2['toc_page_number'] == 33
    
    def test_extract_chapters_with_inline_page_numbers(self):
        """Should extract chapter→page mappings when page numbers are inline with dots."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        strategy = TOCParserStrategy()
        entries = strategy.parse_toc_entries(INLINE_TOC_CONTENT)
        
        assert len(entries) >= 4
        assert entries[0]['chapter_number'] == 1
        assert entries[0]['toc_page_number'] == 1
        assert entries[1]['chapter_number'] == 2
        assert entries[1]['toc_page_number'] == 25
    
    def test_extract_chapters_numeric_prefix_format(self):
        """Should extract chapters with '1 Title' format (no 'Chapter' prefix)."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        strategy = TOCParserStrategy()
        entries = strategy.parse_toc_entries(NUMERIC_PREFIX_TOC)
        
        assert len(entries) >= 4
        assert entries[0]['chapter_number'] == 1
        assert 'Understanding Microservices' in entries[0]['title']
        assert entries[0]['toc_page_number'] == 8
    
    def test_extract_ignores_non_chapter_entries(self):
        """Should skip section entries, appendices, and non-chapter items."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        strategy = TOCParserStrategy()
        entries = strategy.parse_toc_entries(SAMPLE_TOC_CONTENT)
        
        # Should only have Chapter entries, not section titles like "Origins of SOA"
        for entry in entries:
            assert 'chapter_number' in entry
            assert entry['chapter_number'] > 0


class TestTOCParserStrategyOffsetCalculation:
    """Test page offset detection and correction."""
    
    def test_calculate_offset_when_toc_mismatches_actual(self):
        """Should calculate offset between TOC page numbers and actual content."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = create_sample_pages()
        toc_entries = [
            {'chapter_number': 1, 'title': 'Understanding Microservices', 'toc_page_number': 8},
            {'chapter_number': 2, 'title': 'Discovering Flask', 'toc_page_number': 33},
        ]
        
        strategy = TOCParserStrategy()
        offset = strategy.calculate_page_offset(toc_entries, pages)
        
        # TOC says page 8, actual content is on page 22
        # Offset should be approximately 14 (22 - 8)
        assert offset > 0, "Offset should be positive (TOC pages < actual pages)"
        assert 12 <= offset <= 16, f"Offset should be ~14, got {offset}"
    
    def test_apply_offset_to_chapter_pages(self):
        """Should apply calculated offset to all chapter page numbers."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        toc_entries = [
            {'chapter_number': 1, 'title': 'Understanding Microservices', 'toc_page_number': 8},
            {'chapter_number': 2, 'title': 'Discovering Flask', 'toc_page_number': 33},
        ]
        offset = 14
        
        strategy = TOCParserStrategy()
        corrected = strategy.apply_offset(toc_entries, offset)
        
        assert corrected[0]['actual_page_number'] == 22  # 8 + 14
        assert corrected[1]['actual_page_number'] == 47  # 33 + 14
    
    def test_no_offset_when_toc_matches_actual(self):
        """Should return offset of 0 when TOC page numbers match actual."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        # Create pages where Chapter 1 content is actually on page 8
        pages = [
            {'page_number': 1, 'content': 'Front matter'},
            {'page_number': 8, 'content': '1\nUnderstanding Microservices\nWe\'re always trying...'},
        ]
        toc_entries = [
            {'chapter_number': 1, 'title': 'Understanding Microservices', 'toc_page_number': 8},
        ]
        
        strategy = TOCParserStrategy()
        offset = strategy.calculate_page_offset(toc_entries, pages)
        
        assert offset == 0, f"Offset should be 0 when no mismatch, got {offset}"


class TestTOCParserStrategyIntegration:
    """Test full detect() method integration."""
    
    def test_detect_returns_chapter_tuples(self):
        """Should return list of (chapter_num, title, start_page, end_page) tuples."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = create_sample_pages()
        strategy = TOCParserStrategy()
        
        chapters = strategy.detect(pages)
        
        assert len(chapters) >= 2, f"Should detect at least 2 chapters, got {len(chapters)}"
        
        # Check tuple format
        ch1 = chapters[0]
        assert len(ch1) == 4, "Each chapter should be (num, title, start, end)"
        assert ch1[0] == 1, f"First chapter number should be 1, got {ch1[0]}"
        assert 'Understanding Microservices' in ch1[1]
        assert ch1[2] == 22, f"Chapter 1 should start on actual page 22, got {ch1[2]}"
    
    def test_detect_calculates_end_pages(self):
        """Should calculate end pages based on next chapter start."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = create_sample_pages()
        strategy = TOCParserStrategy()
        
        chapters = strategy.detect(pages)
        
        # Chapter 1 end should be just before Chapter 2 start
        ch1_end = chapters[0][3]
        ch2_start = chapters[1][2]
        
        assert ch1_end == ch2_start - 1, f"Ch1 end ({ch1_end}) should be Ch2 start-1 ({ch2_start - 1})"
    
    def test_detect_returns_empty_when_no_toc(self):
        """Should return empty list when no TOC is found."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        pages = [
            {'page_number': 1, 'content': 'No TOC here'},
            {'page_number': 2, 'content': 'Just regular content'},
        ]
        strategy = TOCParserStrategy()
        
        chapters = strategy.detect(pages)
        
        assert chapters == [], "Should return empty list when no TOC found"


class TestTOCParserStrategyYAKEFallback:
    """Test YAKE validation fallback for chapter content verification."""
    
    def test_validates_chapter_content_with_yake(self):
        """Should use YAKE to verify chapters have real content."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
        
        pages = create_sample_pages()
        extractor = StatisticalExtractor()
        strategy = TOCParserStrategy(yake_extractor=extractor, min_keywords=3)
        
        chapters = strategy.detect(pages)
        
        # All returned chapters should have been validated to have content
        assert len(chapters) >= 2
    
    def test_filters_empty_chapters_via_yake(self):
        """Should filter out 'chapters' that have no real content."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        from workflows.metadata_extraction.scripts.adapters.statistical_extractor import StatisticalExtractor
        
        # Create pages where page 8 has no real content (just page number)
        pages = [
            {'page_number': 10, 'content': SAMPLE_TOC_CONTENT},
            {'page_number': 8, 'content': '8\n'},  # Empty page at TOC-listed location
            {'page_number': 22, 'content': 'Real chapter content with many keywords and concepts about microservices architecture patterns software development...'},
        ]
        
        extractor = StatisticalExtractor()
        strategy = TOCParserStrategy(yake_extractor=extractor, min_keywords=3)
        
        chapters = strategy.detect(pages)
        
        # Should filter out chapter at page 8 (no content) and find real content
        for chapter in chapters:
            assert chapter[2] != 8, "Should not include page 8 which has no content"


class TestTOCParserStrategyEdgeCases:
    """Test edge cases and error handling."""
    
    def test_handles_malformed_toc_gracefully(self):
        """Should not crash on malformed TOC content."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        malformed_toc = """Table of Contents
        
        This is not a real TOC, just random text without chapter entries.
        Some more random content here.
        123 456 789
        """
        
        strategy = TOCParserStrategy()
        entries = strategy.parse_toc_entries(malformed_toc)
        
        # Should return empty list, not crash
        assert entries == []
    
    def test_handles_unicode_in_titles(self):
        """Should handle Unicode characters in chapter titles."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        unicode_toc = """Table of Contents
        
Chapter 1: Introducción al Español
5
Chapter 2: Français et Accénts
25
Chapter 3: 日本語の章
45
"""
        
        strategy = TOCParserStrategy()
        entries = strategy.parse_toc_entries(unicode_toc)
        
        assert len(entries) >= 3
        assert 'Introducción' in entries[0]['title']
    
    def test_handles_empty_pages_list(self):
        """Should return empty list for empty pages input."""
        from workflows.metadata_extraction.scripts.strategies.toc_parser_strategy import TOCParserStrategy
        
        strategy = TOCParserStrategy()
        chapters = strategy.detect([])
        
        assert chapters == []


# Run tests: pytest tests/unit/metadata_extraction/strategies/test_toc_parser_strategy.py -v
